// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const {loadEpisode}=await import(pathToFileURL(resolve(tool,'src/episode.mjs')));
const {browserSession}=await import(pathToFileURL(resolve(tool,'src/render.mjs')));
const {frameAt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const {hash}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const film=await loadEpisode(resolve(base,'_build/movie.json'));
const shots=film.chapters.flatMap(c=>c.shots);
assert.equal(film.chapters.length,1);
assert.equal(film.chapters[0].speechOffset,3);
for(let t=0;t<film.output.durationSeconds;t+=1/24){
  const frame=frameAt(film,t), views=Object.values(frame.elements).filter(e=>e.kind==='view');
  const lit=views.filter(v=>v.highlight);
  assert.ok(lit.length<=1,`Multiple highlighted views at ${t}`);
  if(lit.length)assert.equal(lit[0].highlight.paths.length,1,`Multiple highlighted components at ${t}`);
  if(views.length===2){assert.deepEqual(views[0].view,views[1].view,`Mismatched context camera at ${t}`);assert.equal(views[0].time,views[1].time);}
}
assert.equal(frameAt(film,.5).elements['continuous.wheel'].time,frameAt(film,.9).elements['continuous.wheel'].time);
const digest=hash(await readFile(resolve(base,'movie.py')));
const directory=resolve(base,'_build/inspection');
await mkdir(directory,{recursive:true});
const result=await browserSession(film,viewer,1280,[],async({page,pose})=>{
  const frames=[];
  const extra={'openspec-arrival':125.5,'open-wheel-spinning':127.4};
  const cases=['revolution','water','crank','feed-motion','transmission','document','photograph','python-language','face-reveal','behind-the-film','mirror','open-source','openspec-arrival','open-wheel-spinning','wheel-returns','invitation'].map(id=>{
    const shot=shots.find(s=>s.id===(id in extra?'open-source':id));
    return {id,shot,time:extra[id]??shot.start+(shot.end-shot.start)*.72};
  });
  const sourceShot=shots.find(s=>s.id==='behind-the-film');
  for(const [i,cue] of sourceShot.cues.entries())cases.push({
    id:`source-focus-${i+1}`,shot:sourceShot,
    time:sourceShot.start+(cue.at+cue.until)/2,
    token:cue.actions[0].params.token,
  });
  for(const {id,shot,time:t,token} of cases){
    await pose(t);
    const boxes=await page.evaluate(()=>[...document.querySelectorAll('.listing,.listing pre,.tech-label,.incoming,.wordmark,.question')].map(e=>{
      const r=e.getBoundingClientRect();return {text:e.textContent,box:{x:r.x,y:r.y,w:r.width,h:r.height},width:e instanceof HTMLElement?e.clientWidth:0,scrollWidth:e.scrollWidth,digest:e.dataset.sourceSha256};
    }));
    for(const e of boxes){const b=e.box;assert.ok(b.x>=-1&&b.y>=-1&&b.x+b.w<=1281&&b.y+b.h<=721,`${id}: content outside frame`);if(e.width)assert.ok(e.scrollWidth<=e.width+1,`${id}: overflow`);if(e.digest)assert.equal(e.digest,digest);}
    if(['behind-the-film','mirror'].includes(shot.id)){
      const listing=await page.evaluate(()=>({
        text:document.querySelector('.listing pre').textContent,
        focus:[...document.querySelectorAll('.listing .lit-line')].map(e=>e.textContent),
      }));
      assert.ok(listing.text.includes(shot.id==='mirror'?'class ThisScene:':'class CrankStroke:'));
      assert.equal(listing.focus.length,1,`${id}: one expressive line at a time`);
      if(shot.id==='mirror')assert.ok(listing.focus[0].includes("And here's the code of this exact scene! How cool is that?"));
      if(token)assert.ok(listing.focus[0].includes(token),`${id}: wrong line highlighted`);
    }
    const first=await page.screenshot();
    await pose(.8);await pose(t);
    assert.ok(first.equals(await page.screenshot()),`${id}: replay differs`);
    await writeFile(resolve(directory,id+'.png'),first);
    frames.push({id,time:t,sha256:hash(first),boxes});
  }
  return {frames,filmSourceSha256:digest};
});
await writeFile(resolve(directory,'report.json'),JSON.stringify(result,null,2)+'\n');
console.log('One take; one highlight; exact paired cameras; still opening; complete scene classes; 21 replay-identical compositions.');
