// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Keep the approved continuous Jessica performance intact; add reading silence
// after the four code scenes and put the word clock on the measured anchors.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,resolve,basename} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const source=JSON.parse(await readFile(resolve(base,'_build/audition-1/narration-manifest.json')));
const calibrationReport=JSON.parse(await readFile(resolve(base,'_build/audition-1/calibration.json')));
const record=JSON.parse(await readFile(source.cacheFile+'.json'));
const wav=await readFile(source.cacheFile),hash=b=>createHash('sha256').update(b).digest('hex');
assert.equal(hash(wav),source.sha256);
assert.equal(calibrationReport.audioSha256,source.sha256,'Calibrate this take first: calibrate.py.');
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
  ['face-reveal',"The machine's mechanical relations are described in Python.",'You can also build models',3],
  ['testing','then checks the geometry.',"This video's source code",3],
  ['behind-the-film','the spoken words.',"And here's the code",3],
  ['mirror','How cool is that?','And the best part',3],
].map(([shot,after,before,minimum])=>{
  const end=bounds(after)[1],next=bounds(before)[0];
  // The calibration already found this sentence pause in the recording.
  const boundary=calibrationReport.boundaries.find(b=>b.providerEnd===end&&b.providerNext===next);
  assert(boundary?.acousticSilence,`No measured silence after ${shot}; inspect before editing.`);
  // Insert inside sustained acoustic silence, never at a mere zero crossing
  // and never in a breath between two silences.
  const [start,stop]=boundary.acousticSilence.runs.toSorted((a,b)=>(b[1]-b[0])-(a[1]-a[0]))[0];
  assert(stop-start>=.12);
  const sample=Math.round((start+stop)/2*24000);
  for(let n=Math.round(start*24000);n<Math.round(stop*24000);n++)
    assert(Math.abs(wav.readInt16LE(44+n*2))<184,'Insertion run is not silent.');
  const acousticGap=boundary.acousticSilence.end-boundary.acousticSilence.start;
  const samples=Math.max(0,Math.ceil((minimum+1/24-acousticGap)*24000));
  return {kind:'insert-silence',shot,after,before,minimum,originalGap:next-end,
    providerEnd:end,providerNext:next,
    sample,samples,at:sample/24000,seconds:samples/24000,
    acousticSilence:{start:boundary.acousticSilence.start,end:boundary.acousticSilence.end,
      insertionRun:{start,end:stop},peakCeilingDb:-45},sourceSha256:source.sha256};
});
assert(holds.every((h,i)=>!i||h.sample>holds[i-1].sample));
// The provider's word clock drifts into following syllables. Correct it on
// the measured anchors and interpolate only timestamps, never the waveform.
const calibration=calibrationReport.points;
assert(calibration.every((p,i)=>!i||(p.from>calibration[i-1].from&&p.to>=calibration[i-1].to)));
const correct=t=>{
  const i=calibration.findIndex(p=>p.from>=t);
  if(i<=0)return i===0?calibration[0].to:calibration.at(-1).to;
  const a=calibration[i-1],b=calibration[i];
  return a.to+(b.to-a.to)*(t-a.from)/(b.from-a.from);
};
const parts=[wav.subarray(0,44)];let cursor=44;
for(const h of holds){const split=44+h.sample*2;parts.push(wav.subarray(cursor,split),Buffer.alloc(h.samples*2));cursor=split;}
parts.push(wav.subarray(cursor));
// The independently transcribed ending is complete. Preserve all samples and
// leave a breath of room after the last word inside the WAV.
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
// A sentence's last character must not outlast the pause that follows it.
for(let i=1;i<alignment.characters.length;i++)
  assert(alignment.character_start_times_seconds[i]>=alignment.character_start_times_seconds[i-1]);
Object.assign(record,{sha256:hash(edited),duration:(edited.length-44)/48000,audioEdits:holds,
  alignmentCalibration:calibration,alignmentWarning:null,
  source:'Approved continuous Jessica take; editorial silence only at four code-scene transitions. All within-scene pauses belong to the generated performance.'});
const build=resolve(base,'_build/reading-pauses');await mkdir(resolve(build,'audio'),{recursive:true});
const file=resolve(build,'audio',basename(source.cacheFile));
await writeFile(file,edited);await writeFile(file+'.json',JSON.stringify(record,null,2)+'\n');
const manifest={...source,cacheFile:file,sha256:record.sha256,duration:record.duration,audioEdits:holds,
  source:record.source,sections:source.sections.map(s=>({...s,start:shift(correct(s.start)),end:shift(correct(s.end))})),
  alignmentCalibration:calibration,
  pauses,terminalSilence:terminalSamples/24000,
  alignmentWarning:'Sentence and phrase boundaries calibrated to sustained acoustic silence; timing inside a phrase remains approximate. Complete ending independently verified.',
  listeningStatus:'Performance approved by the pilot on 17 November 2026; reading pauses follow the approved Brazilian cut.'};
await writeFile(resolve(build,'narration-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
// The film's cache holds the take it plays: this derivative, under the same
// request key. The untouched audition stays in _build/audition-1.
await mkdir(resolve(base,'_build/audio'),{recursive:true});
await writeFile(resolve(base,'_build/audio',basename(file)),edited);
await writeFile(resolve(base,'_build/audio',basename(file)+'.json'),JSON.stringify(record,null,2)+'\n');
await writeFile(resolve(base,'_build/narration-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const words=Object.fromEntries(['waterwheel','spin','drives','crankshaft'].map(word=>{
  const [start,end]=bounds(word);return [word,{start,end}];
}));
await writeFile(resolve(build,'relation-timing.json'),JSON.stringify({schema:'cut5-relation-timing/1',
  audioSha256:record.sha256,method:'Provider alignment calibrated on measured silences and shifted at code-scene transitions only; not independent phonetic validation.',words},null,2)+'\n');
console.log(JSON.stringify({duration:record.duration,sha256:record.sha256,
  pauses:pauses.map(p=>({shot:p.shot,voiceEnd:p.voiceEnd,nextVoiceStart:p.nextVoiceStart,inserted:p.seconds})),
  spokenSamplesPreserved:true},null,2));
