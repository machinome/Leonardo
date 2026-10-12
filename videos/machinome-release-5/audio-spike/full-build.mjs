// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Audio-only full-film build. Never generates speech or renders video frames.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdtemp} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFile,execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {createRenderer,normalized,texture,rms} from './synthesis.mjs';
import {createFilmPlan,createControls} from './full-plan.mjs';

const own=dirname(fileURLToPath(import.meta.url)),base=resolve(own,'..');
const project=resolve(base,'../..');
if(!process.argv[2])throw Error('Usage: full-build.mjs VIDEOMAKER [OUTPUT]');
const tool=resolve(process.argv[2]);
const out=process.argv[3]?resolve(process.argv[3]):await mkdtemp(resolve(base,'_build/sfx-full-'));
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=async f=>JSON.parse(await readFile(f));
const save=(name,obj)=>writeFile(resolve(out,name),JSON.stringify(obj,null,2)+'\n');
const protectedFiles=['movie.py','narration.py','stage.jsx','stage.css','finish.mjs',
  'ending-motion.mjs','studio-motion.mjs','_build/movie.json','_build/narration.wav','_build/rehearsal.mp4'];
const before=Object.fromEntries(await Promise.all(protectedFiles.map(async p=>[p,sha(await readFile(resolve(base,p)))])));
const movie=await json(resolve(base,'_build/movie-resolved.json'));
const recipe=await json(resolve(own,'sawmill.json'));
const plan=createFilmPlan(movie),duration=plan.duration,sr=48000,hz=240;
assert.equal(Math.round(duration*sr),duration*sr);
const count=Math.round(duration*sr),gridCount=Math.ceil(duration*hz)+1;
const {modelSecondsAt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const times=[],indexes=[],controlSlots=new Array(gridCount).fill(null);
for(let i=0;i<gridCount;i++){
  const t=Math.min(duration,i/hz);
  if(!plan.active(t))continue;
  const shot=plan.shots.find(s=>t>=s.start&&t<s.end)??plan.shots.at(-1);
  indexes.push(i);times.push(modelSecondsAt(shot,t-shot.start));
}
console.log(`Audio only: ${duration}s; ${times.length} real model poses at ${hz} Hz.\nOutput: ${out}`);
await save('movie-resolved.json',movie);
await save('source-hashes.json',before);
const sourceHash=sha(await readFile(resolve(project,'models/hydraulic_sawmill/model.py')));
const signalKey=sha(JSON.stringify({times,sourceHash,adapter:sha(await readFile(resolve(own,'signals.py')))}));
let signalCache;
try{signalCache=await json(resolve(out,'signals.json'));}catch(e){if(e.code!=='ENOENT')throw e;}
if(signalCache?.key!==signalKey){
  console.log('Reading existing machine coordinates; geometry and narration are not rebuilt.');
  const signals=await new Promise((done,reject)=>{
    const child=execFile('/home/asa/devel/machinome/.venv/bin/python',[resolve(own,'signals.py')],
      {cwd:project,env:{...process.env,PYTHONPATH:project},maxBuffer:64*1024*1024,timeout:600000},
      (err,stdout)=>err?reject(err):done(JSON.parse(stdout)));
    child.stdin.end(JSON.stringify({times}));
  });
  signalCache={key:signalKey,indexes,...signals};
  await save('signals.json',signalCache);
}
assert.deepEqual(signalCache.indexes,indexes);
assert.equal(signalCache.rows.length,times.length);
for(let j=0;j<indexes.length;j++)controlSlots[indexes[j]]=signalCache.rows[j];
const readouts=await json(resolve(project,'models/hydraulic_sawmill/readouts.json'));
let poseError=0;
for(const row of signalCache.rows){
  const phase=((row[1]%360)+360)%360,x=phase/.5,j=Math.min(719,Math.floor(x));
  const drop=readouts.rows[j][0]+(readouts.rows[j+1][0]-readouts.rows[j][0])*(x-j);
  poseError=Math.max(poseError,Math.abs(170-row[2]-drop));
}
assert.ok(poseError<.001,`CAD readout disagreement ${poseError} mm`);
const controls=createControls({rows:controlSlots,controlHz:hz,sampleRate:sr,plan});
const decode=(file,args=[])=>{
  const bytes=execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-i',file,...args,
    '-vn','-ac','1','-ar',String(sr),'-f','f32le','pipe:1'],{maxBuffer:128*1024*1024});
  return new Float32Array(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength));
};
const sawFile=resolve(base,'_build/sfx-spike-17-DLBvT2/saw-recording.mp3');
const waterFile=resolve(base,'_build/sfx-audition-G66QJD/opening-effects.wav');
const assets={
  saw:normalized(texture(decode(sawFile,['-ss','5','-t','25','-af','highpass=f=180,lowpass=f=9000']),sr,5,recipe.seed),recipe.saw.rms),
  water:normalized(texture(decode(waterFile,['-t','7','-af','highpass=f=90,lowpass=f=7500']),sr,9,recipe.seed+1),recipe.water.rms),
};
const render=block=>{
  const r=createRenderer({sampleRate:sr,duration,controls,assets,recipe});
  while(r.process(block)){}return r;
};
console.log('Building four sound stems, then checking deterministic block replay.');
const result=render(128),again=render(4096);
for(const [name,stem] of Object.entries(result.stems))
  assert.deepEqual(stem,again.stems[name],`${name}: block replay`);
assert.deepEqual(result.telemetry,again.telemetry);
// Preserve the approved opening's calibration, not a whole-film average which
// would boost sounds merely because this film contains more intentional silence.
const calibration={};
for(const name of ['wheel','paddles']){
  const gain=recipe[name].rms/rms(result.stems[name].subarray(0,17*sr));
  calibration[name]=gain;
  for(let i=0;i<count;i++)result.stems[name][i]*=gain;
}
const narration=decode(resolve(base,'_build/narration.wav'));
assert.equal(narration.length,count,'narration duration unchanged and matches film');
const level=a=>{
  let peak=0;for(const v of a){assert.ok(Number.isFinite(v));peak=Math.max(peak,Math.abs(v));}
  return {peak,rms:rms(a)};
};
const defaultStemGain=.55;
let defaultPeak=0,absoluteBound=0;
for(let i=0;i<count;i++){
  let sum=narration[i],bound=Math.abs(narration[i]);
  for(const a of Object.values(result.stems)){sum+=defaultStemGain*a[i];bound+=defaultStemGain*Math.abs(a[i]);}
  defaultPeak=Math.max(defaultPeak,Math.abs(sum));absoluteBound=Math.max(absoluteBound,bound);
}
// Absolute bound also leaves headroom if any combination is muted or soloed.
const masterGain=Math.min(1,.88/absoluteBound);
const labels={water:'Water flow',paddles:'Paddle splashes',wheel:'Wheel / axle',saw:'Saw'};
const stemEvidence={};
for(const [id,a] of Object.entries(result.stems)){
  const path=resolve(out,`${id}.wav`);
  execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-n','-f','f32le','-ar',String(sr),
    '-ac','1','-i','pipe:0','-c:a','pcm_s24le',path],
    {input:Buffer.from(a.buffer,a.byteOffset,a.byteLength),maxBuffer:1024*1024});
  stemEvidence[id]={...level(a),sha256:sha(await readFile(path)),duration,samples:count};
}
const manifest={format:'videomaker-live-audio/0.1',masterGain,narrationGain:1,
  tracks:Object.keys(labels).map(id=>({id,label:labels[id],path:`${id}.wav`,gain:defaultStemGain}))};
await save('stems.json',manifest);
await save('events.json',result.telemetry);
await save('audio-evidence.json',{duration,sampleRate:sr,controlHz:hz,samples:count,
  blockSizes:[128,4096],blockReplayExact:true,cadStrokeMaxErrorMm:poseError,
  evaluatedPoses:times.length,spans:plan.spans,calibration,stems:stemEvidence,
  defaultMix:{stemGain:defaultStemGain,masterGain,defaultPeak:defaultPeak*masterGain,
    absoluteBound:absoluteBound*masterGain,ducking:false},
  telemetry:{...result.telemetry,events:result.telemetry.events.length},
  inputs:{movie:sha(JSON.stringify(movie)),model:sourceHash,narration:before['_build/narration.wav'],
    recipe:sha(await readFile(resolve(own,'sawmill.json'))),saw:sha(await readFile(sawFile)),water:sha(await readFile(waterFile))},
  limitations:['Project-local illustrative acoustics, not fluid/force/vibration simulation.',
    'Water sample rights need review before publication; reused private audition only.',
    'Scrubbing/rewind and testing pose jumps deliberately silent; no reverse-time physics.',
    'Unducked independent stems. Mixer settings are listening-only, not a render mix.',
    'No agent listening assessment. Pilot auditions in player.']});
for(const [p,digest] of Object.entries(before))
  assert.equal(sha(await readFile(resolve(base,p))),digest,`Protected source changed: ${p}`);
console.log(JSON.stringify({out,duration,masterGain,defaultPeak:defaultPeak*masterGain,
  cadStrokeMaxErrorMm:poseError,events:result.telemetry.events.length,protectedSourcesUnchanged:true}));
