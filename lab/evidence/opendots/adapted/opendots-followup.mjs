import {createRequire} from 'node:module';
import {readFileSync,writeFileSync} from 'node:fs';
const require=createRequire('/home/tester/code/CopilotKit/OpenDots/package.json');
const {chromium}=require('playwright');
const out='/home/tester/evidence/followup';
const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required','--use-fake-ui-for-media-stream']});
const events=[]; const requests=[];
const p=await browser.newPage({viewport:{width:1440,height:1000},hasTouch:true});
p.on('pageerror',e=>console.log('PAGE_ERROR',e.message));
p.on('response',async r=>{if(r.url().includes('/api/'))requests.push({url:r.url(),status:r.status()});});
await p.exposeFunction('recordEvent',e=>{events.push({at:Date.now(),...e}); if(!e.type?.includes('delta'))console.log('EVENT',JSON.stringify(e).slice(0,1200));});
await p.addInitScript(()=>{
 window.lab={recorders:[],chunks:[],streams:[],pcs:[]};
 const ac=new AudioContext({sampleRate:48000});const dest=ac.createMediaStreamDestination();window.lab.ac=ac;const silence=ac.createOscillator();const gain=ac.createGain();gain.gain.value=0.000001;silence.connect(gain).connect(dest);silence.start();
 navigator.mediaDevices.getUserMedia=async()=>{await ac.resume();return dest.stream;};
 window.lab.play=async base64=>{await ac.resume();const buf=await ac.decodeAudioData(Uint8Array.from(atob(base64),c=>c.charCodeAt(0)).buffer);const src=ac.createBufferSource();src.buffer=buf;src.connect(dest);src.start();return buf.duration;};
 const RTC=window.RTCPeerConnection;
 window.RTCPeerConnection=class extends RTC{
 constructor(...args){super(...args);window.lab.pcs.push(this);this.addEventListener('track',e=>{const stream=new MediaStream([e.track]);window.lab.streams.push(stream);const rec=new MediaRecorder(stream,{mimeType:'audio/webm;codecs=opus'});rec.ondataavailable=e=>window.lab.chunks.push(e.data);rec.start(1000);window.lab.recorders.push(rec);});}
 createDataChannel(...args){const dc=super.createDataChannel(...args);dc.addEventListener('message',e=>{try{window.recordEvent(JSON.parse(e.data));}catch{}});return dc;}
 };
});
async function speak(name){console.log('SPEAK',name);const duration=await p.evaluate(b=>window.lab.play(b),readFileSync('/home/tester/evidence/'+name+'.wav').toString('base64'));await p.waitForTimeout(duration*1000+2000);}
async function waitEvent(type,from,timeout=65000){const start=Date.now();while(Date.now()-start<timeout){const e=events.slice(from).find(e=>e.type===type);if(e)return e;await p.waitForTimeout(1000);}throw new Error('Timed out '+type);}
try {
 await p.goto('http://127.0.0.1:14310');
 const ws=await(await p.request.get('http://127.0.0.1:14310/api/workspace')).json();
 const conv=await p.request.post('http://127.0.0.1:14310/api/conversations',{data:{dotId:ws.dots[0].id,title:'Voice followup default destination'}});console.log('CREATE',conv.status(),await conv.text());
 await p.reload();await p.getByRole('button',{name:/Voice followup default destination/}).last().click();await p.setViewportSize({width:390,height:844});
 await p.getByRole('button',{name:'Start voice call',exact:true}).click({timeout:20000});
 await waitEvent('session.updated',0,35000); console.log('CALL_CONNECTED');
 await p.screenshot({path:out+'/call-connected.png',fullPage:true});
 let n=events.length;await speak('opendots-retry');await waitEvent('response.function_call_arguments.done',n,70000);await p.waitForTimeout(25000);
 await p.screenshot({path:out+'/call-compute.png',fullPage:true});
 await p.getByRole('button',{name:'Mute microphone',exact:true}).click();console.log('MUTED_TRACKS',await p.evaluate(()=>window.lab.pcs.flatMap(pc=>pc.getSenders().map(s=>s.track?.enabled))));
 await p.getByRole('button',{name:'Unmute microphone',exact:true}).click();
 await p.getByRole('button',{name:'Minimize call view',exact:true}).click();await p.screenshot({path:out+'/call-minimized.png',fullPage:true});
 await p.getByRole('button',{name:'Expand call view',exact:true}).click();
 await p.getByRole('button',{name:'End voice call',exact:true}).last().click();
 await p.getByRole('button',{name:'Start voice call',exact:true}).waitFor({timeout:60000});
 console.log('CALL_ENDED');
 await p.waitForTimeout(2000);
 console.log('AFTER_CALL_UI',await p.locator('body').innerText());
 await p.getByRole('textbox',{name:'Message your Dot'}).fill('What was the page title and sentence I asked for during our call? Answer briefly from conversation history.');
 const done=p.waitForResponse(r=>r.url().includes('/run') && r.request().method()==='POST',{timeout:60000});
 await p.getByRole('textbox',{name:'Message your Dot'}).press('Enter');
 const result=await done;await result.finished();await p.waitForTimeout(1500);
 console.log('TEXT_FOLLOWUP',await p.locator('body').innerText());
 await p.screenshot({path:out+'/text-followup.png',fullPage:true});
} catch(e) {console.log('TEST_ERROR',e.stack);console.log('BODY',await p.locator('body').innerText());await p.screenshot({path:out+'/call-error.png',fullPage:true});}
finally {
 await p.evaluate(async()=>{for(const r of window.lab.recorders){if(r.state!=='inactive'){await new Promise(resolve=>{r.onstop=resolve;r.stop();});}}});
 const audio=await p.evaluate(async()=>{const bytes=new Uint8Array(await new Blob(window.lab.chunks).arrayBuffer());let s='';for(const b of bytes)s+=String.fromCharCode(b);return btoa(s);});writeFileSync(out+'/remote-audio.webm',Buffer.from(audio,'base64'));
 writeFileSync(out+'/events.json',JSON.stringify(events,null,2));writeFileSync(out+'/requests.json',JSON.stringify(requests,null,2));
 writeFileSync(out+'/final-ui.txt',await p.locator('body').innerText());
 const ws=await(await p.request.get('http://127.0.0.1:14310/api/workspace')).json();for(const call of ws.calls)if(call.threadId)writeFileSync(out+'/thread-'+call.threadId+'.json',JSON.stringify(await(await p.request.get('http://127.0.0.1:14310/api/copilotkit/threads/'+call.threadId+'/messages')).json(),null,2));writeFileSync(out+'/workspace-after.json',JSON.stringify(ws,null,2));
 for(const space of ws.spaces)writeFileSync(out+'/pages-'+space.id+'.json',JSON.stringify(await(await p.request.get('http://127.0.0.1:14310/api/spaces/'+space.id+'/pages')).json(),null,2));
 await browser.close();
}
