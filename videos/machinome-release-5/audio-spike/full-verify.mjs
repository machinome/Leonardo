// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify audio files without encoding a video or touching narration.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const base=resolve(dirname(fileURLToPath(import.meta.url)),'..');
if(!process.argv[2])throw Error('Usage: full-verify.mjs OUTPUT');
const out=resolve(process.argv[2]),sr=48000;
const json=async p=>JSON.parse(await readFile(p));
const evidence=await json(resolve(out,'audio-evidence.json'));
const decode=file=>{
  const b=execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-i',file,
    '-f','f32le','-ac','1','-ar',String(sr),'pipe:1'],{maxBuffer:128*1024*1024});
  return new Float32Array(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength));
};
const checks=[];
for(const id of ['water','paddles','wheel','saw']){
  const a=decode(resolve(out,`${id}.wav`));
  assert.equal(a.length,evidence.samples,`${id} full-film length`);
  const old=decode(resolve(base,`_build/sfx-spike-17-DLBvT2/${id}.wav`));
  let delta=0;for(let i=0;i<old.length;i++)delta=Math.max(delta,Math.abs(a[i]-old[i]));
  assert.ok(delta<=2/8388608,`${id} preserves approved opening: ${delta}`);
  const silent=[83,87,116,125,149,165,194];
  if(id==='saw')silent.push(1,4,185,188);
  for(const t of silent)
    for(let i=Math.round(t*sr);i<Math.round((t+.1)*sr);i++)assert.equal(a[i],0,`${id} silence at ${t}`);
  checks.push({id,samples:a.length,openingMaxSampleDelta:delta,silentWindows:silent});
}
const events=(await json(resolve(out,'events.json'))).events;
const closing=events.filter(e=>e.at>=182.125&&e.at<190.875);
assert.ok(closing.length>20);
const firstSpacing=closing[1].at-closing[0].at;
const lastSpacing=closing.at(-1).at-closing.at(-2).at;
assert.ok(lastSpacing<firstSpacing*.3,'Paddle cadence accelerates through closing zoom');
assert.ok(closing.every(e=>e.pitch===1),'Water splash pitch stays fixed');
const protectedFiles=await json(resolve(out,'source-hashes.json'));
for(const [name,digest] of Object.entries(protectedFiles)){
  const current=createHash('sha256').update(await readFile(resolve(base,name))).digest('hex');
  assert.equal(current,digest,`Protected source ${name}`);
}
const result={status:'passed',checks,closing:{events:closing.length,firstSpacing,lastSpacing,
  waterPitch:1},protectedFilesUnchanged:Object.keys(protectedFiles),noVideoRendered:true};
await writeFile(resolve(out,'verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
