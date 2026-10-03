// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Inspect the actual project elements beyond the shipped stage's checks.
import assert from 'node:assert/strict';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2]&&process.argv[3],'Pass Videomaker and the viewer bundle.');
const tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const {loadEpisode}=await import(pathToFileURL(resolve(tool,'src/episode.mjs')));
const {browserSession}=await import(pathToFileURL(resolve(tool,'src/render.mjs')));
const {frameAt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const {hash}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const film=await loadEpisode(resolve(base,'_build/movie.json'));
const directory=resolve(base,'_build/inspection');
await mkdir(directory,{recursive:true});
const shots=film.chapters.flatMap(c=>c.shots);
// All main-take camera and mechanical endpoints meet, including the reveal.
const checkContinuity=()=>shots.slice(1,8).map(shot=>{
  const before=frameAt(film,shot.start-1e-6);
  const after=frameAt(film,shot.start);
  const a=Object.values(before.elements).find(e=>e.kind==='view');
  const b=Object.values(after.elements).find(e=>e.kind==='view');
  for(const key of ['camera','target'])for(let axis=0;axis<3;axis++)
    assert.ok(Math.abs(a.view[key][axis]-b.view[key][axis])<.01,`Camera jump into ${shot.id}`);
  assert.ok(Math.abs(a.time-b.time)<1e-6,`Model jump into ${shot.id}`);
  return shot.id;
});
const digest=hash(await readFile(resolve(base,'movie.py')));
const result=await browserSession(film,viewer,1280,[],async({page,pose})=>{
  const continuous=checkContinuity();
  const frames=[];
  for(const id of ['revolution','transmission','relationship-source','reveal','mirror','ecosystem','invitation']) {
    const shot=shots.find(s=>s.id===id);
    const t=shot.start+(shot.end-shot.start)*.72;
    const frame=await pose(t);
    const boxes=await page.evaluate(()=>[...document.querySelectorAll('.listing,.listing pre,.constellation-title,.tech-label,.tech-note,.wordmark,.question')].map(e=>{
      const r=e.getBoundingClientRect();
      return {text:e.textContent,box:{x:r.x,y:r.y,w:r.width,h:r.height},
        width:e.clientWidth,scrollWidth:e.scrollWidth,height:e.clientHeight,scrollHeight:e.scrollHeight,
        digest:e.dataset.sourceSha256};
    }));
    for(const element of boxes){
      const b=element.box;
      assert.ok(b.x>=-1&&b.y>=-1&&b.x+b.w<=1281&&b.y+b.h<=721,`${id}: text/graphic outside frame`);
      if(element.width)assert.ok(element.scrollWidth<=element.width+1,`${id}: source overflow`);
      if(element.digest)assert.equal(element.digest,digest,'Film source shown differs from actual movie.py');
    }
    const first=await page.screenshot();
    await pose(shots[0].end/2);
    await pose(t);
    const replay=await page.screenshot();
    assert.ok(first.equals(replay),`${id}: pixels do not replay`);
    await writeFile(resolve(directory,id+'.png'),first);
    frames.push({id,time:t,sha256:hash(first),boxes,shotId:frame.shotId});
  }
  return {continuousCameraBoundaries:continuous,filmSourceSha256:digest,frames};
});
await writeFile(resolve(directory,'report.json'),JSON.stringify(result,null,2)+'\n');
console.log(`Inspected ${result.frames.length} compositions and ${result.continuousCameraBoundaries.length} continuous-camera boundaries; source matches and pixels replay exactly.`);
