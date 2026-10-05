import json, pathlib, subprocess, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path.home()/'code/henryklunaris/hey-jev'))
import siri
from faster_whisper import WhisperModel
out=pathlib.Path('/Volumes/My Shared Files/out/components'); out.mkdir(exist_ok=True)
print('Loading app speech model small.en; component probe, not a full assistant turn', flush=True)
model=WhisperModel(siri.WHISPER_MODEL, device='cpu', compute_type='int8')
rec=siri.Recorder('BlackHole 2ch'); rec.wake=True; rec.sync_mic()
results=[]
try:
 for phrase in ['Hey Jeff, set a timer for five minutes.', 'The quick brown fox jumps over the lazy dog.']:
  print('Injecting: '+phrase, flush=True)
  subprocess.run([str(pathlib.Path.home()/'lab/bin/say-mic'),phrase],check=True)
  audio=rec.segments.get(timeout=20)
  segments,_=model.transcribe(audio,language='en',beam_size=1,vad_filter=True,initial_prompt=siri.WAKE_PROMPT)
  text=' '.join(s.text.strip() for s in segments if s.no_speech_prob<=siri.NO_SPEECH_MAX)
  matched=bool(siri.WAKE.search(text))
  results.append({'spoken':phrase,'transcribed':text,'wake_match':matched,'samples':len(audio)})
  print(json.dumps(results[-1]),flush=True)
 print('Checking paused recorder ignores injected speech',flush=True)
 rec.paused=True
 subprocess.run([str(pathlib.Path.home()/'lab/bin/say-mic'),'Hey Jeff, stop.'],check=True)
 time.sleep(1)
 results.append({'paused_recorder_queue_empty':rec.segments.empty()})
 print(json.dumps(results[-1]),flush=True)
 print('Checking real timer add/read/cancel functions',flush=True)
 added=siri.run_timer('timer_set','set a timer for five minutes')
 before=siri.timer_snapshot()
 cancelled=siri.run_timer('timer_cancel','cancel the timer')
 after=siri.timer_snapshot()
 results.append({'timer_added':added,'before':before,'cancelled':cancelled,'after':after})
 print(json.dumps(results[-1]),flush=True)
finally:
 rec.stream.close()
 (out/'results.json').write_text(json.dumps(results,indent=2))
