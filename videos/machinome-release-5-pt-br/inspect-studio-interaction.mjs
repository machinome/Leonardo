// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Scrubbing is an edit over the real model, with a deterministic UI clock.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {smooth} from './studio-motion.mjs';
const base=dirname(fileURLToPath(import.meta.url)),tool=resolve(process.argv[2]);
const origin=process.argv[3]??'http://127.0.0.1:8787';
const read=name=>readFile(resolve(base,name),'utf8').then(JSON.parse);
const doc=await read('_build/movie-resolved.json'),edit=await read('_build/studio-edit.json');
const chapter=doc.chapters[0],studio=chapter.shots.find(s=>s.id==='studio');
const testing=chapter.shots.find(s=>s.id==='testing'),fps=doc.output.fps;
const sameView=(actual,expected,message)=>{
  for(const key of ['camera','target'])for(let i=0;i<3;i++)
    assert.ok(Math.abs(actual[key][i]-expected[key][i])<1e-8,message);
};
const narration=await read('_build/narration-manifest.json');
assert.ok(narration.text.includes('interage com o modelo para ver diferentes ângulos e momentos da animação'));
assert.ok(narration.text.includes('Você também pode criar modelos pelo navegador, usando o Machinome Studio'));
assert.ok(narration.text.endsWith('O que VOCÊ quer construir?'));
assert.ok(edit.cameraEnd<=edit.sliderHighlight&&edit.sliderHighlight<edit.rewindStart);
assert.ok(Math.abs(edit.departureEnd-edit.testingStart-2.75)<1e-8,
  'Model completes its eased travel in 2.75 seconds');
assert.ok(Math.abs(edit.departureEnd-edit.typingStart-.5)<1e-8,
  'Typing starts during the final half-second of model travel');
assert.equal(testing.transition,undefined,'No cross-fade into testing');
const output=resolve(base,'_build/inspection/studio-interaction');await mkdir(output,{recursive:true});
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const browser=await chromium.launch({headless:true}),checks=[],errors=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'/#movie');await page.waitForFunction(()=>window.player?.generation()>0);
  const frameAt=async time=>{
    const frame=await (await fetch(`${origin}/frame?t=${time}`)).json();return frame;
  };
  const sample=async(name,time)=>{
    await page.evaluate(async t=>{window.player.seek(t);await window.player.idle();},time);
    assert.equal(await page.locator('#fault').textContent(),'');
    const frame=await frameAt(time);
    const dom=await page.evaluate(()=>{
      const w=document.querySelector('iframe').contentWindow,d=w.document;
      const rect=el=>{if(!el)return null;const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
      const model=d.querySelector('.studio-model'),timeline=d.querySelector('.studio-timeline');
      return {focus:d.querySelector('.studio-focus')?.dataset.focus??null,
        pointer:!!d.querySelector('.studio-pointer,[data-pointer]'),
        seconds:timeline?Number(timeline.dataset.seconds):null,
        box:rect(model),canvas:rect(model?.querySelector('canvas')),code:rect(d.querySelector('.slot-code')),
        listing:!!d.querySelector('.slot-code .listing'),sourceText:d.querySelector('.slot-code .listing pre')?.textContent??'',
        imageOpacity:Number(w.getComputedStyle(d.querySelector('.studio-photograph')).opacity),
        detailOpacity:d.querySelector('.studio-detail')?Number(w.getComputedStyle(d.querySelector('.studio-detail')).opacity):null,
        fullOpacity:Number(w.getComputedStyle(model).opacity),width:w.innerWidth,height:w.innerHeight};
    });
    assert.equal(dom.pointer,false,'No staged mouse pointer');
    for(const k of ['x','y','width','height'])assert.ok(Math.abs(dom.box[k]-dom.canvas[k])<1,'Live canvas follows its slot');
    if(dom.seconds!==null)assert.ok(Math.abs(dom.seconds-frame.elements['continuous.mill'].time*doc.model.expectedDurationSeconds)<1e-7,
      'Slider readout and the real model use exactly the same clock');
    const pixels=await page.locator('iframe').screenshot({path:resolve(output,`${name}.png`)});
    checks.push({name,time,dom});return {frame,dom,pixels};
  };
  const modelFocus=studio.cues.find(c=>c.actions.some(a=>a.action==='focus'&&a.params.area==='model'));
  assert.equal((await sample('model-highlight',studio.start+modelFocus.at)).dom.focus,'model');
  let previousAngle=null,total=0;
  for(let frameNo=Math.round(edit.cameraStart*fps);frameNo<=Math.round(edit.cameraEnd*fps);frameNo++){
    const frame=await frameAt(frameNo/fps),v=frame.elements['continuous.mill'].view;
    const angle=Math.atan2(v.camera[1]-v.target[1],v.camera[0]-v.target[0]);
    if(previousAngle!==null){const delta=Math.atan2(Math.sin(angle-previousAngle),Math.cos(angle-previousAngle));
      assert.ok(delta<=1e-9,'The short turn has no direction reversals');total+=Math.abs(delta);}
    previousAngle=angle;
  }
  assert.ok(total>1&&total<Math.PI,'Camera takes less than half a revolution, never the long orbit');
  await sample('angle-middle',(edit.cameraStart+edit.cameraEnd)/2);
  const angleEnd=await sample('angle-end',edit.cameraEnd);
  sameView(angleEnd.frame.elements['continuous.mill'].view,{camera:doc.cameras.test.position,target:doc.cameras.test.target},
    'The short turn reaches the testing camera (within arithmetic roundoff)');
  assert.equal((await sample('timeline-highlight',edit.sliderHighlight)).dom.focus,'timeline');
  let previous=Infinity;
  for(let n=Math.round(edit.rewindStart*fps);n<=Math.round(edit.testingStart*fps);n++){
    const t=n/fps,frame=await frameAt(t),v=frame.elements['continuous.mill'];
    const seconds=v.time*doc.model.expectedDurationSeconds;
    assert.ok(seconds<=previous+1e-7,'The scrub only moves backwards');previous=seconds;
    assert.ok(Math.abs(seconds-edit.rewindFrom*(1-smooth((t-edit.rewindStart)/(edit.rewindEnd-edit.rewindStart))))<1e-6);
    sameView(v.view,angleEnd.frame.elements['continuous.mill'].view,'Camera holds during scrubbing');
  }
  const middle=(edit.rewindStart+edit.rewindEnd)/2;
  for(const [name,t] of [['rewind-start',edit.rewindStart],['rewind-middle',middle],['rewind-end',edit.rewindEnd],
      ['before-testing',testing.start-1/fps],['testing-start',testing.start],
      ['testing-fade-middle',testing.start+.3],['testing-clear-travel',testing.start+.75],
      ...[.1,.25,.75,.9].map(p=>[`testing-ease-${p}`,testing.start+p*(edit.departureEnd-testing.start)]),
      ['testing-middle',(testing.start+edit.departureEnd)/2],['testing-landed',edit.departureEnd]])
    await sample(name,t);
  const before=checks.find(c=>c.name==='before-testing'),first=checks.find(c=>c.name==='testing-start');
  assert.deepEqual(before.dom.box,first.dom.box,'No model layout jump at the testing cut');
  const last=checks.at(-1).dom;
  assert.ok(last.code.x+last.code.width<=last.box.x+1,'Code left, model right');
  assert.ok(Math.abs(last.box.x-last.width*.64)<1,'Model lands at the original right-hand position');
  assert.ok(Math.abs(last.box.y-last.height*.17)<1,'Testing model has a 17% top margin');
  assert.ok(Math.abs(last.box.height-last.height*.83)<1,'Extra top margin does not shrink the model');
  assert.ok(last.box.y+last.box.height<=last.height+1,'Model canvas stays inside the frame');
  for(const c of checks.filter(c=>c.name.startsWith('testing-ease-'))){
    const p=(Math.round(c.time*fps)/fps-testing.start)/(edit.departureEnd-testing.start);
    const eased=10*p**3-15*p**4+6*p**5;
    for(const k of ['x','y','width','height']){
      const expected=first.dom.box[k]+(last.box[k]-first.dom.box[k])*eased;
      assert.ok(Math.abs(c.dom.box[k]-expected)<1,'Model travel has a gentler quintic ease-in/out');
    }
  }
  const mid=checks.find(c=>c.name==='testing-middle').dom;
  assert.ok(first.dom.box.x<mid.box.x&&mid.box.x<last.box.x,'The model travels continuously to the right');
  const fadeMiddle=checks.find(c=>c.name==='testing-fade-middle').dom;
  assert.ok(Math.abs(fadeMiddle.imageOpacity-.5)<.05,'Studio fades halfway in 0.3 seconds');
  const clear=checks.find(c=>c.name==='testing-clear-travel').dom;
  assert.equal(clear.imageOpacity,0,'Studio is gone early in the model travel');
  assert.equal(clear.fullOpacity,0,'Full-machine context clears with Studio');
  assert.equal(clear.detailOpacity,1,'The travelling timber/blade view stays fully visible');
  assert.ok(first.dom.box.x<clear.box.x&&clear.box.x<mid.box.x,'The clear model still has most of its travel ahead');
  assert.equal(clear.listing,false,'Code still waits until the model is nearly at right');
  assert.equal(last.imageOpacity,0);assert.equal(last.fullOpacity,0);
  for(const c of checks.filter(c=>['testing-start','testing-middle'].includes(c.name)))
    assert.equal(c.dom.listing,false,'No code or filename over the departing Studio');
  const blank=await sample('blank-left',edit.typingStart-1/fps);
  assert.equal(blank.dom.listing,false);assert.equal(blank.dom.imageOpacity,0);
  assert.ok(blank.dom.box.x<last.box.x,'The blank left side holds until near the end of travel');
  const typed=await sample('typing-started',edit.typingStart+2/fps);
  assert.ok(typed.dom.listing&&typed.dom.sourceText.length>0);
  assert.equal(typed.dom.imageOpacity,0);
  assert.ok(typed.dom.box.x>blank.dom.box.x&&typed.dom.box.x<last.box.x,
    'Model is still finishing its travel while code starts typing');
  assert.ok((typed.dom.box.x-first.dom.box.x)/(last.box.x-first.dom.box.x)>.97,
    'More than 97% of the faster layout travel is complete as typing becomes visible');
  assert.ok(last.listing&&last.sourceText.length>typed.dom.sourceText.length,
    'Typing continues through the model landing');
  const completed=await sample('typing-complete',edit.typingEnd);
  assert.ok(completed.dom.sourceText.includes('assertNotIntersecting'));
  // Every film frame before typing must carry the conceal action, not merely
  // an empty string: the filename is part of the panel too.
  for(let n=Math.round(testing.start*fps);n<Math.round(edit.typingStart*fps);n++){
    const frame=await frameAt(n/fps);
    assert.ok(frame.elements['continuous.tests'].actions.some(a=>a.action==='conceal'));
  }
  const a=await sample('replay-a',middle);
  await sample('replay-away',edit.departureEnd);
  const b=await sample('replay-b',middle);
  assert.ok(a.pixels.equals(b.pixels),'Scrub frame replays with identical pixels');
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({status:'passed',shortTurnDegrees:total*180/Math.PI,
    edit,checks,errors},null,2)+'\n');
  console.log(`${checks.length} interaction frames checked; short turn, exact rewind, fast fade, eased/lowered model at right, typing during final travel, and pixel replay pass.`);
}finally{await browser.close();}
