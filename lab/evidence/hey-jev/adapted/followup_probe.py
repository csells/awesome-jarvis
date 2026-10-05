"""Retest the short wake follow-up window without transcribing between utterances."""
import pathlib, subprocess, time, json, signal
out=pathlib.Path('/Volumes/My Shared Files/out/followup');out.mkdir(exist_ok=True)
log=pathlib.Path.home()/'Library/Logs/Hey Jev.log';bin=pathlib.Path.home()/'lab/bin'
start=len(log.read_text().splitlines())
def events():
 return [json.loads(x[10:]) for x in log.read_text().splitlines()[start:] if x.startswith('LAB_STATE ')]
def speak(s):
 print('INJECT',s,flush=True);subprocess.run([str(bin/'say-mic'),s],check=True)
rec=subprocess.Popen([str(bin/'record-out'),'60',str(out/'answer.wav')],stderr=subprocess.PIPE,text=True)
result={}
try:
 time.sleep(.4);speak('Hey Jeff.')
 deadline=time.monotonic()+20
 while time.monotonic()<deadline:
  if any(e['state']=='Listening' for e in events()):break
  time.sleep(.05)
 else:raise RuntimeError('no Listening state')
 speak('What is the capital of France?')
 deadline=time.monotonic()+50
 while time.monotonic()<deadline:
  es=events()
  if any(e['state']=='Speaking' for e in es) and es[-1]['state']=='Ready':break
  time.sleep(.1)
 else:raise RuntimeError('no completed answer')
 result={'events':events(),'completed':True}
finally:
 rec.send_signal(signal.SIGINT);_,err=rec.communicate(timeout=10)
 (out/'capture.txt').write_text(err or '')
 (out/'app.txt').write_text('\n'.join(log.read_text().splitlines()[start:])+'\n')
 result['events']=events();(out/'result.json').write_text(json.dumps(result,indent=2))
p=subprocess.run([str(bin/'transcribe'),str(out/'answer.wav')],capture_output=True,text=True,check=True)
(out/'transcript.txt').write_text(p.stdout)
print(p.stdout,flush=True)
