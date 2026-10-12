// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Photograph the real Studio UI with browser-local session/chat fixtures.
// No session is opened on the broker and no conversation is submitted.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {spawn,execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const base=dirname(fileURLToPath(import.meta.url));
const [tool,viewer,origin='http://localhost:9000']=process.argv.slice(2);
assert.ok(tool&&viewer,'Pass the Videomaker checkout and viewer bundle.');
const {firefox}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const exec=promisify(execFile);
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
// A page screenshot excludes browser controls. Capture the whole native window
// instead, on an isolated display that never contains the user's desktop.
const xvfb=spawn('Xvfb',['-displayfd','3','-screen','0','3840x2160x24','-nolisten','tcp'],
  {stdio:['ignore','ignore','pipe','pipe']});
const display=':'+await new Promise((resolve,reject)=>{
  xvfb.stdio[3].once('data',value=>resolve(value.toString().trim()));
  xvfb.once('error',reject);
  xvfb.once('exit',code=>reject(new Error(`Capture display exited: ${code}`)));
});
let context;
await mkdir(resolve(base,'assets'),{recursive:true});
await mkdir(resolve(base,'_build/studio-capture'),{recursive:true});
try{
  context=await firefox.launchPersistentContext('',{
    headless:false,viewport:null,colorScheme:'dark',env:{...process.env,DISPLAY:display},
    firefoxUserPrefs:{'layout.css.devPixelsPerPx':'3.0','browser.urlbar.trimURLs':false,
      'ui.systemUsesDarkTheme':1},
  });
  const page=context.pages()[0];
  const {stdout:tree}=await exec('xwininfo',['-root','-tree'],{env:{...process.env,DISPLAY:display}});
  const windows=tree.split('\n').filter(line=>line.includes('("Navigator" "firefox'));
  assert.equal(windows.length,1,'Resize only the capture browser window.');
  const windowId=windows[0].trim().split(' ')[0];
  await exec('python3',[resolve(base,'resize-capture-window.py'),display,windowId,'3840','2160']);
  await page.waitForFunction(()=>outerWidth===1280&&outerHeight===720);
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
  await page.addStyleTag({content:'.conversation-transcript{scrollbar-width:thin;scrollbar-color:#5b626c #121419}'});
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
    // Keep the staged project visible but show the requested root URL. This
    // updates only this tab's address, not the real hub or application routing.
    history.replaceState(null,'','/');document.title='Machinome Studio';
    const offset={x:window.mozInnerScreenX-screenX,y:window.mozInnerScreenY-screenY};
    const box=selector=>{const r=document.querySelector(selector).getBoundingClientRect();
      return {x:r.x+offset.x,y:r.y+offset.y,width:r.width,height:r.height};};
    return {viewport:{width:outerWidth,height:outerHeight},model:box('.functional-model-host'),
      chat:box('.conversation'),input:box('textarea'),
      code:box('[data-workspace-area="code"]'),build:box('[data-workspace-area="build"]'),
      browserWindow:{browser:'Mozilla Firefox',address:location.href,
        content:{...offset,width:innerWidth,height:innerHeight},
        screen:{x:screenX,y:screenY},pixelRatio:devicePixelRatio},
      scroll:{top:transcript.scrollTop,height:transcript.scrollHeight,clientHeight:transcript.clientHeight},
      inputStyle:{font:getComputedStyle(document.querySelector('textarea')).font,
        color:getComputedStyle(document.querySelector('textarea')).color}};
  });
  assert.ok(geometry.scroll.top>2500);
  assert.equal(mutations.length,0,'Capture must not open sessions or send messages.');
  assert.deepEqual(errors,[]);
  assert.equal(geometry.browserWindow.address,'http://localhost:9000/');
  assert.deepEqual(geometry.browserWindow.screen,{x:0,y:0});
  assert.equal(geometry.browserWindow.pixelRatio,3);
  assert.ok(geometry.browserWindow.content.y>50);
  geometry.browserWindow.version=context.browser().version();
  // Clear the address-bar focus left by the empty startup tab without taking
  // any application action or placing a cursor in the staged message composer.
  await page.locator('.model-tabs').click();
  await page.mouse.move(geometry.viewport.width-20,geometry.browserWindow.content.height-10);
  // Flush content and browser chrome before the native X11 frame capture.
  await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  const screenshot=resolve(base,'assets/studio-background.png');
  await exec('ffmpeg',['-v','error','-f','x11grab','-draw_mouse','0','-video_size','3840x2160',
    '-i',display,'-frames:v','1','-y',screenshot]);
  const png=await readFile(screenshot);
  const record={schema:'studio-staged-capture/1',capturedAt:new Date().toISOString(),
    origin,project:'Leonardo/hydraulic_sawmill',screenshot:'studio-background.png',
    sha256:createHash('sha256').update(png).digest('hex'),pixelRatio:3,...geometry,
    provenance:'Real Mozilla Firefox window and Studio UI, existing sawmill export; browser-only staged session and fictional completion message. Model hidden after it loaded; composited as a moving View by movie.py. Tab-local history replacement displays the requested root URL without changing the project on the server.',
    message,mutations,errors};
  await writeFile(resolve(base,'assets/studio-capture.json'),JSON.stringify(record,null,2)+'\n');
  console.log(JSON.stringify({geometry,errors,mutations},null,2));
}finally{await context?.close();xvfb.kill('SIGTERM');}
