import { writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { DotAgent } from '/Users/csells/code/CopilotKit/OpenDots/src/server/dot-agent.ts';
import { Store } from '/Users/csells/code/CopilotKit/OpenDots/src/server/store.ts';
import { WorkspaceStore } from '/Users/csells/code/CopilotKit/OpenDots/src/server/workspace.ts';
const require = createRequire('/Users/csells/code/CopilotKit/OpenDots/package.json');
const {lastValueFrom,toArray} = require('rxjs');
const out='/Users/csells/.bb/thread-storage/opendots-test-20261005';
const store=new Store(out+'/component.sqlite');
const workspace=new WorkspaceStore(out+'/component.sqlite','opendots-lab');
const dot=workspace.dots()[0];
workspace.bindThread('lab-component',dot.id,'Local model component probe');
// This probe does not instantiate Platform/Intelligence. The gate value is never
// transmitted; it enables direct execution of the real DotAgent against Ollama.
const config={intelligenceKey:'unused-component-probe',apiKey:'ollama',model:'qwen2.5:7b-instruct-q4_K_M',baseUrl:'http://127.0.0.1:11434/v1',runtimeUrl:'',voiceName:'marin',slackUsers:[],webSearchProvider:'disabled' as const};
const originalFetch=globalThis.fetch;
const requests:any[]=[];
globalThis.fetch=async(input:any,init:any)=>{
 const url=String(input instanceof Request?input.url:input);
 if(!url.startsWith('http://127.0.0.1:11434/'))throw new Error('Probe blocked unexpected external request: '+url);
 requests.push({url,time:new Date().toISOString()});
 return originalFetch(input,init);
};
const results:any[]=[];
async function turn(id:string,prompt:string){
 console.log('START',id,new Date().toISOString());
 const agent=new DotAgent(store,workspace,config,dot.id);
 const events=await lastValueFrom(agent.run({threadId:'lab-component',runId:id,messages:[{id:id+'-prompt',role:'user',content:prompt}],tools:[],context:[],state:{},forwardedProps:{}}).pipe(toArray()));
 const text=events.filter((e:any)=>['TEXT_MESSAGE_CONTENT','TEXT_MESSAGE_CHUNK'].includes(e.type)).map((e:any)=>e.delta).join('');
 const errors=events.filter((e:any)=>e.type==='RUN_ERROR');
 console.log('DONE',id,JSON.stringify({text,errors,tools:events.filter((e:any)=>e.type==='TOOL_CALL_START')}));
 writeFileSync(out+'/'+id+'-events.json',JSON.stringify(events,null,2));
 results.push({id,text,errors});
}
try{
 await turn('local-answer','What is two plus two? Answer in one short sentence.');
 await turn('local-page','Create a page in your default Space titled Jarvis lab proof with exactly this body: The violet notebook has seven pages. Use the page tool, then give me the link.');
 const pages=workspace.pages.list(dot.spaceId);
 const saved=pages.find((p:any)=>p.title==='Jarvis lab proof');
 console.log('SAVED_PAGE',JSON.stringify(saved??null));
 writeFileSync(out+'/live-component-results.json',JSON.stringify({scope:'Direct upstream DotAgent, real local Ollama model and real SQLite writes. No Intelligence transport, browser conversation, or voice tested.',model:config.model,results,saved,requests},null,2));
 if(!saved?.content.includes('The violet notebook has seven pages.'))process.exitCode=1;
}finally{store.close();workspace.close();}
