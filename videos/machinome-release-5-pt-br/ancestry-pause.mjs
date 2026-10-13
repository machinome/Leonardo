// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Editorial silence only: retain every sample of the approved performance.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname, resolve, basename} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const source=JSON.parse(await readFile(resolve(base,'auditions/proposal-8/_build/narration-manifest.json')));
const wav=await readFile(source.cacheFile);
const digest=b=>createHash('sha256').update(b).digest('hex');
assert.equal(digest(wav),source.sha256);
assert.equal(source.sha256,'48f80fd90c2896f130e7f4e7084b050b04ef238e5fd7ba7c5c1729746bd09241');
assert.equal(wav.toString('ascii',36,40),'data');
assert.equal(wav.readUInt32LE(24),24000);
assert.equal(wav.readUInt16LE(22),1);
assert.equal(wav.readUInt16LE(34),16);
// Choose a quiet sample inside the existing inter-sentence silence.
let sample=Math.round(30.1*24000);
for(let n=30.05*24000;n<30.15*24000;n++)
  if(Math.abs(wav.readInt16LE(44+2*n))<Math.abs(wav.readInt16LE(44+2*sample)))sample=n;
assert(Math.abs(wav.readInt16LE(44+2*sample))<32);
const at=sample/24000, seconds=2.4, count=seconds*24000*2, split=44+sample*2;
const edited=Buffer.concat([wav.subarray(0,split),Buffer.alloc(count),wav.subarray(split)]);
edited.writeUInt32LE(edited.length-8,4);
edited.writeUInt32LE(edited.length-44,40);
assert(edited.subarray(44,split).equals(wav.subarray(44,split)));
assert(edited.subarray(split+count).equals(wav.subarray(split)));
const record=JSON.parse(await readFile(source.cacheFile+'.json'));
const shift=t=>t>=at?t+seconds:t;
for(const key of ['character_start_times_seconds','character_end_times_seconds'])
  record.alignment[key]=record.alignment[key].map(shift);
const edit={kind:'insert-silence',at,seconds,sourceSha256:source.sha256,
  purpose:'Contemplation after ancestrais while the camera finishes its orbit; no spoken samples replaced or removed.'};
Object.assign(record,{sha256:digest(edited),duration:source.duration+seconds,
  audioEdits:[edit],source:'Approved take 8 with a documented editorial silence; original provider performance preserved separately.'});
const build=resolve(base,'_build/ancestry-pause');
await mkdir(resolve(build,'audio'),{recursive:true});
const file=resolve(build,'audio',basename(source.cacheFile));
for(const target of [file,resolve(base,'_build/audio',basename(file))]){
  await writeFile(target,edited);
  await writeFile(target+'.json',JSON.stringify(record,null,2)+'\n');
}
const manifest={...source,cacheFile:file,sha256:record.sha256,duration:record.duration,
  audioEdits:record.audioEdits,source:record.source,
  sections:source.sections.map(s=>({...s,start:shift(s.start),end:shift(s.end)})),
  listeningStatus:'Editorial pause awaiting pilot review in viewer 8790.'};
for(const target of [resolve(build,'narration-manifest.json'),resolve(base,'_build/narration-manifest.json')])
  await writeFile(target,JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({sha256:record.sha256,duration:record.duration,edit,spokenSamplesPreserved:true},null,2));
