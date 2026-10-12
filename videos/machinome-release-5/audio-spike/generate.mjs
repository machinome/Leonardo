// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Anonymous text-to-audio asset authoring. Never reads credentials.
import assert from 'node:assert/strict';
import {writeFile,readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createHash} from 'node:crypto';
const run=promisify(execFile),out=resolve(process.argv[2]),kind=process.argv[3];
const manualSawPrompt='A person slowly sawing a wooden board by hand, with separate push-and-pull scrapes and quiet gaps.';
const prompts={
  hacksaw:manualSawPrompt,
  saw:manualSawPrompt,
  wheel:'Close dry recording of an iron axle slowly turning an iron crankshaft and moving a system of iron levers. Gentle intermittent iron-on-iron creaking at the moving joints, soft metallic friction under load, restrained and irregular. A manually turned mechanism. No motor, no engine, no saw, no wooden groaning. Isolated mechanical foley with no background ambience.'
};
assert.ok(prompts[kind],'Use hacksaw, saw or wheel');
const origin='https://hkchengrex-mmaudio.hf.space';
const video=process.argv[4]&&resolve(process.argv[4]);
const suffix=video?'-video':'';
const record={created:new Date().toISOString(),service:origin,endpoint:'text_to_audio',
  auth:'anonymous',paid:false,model:'large_44k_v2',prompt:prompts[kind],
  negative:kind==='wheel'?'water, rain, music, speech, traffic, birds':'music, speech, other background sounds',
  seed:kind==='hacksaw'?173:kind==='saw'?73:109,steps:25,guidance:kind==='hacksaw'?4.5:6,duration:8,status:'starting'};
if(video){record.endpoint='video_to_audio';record.duration=4;record.input=video;}
const save=()=>writeFile(resolve(out,`${kind}${suffix}-provider.json`),JSON.stringify(record,null,2)+'\n');
await save();
try{
  const data=[record.prompt,record.negative,record.seed,record.steps,record.guidance,record.duration];
  if(video){
    const upload=await run('curl',['--fail-with-body','-sS','--max-time','45',
      '-F',`files=@${video};type=video/mp4`,`${origin}/gradio_api/upload`]);
    data.unshift({path:JSON.parse(upload.stdout)[0],orig_name:'saw-conditioning.mp4',
      mime_type:'video/mp4',meta:{_type:'gradio.FileData'}});
  }
  const {stdout}=await run('curl',['--fail-with-body','-sS','--max-time','45',
    '-H','Content-Type: application/json','-d',JSON.stringify({data}),
    `${origin}/gradio_api/call/${record.endpoint}`]);
  record.eventId=JSON.parse(stdout).event_id;assert.ok(record.eventId);
  record.status='submitted';await save();console.log(`${kind}: submitted ${record.eventId}`);
  const events=await run('curl',['--fail-with-body','-sS','-N','--max-time','480',
    `${origin}/gradio_api/call/${record.endpoint}/${record.eventId}`]);
  await writeFile(resolve(out,`${kind}${suffix}-provider-events.txt`),events.stdout);
  let result;
  for(const block of events.stdout.replaceAll('\r','').split('\n\n')){
    const type=block.match(/^event: (.*)$/m)?.[1],data=block.match(/^data: (.*)$/m)?.[1];
    if(type==='error')throw Error(`Provider error: ${data}`);
    if(type==='complete')result=JSON.parse(data);
  }
  assert.ok(result?.[0]);record.result=result;
  const url=result[0].url;assert.ok(url?.startsWith(origin+'/'));
  const dest=resolve(out,`${kind}-raw.${video?'mp4':'flac'}`);
  await run('curl',['--fail','-sS','-L','--max-time','90',url,'-o',dest]);
  record.sha256=createHash('sha256').update(await readFile(dest)).digest('hex');
  record.status='complete';await save();console.log(`${kind}: downloaded ${dest}`);
}catch(e){record.status='failed';record.error=e.message;await save();throw e;}
