// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Production checks against the resolved film and the actual browser pixels.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {wheelAngle,driverX} from './ending-motion.mjs';
const base=dirname(fileURLToPath(import.meta.url));
const tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const {loadEpisode}=await import(pathToFileURL(resolve(tool,'src/episode.mjs')));
const {browserSession}=await import(pathToFileURL(resolve(tool,'src/render.mjs')));
const {frameAt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const {hash}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const film=await loadEpisode(resolve(base,'_build/movie.json'));
const shots=film.chapters.flatMap(c=>c.shots),fps=film.output.fps;
assert.equal(film.chapters.length,1);
assert.equal(film.chapters[0].speechOffset,3);
assert.ok(!JSON.stringify(film.chapters).includes('AI content'));
assert.ok(!JSON.stringify(film.stills).includes('museum'));
assert.ok(film.chapters[0].narration.includes('Machinome connects existing CAD technologies:'));
assert.ok(!film.chapters[0].narration.includes('Three.js'));
assert.ok(!film.chapters[0].narration.includes('OpenSpec'));
assert.ok(film.chapters[0].narration.includes('And beneath it all, a stream of open source tools...'));
assert.ok(film.chapters[0].narration.includes('What do YOU want to build next?'));
const elements=film.chapters[0].elements;
const ecosystem=elements.ecosystem.props;
assert.deepEqual(ecosystem.names,['OpenSCAD','SolidPython','CadQuery','Build123d','FreeCAD','JSCAD','OCCT','Trimesh']);
assert.deepEqual(ecosystem.drivers,['Three.js','NumPy','SciPy','Manifold','FastAPI','React','OpenSpec']);
const code=elements.tests.props;
for(const line of [25,604])assert.equal(code.code.split('\n')[code.numbers.indexOf(line)],'');
assert.equal(elements.signature.props.url,'https://github.com/machinome/machinome/');
const orbit=shots.find(s=>s.id==='ancestor');
const cameraCues=orbit.cues.filter(c=>c.actions.some(a=>a.action==='move'));
assert.equal(cameraCues.length,160);
let priorAngle=-Math.PI/2;
for(const cue of cameraCues){
  const action=cue.actions[0],camera=film.cameras[action.camera];
  assert.equal(action.ease,'linear');
  const angle=Math.atan2(camera.position[1],camera.position[0]);
  assert.ok(angle>=priorAngle,'Orbit reverses direction');priorAngle=angle;
}
const relation=shots.find(s=>s.id==='face-reveal');
const blinks=relation.cues.filter(c=>c.actions.some(a=>a.action==='blink'));
assert.deepEqual(blinks.map(c=>c.actions[0].params.token),['waterwheel','spin','drives','crankshaft']);
for(let n=0;n<Math.round(film.output.durationSeconds*fps);n++){
  const frame=frameAt(film,n/fps),views=Object.values(frame.elements).filter(e=>e.kind==='view');
  const lit=views.filter(v=>v.highlight);
  assert.ok(lit.length<=1,`Multiple highlighted views at frame ${n}`);
  if(lit.length)assert.equal(lit[0].highlight.paths.length,1);
  if(views.length===2){assert.deepEqual(views[0].view,views[1].view);assert.equal(views[0].time,views[1].time);}
  const tokens=Object.values(frame.elements).flatMap(e=>e.actions??[]).filter(a=>a.action==='blink');
  assert.ok(tokens.length<=1,`Accumulated source highlights at frame ${n}`);
}
assert.equal(frameAt(film,.5).elements['continuous.wheel'].time,frameAt(film,.9).elements['continuous.wheel'].time);
const directory=resolve(base,'_build/inspection');await mkdir(directory,{recursive:true});
const cases=[];
for(const shot of shots)cases.push({id:shot.id,time:shot.start+(shot.end-shot.start)*.6});
for(let i=0;i<=10;i++)cases.push({id:`orbit-${i}`,time:orbit.start+cameraCues[0].at+(orbit.end-orbit.start-cameraCues[0].at)*i/10-1/fps});
for(const [i,cue]of blinks.entries()){
  cases.push({id:`blink-${i+1}`,time:relation.start+(cue.at+cue.until)/2,token:cue.actions[0].params.token});
  const next=blinks[i+1]?.at??cue.until+.3;
  if(next-cue.until>1/fps)cases.push({id:`after-blink-${i+1}`,time:relation.start+(cue.until+next)/2,token:null});
}
const testing=shots.find(s=>s.id==='testing');
for(const [i,cue]of testing.cues.entries())if(cue.actions.some(a=>a.action==='blink'))
  cases.push({id:`test-blink-${i}`,time:testing.start+(cue.at+cue.until)/2,
    token:cue.actions.find(a=>a.action==='blink').params.token});
const open=shots.find(s=>s.id==='open-source'),drive=open.cues.find(c=>c.actions.some(a=>a.action==='drive'));
cases.push({id:'cad-complete',time:open.start+drive.at-1/fps});
cases.push({id:'invitation-question',time:film.output.durationSeconds-1.4});
for(const d of [.15,.75,ecosystem.arrival,ecosystem.arrival+.5])cases.push({id:`stream-${d}`,time:open.start+drive.at+d,contact:d===ecosystem.arrival});
// Inspect every supporting name at wheel contact, not just the first name.
for(const [i,name] of ecosystem.drivers.entries()){
  const b=ecosystem.entrySpeedFraction,a=1-b,target=1+i*ecosystem.spacing/870;
  const d=ecosystem.arrival*(-b+Math.sqrt(b*b+4*a*target))/(2*a);
  cases.push({id:`contact-${name}`,time:open.start+drive.at+d,contactName:name});
}
const returned=shots.find(s=>s.id==='wheel-returns');
// Every encoded frame uses the same accelerating phase on both wheels.
const driveStart=open.start+drive.at,fade=elements['handoff-ecosystem'].props.fadeDuration;
let previousAngle,previousVelocity;
for(let n=Math.ceil(returned.start*fps);n/fps<returned.start+fade;n++){
  const t=n/fps,frame=frameAt(film,t),graphic=frame.elements['continuous.handoff-ecosystem'];
  const angle=wheelAngle(t-driveStart,ecosystem);
  const physical=(frame.elements['continuous.returned'].time*film.model.expectedDurationSeconds-500)*90;
  assert.ok(Math.abs(angle-physical)<1e-7,`Wheel phase mismatch at frame ${n}: ${angle-physical}`);
  if(previousAngle!==undefined){
    const velocity=angle-previousAngle;
    if(previousVelocity!==undefined)assert.ok(velocity>previousVelocity,'Wheel must keep accelerating');
    previousVelocity=velocity;
  }
  assert.ok(graphic);
  previousAngle=angle;
}
for(const d of [0,.25,.625,1,1.25,1.5])cases.push({id:`handoff-${d}`,time:returned.start+d});
const results=await browserSession(film,viewer,1280,[],async({page,pose})=>{
  const samples=[];
  for(const item of cases.filter(item=>!process.argv[4]||(process.argv[4]==='ending'
    ? /^(open-source|cad-complete|stream-|contact-|handoff-|wheel-returns|invitation)/.test(item.id)
    : item.id.includes(process.argv[4])))){
    const t=Math.min(film.output.durationSeconds-1/fps,Math.round(item.time*fps)/fps);
    const posed=await pose(t);
    const report=await page.evaluate(()=>({
      blinks:[...document.querySelectorAll('.blink-token')].map(e=>e.textContent),
      texts:[...document.querySelectorAll('.listing,.listing pre,.wordmark,.tagline,.repository-url,.question')].map(e=>{
        const r=e.getBoundingClientRect();return {text:e.textContent,x:r.x,y:r.y,w:r.width,h:r.height,
          width:e.clientWidth,scroll:e.scrollWidth,digest:e.dataset.sourceSha256};
      }),
      incoming:[...document.querySelectorAll('.incoming')].map(e=>{
        const b=e.getBBox();
        const dx=Math.max(b.x-960,0,960-b.x-b.width);
        const dy=Math.max(b.y-540,0,540-b.y-b.height);
        return {text:e.textContent,x:e.getAttribute('x'),y:e.getAttribute('y'),
          aboveWater:b.y+b.height<835,hitsWheel:dx*dx+dy*dy<=275*275};
      }),
    }));
    if('token'in item)assert.deepEqual(report.blinks,item.token?[item.token]:[],item.id);
    for(const b of report.texts){
      assert.ok(b.x>=-1&&b.y>=-1&&b.x+b.w<=1281&&b.y+b.h<=721,`${item.id}: text outside frame`);
      if(b.width)assert.ok(b.scroll<=b.width+1,`${item.id}: source overflow`);
    }
    for(const b of report.incoming){
      assert.equal(b.y,'820');assert.equal(b.aboveWater,true,'Supporting tools must travel above the blue line');
      if((item.contact&&b.text===ecosystem.drivers[0])||b.text===item.contactName)
        assert.equal(b.hitsWheel,true,`${b.text} must contact the wheel`);
    }
    const first=await page.screenshot();await pose(.8);await pose(t);
    assert.ok(first.equals(await page.screenshot()),`${item.id}: replay differs`);
    await writeFile(resolve(directory,item.id+'.png'),first);
    samples.push({...item,time:t,sha256:hash(first),report,
      motion:Object.fromEntries(Object.entries(posed.observed.elements).filter(([,e])=>e.rotation!==undefined))});
  }
  return {samples};
});
await writeFile(resolve(directory,process.argv[4]==='ending'?'ending-report.json':process.argv[4]?'partial-report.json':'report.json'),JSON.stringify({status:'passed; visual inspection separate',...results},null,2)+'\n');
console.log(`${results.samples.length} replay-identical samples; phase-locked accelerating handoff; seven-name stream; literal source spacing; enlarged closing tagline and URL.`);
