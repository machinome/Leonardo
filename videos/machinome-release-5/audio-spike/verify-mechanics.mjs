// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const base=resolve(dirname(fileURLToPath(import.meta.url)),'..');
if(!process.argv[2])throw Error('Usage: verify-mechanics.mjs OUTPUT');
const out=resolve(process.argv[2]),json=async p=>JSON.parse(await readFile(p));
const sha=async p=>createHash('sha256').update(await readFile(p)).digest('hex');
const evidence=await json(resolve(out,'mechanics-evidence.json'));
assert.equal(evidence.status,'passed');
const manifest=await json(resolve(out,'stems.json'));
const previous=await json(resolve(evidence.sourceBuild,'stems.json'));
assert.equal(manifest.masterGain,previous.masterGain);assert.equal(manifest.narrationGain,previous.narrationGain);
for(const t of manifest.tracks)assert.equal(t.gain,previous.tracks.find(p=>p.id===t.id).gain);
const decode=file=>{
  const b=execFileSync('ffmpeg',['-v','error','-i',file,'-ac','1','-ar','48000','-f','f32le','pipe:1'],{maxBuffer:128*1024*1024});
  return new Float32Array(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength));
};
const channels={narration:decode(resolve(base,'_build/narration.wav'))},checks=[];
for(const id of ['water','paddles','wheel','saw']){
  const file=resolve(out,`${id}.wav`),digest=await sha(file),a=decode(file);channels[id]=a;
  assert.equal(a.length,evidence.samples);
  if(id==='water'||id==='paddles')assert.equal(digest,await sha(resolve(evidence.sourceBuild,`${id}.wav`)));
  else {assert.equal(digest,evidence.stems[id].sha256);assert.notEqual(digest,await sha(resolve(evidence.sourceBuild,`${id}.wav`)));}
  for(const t of [83,87,116,125,149,165,194,...(id==='saw'?[1,4,185,188]:[])])
    for(let i=t*48000;i<(t+.1)*48000;i++)assert.equal(a[i],0,`${id} silence ${t}`);
  checks.push({id,samples:a.length,sha256:digest,unchanged:id==='water'||id==='paddles'});
}
let peak=0,bound=0;
for(let i=0;i<evidence.samples;i++){
  let sum=channels.narration[i]*manifest.narrationGain,absolute=Math.abs(sum);
  for(const t of manifest.tracks){sum+=channels[t.id][i]*t.gain;absolute+=Math.abs(channels[t.id][i])*t.gain;}
  peak=Math.max(peak,Math.abs(sum)*manifest.masterGain);bound=Math.max(bound,absolute*manifest.masterGain);
}
assert.ok(bound<.881);
const before=await json(resolve(out,'source-hashes.json'));
for(const [p,digest]of Object.entries(before))assert.equal(await sha(resolve(base,p)),digest,p);
assert.equal(await sha(resolve(out,'movie-resolved.json')),await sha(resolve(base,'_build/movie-resolved.json')));
const events=await json(resolve(out,'mechanics-events.json'));
assert.equal(events.length,evidence.ironEvents);assert.ok(events.every(e=>e.pitch>=.8&&e.pitch<=1.3));
assert.ok(evidence.strokeLengths.every(d=>d>1.7&&d<2.3));
const result={status:'passed',checks,peak,bound,protectedFilesUnchanged:Object.keys(before),
  resolvedMovieUnchanged:true,ironEvents:events.length,strokeLengths:evidence.strokeLengths,noVideoRendered:true};
await writeFile(resolve(out,'mechanics-verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
