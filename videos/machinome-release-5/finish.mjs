// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Compile measured edit decisions into the documented movie format.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {wheelAngle} from './ending-motion.mjs';
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
// The provider collapsed crankshaft to 10 ms and delayed drives. Correct
// only these visual spans from local forced alignment of the same recording;
// neither the cached alignment nor audio nor scene boundaries are rewritten.
const relationTiming=JSON.parse(await readFile(resolve(base,'relation-timing.json')));
assert.equal(relationTiming.schema,'cut5-relation-timing/1');
assert.equal(take.sha256,relationTiming.audioSha256,'Realign the relation cues if the take changes.');
const relationText=take.alignment.characters.join('');
const relation=doc.chapters[0].shots.find(s=>s.id==='face-reveal');
for(const [token,timing] of Object.entries(relationTiming.words)){
  const index=relationText.indexOf(token);
  assert.ok(index>=0&&relationText.indexOf(token,index+1)<0,`Ambiguous relation word: ${token}`);
  const first=Array.from(relationText.slice(0,index)).length,last=first+Array.from(token).length-1;
  const cue=relation.cues.find(c=>c.actions.some(a=>a.action==='blink'&&a.params.token===token));
  assert.ok(cue,`Missing relation blink: ${token}`);
  if(timing.start!==undefined)cue.at={spoken:token,
    plus:timing.start-take.alignment.character_start_times_seconds[first]};
  if(timing.end!==undefined)cue.until={spokenEnd:token,
    plus:timing.end-take.alignment.character_end_times_seconds[last]};
}
const measured=resolveMovie(doc,{continuous:take});
const chapter=doc.chapters[0];
// The explanatory tokens flash for their own recorded word, not the rest
// of the locating phrase. The longer phrase only disambiguates the anchor.
const alignedText=take.alignment.characters.join('');
for(const id of ['behind-the-film','mirror']){
  const shot=chapter.shots.find(s=>s.id===id);
  const timed=measured.chapters[0].shots.find(s=>s.id===id);
  for(const cue of shot.cues){
    if(!cue.actions.some(a=>['blink','blink-all'].includes(a.action)))continue;
    const phrase=cue.at.spoken;
    if(id==='mirror'&&!phrase.startsWith('code of'))continue;
    const index=alignedText.indexOf(phrase);
    assert.ok(index>=0&&alignedText.indexOf(phrase,index+1)<0);
    const firstWord=phrase.split(' ')[0].replace(/[.,;:!?]+$/,'');
    const last=Array.from(alignedText.slice(0,index)+firstWord).length-1;
    cue.until=chapter.speechOffset+take.alignment.character_end_times_seconds[last]-timed.start;
  }
}
const feedTimed=measured.chapters[0].shots.find(s=>s.id==='feed-motion');
// Already turning on frame one; still reach the authored pawl phase exactly.
const rate=32/feedTimed.start;
const clock=t=>t<=feedTimed.start?400+t*rate:
  440+(t-feedTimed.end)*.65;
for(const [i,shot] of chapter.shots.entries()){
  const timed=measured.chapters[0].shots[i];
  shot.model={from:clock(timed.start),to:clock(timed.end)};
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
// The graphic remains a live layer over the real wheel during the handoff.
// A continued outgoing custom action would clamp progress at the old cut.
// This incoming instance instead carries the same absolute drive elapsed time.
const open=chapter.shots.find(s=>s.id==='open-source');
const openTimed=measured.chapters[0].shots.find(s=>s.id==='open-source');
const driveStart=openTimed.start+openTimed.cues.find(c=>c.actions.some(a=>a.action==='drive')).at;
// Every label gets the same acceleration, with extra reading time over the
// waterwheel. Clear the stream just before the returning sentence.
const streamPhrase='a stream of open source tools';
const streamIndex=alignedText.indexOf(streamPhrase);
assert.ok(streamIndex>=0&&alignedText.indexOf(streamPhrase,streamIndex+1)<0);
const streamLast=Array.from(alignedText.slice(0,streamIndex)+streamPhrase).length-1;
const spokenStreamEnd=chapter.speechOffset+take.alignment.character_end_times_seconds[streamLast];
const returnPhrase='The wheel... makes revolutions';
const returnIndex=alignedText.indexOf(returnPhrase);
assert.ok(returnIndex>=0&&alignedText.indexOf(returnPhrase,returnIndex+1)<0);
const returnFirst=Array.from(alignedText.slice(0,returnIndex)).length;
const streamEnd=chapter.speechOffset+take.alignment.character_start_times_seconds[returnFirst]-.2;
const streamDuration=streamEnd-driveStart;
const streamRate=streamDuration/5.8;
// Preserve the approved wheel phase exactly; label travel is a separate clock.
const wheelRate=(spokenStreamEnd-driveStart)/5.8;
Object.assign(chapter.elements.ecosystem.props,{arrival:1.65*streamRate,
  spinDelay:1.65*wheelRate,stagger:.45*streamRate,streamDuration});
const returned=chapter.shots.find(s=>s.id==='wheel-returns');
const returnTimed=measured.chapters[0].shots.find(s=>s.id==='wheel-returns');
const handoffDuration=returned.transition.duration;
const offset=returnTimed.start-driveStart;
chapter.elements['handoff-ecosystem']=structuredClone(chapter.elements.ecosystem);
Object.assign(chapter.elements['handoff-ecosystem'].props,{timeOffset:offset,fadeDuration:handoffDuration});
returned.places.graphic='handoff-ecosystem';
delete returned.transition;
returned.cues=[...(returned.cues??[]),{at:0,until:returned.until,actions:[
  {element:'handoff-ecosystem',action:'drive',params:{}},
  ...chapter.elements.ecosystem.props.names.map(name=>({element:'handoff-ecosystem',action:'reveal',params:{name}})),
]}];
const duration=returnTimed.end-returnTimed.start,fps=doc.output.fps;
const times=[0];
for(let n=Math.ceil(returnTimed.start*fps);n/fps<returnTimed.end;n++){
  const at=n/fps-returnTimed.start;
  if(at>0)times.push(at);
}
times.push(duration);
returned.model={keys:times.map((at,i)=>({
  at:i===times.length-1?returned.until:at,
  seconds:500+wheelAngle(offset+at,chapter.elements.ecosystem.props)/90,
}))};
await writeFile(file,JSON.stringify(doc,null,2)+'\n');
const {captionsFromAlignment,srt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
await writeFile(resolve(base,'_build/raw-narration.wav'),await readFile(take.file));
const rawCaptions=captionsFromAlignment(take.alignment);
await writeFile(resolve(base,'_build/raw-captions.json'),JSON.stringify(rawCaptions,null,2)+'\n');
await writeFile(resolve(base,'_build/raw-captions.srt'),srt(rawCaptions));
const {loadEpisode}=await import(pathToFileURL(resolve(tool,'src/episode.mjs')));
const {speech}=await import(pathToFileURL(resolve(tool,'src/speech.mjs')));
await speech(await loadEpisode(file),{generate:false});
console.log('Cut 5 preview: aligned narration mix, individual stream entries, and silent wheel lead-in. No video rendered.');
