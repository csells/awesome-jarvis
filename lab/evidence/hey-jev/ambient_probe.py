"""Probe upstream wake loop; suppress only cloud TTS cache warmup; no fake API replies."""
import os, pathlib, sys, threading, time, subprocess, json
sys.path.insert(0,str(pathlib.Path.home()/'code/henryklunaris/hey-jev'))
import siri
# Isolate local wake loop: main() otherwise requires cloud keys before starting.
# The only replaced function pre-renders Fish Audio replies, irrelevant to ignored speech.
siri.warm_cache=lambda: print('TEST CONFIG: cloud TTS cache warmup disabled',flush=True)
ready=threading.Event()
def notify(state,detail=''):
 print('STATE',state,detail,flush=True)
 if state=='Ready': ready.set()
def inject():
 if not ready.wait(60):
  print('FAIL: recorder did not become ready',flush=True); os._exit(2)
 d=pathlib.Path(siri.SAVE_CLIPS)
 before=set(d.glob('*.wav')) if d.exists() else set()
 subprocess.run([str(pathlib.Path.home()/'lab/bin/say-mic'),'The quick brown fox jumps over the lazy dog.'],check=True)
 for _ in range(200):
  new=set(d.glob('*.wav'))-before if d.exists() else set()
  if new:
   import shutil
   out=pathlib.Path('/Volumes/My Shared Files/out/ambient');out.mkdir(exist_ok=True)
   p=next(iter(new));shutil.copyfile(p,out/'ignored-speech.wav')
   print(json.dumps({'ambient_clip_created':True,'bytes':p.stat().st_size,'default_SAVE_CLIPS':siri.SAVE_CLIPS}),flush=True)
   os._exit(0)
  time.sleep(.1)
 print('FAIL: no ambient clip observed',flush=True);os._exit(1)
threading.Thread(target=inject,daemon=True).start()
siri.run_voice_assistant(notify=notify,mode='wake',mic='BlackHole 2ch')
