"""Loopback-only test bridge to the official, subscription-authenticated Claude CLI."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, subprocess, time
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args): pass
 def do_POST(self):
  if self.path!='/ask': self.send_error(404); return
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<16384: raise ValueError('invalid length')
   text=json.loads(self.rfile.read(length))['text']
   t=time.monotonic()
   p=subprocess.run(['claude','-p','--safe-mode','--tools','','--no-session-persistence','--model','haiku','--output-format','json','--system-prompt','You are a voice assistant. Answer in one short spoken sentence, no markdown.'],input=text,text=True,capture_output=True,timeout=90)
   if p.returncode: raise RuntimeError('Claude CLI exited '+str(p.returncode))
   result=json.loads(p.stdout)
   if result.get('is_error'): raise RuntimeError('Claude reported an error')
   response={'text':result['result'].strip(),'ms':int((time.monotonic()-t)*1000),'cost':None}
   print(json.dumps({'event':'subscription_answer','ms':response['ms'],'text':response['text']}),flush=True)
   body=json.dumps(response).encode();self.send_response(200)
  except Exception as e:
   print(type(e).__name__+': '+str(e),flush=True)
   body=json.dumps({'error':str(e)}).encode();self.send_response(502)
  self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
print('Bridge listening on 127.0.0.1:18765; tools disabled; credentials stay with official CLI',flush=True)
ThreadingHTTPServer(('127.0.0.1',18765),Handler).serve_forever()
