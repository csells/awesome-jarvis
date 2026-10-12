"""Build the single-service deployment without duplicating inference models."""
from copy import deepcopy
from pathlib import Path

def unify(config,release,python,pocket_process=None):
    c=deepcopy(config)
    if not c.get('pocket_url'):raise ValueError('Pocket backend is required')
    c['engine_audio_url']=c['audio_url']
    c['engine_pocket_url']=c['pocket_url']
    router='http://127.0.0.1:18770'
    c['speech_router_port']=18770
    c['audio_url']=router
    c['pocket_url']=router
    c['voice_catalog_url']=router+'/v1/voices'
    c['speech_engine']='pocket-tts'
    c['service_name']='Pocket'
    c['processes']['speech-router']={'argv':[python,str(Path(release)/'managed/speech_router.py')],'health_url':router+'/health'}
    if pocket_process:c['processes']['pocket']=deepcopy(pocket_process)
    a=c['processes']['realtime']['argv']
    for option in ('--stt','--tts'):
        if option in a:
            i=a.index(option);del a[i:i+2]
    a.extend(['--stt','openai','--openai_stt_base_url',router+'/v1','--openai_stt_model','whisper-1',
              '--tts','openai','--openai_tts_base_url',router+'/v1','--openai_tts_model','speech',
              '--openai_tts_voice','alfred','--openai_tts_response_format','pcm','--openai_tts_speed','1.25'])
    c['architecture']={'default_voice':'alfred','inference_workers':{'parakeet':'audio','pocket-tts':'pocket'},
                       'realtime':'HTTP STT/TTS adapters; no duplicate inference model',
                       'synthesis':'Pocket speech synthesis'}
    return c
