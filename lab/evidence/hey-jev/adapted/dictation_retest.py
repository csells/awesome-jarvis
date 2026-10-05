"""Drive the adapted native app with real virtual-microphone speech and capture output."""
import json, os, pathlib, signal, subprocess, time, traceback
OUT=pathlib.Path('/Volumes/My Shared Files/out/dictation-retest');OUT.mkdir(exist_ok=True)
LOG=pathlib.Path.home()/'Library/Logs/Hey Jev.log'
BIN=pathlib.Path.home()/'lab/bin'
results=[]

def events(start):
 rows=[]
 for line in LOG.read_text().splitlines()[start:]:
  if line.startswith('LAB_STATE '):
   try: rows.append(json.loads(line[len('LAB_STATE '):]))
   except json.JSONDecodeError: pass
 return rows

def shot(name):
 p=OUT/(name+'.png')
 subprocess.run(['/usr/sbin/screencapture','-x',str(p)],check=True)

def speak(text):
 print('INJECT '+text,flush=True)
 subprocess.run([str(BIN/'say-mic'),text],check=True)
 return time.time()

def turn(name,phrase,barge=None,finish_state='Ready',timeout=65):
 print('TEST '+name,flush=True)
 start=len(LOG.read_text().splitlines())
 record=subprocess.Popen([str(BIN/'record-out'),'90',str(OUT/(name+'.wav'))],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
 time.sleep(.4)
 row={'test':name,'phrase':phrase};seen=set();interrupt=False
 try:
  ended=speak(phrase);row['injected_end']=ended
  deadline=time.monotonic()+timeout
  while time.monotonic()<deadline:
   evs=events(start)
   for e in evs:
    state=e['state']
    if state not in seen:
     print('STATE '+state+' '+e['detail'],flush=True);seen.add(state)
     shot(name+'-'+state.lower().replace(' ','-'))
     if barge and state=='Speaking' and not interrupt:
      time.sleep(1.5);row['interruption_end']=speak(barge);interrupt=True
   if evs and evs[-1]['state']==finish_state and (len(evs)>1 or finish_state!='Ready'):
    time.sleep(.7)
    row['events']=events(start);row['complete']=True;break
   if any(e['state']=='Something went wrong' for e in evs):
    row['events']=evs;row['complete']=False;break
   time.sleep(.1)
  else:row['events']=events(start);row['complete']=False;row['error']='timeout'
 finally:
  record.send_signal(signal.SIGINT)
  _,err=record.communicate(timeout=10)
  if err:(OUT/(name+'-capture.txt')).write_text(err)
  row['recorder_exit']=record.returncode
  segment='\n'.join(LOG.read_text().splitlines()[start:])+'\n'
  (OUT/(name+'-app.txt')).write_text(segment)
  if barge:
   time.sleep(3)
   row['post_interrupt_events']=events(start)
  p=subprocess.run([str(BIN/'transcribe'),str(OUT/(name+'.wav'))],capture_output=True,text=True,timeout=60)
  row['transcript']=p.stdout.strip();row['transcriber_exit']=p.returncode
  print('HEARD '+row['transcript'],flush=True)
  results.append(row);(OUT/'results.json').write_text(json.dumps(results,indent=2))
 return row


try:
 shot('initial')
 target=pathlib.Path.home()/'hey-jev-dictation-test.txt';target.write_text('')
 subprocess.run(['open','-a','TextEdit',str(target)],check=True);time.sleep(1)
 turn('16-dictation-start','Hey Jeff, transcribe.',finish_state='Dictating')
 speak('The blue notebook is on the wooden desk.');time.sleep(2)
 turn('17-dictation-stop','Hey Jeff, stop transcribing.')
 clipboard=subprocess.run(['pbpaste'],capture_output=True,text=True,check=True).stdout
 subprocess.run(['osascript','-e','tell application "System Events" to keystroke "s" using command down'],check=True)
 time.sleep(1)
 print('DICTATION CLIPBOARD '+repr(clipboard),flush=True)
 (OUT/'dictation-result.json').write_text(json.dumps({'clipboard':clipboard,'saved_file':target.read_text()},indent=2))
 shot('dictation-pasted')
finally:
 print('FINISHED '+str(len(results))+' voice steps',flush=True)
