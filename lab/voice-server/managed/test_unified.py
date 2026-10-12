import copy
import httpx
import pytest
from fastapi.testclient import TestClient
from speech_router import create_app,speech_request
from unified_config import unify

@pytest.mark.parametrize('model',[None,'tts-1','speech','pocket-tts'])
def test_alfred_selects_pocket_without_model_knowledge(model):
    body={'voice':'alfred','input':'Hello'}
    if model:body['model']=model
    dest,b=speech_request(body)
    assert dest=='pocket' and b['voice']=='ralph-fiennes' and b['model']=='pocket-tts'
    assert b['speed']==1.25

@pytest.mark.parametrize('voice',['jeremy-irons','another-profile'])
def test_pocket_voices_are_not_alfred_only(voice):
    assert speech_request({'voice':voice,'input':'Hello'})[1]['voice']==voice

def test_catalog_exposes_all_profiles():
    from speech_router import voice_catalog
    catalog=voice_catalog([{'id':'ralph-fiennes'},{'id':'jeremy-irons'}])
    assert catalog['service']=='Pocket'
    assert [v['id'] for v in catalog['voices']]==['alfred','jeremy-irons']

@pytest.mark.parametrize('body',[{'voice':'alfred','input':''},{'voice':'alfred','input':'x','speed':True},[],{'voice':{},'input':'x'}])
def test_invalid_voice_requests_fail(body):
    with pytest.raises(ValueError):speech_request(body)

def test_shared_route_releases_after_error_and_keeps_pcm():
    calls=[]
    def backend(req):
        calls.append(req)
        if len(calls)==1:return httpx.Response(409,json={'detail':'busy'})
        return httpx.Response(200,content=b'\x01\x02'*100,headers={'content-type':'audio/pcm','x-sample-rate':'24000'})
    with TestClient(create_app({'audio_url':'http://audio','pocket_url':'http://pocket'},httpx.MockTransport(backend))) as c:
        body={'voice':'alfred','input':'Hello'}
        assert c.post('/v1/audio/speech',json=body).status_code==409
        r=c.post('/v1/audio/speech',json=body)
        assert r.status_code==200 and len(r.content)==200 and r.headers['x-sample-rate']=='24000'
    assert all(str(r.url)=='http://pocket/v1/audio/speech' for r in calls)

def test_realtime_and_rest_use_same_workers():
    old={'audio_url':'http://audio','pocket_url':'http://pocket','processes':{'audio':{'argv':['python','audio_serve.py']},'realtime':{'argv':['python','s2s','serve','--stt','parakeet-tdt','--tts','openai']}}}
    before=copy.deepcopy(old);new=unify(old,'/release','python',{'argv':['python','pocket']})
    assert old==before
    args=new['processes']['realtime']['argv']
    assert 'parakeet-tdt' not in args
    assert args[args.index('--stt')+1]=='openai'
    assert args[args.index('--tts')+1]=='openai'
    assert args[args.index('--openai_tts_voice')+1]=='alfred'
    assert new['audio_url']==new['pocket_url']==args[args.index('--openai_tts_base_url')+1].removesuffix('/v1')
    assert 'pocket' in new['processes']
    assert new['service_name']=='Pocket'

def test_realtime_wire_format_is_normalized_for_pocket():
    _,b=speech_request({'voice':'alfred','input':'Warmup','model':'speech','stream_format':'audio'})
    assert 'stream_format' not in b and b['model']=='pocket-tts'



def test_transcription_worker_cannot_load_speech_models():
    from transcription_app import create_app as stt_app
    async def transcribe():return {'text':'hello'}
    with TestClient(stt_app(transcribe,'parakeet')) as c:
        assert c.post('/v1/audio/transcriptions').json()=={'text':'hello'}
        assert c.get('/health').json()=={'ok':True,'stt_model':'parakeet'}
        for path in ['/v1/audio/speech','/v1/models','/models/load']:
            assert c.post(path,json={'model':'speech'}).status_code==404
