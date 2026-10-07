// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Audio-only auditions. Deliberately contains no film build/render command.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync, spawnSync} from 'node:child_process';
import {parseEnv} from 'node:util';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {pcmWav, keyFiles} from '/home/asa/devel/machinome/videomaker/src/speech.mjs';
const base=dirname(fileURLToPath(import.meta.url)), build=resolve(base,'../_build/auditions-1');
const input=JSON.parse(await readFile(resolve(base,'opening.json'),'utf8'));
const mode=process.argv[2];
assert.ok(process.argv.length<=3&&[undefined,'--check','--generate'].includes(mode));
const hash=value=>createHash('sha256').update(value).digest('hex');
const canonical=text=>text.replace(/\s+/gu,' ').trim();
const strip=text=>text.replace(/\[([^\]]+)\]/g,(full,tag)=>{
  assert.ok(input.tags.includes(tag),`Unknown direction: ${tag}`);return '';
});
assert.equal(canonical(strip(input.directedText)),canonical(input.text));
assert.ok(input.text.endsWith('Vou mostrar como ela funciona.'));
assert.ok(!input.text.includes('A água sob a roda'));
assert.ok(!/copyright|licen[cs]e|vibecoded|made with|created by/i.test(input.text));
assert.equal(input.voices.length,3);
assert.equal(new Set(input.voices.map(v=>v.id)).size,3);
assert.ok(input.voices.every(v=>v.locale==='pt-BR'));
const request={text:input.directedText,model_id:input.model,
  voice_settings:input.settings,seed:4217};
console.log(`Three opening-only auditions: ${canonical(input.text).length} spoken characters each; no full narration or video.`);
if(mode==='--check')process.exit(0);
await mkdir(build,{recursive:true});
let key;
async function configuredKey(){
  if(key)return key;
  key=process.env.ELEVENLABS_API_KEY;
  if(!key)for(const file of keyFiles('/home/asa/devel/machinome/videomaker')){
    try{key=parseEnv(await readFile(file,'utf8')).ELEVENLABS_API_KEY;}
    catch(error){if(error.code!=='ENOENT')throw error;}
    if(key)break;
  }
  assert.ok(key,'No configured speech key');return key;
}
async function optional(file){
  try{return JSON.parse(await readFile(file,'utf8'));}
  catch(error){if(error.code!=='ENOENT')throw error;return null;}
}
async function accountVoice(voice){
  const credential=await configuredKey();
  let response=await fetch(`https://api.elevenlabs.io/v1/voices/${voice.voice}`,
    {headers:{'xi-api-key':credential}});
  let data=await response.json();
  if(response.ok)return data.voice_id;
  assert.ok(data.detail?.status==='voice_not_found'||data.detail?.code==='voice_not_found',
    `Voice lookup HTTP ${response.status}; not retried.`);
  response=await fetch(`https://api.elevenlabs.io/v1/voices/add/${voice.owner}/${voice.voice}`,{
    method:'POST',headers:{'xi-api-key':credential,'Content-Type':'application/json'},
    body:JSON.stringify({new_name:voice.libraryName,bookmarked:true}),
  });
  data=await response.json();assert.ok(response.ok,`Voice add HTTP ${response.status}; not retried.`);
  assert.ok(data.voice_id);return data.voice_id;
}
function cleanAlignment(raw){
  if(!raw?.characters)return null;
  const ranges=[...raw.characters.join('').matchAll(/\[([^\]]+)\]/g)].map(m=>{
    assert.ok(input.tags.includes(m[1]),'Unrecognized provider tag');
    return [Array.from(raw.characters.join('').slice(0,m.index)).length,Array.from(m[0]).length];
  });
  const keep=raw.characters.map((_,i)=>!ranges.some(([a,n])=>i>=a&&i<a+n));
  return Object.fromEntries(['characters','character_start_times_seconds','character_end_times_seconds']
    .map(k=>[k,raw[k].filter((_,i)=>keep[i])]));
}
async function audition(voice){
  const identity=hash(JSON.stringify({libraryVoice:voice.voice,request,format:input.format}));
  const stem=resolve(build,voice.id+'-'+identity.slice(0,16));
  let receipt=await optional(stem+'.provider.json');
  if(!receipt){
    assert.equal(mode,'--generate',`Missing ${voice.id}; cache-only run made no request.`);
    const accountId=await accountVoice(voice),credential=await configuredKey();
    console.log(`${voice.label}: generating one directed opening.`);
    const response=await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${accountId}/with-timestamps?output_format=${input.format}`,{
      method:'POST',headers:{'xi-api-key':credential,'Content-Type':'application/json'},
      body:JSON.stringify(request),signal:AbortSignal.timeout(180000),
    });
    const body=await response.text();
    assert.ok(response.ok,`Speech HTTP ${response.status} for ${voice.id}; no automatic retry.`);
    receipt={identity,libraryVoice:voice.voice,accountVoice:accountId,request,
      generatedAt:new Date().toISOString(),requestId:response.headers.get('request-id'),
      characterCost:response.headers.get('character-cost'),body};
    await writeFile(stem+'.provider.json',JSON.stringify(receipt)+'\n',{flag:'wx'});
  }else console.log(`${voice.label}: reusing provider receipt; no paid request.`);
  assert.equal(receipt.identity,identity);
  const data=JSON.parse(receipt.body);
  assert.ok(data.audio_base64,'Successful receipt retained; missing audio requires inspection.');
  const pcm=Buffer.from(data.audio_base64,'base64'),wav=pcmWav(pcm,24000);
  const duration=pcm.length/48000;
  const alignment=[data.normalized_alignment,data.alignment].map(cleanAlignment)
    .find(a=>a&&canonical(a.characters.join(''))===canonical(input.text));
  assert.ok(alignment,'Text differs from script; receipt retained, no retry.');
  assert.equal(alignment.characters.length,alignment.character_start_times_seconds.length);
  assert.equal(alignment.characters.length,alignment.character_end_times_seconds.length);
  // Provider punctuation can extend beyond the PCM by a few milliseconds;
  // prove the final spoken character fits, and retain the raw timing as-is.
  const lastSpoken=alignment.characters.findLastIndex(c=>/[\p{L}\p{N}]/u.test(c));
  assert.ok(lastSpoken>=0&&alignment.character_end_times_seconds[lastSpoken]<=duration+.02);
  for(let i=0;i<alignment.characters.length;i++){
    assert.ok(alignment.character_start_times_seconds[i]>=0);
    assert.ok(alignment.character_end_times_seconds[i]>=alignment.character_start_times_seconds[i]);
    if(i)assert.ok(alignment.character_start_times_seconds[i]>=alignment.character_start_times_seconds[i-1]);
  }
  await writeFile(stem+'.wav',wav);
  await writeFile(resolve(build,voice.id+'.wav'),wav);
  await writeFile(stem+'.alignment.json',JSON.stringify(alignment,null,2)+'\n');
  execFileSync('ffmpeg',['-v','error','-y','-i',stem+'.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11',
    '-ar','48000','-codec:a','libmp3lame','-b:a','160k',resolve(build,voice.id+'.mp3')]);
  const silence=spawnSync('ffmpeg',['-hide_banner','-i',stem+'.wav','-af','silencedetect=noise=-42dB:d=0.15','-f','null','-'],{encoding:'utf8'});
  assert.equal(silence.status,0);
  const pauses=[...silence.stderr.matchAll(/silence_end: ([\d.]+) \| silence_duration: ([\d.]+)/g)]
    .map(m=>({start:Number(m[1])-Number(m[2]),end:Number(m[1]),duration:Number(m[2])}));
  const words=input.text.match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu).length;
  const manifest={...voice,identity,accountVoice:receipt.accountVoice,status:'awaiting pilot listening and selection',
    duration,words,wordsPerMinute:60*words/duration,sha256:hash(wav),source:'one-provider-request',
    punctuationTailOverrun:Math.max(0,alignment.character_end_times_seconds.at(-1)-duration),
    audioEdits:[],comparisonEdits:['loudness normalization and MP3 encoding only'],
    requestId:receipt.requestId,generatedAt:receipt.generatedAt,pauses,
    mp3:`../_build/auditions-1/${voice.id}.mp3`,wav:`../_build/auditions-1/${voice.id}.wav`};
  await writeFile(stem+'.json',JSON.stringify(manifest,null,2)+'\n');
  console.log(`${voice.label}: ${duration.toFixed(2)} s; ${manifest.wordsPerMinute.toFixed(0)} words/min including pauses; ${pauses.filter(p=>p.duration>=.5).length} pauses of at least 0.5 s.`);
  return manifest;
}
const queue=[...input.voices],results=[],failures=[];
async function worker(){
  while(queue.length){const voice=queue.shift();try{results.push(await audition(voice));}
    catch(error){failures.push({id:voice.id,error:error.message.replaceAll(key??'SECRET_PLACEHOLDER','[REDACTED]')});}}
}
await Promise.all([worker(),worker()]);
results.sort((a,b)=>input.voices.findIndex(v=>v.id===a.id)-input.voices.findIndex(v=>v.id===b.id));
await writeFile(resolve(build,'manifest.json'),JSON.stringify({status:'awaiting pilot approval; audio only',
  text:input.text,direction:input.directedText,voices:results,failures},null,2)+'\n');
if(failures.length){console.error(JSON.stringify(failures));process.exitCode=1;}
