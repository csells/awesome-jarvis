from pathlib import Path
import json, sys
import numpy as np
import soundfile as sf
from mlx_audio.stt.generate import load_model
import mlx.core as mx
root=Path('/Users/csells/.bb/thread-storage/opendots-adapted-20261005')
model=load_model('mlx-community/parakeet-tdt-0.6b-v3')
for name in (sys.argv[1:] or ['remote-audio','followup-audio']):
 p=root/(name+'.wav')
 if not p.exists():continue
 a,sr=sf.read(p); print('TRANSCRIBE',name,len(a)/sr,flush=True)
 segments=[]
 for start in range(0,len(a),sr*20):
  chunk=a[start:start+sr*20]
  if np.max(np.abs(chunk))<.005:continue
  result=model.decode_chunk(mx.array(chunk,dtype=mx.float32),verbose=False)
  segments.append({'start':start/sr,'end':(start+len(chunk))/sr,'text':result.text})
  print(segments[-1],flush=True)
 (root/(name+'.transcript.json')).write_text(json.dumps(segments,indent=2))
 (root/(name+'.transcript.txt')).write_text('\n'.join(f"[{s['start']:.0f}-{s['end']:.0f}s] {s['text']}" for s in segments)+'\n')
