// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Production adapter for the already-approved pronunciation dictionary.
// Videomaker's current public speech command does not pass dictionaries.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';

const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker checkout as the first argument.');
const tool=resolve(process.argv[2]);
const {pendingMovie}=await import(pathToFileURL(resolve(tool,'src/movie.mjs')));
const {speechCacheEntry,spokenChapters,pcmWav,keyFiles}=await import(pathToFileURL(resolve(tool,'src/speech.mjs')));
const {hash,fileHash}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const {validateAlignment}=await import(pathToFileURL(resolve(tool,'src/words.mjs')));
const film=await pendingMovie(resolve(base,'_build/movie.json'));
const dictionary=JSON.parse(await readFile(resolve(base,'assets/pronunciation.json'),'utf8'));
assert.equal(dictionary.rules[0].phoneme,'məˈʃiːnoʊm');
const spoken=spokenChapters(film);
await mkdir(resolve(base,'_build/audio'),{recursive:true});

for(let i=0;i<film.chapters.length;i++) {
  const entry=speechCacheEntry(film,spoken,i);
  const request={...entry.request,pronunciation_dictionary_locators:[{
    pronunciation_dictionary_id:dictionary.id,version_id:dictionary.version_id,
  }]};
  const productionRequestHash=hash(JSON.stringify({request,voice:film.audio.voice,format:entry.format}));
  let cached;
  try {cached=JSON.parse(await readFile(entry.meta,'utf8'));}
  catch(error) {if(error.code!=='ENOENT') throw error;}
  if(cached) {
    assert.equal(cached.productionRequestHash,productionRequestHash,'Dictionary/request changed; preserve old take and choose a new production cache.');
    assert.equal(cached.sha256,await fileHash(entry.file),'Cached speech bytes changed.');
    console.log(`Reusing approved-dictionary take: ${film.chapters[i].id}`);
    continue;
  }
  let key=process.env.ELEVENLABS_API_KEY;
  if(key===undefined) for(const path of keyFiles(tool)) {
    try {key=parseEnv(await readFile(path,'utf8')).ELEVENLABS_API_KEY;}
    catch(error) {if(error.code!=='ENOENT') throw error;}
    if(key) break;
  }
  assert.ok(key,'No ElevenLabs key is configured; no speech generated.');
  console.log(`Generating Jessica narration: ${film.chapters[i].id}, ${request.text.length} characters.`);
  const response=await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(film.audio.voice)}/with-timestamps?output_format=pcm_24000`,{
    method:'POST',headers:{'xi-api-key':key,'Content-Type':'application/json'},
    body:JSON.stringify(request),signal:AbortSignal.timeout(180000),
  });
  const data=await response.json();
  assert.ok(response.ok,`Speech request failed: HTTP ${response.status}; ${data.detail?.status??'provider error'} (key omitted).`);
  assert.ok(data.audio_base64,'Provider returned no audio.');
  const pcm=Buffer.from(data.audio_base64,'base64');
  const wav=pcmWav(pcm,24000);
  const alignment=data.normalized_alignment??data.alignment;
  // Cache the paid result before downstream validation, without credentials.
  await writeFile(entry.file,wav);
  await writeFile(entry.meta,JSON.stringify({
    cache:entry.cache,voice:film.audio.voice,model:film.audio.model,
    format:entry.format,request,productionRequestHash,
    pronunciation:dictionary,alignment,sha256:hash(wav),duration:pcm.length/48000,
  },null,2)+'\n');
  validateAlignment(alignment,film.chapters[i].id);
}
