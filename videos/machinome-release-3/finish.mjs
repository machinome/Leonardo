// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Compile measured edit decisions into the documented movie format.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2],'Pass Videomaker checkout.');
const tool=resolve(process.argv[2]);
const {readMovie,resolveMovie}=await import(pathToFileURL(resolve(tool,'src/movie.mjs')));
const {cachedTake}=await import(pathToFileURL(resolve(tool,'src/speech.mjs')));
const file=resolve(base,'_build/movie.json');
const {doc,build}=await readMovie(file);
const approved=JSON.parse(await readFile(resolve(base,'_build/narration-manifest.json')));
// The tool's request key uses JSON property order; restore the approved order
// after Python's sorted JSON serialization. No request or audio bytes change.
doc.audio=approved.voice;
const take=await cachedTake({audio:doc.audio,chapters:doc.chapters,paths:{build}},0);
assert.ok(take,'Continuous take is missing. This command does not generate speech.');
assert.equal(take.sha256,approved.sha256,'The film must reuse the recorded audio bytes.');
assert.equal(doc.chapters.length,1);
assert.equal(doc.chapters[0].narration,approved.text);
const measured=resolveMovie(doc,{continuous:take});
const chapter=doc.chapters[0];
const feedTimed=measured.chapters[0].shots.find(s=>s.id==='feed-motion');
const rate=32/(feedTimed.start-3+2/3);
const clock=t=>t<=feedTimed.start?400+rate*2/3+Math.max(0,t-3)*rate:
  440+(t-feedTimed.end)*.65;
for(const [i,shot] of chapter.shots.entries()){
  const timed=measured.chapters[0].shots[i];
  shot.model=i?{from:clock(timed.start),to:clock(timed.end)}:{keys:[
    {at:0,seconds:400},{at:1,seconds:400},
    {at:3,seconds:clock(3),ease:'in'},
    {at:shot.until,seconds:clock(timed.end)},
  ]};
}
chapter.shots.find(s=>s.id==='feed-motion').model={keys:[
  {at:0,seconds:432},
  {at:{spoken:'On the cutting stroke'},seconds:436},
  {at:{spoken:'A second pawl'},seconds:438},
  {at:{spoken:'That small step'},seconds:440},
]};
// A single analytic orbit, sampled densely with linear microsegments. Only
// the whole move eases; there are no corner stops or independently eased legs.
const ancestor=chapter.shots.find(s=>s.id==='ancestor');
const orbit=ancestor.cues.find(c=>c.actions.some(a=>a.action==='move'));
const timedAncestor=measured.chapters[0].shots.find(s=>s.id==='ancestor');
const timedOrbit=timedAncestor.cues.find(c=>c.actions.some(a=>a.action==='move'));
const start=timedOrbit.at, end=timedOrbit.actions[0].until;
ancestor.cues=ancestor.cues.filter(c=>c!==orbit);
for(let i=1;i<=160;i++){
  const u=i/160, p=u*u*u*(10+u*(-15+6*u));
  const theta=-Math.PI/2+3*Math.PI/4*p;
  const radius=575+(Math.hypot(850,850)-575)*p+550*Math.sin(Math.PI*p);
  const name=`orbit-${String(i).padStart(3,'0')}`;
  doc.cameras[name]={position:[radius*Math.cos(theta),radius*Math.sin(theta),120+590*p+160*Math.sin(Math.PI*p)],
    target:[0,-151*(1-p),120+165*p],up:[0,0,1],fov:37};
  if(i===160)doc.cameras[name]=structuredClone(doc.cameras.rear);
  ancestor.cues.push({at:start+(end-start)*(i-1)/160,
    actions:[{element:'mill',action:'move',camera:name,ease:'linear',until:start+(end-start)*u}]});
}
// Illustrate the actual test's 13 instants over its first four model seconds.
// Hold each sample, with one frame of travel to the next; not a continuous
// collision proof or an invented simulation of test execution.
const testing=chapter.shots.find(s=>s.id==='testing');
const timedTesting=measured.chapters[0].shots.find(s=>s.id==='testing');
const stepsCue=timedTesting.cues.find(c=>c.actions.some(a=>a.params?.token==='testing_steps'));
const sampleStart=stepsCue.at, sampleEnd=timedTesting.end-timedTesting.start-1;
const samplePeriod=(sampleEnd-sampleStart)/13;
const keys=[{at:0,seconds:0},{at:sampleStart,seconds:0}];
for(let i=1;i<13;i++){
  const t=sampleStart+i*samplePeriod;
  keys.push({at:t-1/24,seconds:(i-1)/3},{at:t,seconds:i/3});
}
keys.push({at:testing.until,seconds:4});
testing.model={keys};
// The demonstration source really drives this shot. Its faint context plate
// follows that same camera, using the same export, not a second simulation.
const crank=chapter.shots.find(s=>s.id==='crank');
crank.places.ghost='ghost';
for(const cue of crank.cues){
  for(const action of [...cue.actions])if(action.action==='move')
    cue.actions.push({...action,element:'ghost'});
}
// The ordinary full view returns from the same lens as the preceding lesson.
const two=chapter.shots.find(s=>s.id==='two-jobs');
chapter.elements.returnedMill={...chapter.elements.mill,camera:'carriage'};
// IDs in the format are slugs.
chapter.elements['returned-mill']=chapter.elements.returnedMill;
delete chapter.elements.returnedMill;
two.places.stage='returned-mill';
for(const cue of two.cues)for(const action of cue.actions)action.element='returned-mill';
await writeFile(file,JSON.stringify(doc,null,2)+'\n');
const {captionsFromAlignment,srt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
await writeFile(resolve(base,'_build/raw-narration.wav'),await readFile(take.file));
const rawCaptions=captionsFromAlignment(take.alignment);
await writeFile(resolve(base,'_build/raw-captions.json'),JSON.stringify(rawCaptions,null,2)+'\n');
await writeFile(resolve(base,'_build/raw-captions.srt'),srt(rawCaptions));
console.log('One Jessica take; 3-second silent start; continuous orbit; word blinks; 13 test poses.');
