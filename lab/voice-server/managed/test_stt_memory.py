"""Request-boundary regression tests; live MLX measurements run in staging."""
import types
import unittest
import asyncio
from stt_memory import install_memory_policy


class MemoryPolicyTests(unittest.TestCase):
    def server(self, fail=False):
        self.events = []
        events = self.events

        class Adapter:
            def run_serial(self, request):
                events.append(('inference', request))
                if fail:
                    raise ValueError('invalid recording')

        class Metal:
            def set_cache_limit(self, limit): events.append(('limit', limit))
            def synchronize(self): events.append('synchronize')
            def clear_cache(self): events.append('clear')
            def get_active_memory(self): return 2500000000
            def get_cache_memory(self): return 0
            def get_peak_memory(self): return 3000000000

        self.adapters = {}
        broker = types.SimpleNamespace(register_adapter=self.adapters.__setitem__)
        return types.SimpleNamespace(mx=Metal(), STTExecutionAdapter=Adapter,
                                     get_inference_broker=lambda: broker)

    def test_short_request_cleans_up_on_inference_thread_boundary(self):
        server = self.server()
        stats = install_memory_policy(server, 256 * 1024**2)
        self.adapters['stt'].run_serial('short recording')
        self.assertEqual(self.events, [('limit', 256 * 1024**2),
                         ('inference', 'short recording'), 'synchronize', 'clear'])
        self.assertEqual(stats['completed_requests'], 1)
        self.assertEqual(stats['cache_bytes'], 0)
        self.assertEqual(stats['active_bytes'], 2500000000)

    def test_failed_request_cleans_up_and_preserves_error(self):
        server = self.server(fail=True)
        install_memory_policy(server, 0)
        with self.assertRaisesRegex(ValueError, 'invalid recording'):
            self.adapters['stt'].run_serial('bad recording')
        self.assertEqual(self.events[-2:], ['synchronize', 'clear'])

    def test_cleanup_failures_are_not_hidden(self):
        server = self.server()
        def fail(): raise RuntimeError('GPU cleanup failed')
        server.mx.clear_cache = fail
        install_memory_policy(server, 0)
        with self.assertRaisesRegex(RuntimeError, 'GPU cleanup failed'):
            self.adapters['stt'].run_serial('recording')

    def test_cancelled_inference_cleans_up(self):
        server = self.server()
        def cancel(self, request): raise asyncio.CancelledError()
        server.STTExecutionAdapter.run_serial = cancel
        install_memory_policy(server, 0)
        with self.assertRaises(asyncio.CancelledError):
            self.adapters['stt'].run_serial('cancelled recording')
        self.assertEqual(self.events[-2:], ['synchronize', 'clear'])

    def test_negative_limit_is_rejected_before_broker_starts(self):
        server = self.server()
        with self.assertRaises(ValueError):
            install_memory_policy(server, -1)
        self.assertEqual(self.events, [])
        self.assertEqual(self.adapters, {})


if __name__ == '__main__':
    unittest.main()
