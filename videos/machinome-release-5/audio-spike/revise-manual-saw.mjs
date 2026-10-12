// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Saw-only revision: retain all other audition bytes and the approved film.
import assert from 'node:assert/strict';
import {readFile,writeFile,copyFile,constants} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createFilmPlan,createControls} from './full-plan.mjs';
import {createManualSaw} from './manual-saw.mjs';
const own=dirname(fileURLToPath(import.meta.url)),base=resolve(own,'..'),project=resolve(base,'../..');
const verifyOnly=process.argv[2]==='--verify';
if(!process.argv[2]||!process.argv[3])throw Error('Usage: revise-manual-saw.mjs PREVIOUS FRESH_OUTPUT | --verify OUTPUT');
const out=resolve(process.argv[3]),sr=48000;
const json=async p=>JSON.parse(await readFile(p));
const sha=b=>createHash('sha256').update(b).digest('hex');
const digest=async p=>sha(await readFile(p));
const save=(name,value)=>writeFile(resolve(out,name),JSON.stringify(value,null,2)+'\n');
const decode=file=>{
  const b=execFileSync('ffmpeg',['-v','error','-i',file,'-ac','1','-ar',String(sr),'-f','f32le','pipe:1'],{maxBuffer:128*1024*1024});
  return new Float32Array(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength));
};
const wav=(name,a)=>execFileSync('ffmpeg',['-v','error','-n','-f','f32le','-ar',String(sr),'-ac','1','-i','pipe:0',
  '-c:a','pcm_s24le',resolve(out,name)],{input:Buffer.from(a.buffer,a.byteOffset,a.byteLength)});
if(!verifyOnly){
  const previous=resolve(process.argv[2]);assert.notEqual(previous,out);
  const prior=await json(resolve(previous,'mechanics-evidence.json'));
  const signalBuild=prior.sourceBuild,full=await json(resolve(signalBuild,'audio-evidence.json'));
  const recipe=await json(resolve(own,'manual-saw.json'));
  const movie=await json(resolve(previous,'movie-resolved.json'));
  assert.equal(await digest(resolve(previous,'movie-resolved.json')),await digest(resolve(base,'_build/movie-resolved.json')));
  const signals=await json(resolve(signalBuild,'signals.json'));
  const sourceHash=await digest(resolve(project,'models/hydraulic_sawmill/model.py'));
  assert.equal(sourceHash,full.inputs.model);
  assert.equal(signals.key,sha(JSON.stringify({times:signals.rows.map(r=>r[0]),sourceHash,adapter:await digest(resolve(own,'signals.py'))})));
  const plan=createFilmPlan(movie),hz=240,duration=plan.duration;
  const rows=new Array(Math.ceil(duration*hz)+1).fill(null);
  signals.indexes.forEach((index,j)=>{rows[index]=signals.rows[j];});
  const controls=createControls({rows,controlHz:hz,sampleRate:sr,plan});
  const recording=resolve(previous,recipe.source.file);
  assert.equal(await digest(recording),recipe.source.sha256);
  const source=decode(recording);
  // Exact contiguous source samples, one constant amplitude multiplier only.
  // Deliberately no filter, atempo, granular texture, interpolation or resample.
  const strokes=recipe.segments.map(([start,length])=>Float32Array.from(
    source.subarray(Math.round(start*sr),Math.round((start+length)*sr)),v=>v*recipe.sourceGain));
  const render=block=>{const r=createManualSaw({sampleRate:sr,duration,controls,strokes,recipe});while(r.process(block)){}return r;};
  const a=render(128),b=render(4096);
  assert.deepEqual(a.audio,b.audio);assert.deepEqual(a.events,b.events);
  console.log(`Saw only: ${a.events.length} native-pitch hand scrapes, ${duration}s, exact block replay.`);
  wav('saw.wav',a.audio);
  for(let j=0;j<strokes.length;j++)wav(`hand-stroke-${j}.wav`,strokes[j]);
  for(const name of ['water.wav','paddles.wav','wheel.wav','source-hashes.json','movie-resolved.json',recipe.source.file])
    await copyFile(resolve(previous,name),resolve(out,name),constants.COPYFILE_EXCL);
  const manifest=await json(resolve(previous,'stems.json'));
  manifest.tracks.find(t=>t.id==='saw').label='Manual saw';
  await save('stems.json',manifest);await save('manual-saw-recipe.json',recipe);await save('manual-saw-events.json',a.events);
  await save('manual-saw-evidence.json',{status:'built',previous,signalBuild,signalKey:signals.key,duration,sampleRate:sr,
    samples:a.audio.length,source:recipe.source,sourceGain:recipe.sourceGain,segments:recipe.segments,
    sourceProcessing:'Only stereo-to-mono decode, contiguous trims, constant gain and 8ms fades; no time stretch, loop, pitch shift or synthesis.',
    blockSizes:[128,4096],exactReplay:true,events:a.events.length,playbackRate:1,
    sawSha256:await digest(resolve(out,'saw.wav')),unchanged:['narration','water','paddles','iron axle','pictures','timeline','mixer defaults'],
    generator:'The simple person-sawing-by-hand prompt failed at MMAudio with null error. Original hand-tool recording used.',
    limitations:[recipe.limits,'No subjective listening assessment by the agent.','No video rendered.']});
}
const evidence=await json(resolve(out,'manual-saw-evidence.json'));
const manifest=await json(resolve(out,'stems.json')),previous=await json(resolve(evidence.previous,'stems.json'));
assert.equal(manifest.masterGain,previous.masterGain);assert.equal(manifest.narrationGain,previous.narrationGain);
const before=await json(resolve(out,'source-hashes.json'));
for(const [name,hash]of Object.entries(before))assert.equal(await digest(resolve(base,name)),hash,name);
assert.equal(await digest(resolve(out,'movie-resolved.json')),await digest(resolve(base,'_build/movie-resolved.json')));
const channels={narration:decode(resolve(base,'_build/narration.wav'))},checks=[];
for(const t of manifest.tracks){
  assert.equal(t.gain,previous.tracks.find(p=>p.id===t.id).gain);
  const file=resolve(out,t.path),hash=await digest(file);channels[t.id]=decode(file);
  assert.equal(channels[t.id].length,evidence.samples);
  if(t.id==='saw'){
    assert.equal(hash,evidence.sawSha256);assert.notEqual(hash,await digest(resolve(evidence.previous,t.path)));
  }else assert.equal(hash,await digest(resolve(evidence.previous,t.path)),`${t.id} unchanged`);
  checks.push({id:t.id,sha256:hash,unchanged:t.id!=='saw'});
}
for(const t of [1,4,83,87,116,125,149,165,185,188,194])
  for(let i=t*sr;i<(t+.1)*sr;i++)assert.equal(channels.saw[i],0,`Silent saw at ${t}`);
let peak=0,bound=0,active=0;
for(let i=0;i<evidence.samples;i++){
  let sum=channels.narration[i]*manifest.narrationGain,abs=Math.abs(sum);
  for(const t of manifest.tracks){sum+=channels[t.id][i]*t.gain;abs+=Math.abs(channels[t.id][i])*t.gain;}
  peak=Math.max(peak,Math.abs(sum)*manifest.masterGain);bound=Math.max(bound,abs*manifest.masterGain);
  if(channels.saw[i]!==0)active++;
}
assert.ok(bound<.881);
const events=await json(resolve(out,'manual-saw-events.json'));
assert.ok(events.every(e=>e.playbackRate===1&&e.sourceSamples<=.5*sr));
assert.equal(events.length,evidence.events);
const result={status:'passed',checks,peak,bound,events:events.length,sourcePlaybackRate:1,
  audibleSeconds:active/sr,protectedFilesUnchanged:Object.keys(before),resolvedMovieUnchanged:true,noVideoRendered:true};
await save('manual-saw-verification.json',result);console.log(JSON.stringify(result,null,2));
