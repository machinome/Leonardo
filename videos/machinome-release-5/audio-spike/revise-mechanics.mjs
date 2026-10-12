// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Replaces only two audition stems; no CAD evaluation, narration or video render.
import assert from 'node:assert/strict';
import {readFile,writeFile,copyFile,constants} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createMechanics} from './mechanics.mjs';
import {createFilmPlan,createControls} from './full-plan.mjs';
import {normalized,rms} from './synthesis.mjs';
const own=dirname(fileURLToPath(import.meta.url)),base=resolve(own,'..'),project=resolve(base,'../..');
if(!process.argv[2]||!process.argv[3])throw Error('Usage: revise-mechanics.mjs ORIGINAL_FULL_BUILD FRESH_OUTPUT_WITH_RECORDINGS');
const original=resolve(process.argv[2]),out=resolve(process.argv[3]);
assert.notEqual(out,original,'Keep the previous audition recoverable');
const json=async f=>JSON.parse(await readFile(f));
const sha=b=>createHash('sha256').update(b).digest('hex');
const save=(name,value)=>writeFile(resolve(out,name),JSON.stringify(value,null,2)+'\n');
const movie=await json(resolve(original,'movie-resolved.json')),recipe=await json(resolve(own,'mechanics.json'));
assert.equal(sha(await readFile(resolve(original,'movie-resolved.json'))),sha(await readFile(resolve(base,'_build/movie-resolved.json'))),'Film changed: rebuild its signals first');
const before=await json(resolve(original,'source-hashes.json'));
const checkProtected=async()=>{for(const [name,digest]of Object.entries(before))
  assert.equal(sha(await readFile(resolve(base,name))),digest,`Protected source changed: ${name}`);};
await checkProtected();
const evidence=await json(resolve(original,'audio-evidence.json'));
const signals=await json(resolve(original,'signals.json'));
const sourceHash=sha(await readFile(resolve(project,'models/hydraulic_sawmill/model.py')));
assert.equal(sourceHash,evidence.inputs.model,'Model changed: rebuild signals first');
assert.equal(signals.key,sha(JSON.stringify({times:signals.rows.map(r=>r[0]),sourceHash,
  adapter:sha(await readFile(resolve(own,'signals.py')))})),'Signal cache no longer matches its adapter/model');
const plan=createFilmPlan(movie),duration=plan.duration,sr=48000,hz=240,count=Math.round(sr*duration);
const rows=new Array(Math.ceil(duration*hz)+1).fill(null);
signals.indexes.forEach((index,j)=>{rows[index]=signals.rows[j];});
assert.equal(Math.min(...signals.rows.map(r=>r[2])),recipe.bottomMm);
assert.equal(Math.max(...signals.rows.map(r=>r[2])),recipe.topMm);
const controls=createControls({rows,controlHz:hz,sampleRate:sr,plan});
const decode=(file,args=[])=>{
  const bytes=execFileSync('ffmpeg',['-v','error','-i',file,...args,'-vn','-ac','1','-ar',String(sr),'-f','f32le','pipe:1'],
    {maxBuffer:128*1024*1024});
  return new Float32Array(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength));
};
const wav=(name,a)=>execFileSync('ffmpeg',['-v','error','-n','-f','f32le','-ar',String(sr),'-ac','1',
  '-i','pipe:0','-c:a','pcm_s24le',resolve(out,name)],{input:Buffer.from(a.buffer,a.byteOffset,a.byteLength)});
const assets={},sources={};
for(const id of ['saw','iron']){
  const source=recipe.sources[id],file=resolve(out,source.file);
  sources[id]={...source,sha256:sha(await readFile(file))};
  assets[id]=recipe[`${id}Segments`].map(([start,length])=>normalized(
    decode(file,['-af',`atrim=start=${start}:duration=${length},asetpts=PTS-STARTPTS,${recipe[`${id}Filter`]}`]),recipe[`${id}Rms`]));
  for(let j=0;j<assets[id].length;j++){
    const expected=recipe[`${id}Segments`][j][1]*(id==='saw'?5:1);
    assert.ok(Math.abs(assets[id][j].length/sr-expected)<.2,`${id} stroke ${j}: extraction truncated the stretched stroke`);
  }
  for(let j=0;j<assets[id].length;j++)wav(`${id}-stroke-${j}.wav`,assets[id][j]);
}
console.log(`Replacing hacksaw and iron axle for ${duration}s using cached real-model coordinates.`);
const render=block=>{const r=createMechanics({sampleRate:sr,duration,controls,assets,recipe});while(r.process(block)){}return r;};
const result=render(128),again=render(4096);
assert.deepEqual(result.stems,again.stems,'Audio block replay');assert.deepEqual(result.events,again.events);
const manifest=await json(resolve(original,'stems.json'));
const gain=id=>manifest.tracks.find(t=>t.id===id).gain;
const narration=decode(resolve(base,'_build/narration.wav'));
const water=decode(resolve(original,'water.wav')),paddles=decode(resolve(original,'paddles.wav'));
for(const a of [narration,water,paddles])assert.equal(a.length,count);
// Keep every existing mixer default and all unchanged channels. If necessary,
// attenuate only the two new sources to retain the original absolute headroom.
let trim=1;
for(let i=0;i<count;i++){
  const fixed=Math.abs(narration[i])*manifest.narrationGain+Math.abs(water[i])*gain('water')+Math.abs(paddles[i])*gain('paddles');
  const variable=Math.abs(result.stems.saw[i])*gain('saw')+Math.abs(result.stems.wheel[i])*gain('wheel');
  if(variable>0)trim=Math.min(trim,Math.max(0,(.88/manifest.masterGain-fixed)/variable));
}
const measurements={};let peak=0,bound=0;
for(const [id,a]of Object.entries(result.stems)){
  for(let i=0;i<count;i++)a[i]*=trim;
  wav(`${id}.wav`,a);
  const decoded=decode(resolve(out,`${id}.wav`));assert.equal(decoded.length,count);
  for(const t of [83,87,116,125,149,165,194,...(id==='saw'?[1,4,185,188]:[])])
    assert.equal(rms(decoded.subarray(t*sr,Math.round((t+.2)*sr))),0,`${id} silent at ${t}s`);
  measurements[id]={sha256:sha(await readFile(resolve(out,`${id}.wav`))),samples:count,rms:rms(decoded)};
}
for(let i=0;i<count;i++){
  let sum=narration[i]*manifest.narrationGain,abs=Math.abs(sum);
  for(const [id,a]of Object.entries({water,paddles,...result.stems})){
    sum+=a[i]*gain(id);abs+=Math.abs(a[i])*gain(id);
  }
  peak=Math.max(peak,Math.abs(sum)*manifest.masterGain);bound=Math.max(bound,abs*manifest.masterGain);
}
assert.ok(bound<.880001);
for(const id of ['water','paddles']){
  await copyFile(resolve(original,`${id}.wav`),resolve(out,`${id}.wav`),constants.COPYFILE_EXCL);
  assert.equal(sha(await readFile(resolve(out,`${id}.wav`))),sha(await readFile(resolve(original,`${id}.wav`))));
}
for(const name of ['movie-resolved.json','source-hashes.json'])
  await copyFile(resolve(original,name),resolve(out,name),constants.COPYFILE_EXCL);
manifest.tracks.find(t=>t.id==='saw').label='Hacksaw';
manifest.tracks.find(t=>t.id==='wheel').label='Iron axle / crank';
await save('stems.json',manifest);
await save('mechanics-recipe.json',recipe);
await save('mechanics-events.json',result.events);
await save('mechanics-evidence.json',{status:'passed',duration,sampleRate:sr,samples:count,
  sourceBuild:original,signalKey:signals.key,recipeSha256:sha(await readFile(resolve(own,'mechanics.json'))),
  sources,stems:measurements,strokeLengths:assets.saw.map(a=>a.length/sr),
  blocks:[128,4096],exactReplay:true,unchanged:['narration','water','paddles','movie','mixer default gains'],
  replacementOnlyTrim:trim,defaultPeak:peak,absoluteBound:bound,ironEvents:result.events.length,
  generator:'Anonymous MMAudio hacksaw request failed with null provider error; no generated sample used.',
  limitations:[recipe.limits,'No subjective listening assessment by the agent.','No video rendered; previous audition retained.']});
await checkProtected();
console.log(JSON.stringify({out,trim,peak,bound,ironEvents:result.events.length,protectedFilesUnchanged:true}));
