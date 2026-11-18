// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Recover timing against existing speech, never generate or modify its audio.
// https://elevenlabs.io/docs/api-reference/forced-alignment/create
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {parseEnv} from 'node:util';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {speechCacheEntry,spokenChapters,pcmWav,keyFiles} from '/home/asa/devel/machinome/videomaker/src/speech.mjs';
const build=resolve(dirname(fileURLToPath(import.meta.url)),'_build');
const input=JSON.parse(await readFile(resolve(build,'narration-input.json')));
const film={...input,paths:{build}},entry=speechCacheEntry(film,spokenChapters(film),0);
const source=JSON.parse(await readFile(entry.file+'.provider.json'));
const pcm=Buffer.from(JSON.parse(source.body).audio_base64,'base64'),wav=pcmWav(pcm,24000);
const hash=value=>createHash('sha256').update(value).digest('hex');
const text=input.chapters[0].narration,identity=hash(JSON.stringify({audio:hash(wav),text}));
const path=entry.file+'.forced-alignment.json';
let receipt;
try{receipt=JSON.parse(await readFile(path));}
catch(error){if(error.code!=='ENOENT')throw error;}
if(!receipt){
  assert.equal(process.argv[2],'--generate','No alignment cached; --generate authorizes one alignment request, not new speech.');
  let key=process.env.ELEVENLABS_API_KEY;
  if(!key)for(const file of keyFiles('/home/asa/devel/machinome/videomaker')){
    try{key=parseEnv(await readFile(file,'utf8')).ELEVENLABS_API_KEY;}
    catch(error){if(error.code!=='ENOENT')throw error;}
    if(key)break;
  }
  assert.ok(key,'No speech key configured');
  const form=new FormData();form.append('file',new Blob([wav],{type:'audio/wav'}),'leo-full.wav');form.append('text',text);
  const response=await fetch('https://api.elevenlabs.io/v1/forced-alignment',{
    method:'POST',headers:{'xi-api-key':key},body:form,signal:AbortSignal.timeout(240000),
  });
  const body=await response.text();
  assert.ok(response.ok,`Alignment HTTP ${response.status}; no automatic retry. Response and key omitted.`);
  receipt={identity,audioSha256:hash(wav),text,generatedAt:new Date().toISOString(),
    requestId:response.headers.get('request-id'),body};
  await writeFile(path,JSON.stringify(receipt)+'\n',{flag:'wx'});
}
assert.equal(receipt.identity,identity);
const result=JSON.parse(receipt.body);
assert.equal(result.characters.map(c=>c.text).join(''),text);
assert.ok(result.characters.every(c=>c.start>=0&&c.end>=c.start&&c.end<=pcm.length/48000+.02));
console.log(`Existing ${pcm.length/48000}s take aligned; ${result.words.length} words; final end ${result.characters.at(-1).end}s; no speech regenerated or edited.`);
