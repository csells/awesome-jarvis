import io,json,wave,time
from pathlib import Path
from openai import OpenAI
root=Path('/Users/csells/.bb/thread-storage/opendots-integration-20261006');session=json.loads((root/'voice-session-verified.json').read_text())
c=OpenAI(base_url='http://127.0.0.1:18800/v1',api_key=session['api_key'],max_retries=0)
import sys
folder=sys.argv[1]
with wave.open(str(root/folder/'speaker.wav')) as w:rate=w.getframerate();audio=w.readframes(w.getnframes())
size=rate*2*20;segments=[];total=(len(audio)+size-1)//size
for i,start in enumerate(range(0,len(audio),size),1):
 chunk=audio[start:start+size]
 import array
 samples=array.array('h',chunk)
 if max(map(abs,samples),default=0)<150:continue
 f=io.BytesIO()
 with wave.open(f,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(chunk)
 f.seek(0)
 text=c.audio.transcriptions.create(model='whisper-1',file=('speaker.wav',f,'audio/wav')).text
 item={'start':start/(rate*2),'end':(start+len(chunk))/(rate*2),'text':text};segments.append(item)
 print(f'[{i}/{total}] {item}',flush=True)
(root/folder/'speaker-transcript.json').write_text(json.dumps(segments,indent=2))
