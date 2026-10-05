import {createRequire} from 'node:module';
import {writeFileSync} from 'node:fs';
const require=createRequire('/Users/csells/code/CopilotKit/OpenDots/package.json');
const {chromium}=require('playwright');
const out='/Users/csells/.bb/thread-storage/opendots-test-20261005';
const browser=await chromium.launch({executablePath:'/Users/csells/.chrome-agent/chromium/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:14310');
 await page.getByText('Settings & setup',{exact:true}).waitFor();
 await page.screenshot({path:out+'/desktop.png',fullPage:true});
 writeFileSync(out+'/desktop-text.txt',await page.locator('body').innerText());
 console.log(await page.locator('body').innerText());
 console.log('BUTTONS',await page.getByRole('button').evaluateAll(es=>es.map(e=>({text:e.textContent,label:e.getAttribute('aria-label'),disabled:e.disabled}))));
 await page.getByText('Settings & setup',{exact:true}).click();
 await page.screenshot({path:out+'/setup.png',fullPage:true});
 writeFileSync(out+'/setup-text.txt',await page.locator('body').innerText());
 const mobile=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2});
 await mobile.goto('http://127.0.0.1:14310');
 await mobile.getByText('Connect your Dot',{exact:true}).waitFor();
 await mobile.screenshot({path:out+'/mobile.png',fullPage:true});
 writeFileSync(out+'/mobile-text.txt',await mobile.locator('body').innerText());
 console.log('MOBILE BUTTONS',await mobile.getByRole('button').evaluateAll(es=>es.map(e=>({text:e.textContent,label:e.getAttribute('aria-label'),disabled:e.disabled}))));
 writeFileSync(out+'/ui-initial.json',JSON.stringify({browser:browser.version(),mobileViewport:{width:390,height:844},pageErrors:errors},null,2));
}finally{await browser.close()}
