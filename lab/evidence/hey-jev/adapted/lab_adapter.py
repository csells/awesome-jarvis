"""Test-only real service substitutions; no fabricated model or speech responses."""
import hashlib, json, os, pathlib, re, subprocess, tempfile, threading, time
import requests
CACHE=pathlib.Path.home()/'Library/Caches/HeyJevLabNativeSpeech'
CACHE.mkdir(parents=True,exist_ok=True)
_lock=threading.Lock()
_model=None

def fetch_tts(text):
    start=time.monotonic()
    text=re.sub(r'\[(?:chuckling|laughing|sighing|cheerful)\]', '',text).strip()
    path=CACHE/(hashlib.sha256(('native-default|'+text).encode()).hexdigest()+'.wav')
    if path.exists(): return str(path),0,True
    with _lock:
        if not path.exists():
            fd,tmp=tempfile.mkstemp(suffix='.wav',dir=CACHE);os.close(fd)
            try:
                subprocess.run(['/usr/bin/say','-o',tmp,'--data-format=LEI16@16000','-f','-'],input=text,text=True,check=True,capture_output=True)
                os.replace(tmp,path)
            finally:
                if os.path.exists(tmp):os.unlink(tmp)
    return str(path),int((time.monotonic()-start)*1000),False

def ask_llm(text):
    r=requests.post('http://127.0.0.1:18765/ask',json={'text':text},timeout=100)
    r.raise_for_status();d=r.json();return d['text'],d['ms'],None

def local_dictation(self,audio,part):
    global _model
    from faster_whisper import WhisperModel
    with _lock:
        if _model is None:_model=WhisperModel('small.en',device='cpu',compute_type='int8')
        segs,_=_model.transcribe(audio,language='en',beam_size=1,vad_filter=True)
        text=' '.join(s.text.strip() for s in segs)
    print('LAB_DICTATION '+json.dumps({'part':part,'text':text}),flush=True)
    return text

def install(siri):
    siri.fetch_tts=fetch_tts
    siri.ask_llm=ask_llm
    siri.Dictation._transcribe=local_dictation
    original=siri.emit
    def emit(notify,state,detail=''):
        print('LAB_STATE '+json.dumps({'time':time.time(),'state':state,'detail':detail}),flush=True)
        return original(notify,state,detail)
    siri.emit=emit
    print('LAB ADAPTED: real TypeSafe; Claude subscription CLI; local macOS TTS; local Whisper dictation',flush=True)
