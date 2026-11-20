"""Bound Parakeet's idle GPU cache without unloading its warm model."""
import logging

LOG = logging.getLogger('voice.stt.memory')


def install_memory_policy(server, cache_limit_bytes):
    """Install before accepting requests; cleanup runs on the GPU broker thread.

    HTTP finally blocks are too early for disconnected/streaming requests: the
    inference broker can still be evaluating MLX arrays after the client leaves.
    Its serial execution boundary also covers Parakeet's short-audio early return.
    """
    if cache_limit_bytes < 0:
        raise ValueError('VOICE_MLX_CACHE_LIMIT_MIB must be nonnegative')
    mx = server.mx
    mx.set_cache_limit(cache_limit_bytes)
    statistics = {'cache_limit_bytes': cache_limit_bytes, 'completed_requests': 0}

    class BoundedSTTAdapter(server.STTExecutionAdapter):
        def run_serial(self, request):
            try:
                return super().run_serial(request)
            finally:
                mx.synchronize()
                mx.clear_cache()
                statistics.update(active_bytes=mx.get_active_memory(),
                                  cache_bytes=mx.get_cache_memory(),
                                  peak_bytes=mx.get_peak_memory(),
                                  completed_requests=statistics['completed_requests'] + 1)
                LOG.info('STT memory after cleanup: active=%d cache=%d peak=%d bytes',
                         statistics['active_bytes'], statistics['cache_bytes'],
                         statistics['peak_bytes'])

    server.get_inference_broker().register_adapter('stt', BoundedSTTAdapter())
    LOG.info('STT GPU cache limit: %d bytes', cache_limit_bytes)
    return statistics
