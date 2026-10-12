"""Loopback-only shared speech worker routing for REST and realtime clients.

One catalogue chooses the engine. Realtime uses the upstream HTTP adapters,
so it loads neither a second TTS model nor a second transcription model.
"""
import asyncio
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
import sys
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from starlette.background import BackgroundTask
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'bin'))
def voice_catalog(profiles):
    voices=[]
    for profile in profiles:
        item=dict(profile)
        item['id']='alfred' if profile['id']=='ralph-fiennes' else profile['id']
        item.update(engine='pocket-tts', formats=['pcm','wav'], realtime=True,
                    default_speed=1.25, speed_range=[0.5,2.0], sample_rate=24000, channels=1)
        voices.append(item)
    return {'service':'Pocket','voices':voices,'default':'alfred'}

def speech_request(body):
    if not isinstance(body,dict): raise ValueError('Expected an object')
    body=dict(body)
    # Upstream realtime adapter describes the wire stream; our PCM route already streams.
    if body.pop('stream_format', 'audio') != 'audio': raise ValueError('Use audio streaming')
    stream=body.pop('stream', False)
    if not isinstance(stream,bool): raise ValueError('Invalid stream flag')
    voice=body.get('voice','alfred')
    if not isinstance(voice,str): raise ValueError('Voice must be a name')
    if not voice or len(voice)>100: raise ValueError('Invalid voice name')
    if body.get('model') not in (None,'speech','pocket-tts','tts-1'):
        raise ValueError('Unknown speech model')
    text=body.get('input')
    if not isinstance(text,str) or not 0<len(text.strip())<=2000: raise ValueError('Invalid speech text')
    speed=body.get('speed',1.25)
    if isinstance(speed,bool) or not isinstance(speed,(int,float)) or not .5<=speed<=2: raise ValueError('Invalid speed')
    formats=('pcm','wav')
    if body.get('response_format','pcm') not in formats: raise ValueError('Unsupported format for selected voice')
    body.update(model='pocket-tts',voice='ralph-fiennes' if voice=='alfred' else voice,speed=speed,response_format=body.get('response_format','pcm'))
    return 'pocket',body

def create_app(config,transport=None):
    gate=asyncio.Lock()
    @asynccontextmanager
    async def lifespan(app):
        async with httpx.AsyncClient(timeout=90,transport=transport) as client:
            app.state.http=client
            yield
    app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None)
    @app.get('/v1/voices')
    async def voices():
        r=await app.state.http.get(config['pocket_url']+'/api/voices')
        r.raise_for_status()
        return voice_catalog(r.json())
    @app.get('/health')
    @app.get('/healthz')
    async def health():
        try:
            for name,path in [('audio','/health'),('pocket','/healthz')]:
                r=await app.state.http.get(config[name+'_url']+path,timeout=5)
                r.raise_for_status()
                if r.json().get('ok') is False: raise ValueError('not ready')
        except (httpx.HTTPError,ValueError):return Response(status_code=503)
        return {'ok':True,'engines':['pocket-tts'],'transcription':'parakeet'}
    @app.post('/v1/audio/{operation}')
    async def audio(operation:str,request:Request):
        if operation not in ('speech','transcriptions'): raise HTTPException(404)
        data=bytearray()
        async for chunk in request.stream():
            data.extend(chunk)
            if len(data)>8*1024*1024: raise HTTPException(413)
        dest='audio'
        content_type=request.headers.get('content-type','application/json')
        if operation=='speech':
            try: dest,body=speech_request(json.loads(data))
            except (ValueError,TypeError) as e: raise HTTPException(422,str(e))
            data=json.dumps(body).encode();content_type='application/json'
        await gate.acquire()
        upstream=None
        released=False
        async def cleanup():
            nonlocal released
            if released:return
            released=True
            try:
                if upstream is not None:await upstream.aclose()
            finally:gate.release()
        try:
            req=app.state.http.build_request('POST',config[dest+'_url']+'/v1/audio/'+operation,content=bytes(data),headers={'content-type':content_type})
            upstream=await app.state.http.send(req,stream=True)
            if not upstream.is_success:
                body=await upstream.aread();await cleanup()
                return Response(body,status_code=upstream.status_code,media_type=upstream.headers.get('content-type'))
            async def chunks():
                try:
                    async for chunk in upstream.aiter_bytes():yield chunk
                finally:await cleanup()
            headers={k:v for k,v in upstream.headers.items() if k in ('x-sample-rate','x-audio-channels','x-audio-format')}
            headers['X-Accel-Buffering']='no'
            return StreamingResponse(chunks(),media_type=upstream.headers.get('content-type'),headers=headers,background=BackgroundTask(cleanup))
        except BaseException:
            await cleanup();raise
    return app

if __name__=='__main__':
    import uvicorn
    c=json.loads(Path(os.environ['VOICE_SERVICE_CONFIG']).read_text())
    uvicorn.run(create_app({'audio_url':c['engine_audio_url'],'pocket_url':c['engine_pocket_url']}),host='127.0.0.1',port=c.get('speech_router_port',18770),access_log=False)
