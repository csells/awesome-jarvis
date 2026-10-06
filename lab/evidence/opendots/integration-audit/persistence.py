import json,urllib.request,sys
from pathlib import Path
p=Path('/home/tester/evidence/integration-audit');k=json.loads((p/'owner.json').read_text())['owner']
def get(path):
 with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:14310/api'+path,headers={'Authorization':'Bearer '+k}),timeout=30) as r:return json.load(r)
w=get('/workspace');reference=json.loads((p/'live/workspace.json').read_text());call=next(c for c in reference['calls'] if 'orange notebook' in c.get('transcript',''))
pages=[page for s in w['spaces'] for page in get('/spaces/'+s['id']+'/pages')]
history=get('/copilotkit/threads/'+call['threadId']+'/messages')
result={'threadId':call['threadId'],'history':history,'pages':pages,'calls':w['calls']}
(p/('persistence-'+sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2))
print(sys.argv[1], 'history messages',len(history['messages']),'pages',len(pages),'calls',len(w['calls']))
