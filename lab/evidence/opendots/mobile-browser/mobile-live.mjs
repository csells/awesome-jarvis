import {createRequire} from 'node:module';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {spawn} from 'node:child_process';
const require=createRequire('/home/tester/code/CopilotKit/OpenDots/package.json');
const {chromium,devices}=require('playwright');
const root='/home/tester/evidence/mobile-full',out=root+'/live';mkdirSync(out,{recursive:true});
const owner=JSON.parse(readFileSync(root+'/owner.json')).owner;
const log=console.log;console.log=(...args)=>log(...args.map(v=>typeof v==='string'?v.replaceAll(owner,'[redacted]'):v));
const base='https://chriss-mac-mini.tail3127c0.ts.net:8444';
const browser=await chromium.launch({headless:false,ignoreDefaultArgs:['--mute-audio'],args:['--host-resolver-rules=MAP chriss-mac-mini.tail3127c0.ts.net 127.0.0.1'],env:{...process.env,PULSE_SOURCE:'jarvis_mic',PULSE_SINK:'voice_output'}});
const ctx=await browser.newContext({...devices['Pixel 7'],permissions:['microphone']});
const p=await ctx.newPage();const events=[],checks=[],errors=[],audio=[],marks=[];let bytes=0,rms=0,lastSound=0,maxRms=0,step='setup';
const recorder=spawn('parec',['--device=voice_output.monitor','--raw','--format=s16le','--rate=24000','--channels=1','--latency-msec=40']);
recorder.stdout.on('data',b=>{audio.push(b);bytes+=b.length;let sum=0;for(let i=0;i+1<b.length;i+=2)sum+=(b.readInt16LE(i)/32768)**2;rms=Math.sqrt(sum/(b.length/2));maxRms=Math.max(maxRms,rms);if(rms>.01)lastSound=Date.now();});
recorder.stderr.on('data',b=>console.log('RECORDER',b.toString().trim()));
p.on('pageerror',e=>{errors.push(e.message);console.log('PAGE_ERROR',e.message)});
await p.exposeFunction('recordVoiceEvent',e=>{events.push({at:Date.now(),...e});if(['error','response.done','conversation.item.input_audio_transcription.completed','response.function_call_arguments.done'].includes(e.type))console.log('EVENT',JSON.stringify(e).slice(0,1000));});
await p.addInitScript(()=>{
 window.lab={pcs:[],streams:[],audios:[]};
 const native=navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
 navigator.mediaDevices.getUserMedia=async(...args)=>{const stream=await native(...args);window.lab.streams.push(stream);return stream;};
 const play=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(...args){if(!window.lab.audios.includes(this))window.lab.audios.push(this);return play.apply(this,args);};
 const RTC=window.RTCPeerConnection;window.RTCPeerConnection=class extends RTC{constructor(...a){super(...a);window.lab.pcs.push(this);}createDataChannel(...a){const dc=super.createDataChannel(...a);dc.addEventListener('message',e=>{try{window.recordVoiceEvent(JSON.parse(e.data));}catch{}});return dc;}};
});
function assert(ok,message){if(!ok)throw new Error(message);}
async function waitUntil(fn,timeout=60000){const start=Date.now();while(Date.now()-start<timeout){if(await fn())return;await p.waitForTimeout(100);}throw new Error('Timed out waiting in '+step);}
async function event(type,from=0,timeout=60000){await waitUntil(()=>events.slice(from).some(e=>e.type===type),timeout);return events.slice(from).find(e=>e.type===type);}
async function speak(name){marks.push({name,at:Date.now(),audioSeconds:bytes/48000});console.log('MIC',name);await new Promise((resolve,reject)=>{const c=spawn('paplay',['--device=voice_input','/home/tester/evidence/'+name+'.wav']);c.on('exit',code=>code===0?resolve():reject(new Error('paplay '+code)));});}
async function quiet(){await waitUntil(()=>Date.now()-lastSound>1500,30000);}
async function check(name,fn){step=name;console.log('STEP',checks.length+1,name);const start=Date.now();try{const details=await fn();checks.push({name,result:'PASS',seconds:(Date.now()-start)/1000,details});console.log('PASS',name);}catch(e){checks.push({name,result:'FAIL',error:e.message});throw e;}}
async function api(path){const r=await p.request.get(base+'/api'+path,{headers:{Authorization:'Bearer '+owner}});assert(r.ok(),'GET '+path+' '+r.status());return r.json();}
try{
 await check('fresh mobile authentication and navigation',async()=>{
  await p.goto(base);await p.getByRole('textbox',{name:'Owner access token'}).fill('wrong-test-token');await p.getByRole('button',{name:'Unlock OpenDots',exact:true}).click();await p.getByRole('alert').waitFor();
  await p.getByRole('textbox',{name:'Owner access token'}).fill(owner);await p.getByRole('button',{name:'Unlock OpenDots',exact:true}).click();await p.getByRole('button',{name:'Open navigation',exact:true}).click();await p.getByRole('button',{name:'New chat',exact:true}).click();
  await p.getByRole('button',{name:'Start voice call',exact:true}).waitFor();await p.screenshot({path:out+'/mobile-chat.png',fullPage:true});return {viewport:p.viewportSize(),secure:await p.evaluate(()=>isSecureContext)};
 });
 await check('native microphone and WebRTC connection',async()=>{
  await p.getByRole('button',{name:'Start voice call',exact:true}).click();await event('session.updated',0,40000);
  await waitUntil(()=>p.evaluate(()=>window.lab.pcs.some(pc=>pc.connectionState==='connected')),20000);
  const media=await p.evaluate(async()=>{const pc=window.lab.pcs.at(-1);const stats=await pc.getStats();const selected=[...stats.values()].find(s=>s.type==='candidate-pair'&&s.state==='succeeded');return{microphone:window.lab.streams.at(-1).getAudioTracks().map(t=>({label:t.label,settings:t.getSettings(),readyState:t.readyState})),ice:pc.getConfiguration(),selectedPair:selected?{local:stats.get(selected.localCandidateId),remote:stats.get(selected.remoteCandidateId)}:null};});
  await p.screenshot({path:out+'/call-connected.png',fullPage:true});return media;
 });
 await check('spoken question and audible browser playback',async()=>{const n=events.length;maxRms=0;await speak('opendots-question');await event('response.done',n);await waitUntil(()=>maxRms>.01,20000);await quiet();assert(events.slice(n).some(e=>e.transcript?.toLowerCase().includes('twelve')),'No twelve response');return{speakerPeakRms:maxRms};});
 await check('spoken task performs real page write',async()=>{const before=await api('/workspace');const existing=new Set((await Promise.all(before.spaces.map(s=>api('/spaces/'+s.id+'/pages')))).flat().map(p=>p.id));const n=events.length;await speak('opendots-retry');await event('response.function_call_arguments.done',n,90000);let pages=[];await waitUntil(async()=>{const w=await api('/workspace');pages=(await Promise.all(w.spaces.map(s=>api('/spaces/'+s.id+'/pages')))).flat();return pages.some(p=>!existing.has(p.id)&&p.title.toLowerCase()==='voice follow-up'&&/orange notebook/i.test(p.content));},90000);await p.waitForTimeout(7000);await quiet();writeFileSync(out+'/pages.json',JSON.stringify(pages,null,2));await p.screenshot({path:out+'/page-created.png',fullPage:true});return pages.map(p=>({id:p.id,title:p.title,body:p.body??p.content}));});
 await check('microphone mute blocks actual captured input',async()=>{await p.getByRole('button',{name:'Mute microphone',exact:true}).click();assert(await p.evaluate(()=>window.lab.streams.at(-1).getAudioTracks().every(t=>!t.enabled)),'Mic still enabled');const n=events.length;await speak('opendots-question');await p.waitForTimeout(3500);assert(!events.slice(n).some(e=>e.type==='conversation.item.input_audio_transcription.completed'),'Muted speech reached server');await p.getByRole('button',{name:'Unmute microphone',exact:true}).click();});
 await check('speaker mute suppresses real playback',async()=>{const buttons=await p.getByRole('button').evaluateAll(ns=>ns.map(n=>n.getAttribute('aria-label')));console.log('CALL_BUTTONS',buttons);await p.getByRole('button',{name:'Mute call audio',exact:true}).click();await p.waitForTimeout(500);maxRms=0;const n=events.length;await speak('opendots-question');await event('response.done',n);await p.waitForTimeout(2000);assert(maxRms<.01,'Muted speaker emitted audible PCM');await p.getByRole('button',{name:'Enable call audio',exact:true}).click();return{speakerPeakRms:maxRms};});
 await check('barge-in during measured speaker output',async()=>{const n=events.length;await speak('opendots-long');await waitUntil(()=>rms>.01,50000);await p.waitForTimeout(1000);marks.push({name:'interrupt-during-speaker-output',at:Date.now(),audioSeconds:bytes/48000,rms});await speak('opendots-interrupt');await waitUntil(()=>events.slice(n).some(e=>e.type==='response.output_audio_transcript.done'&&/Paris/i.test(e.transcript)),65000);await p.waitForTimeout(2000);await quiet();return events.slice(n).filter(e=>e.type==='response.done').map(e=>e.response.status);});
 await check('minimize and expand on mobile',async()=>{await p.getByRole('button',{name:'Minimize call view',exact:true}).click();await p.screenshot({path:out+'/call-minimized.png',fullPage:true});await p.getByRole('button',{name:'Expand call view',exact:true}).click();await p.screenshot({path:out+'/call-expanded.png',fullPage:true});});
 await check('hangup releases media and preserves same-chat follow-up',async()=>{await p.getByRole('button',{name:'End voice call',exact:true}).last().click();await p.getByRole('button',{name:'Start voice call',exact:true}).waitFor({timeout:65000});assert(await p.evaluate(()=>window.lab.streams.every(s=>s.getTracks().every(t=>t.readyState==='ended'))),'Microphone not released');await p.getByRole('textbox',{name:'Message your Dot'}).fill('What page title and sentence did I ask you to save in our voice call?');const response=p.waitForResponse(r=>r.url().includes('/run')&&r.request().method()==='POST',{timeout:65000});await p.getByRole('textbox',{name:'Message your Dot'}).press('Enter');await(await response).finished();await p.waitForTimeout(1000);const body=await p.locator('body').innerText();assert(/orange notebook/i.test(body),'Follow-up did not recall saved content');await p.screenshot({path:out+'/text-followup.png',fullPage:true});return body;});
}catch(e){console.log('TEST_ERROR',e.stack);console.log('BODY',await p.locator('body').innerText());await p.screenshot({path:out+'/failure.png',fullPage:true});process.exitCode=1;}
finally{
 try{const w=await api('/workspace');writeFileSync(out+'/workspace.json',JSON.stringify(w,null,2));for(const call of w.calls.filter(c=>['active','connecting'].includes(c.status))){console.log('CLEANUP_TEST_CALL',call.id);await p.request.post(base+'/api/voice/calls/'+call.id+'/end',{headers:{Authorization:'Bearer '+owner},data:{transcript:'Harness cleanup after unfinished test.'},timeout:70000});}}catch(e){errors.push(String(e.message).replaceAll(owner,'[redacted]'));}
 await browser.close();recorder.kill('SIGINT');await new Promise(r=>recorder.on('exit',r));const pcm=Buffer.concat(audio);const h=Buffer.alloc(44);h.write('RIFF');h.writeUInt32LE(pcm.length+36,4);h.write('WAVEfmt ',8);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(1,22);h.writeUInt32LE(24000,24);h.writeUInt32LE(48000,28);h.writeUInt16LE(2,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(pcm.length,40);writeFileSync(out+'/speaker.wav',Buffer.concat([h,pcm]));
 writeFileSync(out+'/results.json',JSON.stringify({checks,errors,marks},null,2));writeFileSync(out+'/events.json',JSON.stringify(events,null,2));console.log('RESULT',checks.map(c=>c.result+' '+c.name));
}
