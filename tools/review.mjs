// Real-browser checks for the static hub. Screenshots are restricted to CI.
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const captures=process.env.CI==='true';
const output=path.join(root,'review-output');
if(captures)fs.mkdirSync(output,{recursive:true});
const server=http.createServer((req,res)=>{
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405).end();return;}
  let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(name.endsWith('/'))name+='index.html';
  let file=path.resolve(root,'.'+name);
  if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  if(!fs.existsSync(file)&&fs.existsSync(file+'.html'))file+='.html';
  if(!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404).end();return;}
  const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json','.woff2':'font/woff2','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.jpg':'image/jpeg'};
  res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');
  res.end(req.method==='HEAD'?undefined:fs.readFileSync(file));
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin=`http://127.0.0.1:${server.address().port}`;
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'galileo-site-browser-'));
const chrome=process.env.CHROME||(process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome');
const proc=spawn(chrome,['--headless=new','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--no-first-run','--no-default-browser-check','--mute-audio','about:blank'],{stdio:['ignore','ignore','pipe']});
let ws;
const problems=[];const results=[];
try{
  const endpoint=await new Promise((resolve,reject)=>{let text='';const timeout=setTimeout(()=>reject(new Error('Chrome startup timed out')),15000);proc.stderr.on('data',d=>{text+=d;const m=/DevTools listening on (ws:\S+)/.exec(text);if(m){clearTimeout(timeout);resolve(m[1]);}});proc.once('error',reject);proc.once('exit',c=>{clearTimeout(timeout);reject(new Error(`Chrome exited ${c}`));});});
  ws=new WebSocket(endpoint);await new Promise(r=>ws.addEventListener('open',r,{once:true}));
  let id=1;const pending=new Map();const listeners=[];
  ws.addEventListener('message',event=>{const m=JSON.parse(event.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timeout);m.error?p.reject(new Error(m.error.message)):p.resolve(m.result);}else if(m.method)listeners.forEach(f=>f(m));});
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=id++;const timeout=setTimeout(()=>{pending.delete(n);reject(new Error(method+' timed out'));},12000);pending.set(n,{resolve,reject,timeout});ws.send(JSON.stringify({id:n,method,params,sessionId}));});
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  for(const [width,height] of [[360,800],[430,932],[768,1024],[1280,900]]){
    const size=`${width}x${height}`;
    const {targetId}=await send('Target.createTarget',{url:'about:blank'});
    const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
    const S=(m,p={})=>send(m,p,sessionId);
    const evaluate=async expression=>{const r=await S('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result.value;};
    const click=async selector=>{
      const r=await evaluate(`(async()=>{const e=document.querySelector(${JSON.stringify(selector)});if(!e)throw Error('Missing control');e.scrollIntoView({block:'center',behavior:'instant'});await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const r=e.getBoundingClientRect();const v=visualViewport;return{x:(r.x+r.width/2-v.offsetLeft)*v.scale,y:(r.y+r.height/2-v.offsetTop)*v.scale}})()`);
      await S('Input.dispatchMouseEvent',{type:'mouseMoved',...r});
      await S('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',buttons:1,clickCount:1,...r});
      await S('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',buttons:0,clickCount:1,...r});
    };
    const shot=async name=>{if(!captures)return;const r=await S('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(output,`${size}_${name}.png`),Buffer.from(r.data,'base64'));};
    listeners.length=0;
    listeners.push(m=>{if(m.sessionId!==sessionId)return;if(m.method==='Runtime.exceptionThrown')problems.push(size+' '+(m.params.exceptionDetails.exception?.description||m.params.exceptionDetails.text));if(m.method==='Network.requestWillBeSent'){const u=m.params.request.url;if(!u.startsWith(origin)&&!u.startsWith('data:')&&!u.startsWith('blob:'))problems.push(size+' external request '+u);}if(m.method==='Network.responseReceived'&&m.params.response.status>=400)problems.push(size+' HTTP '+m.params.response.status+' '+m.params.response.url);});
    await S('Runtime.enable');await S('Network.enable');await S('Page.enable');await S('Page.bringToFront');
    await S('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<500});
    await S('Page.navigate',{url:origin+'/play/'});await wait(900);
    await evaluate('document.fonts.ready.then(()=>true)');
    assert.equal(await evaluate('document.querySelectorAll("[data-demo]").length'),5);
    assert.equal(await evaluate('document.documentElement.scrollWidth<=innerWidth'),true,size+' horizontal overflow');
    assert.equal(await evaluate('document.querySelector("iframe")===null'),true,'demo starts only after a tap');
    await S('Runtime.evaluate',{expression:'window.scrollTo(0,0)'});await shot('hub');
    for(const slug of ['corral','eight-seconds','gold-shaft','tumbleweed','idle-rancher']){
      await click(`[data-demo="${slug}"]`);await click('#start');await wait(750);
      assert.equal(await evaluate(`document.querySelector('iframe').getAttribute('src')`),`/play/demos/${slug}.html`);
      assert.equal(await evaluate(`document.querySelector('iframe').getAttribute('sandbox')`),'allow-scripts');
      assert.equal(await evaluate('document.querySelectorAll("iframe").length'),1);
      assert.equal(await evaluate('document.documentElement.scrollWidth<=innerWidth'),true);
      await shot(slug);results.push({size,case:slug,passed:true});
      await click('#restart');await wait(100);
    }
    const before=await evaluate('document.documentElement.lang');await click('#language');
    assert.notEqual(await evaluate('document.documentElement.lang'),before);
    await evaluate(`(()=>{const f=document.getElementById('feedback');f.elements.clear.value='yes';f.elements.again.value='maybe';f.elements.bug.value='no';f.elements.note.value='Browser QA sample';return true})()`);
    await click('#feedback button[type=submit]');
    const data=JSON.parse(await evaluate('document.getElementById("feedback-text").value'));
    assert.equal(data.game,'idle-rancher');assert.equal(data.note,'Browser QA sample');assert.equal(data.again,'maybe');
    assert.equal(await evaluate('document.getElementById("feedback-result").hidden'),false);
    assert.equal(await evaluate('document.cookie'), '');
    assert.equal(await evaluate('localStorage.length'),0);
    await shot('feedback');results.push({size,case:'language-and-local-feedback',passed:true});
    await send('Target.closeTarget',{targetId});
    console.log(size+' five demo loads/restarts, language, local feedback and layout PASS');
  }
  assert.deepEqual(problems,[]);
  if(captures)fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({results,problems},null,2)+'\n');
  console.log(`${results.length} browser cases passed; no external requests or page exceptions; screenshots ${captures?'saved in CI':'skipped locally'}`);
}catch(error){console.error('Browser problems:',JSON.stringify(problems));throw error;}finally{
  ws?.close();proc.kill();server.close();
  await new Promise(r=>{if(proc.exitCode!==null)return r();proc.once('exit',r);setTimeout(r,3000);});
  fs.rmSync(profile,{recursive:true,force:true});
}
