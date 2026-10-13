// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Real-browser evidence for the Studio reveal and its narration boundary.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url)),tool=resolve(process.argv[2]);
const origin=process.argv[3]??'http://127.0.0.1:8787';
const doc=JSON.parse(await readFile(resolve(base,'_build/movie-resolved.json')));
const chapter=doc.chapters[0],shot=id=>chapter.shots.find(s=>s.id===id);
const meta=JSON.parse(await readFile(resolve(base,'_build/narration-manifest.json')));
assert.ok(meta.text.includes('uma corrente de tecnologias de código aberto'));
assert.ok(meta.text.includes('O Machinome também oferece uma estrutura de testes, que permite verificar como as peças se encaixam.'));
assert.ok(meta.text.endsWith('O que VOCÊ quer construir?'));
assert.ok(!meta.text.includes('Agents can write mechanical models because of tests'));
assert.deepEqual(meta.audioEdits,[]);
assert.ok((await readFile(meta.cacheFile)).equals(await readFile(resolve(base,'_build/provider-original.wav'))),
  'No audio splicing: the take is byte-identical to the provider WAV');
const capture=JSON.parse(await readFile(resolve(base,'assets/studio-capture.json')));
assert.equal(capture.browserWindow?.browser,'Mozilla Firefox');
assert.equal(capture.browserWindow.address,'http://localhost:9000/');
assert.ok(capture.browserWindow.content.y>50,'The actual tab and address bars are visible');
assert.ok(capture.model.y>capture.browserWindow.content.y,'The live model sits below the browser controls');
assert.equal(createHash('sha256').update(await readFile(resolve(base,'assets/studio-background.png'))).digest('hex'),capture.sha256);
assert.deepEqual(capture.mutations,[]);assert.ok(capture.scroll.top>2500);
const face=shot('face-reveal'),studio=shot('studio'),testing=shot('testing');
const rewinds=chapter.shots.filter(s=>s.id.startsWith('studio-rewind-'));
assert.equal(face.end,studio.start);assert.equal(studio.end,rewinds[0].start);
assert.equal(rewinds.at(-1).end,testing.start);
const reveal=face.cues.find(c=>c.actions.some(a=>a.action==='reveal'));
const output=resolve(base,'_build/inspection/studio');await mkdir(output,{recursive:true});
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const browser=await chromium.launch({headless:true}),checks=[],errors=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'/#movie');await page.waitForFunction(()=>window.player?.generation()>0);
  const sample=async(name,time)=>{
    await page.evaluate(async time=>{window.player.seek(time);await window.player.idle();},time);
    assert.equal(await page.locator('#fault').textContent(),'');
    const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();
    const dom=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow,d=w.document;
      const rect=el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
      const picture=d.querySelector('.studio-photograph'),model=d.querySelector('.studio-model');
      const canvas=model?.querySelector('canvas');
      return {picture:picture?{...rect(picture),opacity:Number(w.getComputedStyle(picture).opacity),loaded:picture.querySelector('img').complete}:null,
        model:model?rect(model):null,canvas:canvas?rect(canvas):null,
        focus:d.querySelector('.studio-focus')?.dataset.focus??null,prompt:d.querySelector('.studio-prompt')?.textContent??'',
        focusBox:d.querySelector('.studio-focus')?rect(d.querySelector('.studio-focus')):null,
        promptBox:d.querySelector('.studio-prompt')?rect(d.querySelector('.studio-prompt')):null,
        viewport:{width:w.innerWidth,height:w.innerHeight}};
    });
    await page.locator('iframe').screenshot({path:resolve(output,`${name}.png`)});
    checks.push({name,time,dom});return {frame,dom};
  };
  let previousTime=-Infinity,previousX=Infinity;
  const times=[['before',face.start+reveal.at-1/doc.output.fps],
    ['fade-start',face.start+reveal.at],['fade-middle',face.start+(reveal.at+reveal.until)/2],
    ['arrive-start',studio.start],['arrive-quarter',studio.start+.7],
    ['arrive-middle',studio.start+1.4],['arrive-late',studio.start+2.1],['full-screen',studio.start+2.8]];
  for(const [name,time] of times){
    const {frame,dom}=await sample(name,time),view=frame.elements['continuous.mill'];
    assert.deepEqual(view.view,{camera:[1200,-1540,960],target:[0,-20,205]},'No camera change through the reveal');
    assert.equal(view.fov,37);assert.deepEqual(view.up,[0,0,1],'The lens remains unchanged');
    assert.ok(view.time>previousTime,'The same model keeps moving');previousTime=view.time;
    assert.ok(dom.model&&dom.canvas&&dom.picture.loaded);
    for(const key of ['x','y','width','height'])assert.ok(Math.abs(dom.canvas[key]-dom.model[key])<1,'Canvas fills the moving slot');
    if(time<studio.start){
      assert.ok(Math.abs(dom.model.x-dom.viewport.width*.6)<1);
      assert.ok(Math.abs(dom.model.height-dom.viewport.height*.9)<1);
    }else{
      assert.ok(dom.model.x<previousX);previousX=dom.model.x;
      assert.equal(dom.picture.opacity,1,'Background does not blink during the move');
    }
    if(name==='fade-middle')assert.ok(Math.abs(dom.picture.opacity-.5)<.05);
    if(name==='full-screen'){
      assert.ok(Math.abs(dom.picture.x)<1&&Math.abs(dom.picture.y)<1);
      assert.ok(Math.abs(dom.picture.width-dom.viewport.width)<1);
      for(const key of ['x','y','width','height']){
        const axis=['x','width'].includes(key)?'width':'height';
        assert.ok(Math.abs(dom.model[key]-dom.viewport[axis]*capture.model[key]/capture.viewport[axis])<1,
          'The model fits the photographed viewport below the Firefox bars');
      }
    }
  }
  for(const area of ['chat','code','build']){
    const cue=studio.cues.find(c=>c.actions.some(a=>a.action==='focus'&&a.params.area===area));
    const {dom}=await sample(area,studio.start+(cue.at+cue.until)/2);
    assert.equal(dom.focus,area);
    for(const [box,target] of [[dom.focusBox,capture[area]],[dom.promptBox,capture.input]]){
      for(const key of ['x','y','width','height']){
        const axis=['x','width'].includes(key)?'width':'height';
        assert.ok(Math.abs(box[key]-dom.viewport[axis]*target[key]/capture.viewport[axis])<1,
          'Highlights and typing include the native browser-controls offset');
      }
    }
    if(area==='chat')assert.ok(dom.prompt.length>0&&dom.prompt.length<"Há mais um ajuste:".length);
    else assert.equal(dom.prompt,"Há mais um ajuste:");
  }
  const {dom}=await sample('before-testing',testing.start-1/doc.output.fps);
  assert.equal(dom.prompt,"Há mais um ajuste:");
  await sample('testing',testing.start+2);
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({status:'passed',checks,errors},null,2)+'\n');
  console.log(`${checks.length} Studio frames checked; continuous audio intact; no video rendered.`);
}finally{await browser.close();}
