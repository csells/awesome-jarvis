"""Private voice gateway: one expiring reservation, one realtime session, bounded REST calls."""
import asyncio
import contextlib
from email import policy
from email.parser import BytesParser
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import re
import secrets
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

import httpx
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pydantic import BaseModel, Field, ConfigDict
import uvicorn
import websockets

LOG = logging.getLogger('voice.gateway')
MAX_BODY = 8 * 1024 * 1024
CALL_ID = re.compile(r'^[A-Za-z0-9_-]{1,200}$')


class LeaseRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    owner: str = Field(min_length=1, max_length=120)
    ttl_seconds: int = Field(default=900, ge=30, le=900)


class Renewal(BaseModel):
    model_config = ConfigDict(extra='forbid')
    ttl_seconds: int = Field(default=900, ge=30, le=900)


@dataclass
class Reservation:
    owner: str
    digest: str
    expires: float
    calls: set = field(default_factory=set)
    websocket: object = None
    relay: object = None
    uncertain: bool = False

    def summary(self):
        return {'owner': self.owner, 'remaining_seconds': max(0, round(self.expires-time.monotonic())),
                'realtime_active': bool(self.calls or self.websocket)}


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def bearer(headers):
    auth = headers.get('authorization', '')
    return auth[7:] if auth.startswith('Bearer ') else ''


def create_app(config, transport=None):
    key_path = Path(config['admin_key_file'])
    if key_path.stat().st_mode & 0o077:
        raise RuntimeError('Admin key file must be private (0600).')
    admin = key_path.read_text().strip()
    if not admin:
        raise RuntimeError('Admin key is empty.')
    rt = config.get('realtime_url', 'http://127.0.0.1:18765')
    audio = config.get('audio_url', 'http://127.0.0.1:18766')
    llm = config.get('ollama_url', 'http://127.0.0.1:11434')
    gate = asyncio.Lock()

    def require_admin(request):
        if not hmac.compare_digest(bearer(request.headers), admin):
            raise HTTPException(401, 'Administrator authentication required.')

    def require_lease(headers):
        lease = app.state.reservation
        token = bearer(headers)
        if not lease or lease.expires <= time.monotonic() or not token or not hmac.compare_digest(digest(token), lease.digest):
            raise HTTPException(401, 'An active reservation key is required.')
        return lease

    async def reconcile_pool():
        deadline = time.monotonic()+15
        while True:
            response = await app.state.http.get(rt+'/v1/pool', timeout=5)
            response.raise_for_status()
            pool = response.json()
            units = pool.get('units', [])
            if pool.get('in_use') == 0 and all(u.get('state') == 'idle' for u in units):
                return
            for unit in units:
                call = unit.get('session_id')
                if call and CALL_ID.fullmatch(call) and unit.get('state') == 'active':
                    ended = await app.state.http.delete(f'{rt}/v1/realtime/calls/{call}', timeout=10)
                    if ended.status_code not in (200, 204, 404):
                        raise HTTPException(503, 'Backend call cleanup failed.')
            if time.monotonic() >= deadline:
                raise HTTPException(503, 'Backend has not released its worker; reservation remains held.')
            await asyncio.sleep(.2)

    async def clear_lease():
        lease = app.state.reservation
        if lease is None:
            return
        # Keep the reservation until cleanup succeeds; a broken backend must not be reassigned.
        if lease.relay:
            lease.relay.cancel()
            await asyncio.gather(lease.relay, return_exceptions=True)
        for call in list(lease.calls):
            response = await app.state.http.delete(f'{rt}/v1/realtime/calls/{call}', timeout=10)
            if response.status_code not in (200, 204, 404):
                raise HTTPException(503, 'Call cleanup failed; reservation remains held.')
            lease.calls.discard(call)
        await reconcile_pool()
        app.state.reservation = None

    async def probe():
        async def check(url, kind):
            try:
                response = await app.state.http.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                if kind == 'realtime':
                    return all(u.get('state') != 'stuck' for u in data.get('units', []))
                if kind == 'model':
                    return config.get('model') in [m.get('name') for m in data.get('models', [])]
                return True
            except (httpx.HTTPError, ValueError):
                return False
        values = await asyncio.gather(check(rt+'/v1/pool', 'realtime'), check(audio+'/health', 'audio'), check(llm+'/api/tags', 'model'))
        return dict(zip(('realtime', 'audio', 'model'), values))

    async def maintenance():
        # On gateway restart, orphaned WebRTC calls cannot retain a worker indefinitely.
        while not app.state.initialized:
            try:
                await reconcile_pool()
                app.state.initialized = True
            except (httpx.HTTPError, HTTPException, ValueError):
                await asyncio.sleep(2)
        while True:
            await asyncio.sleep(1)
            async with gate:
                lease = app.state.reservation
                if lease and lease.expires <= time.monotonic():
                    try:
                        await clear_lease()
                    except (httpx.HTTPError, HTTPException):
                        LOG.error('Expired reservation cleanup failed; retrying')

    @asynccontextmanager
    async def lifespan(application):
        application.state.http = httpx.AsyncClient(transport=transport, trust_env=False, timeout=120)
        task = asyncio.create_task(maintenance())
        try:
            yield
        finally:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
            async with gate:
                try:
                    await clear_lease()
                except (httpx.HTTPError, HTTPException):
                    LOG.error('Shutdown call cleanup failed')
            await application.state.http.aclose()

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.reservation = None
    app.state.initialized = False

    @app.exception_handler(httpx.HTTPError)
    async def backend_error(request, error):
        LOG.error('Backend request failed: %s', type(error).__name__)
        return Response('Voice backend unavailable', status_code=503)

    @app.get('/healthz')
    async def health():
        checks = await probe()
        ready = app.state.initialized and all(checks.values())
        return Response(json.dumps({'ok': ready}), media_type='application/json', status_code=200 if ready else 503)

    @app.get('/status')
    async def status(request: Request):
        require_admin(request)
        lease = app.state.reservation
        return {'ready': app.state.initialized, 'components': await probe(),
                'lease': lease.summary() if lease else None, 'max_realtime_sessions': 1}

    @app.post('/leases', status_code=201)
    async def reserve(request: Request, body: LeaseRequest):
        require_admin(request)
        async with gate:
            existing = app.state.reservation
            if existing and existing.expires <= time.monotonic():
                await clear_lease()
            if app.state.reservation:
                raise HTTPException(409, 'Voice service is reserved; retry after the current owner releases it.')
            await reconcile_pool()
            if not app.state.initialized or not all((await probe()).values()):
                raise HTTPException(503, 'Voice service is warming up or unhealthy.')
            key = secrets.token_urlsafe(32)
            lease = Reservation(body.owner, digest(key), time.monotonic()+body.ttl_seconds)
            app.state.reservation = lease
            return {**lease.summary(), 'api_key': key}

    @app.post('/leases/current/renew')
    async def renew(request: Request, body: Renewal):
        async with gate:
            lease = require_lease(request.headers)
            lease.expires = time.monotonic()+body.ttl_seconds
            return lease.summary()

    @app.delete('/leases/current')
    async def release(request: Request):
        async with gate:
            if not hmac.compare_digest(bearer(request.headers), admin):
                require_lease(request.headers)
            await clear_lease()
            return {'released': True}

    async def bounded_body(request):
        chunks, length = [], 0
        async for chunk in request.stream():
            length += len(chunk)
            if length > MAX_BODY:
                raise HTTPException(413, 'Request exceeds 8 MiB.')
            chunks.append(chunk)
        return b''.join(chunks)

    @app.post('/v1/audio/{operation}')
    async def audio_request(operation: str, request: Request):
        require_lease(request.headers)
        if operation not in ('speech', 'transcriptions'):
            raise HTTPException(404)
        data = await bounded_body(request)
        if operation == 'speech':
            try:
                body = json.loads(data)
                if body.get('model') not in (None, 'tts-1', 'tts-1-hd', 'gpt-4o-mini-tts', 'mlx-community/Kokoro-82M-bf16'):
                    raise ValueError()
                if body.get('voice') and not re.fullmatch(r'[a-z_]{1,40}', body['voice']):
                    raise ValueError()
                if not isinstance(body.get('input'), str) or not 0 < len(body['input']) <= 4000:
                    raise ValueError()
            except (ValueError, AttributeError):
                raise HTTPException(422, 'Use a supported speech model/voice and 1–4000 input characters.')
        else:
            content_type = request.headers.get('content-type', '')
            if not content_type.startswith('multipart/form-data;'):
                raise HTTPException(415, 'Transcription requires multipart/form-data.')
            form = BytesParser(policy=policy.default).parsebytes(('Content-Type: '+content_type+'\r\n\r\n').encode()+data)
            for part in form.iter_parts():
                if part.get_param('name', header='content-disposition') == 'model':
                    if part.get_content().strip() not in ('whisper-1', 'gpt-4o-mini-transcribe', 'gpt-4o-transcribe', 'mlx-community/parakeet-tdt-0.6b-v3'):
                        raise HTTPException(422, 'Use a supported transcription model.')
        async with gate:
            lease = require_lease(request.headers)
            if lease.calls or lease.websocket or lease.uncertain:
                raise HTTPException(409, 'End or clean up the realtime session before REST speech work.')
            response = await app.state.http.post(audio+'/v1/audio/'+operation, content=data,
                headers={'content-type': request.headers.get('content-type', '')})
            return Response(response.content, status_code=response.status_code,
                            media_type=response.headers.get('content-type'))

    @app.post('/v1/realtime/calls')
    async def call(request: Request):
        require_lease(request.headers)
        if 'application/sdp' not in request.headers.get('content-type', ''):
            raise HTTPException(415, 'Send raw application/sdp; configure the session through its data channel.')
        data = await bounded_body(request)
        if len(data) > 100000 or not data.startswith(b'v=0') or b'm=audio' not in data:
            raise HTTPException(422, 'An audio SDP offer is required.')
        async with gate:
            lease = require_lease(request.headers)
            if lease.calls or lease.websocket or lease.uncertain:
                raise HTTPException(409, 'A realtime session is active or requires cleanup.')
            lease.uncertain = True
            response = await app.state.http.post(rt+'/v1/realtime/calls', content=data,
                headers={'content-type': 'application/sdp'}, timeout=25)
            location = response.headers.get('location', '')
            call_id = location.rsplit('/', 1)[-1]
            if response.is_success:
                if not CALL_ID.fullmatch(call_id):
                    raise HTTPException(502, 'Backend did not supply a controllable call ID.')
                lease.calls.add(call_id)
                lease.uncertain = False
            headers = {'location': '/v1/realtime/calls/'+call_id} if response.is_success else {}
            return Response(response.content, status_code=response.status_code, headers=headers,
                            media_type=response.headers.get('content-type'))

    @app.delete('/v1/realtime/calls/{call_id}')
    @app.post('/v1/realtime/calls/{call_id}/hangup')
    async def hangup(call_id: str, request: Request):
        async with gate:
            lease = require_lease(request.headers)
            if call_id not in lease.calls:
                raise HTTPException(404, 'Call does not belong to this reservation.')
            response = await app.state.http.delete(rt+'/v1/realtime/calls/'+call_id, timeout=10)
            if response.status_code in (200, 204, 404):
                lease.calls.discard(call_id)
            return Response(response.content, status_code=response.status_code)

    @app.websocket('/v1/realtime')
    async def realtime(socket: WebSocket):
        protocols = socket.headers.get('sec-websocket-protocol', '').split(',')
        protocols = [p.strip() for p in protocols]
        headers = dict(socket.headers)
        if 'authorization' not in headers:
            keys = [p.removeprefix('openai-insecure-api-key.') for p in protocols if p.startswith('openai-insecure-api-key.')]
            if len(keys) == 1:
                headers['authorization'] = 'Bearer '+keys[0]
        try:
            async with gate:
                lease = require_lease(headers)
                if lease.calls or lease.websocket or lease.uncertain:
                    await socket.close(code=1008, reason='Realtime session already active')
                    return
                await socket.accept(subprotocol='realtime' if 'realtime' in protocols else None)
                lease.websocket = socket
                lease.relay = asyncio.current_task()
        except HTTPException:
            await socket.close(code=1008)
            return
        tasks = []
        try:
            # Never relay client-controlled URLs, authentication, or query strings to the backend.
            async with websockets.connect(rt.replace('http://', 'ws://')+'/v1/realtime', max_size=MAX_BODY) as upstream:
                async def to_server():
                    while True:
                        data = await socket.receive_text()
                        if len(data) > MAX_BODY:
                            await socket.close(code=1009)
                            return
                        await upstream.send(data)
                async def to_client():
                    async for data in upstream:
                        await socket.send_text(data)
                tasks = [asyncio.create_task(to_server()), asyncio.create_task(to_client())]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    task.result()
        except (asyncio.CancelledError, WebSocketDisconnect, websockets.ConnectionClosed, RuntimeError):
            pass
        except Exception:
            LOG.exception('Realtime relay failed')
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            with contextlib.suppress(RuntimeError, WebSocketDisconnect):
                await socket.close()
            if app.state.reservation is lease:
                lease.websocket = None
                lease.relay = None

    return app


if __name__ == '__main__':
    config = json.loads(Path(os.environ['VOICE_SERVICE_CONFIG']).read_text())
    uvicorn.run(create_app(config), host='127.0.0.1', port=config.get('gateway_port', 18800),
                access_log=False, ws_max_size=MAX_BODY)
