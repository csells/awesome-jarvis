import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from fastapi import WebSocketDisconnect

import httpx
from fastapi.testclient import TestClient

from gateway import create_app


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.secret = Path(self.temp.name) / 'admin.key'
        self.secret.write_text('test-admin-secret')
        self.secret.chmod(0o600)
        self.calls = []
        self.active_calls = set()
        self.fail_setup = False
        async def backend(request):
            self.calls.append((request.method, request.url.path))
            if request.url.path == '/v1/pool':
                return httpx.Response(200, json={'size': 1, 'in_use': len(self.active_calls), 'units': [{'state': 'active', 'session_id': c} for c in self.active_calls]})
            if request.url.path == '/api/tags':
                return httpx.Response(200, json={'models': [{'name': 'test-model'}]})
            if request.method == 'DELETE':
                self.active_calls.discard(request.url.path.rsplit('/', 1)[-1])
            if request.url.path == '/v1/realtime/calls':
                if self.fail_setup:
                    return httpx.Response(500, text='setup failed')
                self.active_calls.add('session_test')
                return httpx.Response(201, text='v=0\r\nm=audio 9 RTP/AVP 0', headers={'location': '/v1/realtime/calls/session_test'})
            return httpx.Response(200, json={'ok': True})
        self.app = create_app({'admin_key_file': str(self.secret), 'model': 'test-model'}, transport=httpx.MockTransport(backend))
        self.client = TestClient(self.app)
        self.client.__enter__()
        self.admin = {'Authorization': 'Bearer test-admin-secret'}

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.temp.cleanup()

    def lease(self, owner='test-one'):
        r = self.client.post('/leases', headers=self.admin, json={'owner': owner, 'ttl_seconds': 60})
        self.assertEqual(r.status_code, 201, r.text)
        return {'Authorization': 'Bearer ' + r.json()['api_key']}

    def test_authentication_and_route_boundary(self):
        self.assertEqual(self.client.post('/leases', json={'owner': 'x'}).status_code, 401)
        self.assertEqual(self.client.post('/v1/audio/speech', headers=self.admin, json={'input': 'hello'}).status_code, 401)
        lease = self.lease()
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello'}).status_code, 200)
        self.assertEqual(self.client.get('/v1/models', headers=lease).status_code, 404)

    def test_exclusive_reservation_and_revocation(self):
        first = self.lease()
        self.assertEqual(self.client.post('/leases', headers=self.admin, json={'owner': 'other'}).status_code, 409)
        self.assertEqual(self.client.delete('/leases/current', headers={'Authorization': 'Bearer wrong'}).status_code, 401)
        self.assertEqual(self.client.delete('/leases/current', headers=first).status_code, 200)
        self.lease('second')
        self.assertEqual(self.client.post('/v1/audio/speech', headers=first, json={'input': 'hello'}).status_code, 401)

    def test_release_hangs_up_owned_call_and_limits_concurrency(self):
        lease = self.lease()
        headers = {**lease, 'Content-Type': 'application/sdp'}
        r = self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.headers['location'], '/v1/realtime/calls/session_test')
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0').status_code, 409)
        self.assertEqual(self.client.delete('/v1/realtime/calls/not-owned', headers=lease).status_code, 404)
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello'}).status_code, 409)
        self.client.delete('/leases/current', headers=lease)
        self.assertIn(('DELETE', '/v1/realtime/calls/session_test'), self.calls)

    def test_expired_lease_is_denied_and_can_be_reclaimed(self):
        lease = self.lease()
        self.app.state.reservation.expires = 0
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello'}).status_code, 401)
        self.lease('replacement')

    def test_renewal_and_health_do_not_disclose_keys(self):
        lease = self.lease()
        r = self.client.post('/leases/current/renew', headers=lease, json={'ttl_seconds': 90})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('api_key', r.json())
        public = self.client.get('/healthz')
        self.assertEqual(public.status_code, 200)
        self.assertNotIn('test-one', public.text)
        self.assertNotIn('secret', public.text)
        self.assertEqual(self.client.get('/status', headers=lease).status_code, 401)
        self.assertEqual(self.client.get('/status', headers=self.admin).json()['lease']['owner'], 'test-one')

    def test_unapproved_models_are_rejected(self):
        lease = self.lease()
        r = self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello', 'model': 'other/unbounded-model'})
        self.assertEqual(r.status_code, 422)
        r = self.client.post('/v1/audio/transcriptions', headers=lease, data={'model': 'other/unbounded-model'}, files={'file': ('input.wav', b'fake wav', 'audio/wav')})
        self.assertEqual(r.status_code, 422)

    def test_uncertain_orphan_is_cleaned_before_retry(self):
        lease = self.lease()
        self.app.state.reservation.uncertain = True
        self.active_calls.add('orphan')
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello'}).status_code, 200)
        self.assertIn(('DELETE', '/v1/realtime/calls/orphan'), self.calls)
        self.assertFalse(self.app.state.reservation.uncertain)

    def test_failed_setup_can_retry_without_releasing_reservation(self):
        lease = self.lease()
        headers = {**lease, 'Content-Type': 'application/sdp'}
        self.fail_setup = True
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0').status_code, 500)
        self.fail_setup = False
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0').status_code, 201)

    def test_disconnected_peer_releases_slot_for_same_reservation(self):
        lease = self.lease()
        headers = {**lease, 'Content-Type': 'application/sdp'}
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0').status_code, 201)
        self.active_calls.clear()  # backend observed WebRTC disconnect
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'hello'}).status_code, 200)
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0').status_code, 201)

    def test_call_status_distinguishes_owned_live_and_disconnected_peers(self):
        lease = self.lease()
        headers = {**lease, 'Content-Type': 'application/sdp'}
        response = self.client.post('/v1/realtime/calls', headers=headers, content='v=0\r\nm=audio 9 RTP/AVP 0')
        location = response.headers['location']
        self.assertEqual(self.client.get(location, headers=lease).status_code, 200)
        self.assertEqual(self.client.get(location, headers={'Authorization': 'Bearer wrong'}).status_code, 401)
        self.active_calls.clear()
        self.assertEqual(self.client.get(location, headers=lease).status_code, 404)

    def test_disconnected_socket_still_releases_realtime_slot(self):
        headers = self.lease()
        class Socket:
            async def accept(self, **kw): pass
            async def receive_text(self): raise WebSocketDisconnect(1006)
            async def close(self): raise WebSocketDisconnect(1006)
        socket = Socket()
        socket.headers = {k.lower():v for k,v in headers.items()}
        class Upstream:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            def __aiter__(self): return self
            async def __anext__(self):
                await asyncio.sleep(60)
        endpoint = next(r.endpoint for r in self.app.routes if r.path == '/v1/realtime')
        with patch('gateway.websockets.connect', return_value=Upstream()):
            asyncio.run(endpoint(socket))
        self.assertIsNone(self.app.state.reservation.websocket)
        self.assertIsNone(self.app.state.reservation.relay)

    def test_invalid_limits_and_unsupported_protocol_fail_before_backend(self):
        self.assertEqual(self.client.post('/leases', headers=self.admin, json={'owner': 'x', 'ttl_seconds': 100000}).status_code, 422)
        lease = self.lease()
        self.assertEqual(self.client.post('/v1/audio/speech', headers=lease, json={'input': 'x'*4001}).status_code, 422)
        self.assertEqual(self.client.post('/v1/realtime/calls', headers=lease, json={'sdp': 'not-sdp'}).status_code, 415)


if __name__ == '__main__':
    unittest.main(verbosity=2)
