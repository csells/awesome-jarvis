import asyncio,tempfile,time,unittest,json
from pathlib import Path
import httpx
from fastapi.testclient import TestClient
from gateway import create_app
class Chunks(httpx.AsyncByteStream):
 async def __aiter__(self):
  yield b'first'
  await asyncio.sleep(.01)
  yield b'second'
 async def aclose(self):self.closed=True
class PocketGatewayTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name)/'key';p.write_text('test-secret');p.chmod(0o600)
  self.seen=[];self.stream=None;self.upstream_status=200
  async def handle(r):
   self.seen.append((r.url.host,r.url.path,r.content))
   if r.url.path=='/api/voices':return httpx.Response(200,json=[{'id':'ralph-fiennes'},{'id':'jeremy-irons'}])
   if r.url.path=='/v1/pool':return httpx.Response(200,json={'in_use':0,'units':[]})
   if r.url.path=='/api/tags':return httpx.Response(200,json={'models':[{'name':'test'}]})
   if r.url.host=='pocket' and r.url.path=='/v1/audio/speech':
    if self.upstream_status!=200:return httpx.Response(self.upstream_status,json={'detail':'unavailable'})
    self.stream=Chunks();return httpx.Response(200,stream=self.stream,headers={'content-type':'audio/pcm','x-sample-rate':'24000'})
   return httpx.Response(200,json={'ok':True})
  self.config={'admin_key_file':str(p),'model':'test','pocket_url':'http://pocket'}
  self.app=create_app(self.config,httpx.MockTransport(handle))
  self.client=TestClient(self.app);self.client.__enter__()
  r=self.client.post('/leases',headers={'Authorization':'Bearer test-secret'},json={'owner':'pocket-test'})
  assert r.status_code==201,r.text
  self.headers={'Authorization':'Bearer '+r.json()['api_key']}
  self.body={'model':'pocket-tts','voice':'alfred','input':'Good evening.','speed':1.3,'response_format':'pcm'}
 def tearDown(self):self.client.__exit__(None,None,None);self.tmp.cleanup()
 def test_pocket_routes_and_releases_capacity(self):
  r=self.client.post('/v1/audio/speech',headers=self.headers,json=self.body)
  self.assertEqual(r.status_code,200);self.assertEqual(r.content,b'firstsecond');self.assertEqual(r.headers['x-sample-rate'],'24000');self.assertTrue(self.stream.closed)
  self.assertTrue(any(host=='pocket' and path=='/v1/audio/speech' for host,path,_ in self.seen))
  self.assertEqual(self.client.delete('/leases/current',headers=self.headers).status_code,200)
 def test_invalid_voice_speed_and_format_never_reach_pocket(self):
  for patch in ({'speed':3},{'speed':True},{'response_format':'mp3'},{'input':' '*3},{'input':'x'*2001}):
   self.assertEqual(self.client.post('/v1/audio/speech',headers=self.headers,json={**self.body,**patch}).status_code,422)
  self.assertFalse(any(path=='/v1/audio/speech' for _,path,_ in self.seen))
 def test_upstream_error_releases_lock_and_is_returned(self):
  self.upstream_status=503
  self.assertEqual(self.client.post('/v1/audio/speech',headers=self.headers,json=self.body).status_code,503)
  self.assertEqual(self.client.delete('/leases/current',headers=self.headers).status_code,200)
 def test_missing_lease_is_rejected(self):
  self.assertEqual(self.client.post('/v1/audio/speech',json=self.body).status_code,401)

 def test_alfred_maps_to_approved_ralph_profile(self):
  self.assertEqual(self.client.post('/v1/audio/speech',headers=self.headers,json=self.body).status_code,200)
  body=json.loads(next(body for host,path,body in self.seen if path=='/v1/audio/speech'))
  self.assertEqual(body['voice'],'ralph-fiennes')
  self.assertEqual(body['speed'],1.3)
 def test_catalog_requires_lease_and_describes_alfred(self):
  self.assertEqual(self.client.get('/v1/voices').status_code,401)
  voices=self.client.get('/v1/voices',headers=self.headers).json()['voices']
  self.assertEqual(voices[0]['id'],'alfred')
  self.assertEqual(voices[0]['default_speed'],1.25)

 def test_unified_gateway_validates_models(self):
  self.config.update(speech_engine='pocket-tts',voice_catalog_url='http://pocket/v1/voices')
  for patch in ({'model':'unknown'},):
   self.assertEqual(self.client.post('/v1/audio/speech',headers=self.headers,json={**self.body,**patch}).status_code,422)
  self.assertFalse(any(path=='/v1/audio/speech' for _,path,_ in self.seen))
  self.assertEqual(self.client.post('/v1/audio/speech',headers=self.headers,json={'input':'Hello'}).status_code,200)

 def test_other_pocket_profile_is_routed_without_remapping(self):
  r=self.client.post('/v1/audio/speech',headers=self.headers,json={**self.body,'voice':'jeremy-irons'})
  self.assertEqual(r.status_code,200)
  body=json.loads(next(body for host,path,body in self.seen if path=='/v1/audio/speech'))
  self.assertEqual(body['voice'],'jeremy-irons')
