// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Project-specific film adapter and offline audition builder. No production writes.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createRenderer,normalized,texture,smooth,rms} from './synthesis.mjs';
const own=dirname(fileURLToPath(import.meta.url)),filmBase=resolve(own,'..');
const project=resolve(filmBase,'../..'),out=resolve(process.argv[2]),tool=resolve(process.argv[3]);
const sr=48000,duration=17,hz=240,count=sr*duration;
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=async f=>JSON.parse(await readFile(f));
const writeJson=(name,obj)=>writeFile(resolve(out,name),JSON.stringify(obj,null,2)+'\n');
const movie=await json(resolve(out,'movie-resolved.json'));
const recipe=await json(resolve(own,'sawmill.json'));
const {modelSecondsAt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const shots=movie.chapters.flatMap(c=>c.shots),reveal=shots.find(s=>s.id==='ancestor');
const shotAt=t=>shots.find(s=>t>=s.start&&t<s.end);
const times=Array.from({length:duration*hz+1},(_,i)=>{
  const t=i/hz,s=shotAt(t);return modelSecondsAt(s,t-s.start);
});
console.log('Evaluating existing sawmill coordinates (no geometry rebuild).');
const signals=JSON.parse(execFileSync('/home/asa/devel/machinome/.venv/bin/python',
  [resolve(own,'signals.py')],{cwd:project,env:{...process.env,PYTHONPATH:project},
    input:JSON.stringify({times}),encoding:'utf8',maxBuffer:16*1024*1024,timeout:180000}));
await writeJson('signals.json',signals);
const rows=signals.rows;
assert.equal(rows.length,times.length);
// Cross-check the adapter against the already measured, checked-in CAD stroke.
const readouts=await json(resolve(project,'models/hydraulic_sawmill/readouts.json'));
let poseError=0;
for(const row of rows){
  const phase=((row[1]%360)+360)%360,x=phase/.5,j=Math.min(719,Math.floor(x));
  const drop=readouts.rows[j][0]+(readouts.rows[j+1][0]-readouts.rows[j][0])*(x-j);
  poseError=Math.max(poseError,Math.abs(170-row[2]-drop));
}
assert.ok(poseError<.001,`CAD readout disagreement ${poseError} mm`);
// A snapshot is a project-local boundary. The synthesis module never knows
// where these curves or the presentation envelopes came from.
const controls={sample(i){
  const t=i/sr,x=t*hz,j=Math.min(rows.length-2,Math.floor(x)),u=x-j;
  const a=rows[j],b=rows[j+1],mix=k=>a[k]+(b[k]-a[k])*u;
  return {phase:mix(1),phaseRate:(b[1]-a[1])*hz,velocity:(b[2]-a[2])*hz,
    engaged:Math.min(a[4],b[4]),continuous:true,
    sawGain:smooth((t-reveal.start)/reveal.transition.duration),
    waterGain:smooth(t/.18),wheelGain:smooth((t-.25)/1.1)};
}};
const decode=(file,args=[])=>{
  const bytes=execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-i',file,...args,
    '-vn','-ac','1','-ar',String(sr),'-f','f32le','pipe:1'],{maxBuffer:64*1024*1024});
  return new Float32Array(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength));
};
const sawFile=resolve(out,'saw-recording.mp3');
const waterFile=resolve(filmBase,'_build/sfx-audition-G66QJD/opening-effects.wav');
const waterSource=decode(waterFile,['-t','7','-af','highpass=f=90,lowpass=f=7500']);
const sawSource=decode(sawFile,['-ss','5','-t','25','-af','highpass=f=180,lowpass=f=9000']);
const assets={
  saw:normalized(texture(sawSource,sr,5,recipe.seed),recipe.saw.rms),
  water:normalized(texture(waterSource,sr,9,recipe.seed+1),recipe.water.rms),
};
const render=block=>{
  const r=createRenderer({sampleRate:sr,duration,controls,assets,recipe});
  while(r.process(block)){}return r;
};
console.log('Rendering motion-driven water, splashes, axle and saw tracks.');
const result=render(128),again=render(4096);
for(const k of Object.keys(result.stems))
  assert.deepEqual(result.stems[k],again.stems[k],`${k}: independent of audio block size`);
const stems=result.stems;
stems.wheel=normalized(stems.wheel,recipe.wheel.rms);
stems.paddles=normalized(stems.paddles,recipe.paddles.rms);
const narrationFile=resolve(filmBase,'_build/narration.wav');
const narration=decode(narrationFile,['-t',String(duration)]);
assert.equal(narration.length,count);
const effects=new Float32Array(count),mix=new Float32Array(count),duck=new Float32Array(count);
let speechEnvelope=0;
for(let i=0;i<count;i++){
  const level=Math.abs(narration[i]);
  speechEnvelope+=(level-speechEnvelope)*(level>speechEnvelope?.005:.000035);
  duck[i]=1-.48*smooth(speechEnvelope/.045);
  // End only the audition's effect tails; leave narration's samples untouched.
  const tail=smooth((duration-i/sr)/.045);
  effects[i]=Object.values(stems).reduce((v,a)=>v+a[i],0)*tail;
  mix[i]=narration[i]+effects[i]*duck[i];
}
let peak=0;for(const v of mix)peak=Math.max(peak,Math.abs(v));
// A constant final bus gain only when required; never alter the source take.
const gain=Math.min(1,.92/peak);for(let i=0;i<count;i++)mix[i]*=gain;
const wav=(name,a)=>execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-y',
  '-f','f32le','-ar',String(sr),'-ac','1','-i','pipe:0','-c:a','pcm_s24le',resolve(out,name)],
  {input:Buffer.from(a.buffer,a.byteOffset,a.byteLength),maxBuffer:1024*1024});
for(const [name,a] of Object.entries(stems))wav(`${name}.wav`,a);
wav('effects.wav',effects);wav('mix.wav',mix);wav('saw-texture.wav',assets.saw);
wav('water-texture.wav',assets.water);
await writeJson('events.json',result.telemetry);
await writeJson('audio-evidence.json',{sampleRate:sr,duration,samples:count,
  blockSizes:[128,4096],blockReplayExact:true,cadStrokeMaxErrorMm:poseError,
  sourceRate:(times.at(-1)-times[0])/duration,modelInterval:[times[0],times.at(-1)],
  reveal:[reveal.start,reveal.start+reveal.transition.duration],
  telemetry:result.telemetry,busGain:gain,peakBeforeBusGain:peak,
  levels:Object.fromEntries(Object.entries({...stems,effects,mix}).map(([k,a])=>[k,{rms:rms(a),db:20*Math.log10(rms(a))}])),
  inputs:{movie:sha(await readFile(resolve(out,'movie-resolved.json'))),
    model:sha(await readFile(resolve(filmBase,movie.model.manifest))),
    narration:sha(await readFile(narrationFile)),saw:sha(await readFile(sawFile)),
    water:sha(await readFile(waterFile))},
  limitations:['Generated water, recorded handsaw texture, procedural wooden axle.',
    'Authored acoustics, not fluid/force/vibration simulation.',
    'Paddle bottom-contact timing approximation, not solved water-surface intersection.',
    'Numerical audio checks only; listening review belongs to the pilot.']});
const before=await json(resolve(out,'source-hashes.json'));
for(const [name,digest] of Object.entries(before))
  assert.equal(sha(await readFile(resolve(filmBase,name))),digest,`Production changed: ${name}`);
console.log(JSON.stringify({duration,peak:peak*gain,busGain:gain,cadStrokeMaxErrorMm:poseError,
  events:result.telemetry.events.length,levels:Object.fromEntries(Object.entries(stems).map(([k,a])=>[k,20*Math.log10(rms(a))]))}));
