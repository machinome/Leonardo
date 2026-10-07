// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Preserve the approved performance and replace only its first technology name.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,copyFile,link,access} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {resolveBeats} from './speech.mjs';
const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'_build');
const tool=resolve(process.argv[2]),mode=process.argv[3];
const dir=resolve(build,'model-layer-refinement');
const {hash,fileHash,command}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const {pcmWav,keyFiles,speechCacheEntry,spokenChapters}=await import(pathToFileURL(resolve(tool,'src/speech.mjs')));
const {validateAlignment}=await import(pathToFileURL(resolve(tool,'src/words.mjs')));
const {captionsFromAlignment,srt}=await import(pathToFileURL(resolve(tool,'src/timeline.mjs')));
const json=async path=>JSON.parse(await readFile(path,'utf8'));
const exists=async path=>access(path).then(()=>true,e=>{if(e.code==='ENOENT')return false;throw e;});
if(mode==='--prepare'){
  assert.equal(await exists(dir),false,'Prepared source already exists; do not replace it.');
  const original=await json(resolve(build,'rehearsal-manifest.json'));
  assert.equal(original.outputSha256,'2be35f56bb2993b7c0d0bd2530325f56699f33e419ac3b9b5a5628553103a1c6');
  assert.equal(await fileHash(original.output),original.outputSha256);
  await mkdir(dir);
  await link(original.output,resolve(dir,'source.mp4'));
  for(const file of ['rehearsal-manifest.json','narration-manifest.json','movie.json','movie-resolved.json',
    'raw-narration.wav','raw-captions.json','captions.json','rehearsal.srt','narration.wav'])
    await copyFile(resolve(build,file),resolve(dir,'source-'+file));
  console.log('Approved cut and narration preserved for the bounded refinement.');
  process.exit(0);
}
assert.ok(!mode||mode==='--generate');
const original=await json(resolve(dir,'source-narration-manifest.json'));
const old=await json(original.cacheFile+'.json');
assert.equal(await fileHash(original.cacheFile),original.sha256);
const input=await json(resolve(build,'narration-input.json'));
assert.equal(input.chapters[0].narration,original.text.replace('Three.js','Manifold 3D'));
assert.deepEqual(input.audio,original.voice);
const request={text:'Manifold 3D, OpenSCAD, SolidPython.',model_id:input.audio.model,
  voice_settings:input.audio.voiceSettings,seed:4217};
const requestHash=hash(JSON.stringify({request,voice:input.audio.voice,format:'pcm_24000'}));
const receiptPath=resolve(dir,'pickup-provider.json');
let receipt;
if(await exists(receiptPath))receipt=await json(receiptPath);
else{
  assert.equal(mode,'--generate','No pickup cached; --generate permits one small paid request.');
  let key=process.env.ELEVENLABS_API_KEY;
  if(key===undefined)for(const path of keyFiles(tool)){
    try{key=parseEnv(await readFile(path,'utf8')).ELEVENLABS_API_KEY;}
    catch(e){if(e.code!=='ENOENT')throw e;}
    if(key)break;
  }
  assert.ok(key,'No ElevenLabs key; no request made.');
  console.log(`Generating one ${request.text.length}-character Jessica pickup; no full narration request.`);
  const response=await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${input.audio.voice}/with-timestamps?output_format=pcm_24000`,{
    method:'POST',headers:{'xi-api-key':key,'Content-Type':'application/json'},body:JSON.stringify(request),signal:AbortSignal.timeout(240000)});
  const body=await response.text();
  assert.ok(response.ok,`Pickup HTTP ${response.status}; no automatic retry.`);
  receipt={requestHash,request,voice:input.audio.voice,requestId:response.headers.get('request-id'),
    characterCost:response.headers.get('character-cost'),generatedAt:new Date().toISOString(),body};
  await writeFile(receiptPath,JSON.stringify(receipt)+'\n',{flag:'wx'});
}
assert.equal(receipt.requestHash,requestHash);
const data=JSON.parse(receipt.body),pcm=Buffer.from(data.audio_base64,'base64');
const alignment=[data.alignment,data.normalized_alignment].find(a=>a?.characters?.join('')===request.text);
assert.ok(alignment,'Pickup alignment differs; receipt retained, no new request.');
validateAlignment(alignment,'manifold-pickup');
await writeFile(resolve(dir,'pickup-full.wav'),pcmWav(pcm,24000));
const a=old.alignment,text=a.characters.join(''),i=text.indexOf('Three.js'),j=text.indexOf('OpenSCAD',i);
assert.ok(i>=0&&j>i);
const p=alignment.characters.join('').indexOf('OpenSCAD');
const startSample=Math.round((a.character_start_times_seconds[i]-.128)*24000);
const endSample=Math.round((a.character_start_times_seconds[j]-.04)*24000);
const pickupEnd=Math.round((alignment.character_start_times_seconds[p]-.04)*24000);
assert.ok(pickupEnd>0&&pickupEnd*2<=pcm.length);
const pickup=Buffer.from(pcm.subarray(0,pickupEnd*2));
// Four-millisecond edge ramps within the retained pauses avoid splice clicks.
for(let n=0;n<96;n++){
  pickup.writeInt16LE(Math.round(pickup.readInt16LE(n*2)*n/96),n*2);
  const at=pickup.length-2-n*2;
  pickup.writeInt16LE(Math.round(pickup.readInt16LE(at)*n/96),at);
}
const leading=Math.max(0,Math.round(a.character_start_times_seconds[i]*24000)-startSample);
const padding=Math.max(0,endSample-startSample-leading-pickupEnd);
const replacement=Buffer.concat([Buffer.alloc(leading*2),pickup,Buffer.alloc(padding*2)]);
const replacementSamples=replacement.length/2;
const oldWav=await readFile(original.cacheFile);
assert.equal(oldWav.toString('ascii',36,40),'data');
const oldPcm=oldWav.subarray(44);
const combined=Buffer.concat([oldPcm.subarray(0,startSample*2),replacement,oldPcm.subarray(endSample*2)]);
const delta=(replacementSamples-(endSample-startSample))/24000,start=startSample/24000;
const result={characters:[...a.characters.slice(0,i),...alignment.characters.slice(0,p),...a.characters.slice(j)]};
for(const field of ['character_start_times_seconds','character_end_times_seconds']){
  result[field]=[...a[field].slice(0,i).map(t=>Math.min(t,start)),
    ...alignment[field].slice(0,p).map(t=>t+start+leading/24000),...a[field].slice(j).map(t=>t+delta)];
}
assert.equal(result.characters.join(''),text.replace('Three.js','Manifold 3D'));
validateAlignment(result,'edited-continuous');
const wav=pcmWav(combined,24000),duration=combined.length/48000;
const entry=speechCacheEntry({...input,paths:{build}},spokenChapters(input),0);
const edit={kind:'single-name-pickup',sourceSha256:original.sha256,providerReceipt:receiptPath,
  requestHash,rawStart:start,rawEnd:endSample/24000,replacementSeconds:replacementSamples/24000,
  pickupSeconds:pickupEnd/24000,leadingSilence:leading/24000,trailingSilence:padding/24000,delta,
  sourceCharacters:'Three.js, ',replacementCharacters:'Manifold 3D, ',
  prefixPcmSha256:hash(oldPcm.subarray(0,startSample*2)),suffixPcmSha256:hash(oldPcm.subarray(endSample*2)),
  edgeRampSeconds:.004,timeStretch:false};
assert.equal(hash(combined.subarray(0,startSample*2)),edit.prefixPcmSha256);
assert.equal(hash(combined.subarray((startSample+replacementSamples)*2)),edit.suffixPcmSha256);
const record={cache:entry.cache,voice:input.audio.voice,model:input.audio.model,format:entry.format,
  request:entry.request,alignment:result,sha256:hash(wav),duration,source:'approved-performance-with-single-name-pickup',edits:[edit]};
await writeFile(entry.file,wav);
await writeFile(entry.meta,JSON.stringify(record,null,2)+'\n');
const captions=captionsFromAlignment(result),beats=resolveBeats(result,input.beats,duration);
const manifest={...original,status:'pickup-awaiting-listening-review',sourceSha256:await fileHash(resolve(base,'narration.py')),
  text:input.chapters[0].narration,characters:input.chapters[0].narration.length,
  generation:record.source,edits:[edit],duration,sha256:record.sha256,cacheFile:entry.file,
  originalProviderRequestId:original.providerRequestId,providerRequestId:receipt.requestId,
  generatedAt:receipt.generatedAt,productionRequestHash:requestHash,captions:captions.length,beats};
await writeFile(resolve(build,'narration-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
await writeFile(resolve(build,'raw-narration.wav'),wav);
await writeFile(resolve(build,'raw-captions.json'),JSON.stringify(captions,null,2)+'\n');
await writeFile(resolve(build,'raw-captions.srt'),srt(captions));
await writeFile(resolve(dir,'pickup-edit.json'),JSON.stringify(edit,null,2)+'\n');
console.log(`Replaced only Three.js: ${edit.replacementSeconds.toFixed(3)} s pickup, duration delta ${delta.toFixed(3)} s; all other source PCM preserved.`);
