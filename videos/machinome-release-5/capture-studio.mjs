// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Photograph the real Studio UI with browser-local session/chat fixtures.
// No session is opened on the broker and no conversation is submitted.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const base=dirname(fileURLToPath(import.meta.url));
const [tool,viewer,origin='http://127.0.0.1:9000']=process.argv.slice(2);
assert.ok(tool&&viewer,'Pass the Videomaker checkout and viewer bundle.');
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const model=resolve(base,'../machinome-release-3/_build/model');
const session='release-video-staged-capture';
const prefix=`/api/sessions/${session}/`;
const message=`The sawmill adjustments are complete.

✓ Waterwheel and crankshaft are linked through the drive relation.

✓ The connecting rod moves the saw through its full up-and-down stroke.

✓ The driving pawl advances the ratchet, and the holding pawl keeps that progress while it returns.

✓ Both ropes follow the compound shaft through to the timber carriage.

✓ Blade clearance is checked against both halves of the timber at thirteen positions across a full wheel turn.

✓ Source, tests and the browser model are ready for review.

The machine is moving in the viewer. You can inspect the mechanism or ask for another adjustment.`;
const run={id:session,status:'open',profile_id:'openspec-builder',work_mode:'direct',
  user_label:'You',user_agent:{id:'builder',label:'Builder'},roster:[{id:'builder',label:'Builder'}],
  agents:[{role:'builder',label:'Builder',state:'waiting',failure:'',backend:'codex',provider:null,
    model:'',effort:'',tools:[],backend_idle:true,runtime_idle:true,runtime_pristine:false,
    assignment_id:null,pending_assignments:[]}],activity:[],events:[],latest_event_sequence:1,
  model_build_error:null,model_building:false};
const browser=await chromium.launch({headless:true});
await mkdir(resolve(base,'assets'),{recursive:true});
await mkdir(resolve(base,'_build/studio-capture'),{recursive:true});
try{
  const context=await browser.newContext({viewport:{width:1280,height:720},deviceScaleFactor:3});
  const page=await context.newPage();
  const errors=[],mutations=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(({run,message})=>{
    // Stop real event subscriptions; render a fixed, disclosed demonstration.
    window.EventSource=class extends EventTarget{
      constructor(){super();this.readyState=1;setTimeout(()=>{
        this.onopen?.(new Event('open'));
        this.dispatchEvent(new MessageEvent('snapshot',{data:JSON.stringify({run,
          conversation:[{sequence:1,author:'builder',text:message}]})}));
      },25);}
      close(){this.readyState=2;}
    };
  },{run,message});
  await page.route('**/*',async route=>{
    const request=route.request(),url=new URL(request.url());
    if(!['GET','HEAD'].includes(request.method())){
      mutations.push(`${request.method()} ${url.pathname}`);return route.abort();
    }
    if(url.pathname==='/api/entries'){
      const response=await route.fetch(),data=await response.json();
      data.entries=data.entries.map(entry=>entry.path==='Leonardo/hydraulic_sawmill'
        ?{...entry,state:'open',session_id:session}:entry);
      return route.fulfill({json:data});
    }
    if(url.pathname===prefix+'viewer/machinome-viewer.js')
      return route.fulfill({path:resolve(viewer),contentType:'text/javascript'});
    if(url.pathname.startsWith(prefix+'artifacts/')){
      const relative=decodeURIComponent(url.pathname.slice((prefix+'artifacts/').length));
      const path=resolve(model,relative==='viewer.json'?'manifest.json':relative);
      assert.ok(path.startsWith(model+'/'));
      return route.fulfill({path,contentType:path.endsWith('.json')?'application/json':'application/octet-stream'});
    }
    if(url.pathname.startsWith(prefix+'source'))return route.fulfill({json:{entries:[]}});
    if(url.pathname.startsWith(prefix))return route.fulfill({status:404,body:'Capture-only session'});
    return route.continue();
  });
  await page.goto(origin+'/projects/Leonardo/hydraulic_sawmill');
  await page.locator('.functional-model-host canvas').waitFor({timeout:60000});
  await page.getByText('Water drive',{exact:true}).waitFor({timeout:60000});
  await page.evaluate(()=>document.fonts.ready);
  await page.addStyleTag({content:'.conversation-transcript::-webkit-scrollbar{width:6px}.conversation-transcript::-webkit-scrollbar-thumb{background:#5b626c;border-radius:3px}.conversation-transcript::-webkit-scrollbar-track{background:#121419}'});
  await page.screenshot({path:resolve(base,'_build/studio-capture/model-open.png')});
  const geometry=await page.evaluate(()=>{
    const transcript=document.querySelector('.conversation-transcript');
    const item=transcript.querySelector('li');
    // Long scroll without manufacturing thousands of words; only its tail is seen.
    item.style.paddingTop='3000px';item.style.flexShrink='0';
    transcript.scrollTop=transcript.scrollHeight;
    const host=document.querySelector('.functional-model-host');
    // Keep the assembly navigator and all real UI. The live film supplies the model.
    host.style.visibility='hidden';
    const box=selector=>{const r=document.querySelector(selector).getBoundingClientRect();
      return {x:r.x,y:r.y,width:r.width,height:r.height};};
    return {viewport:{width:innerWidth,height:innerHeight},model:box('.functional-model-host'),
      chat:box('.conversation'),input:box('textarea'),
      code:box('[data-workspace-area="code"]'),build:box('[data-workspace-area="build"]'),
      scroll:{top:transcript.scrollTop,height:transcript.scrollHeight,clientHeight:transcript.clientHeight},
      inputStyle:{font:getComputedStyle(document.querySelector('textarea')).font,
        color:getComputedStyle(document.querySelector('textarea')).color}};
  });
  assert.ok(geometry.scroll.top>2500);
  assert.equal(mutations.length,0,'Capture must not open sessions or send messages.');
  assert.deepEqual(errors,[]);
  const png=await page.screenshot({path:resolve(base,'assets/studio-background.png')});
  const record={schema:'studio-staged-capture/1',capturedAt:new Date().toISOString(),
    origin,project:'Leonardo/hydraulic_sawmill',screenshot:'studio-background.png',
    sha256:createHash('sha256').update(png).digest('hex'),pixelRatio:3,...geometry,
    provenance:'Real Machinome Studio UI, existing sawmill export; browser-only staged session and fictional completion message. Model hidden after it loaded; composited as a moving View by movie.py.',
    message,mutations,errors};
  await writeFile(resolve(base,'assets/studio-capture.json'),JSON.stringify(record,null,2)+'\n');
  console.log(JSON.stringify({geometry,errors,mutations},null,2));
}finally{await browser.close();}
