// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Keep the new continuous Jessica performance intact; add reading silence.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,resolve,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const source=JSON.parse(await readFile(resolve(base,'auditions/proposal-10/_build/narration-manifest.json')));
const record=JSON.parse(await readFile(source.cacheFile+'.json'));
const wav=await readFile(source.cacheFile),hash=b=>createHash('sha256').update(b).digest('hex');
assert.equal(hash(wav),source.sha256);
assert.equal(wav.toString('ascii',36,40),'data');
assert.equal(wav.readUInt32LE(24),24000);
assert.equal(wav.readUInt16LE(22),1);
assert.equal(wav.readUInt16LE(34),16);
const alignment=record.alignment,text=alignment.characters.join('');
assert.equal(text,source.text);
const bounds=phrase=>{
  const i=text.indexOf(phrase);
  assert(i>=0&&text.indexOf(phrase,i+1)<0,`Ambiguous phrase: ${phrase}`);
  const first=Array.from(text.slice(0,i)).length,last=first+Array.from(phrase).length-1;
  return [alignment.character_start_times_seconds[first],alignment.character_end_times_seconds[last]];
};
const holds=[
  ['ancestor','minhas ancestrais.','Vou mostrar como ela funciona!',3],
  ['face-reveal','As relações mecânicas da máquina são descritas em Python.','Você também pode criar modelos',5],
  ['studio-chat','seus agentes,','vê o código-fonte',1.3],
  ['studio-code','vê o código-fonte,','constrói o projeto',1.3],
  ['studio-build','constrói o projeto','e interage com o modelo',1.3],
  ['studio-angle','diferentes ângulos','e momentos',1.3],
  ['testing','verifica a geometria.','O código-fonte deste vídeo',5],
  ['behind-the-film','palavras faladas.','E aqui está o código',5],
  ['mirror','Olha que legal!','E a melhor parte',5],
].map(([shot,after,before,minimum])=>{
  const end=bounds(after)[1],next=bounds(before)[0],gap=next-end;
  assert(gap>.06,`No safe sentence gap for ${shot}`);
  // One output-frame margin ensures rounding never shortens the requested hold.
  const samples=Math.max(0,Math.ceil((minimum+1/24-gap)*24000));
  let sample=Math.round((end+next)/2*24000);
  for(let n=Math.ceil((end+gap*.3)*24000);n<Math.floor((next-gap*.3)*24000);n++)
    if(Math.abs(wav.readInt16LE(44+n*2))<Math.abs(wav.readInt16LE(44+sample*2)))sample=n;
  assert(Math.abs(wav.readInt16LE(44+sample*2))<64,`Sentence gap is not quiet: ${shot}`);
  return {kind:'insert-silence',shot,after,before,minimum,originalGap:gap,
    sample,samples,at:sample/24000,seconds:samples/24000,sourceSha256:source.sha256};
});
assert(holds.every((h,i)=>!i||h.sample>holds[i-1].sample));
const parts=[wav.subarray(0,44)];let cursor=44;
for(const h of holds){const split=44+h.sample*2;parts.push(wav.subarray(cursor,split),Buffer.alloc(h.samples*2));cursor=split;}
parts.push(wav.subarray(cursor));
// The independently transcribed ending is complete. Preserve all samples and
// give the provider's slightly late terminal timestamp space inside the WAV.
const terminalSamples=Math.max(0,Math.ceil((alignment.character_end_times_seconds.at(-1)-source.duration+.05)*24000));
parts.push(Buffer.alloc(terminalSamples*2));const edited=Buffer.concat(parts);
edited.writeUInt32LE(edited.length-8,4);edited.writeUInt32LE(edited.length-44,40);
// Removing only inserted zero samples must reproduce every original PCM byte.
let originalCursor=44,editedCursor=44;
for(const h of holds){const length=44+h.sample*2-originalCursor;
  assert(edited.subarray(editedCursor,editedCursor+length).equals(wav.subarray(originalCursor,originalCursor+length)));
  originalCursor+=length;editedCursor+=length+h.samples*2;
}
assert(edited.subarray(editedCursor,edited.length-terminalSamples*2).equals(wav.subarray(originalCursor)));
const shift=t=>t+holds.filter(h=>t>=h.at).reduce((sum,h)=>sum+h.seconds,0);
const pauses=holds.map(h=>({...h,voiceEnd:shift(bounds(h.after)[1]),nextVoiceStart:shift(bounds(h.before)[0])}));
for(const key of ['character_start_times_seconds','character_end_times_seconds'])alignment[key]=alignment[key].map(shift);
Object.assign(record,{sha256:hash(edited),duration:(edited.length-44)/48000,audioEdits:holds,
  source:'Continuous Jessica take 10 plus documented reading silences; no voice stretching or phrase replacement.'});
const build=resolve(base,'_build/reading-pauses');await mkdir(resolve(build,'audio'),{recursive:true});
const file=resolve(build,'audio',basename(source.cacheFile));
await writeFile(file,edited);await writeFile(file+'.json',JSON.stringify(record,null,2)+'\n');
const manifest={...source,cacheFile:file,sha256:record.sha256,duration:record.duration,audioEdits:holds,
  source:record.source,sections:source.sections.map(s=>({...s,start:shift(s.start),end:shift(s.end)})),
  pauses,terminalSilence:terminalSamples/24000,
  alignmentWarning:'Provider end timestamps are approximate; complete ending independently verified. Terminal silence accommodates the late timestamp without altering speech.',
  listeningStatus:'New performance and reading pauses awaiting pilot review.'};
await writeFile(resolve(build,'narration-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const words=Object.fromEntries(['waterwheel','spin','drives','crankshaft'].map(word=>{
  const [start,end]=bounds(word);return [word,{start,end}];
}));
await writeFile(resolve(build,'relation-timing.json'),JSON.stringify({schema:'cut5-relation-timing/1',
  audioSha256:record.sha256,method:'Take 10 provider alignment shifted by documented reading silences; not independent phonetic validation.',words},null,2)+'\n');
console.log(JSON.stringify({duration:record.duration,sha256:record.sha256,pauses,spokenSamplesPreserved:true},null,2));
