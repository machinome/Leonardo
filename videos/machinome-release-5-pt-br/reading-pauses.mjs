// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Keep the new continuous Jessica performance intact; add reading silence.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,resolve,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const source=JSON.parse(await readFile(resolve(base,'auditions/proposal-12/_build/narration-manifest.json')));
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
  ['face-reveal','As relações mecânicas da máquina são descritas em Python.','Você também pode criar modelos',3],
  ['testing','verifica a geometria.','O código-fonte deste vídeo',3],
  ['behind-the-film','palavras faladas.','E aqui está o código',3],
  ['mirror','Olha que legal!','E a melhor parte',3],
].map(([shot,after,before,minimum])=>{
  const end=bounds(after)[1],next=bounds(before)[0],gap=next-end;
  assert(gap>.06,`No safe sentence gap for ${shot}`);
  // A zero crossing can be inside a syllable. Require sustained acoustic
  // silence instead, and only insert between complete sentences.
  const runs=[];let quietStart=null;
  const low=Math.ceil(Math.max(0,end-.5)*24000),high=Math.floor((next+.5)*24000);
  for(let n=low;n<=high;n++){
    const quiet=n<high&&Math.abs(wav.readInt16LE(44+n*2))<184; // below -45dBFS
    if(quiet&&quietStart===null)quietStart=n;
    if(!quiet&&quietStart!==null){
      if(n-quietStart>=.12*24000)runs.push({start:quietStart,end:n});
      quietStart=null;
    }
  }
  const middle=(end+next)/2*24000;
  runs.sort((a,b)=>Math.abs((a.start+a.end)/2-middle)-Math.abs((b.start+b.end)/2-middle));
  assert(runs.length,`No sustained acoustic silence for ${shot}; inspect before editing.`);
  const silence=runs[0],sample=Math.round((silence.start+silence.end)/2);
  assert(sample/24000>end-.5&&sample/24000<next+.5);
  // Use the measured silent interval, not the drifting provider gap.
  const acousticGap=(silence.end-silence.start)/24000;
  const samples=Math.max(0,Math.ceil((minimum+1/24-acousticGap)*24000));
  return {kind:'insert-silence',shot,after,before,minimum,originalGap:gap,
    providerEnd:end,providerNext:next,
    sample,samples,at:sample/24000,seconds:samples/24000,
    acousticSilence:{start:silence.start/24000,end:silence.end/24000,peakCeilingDb:-45},sourceSha256:source.sha256};
});
assert(holds.every((h,i)=>!i||h.sample>holds[i-1].sample));
// The provider's word clock drifts into following syllables. Correct its
// sentence boundaries to measured silence and interpolate only timestamps,
// never the waveform. Preserve these calibration points as evidence.
const calibration=[{from:0,to:0},...holds.flatMap(h=>[
  {from:h.providerEnd,to:h.acousticSilence.start},
  {from:h.providerNext,to:h.acousticSilence.end},
]),{from:alignment.character_end_times_seconds.at(-1),to:source.duration}];
assert(calibration.every((p,i)=>!i||(p.from>calibration[i-1].from&&p.to>calibration[i-1].to)));
const correct=t=>{
  const i=calibration.findIndex(p=>p.from>=t);
  if(i<=0)return i===0?calibration[0].to:t;
  const a=calibration[i-1],b=calibration[i];
  return a.to+(b.to-a.to)*(t-a.from)/(b.from-a.from);
};
const parts=[wav.subarray(0,44)];let cursor=44;
for(const h of holds){const split=44+h.sample*2;parts.push(wav.subarray(cursor,split),Buffer.alloc(h.samples*2));cursor=split;}
parts.push(wav.subarray(cursor));
// The independently transcribed ending is complete. Preserve all samples and
// give the provider's slightly late terminal timestamp space inside the WAV.
const terminalSamples=1200; // 50ms after the independently verified complete ending.
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
const pauses=holds.map(h=>({...h,voiceEnd:shift(h.acousticSilence.start),nextVoiceStart:shift(h.acousticSilence.end)}));
for(const key of ['character_start_times_seconds','character_end_times_seconds'])alignment[key]=alignment[key].map(t=>shift(correct(t)));
Object.assign(record,{sha256:hash(edited),duration:(edited.length-44)/48000,audioEdits:holds,
  alignmentCalibration:calibration,
  source:'Continuous Jessica take 12; editorial silence only at four code-scene transitions. All within-scene pauses belong to the generated performance.'});
const build=resolve(base,'_build/reading-pauses-12');await mkdir(resolve(build,'audio'),{recursive:true});
const file=resolve(build,'audio',basename(source.cacheFile));
await writeFile(file,edited);await writeFile(file+'.json',JSON.stringify(record,null,2)+'\n');
const manifest={...source,cacheFile:file,sha256:record.sha256,duration:record.duration,audioEdits:holds,
  source:record.source,sections:source.sections.map(s=>({...s,start:shift(correct(s.start)),end:shift(correct(s.end))})),
  alignmentCalibration:calibration,
  pauses,terminalSilence:terminalSamples/24000,
  alignmentWarning:'Sentence boundaries calibrated to sustained acoustic silence; in-phrase timing remains approximate. Complete ending independently verified.',
  listeningStatus:'New performance and reading pauses awaiting pilot review.'};
await writeFile(resolve(build,'narration-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const words=Object.fromEntries(['waterwheel','spin','drives','crankshaft'].map(word=>{
  const [start,end]=bounds(word);return [word,{start,end}];
}));
await writeFile(resolve(build,'relation-timing.json'),JSON.stringify({schema:'cut5-relation-timing/1',
  audioSha256:record.sha256,method:'Take 12 provider alignment calibrated and shifted at code-scene transitions only; not independent phonetic validation.',words},null,2)+'\n');
console.log(JSON.stringify({duration:record.duration,sha256:record.sha256,pauses,spokenSamplesPreserved:true},null,2));
