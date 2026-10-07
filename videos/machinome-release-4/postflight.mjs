// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'_build');
const json=async name=>JSON.parse(await readFile(resolve(build,name)));
const digest=async path=>createHash('sha256').update(await readFile(path)).digest('hex');
const manifest=await json('rehearsal-manifest.json'),take=await json('narration-manifest.json');
const film=await json('movie-resolved.json'),mp4=resolve(build,'rehearsal.mp4');
assert.equal(take.generation,'one-provider-request');
assert.deepEqual(take.edits,[]);
assert.equal(await digest(resolve(base,'../machinome-release-3/_build/rehearsal.mp4')),
  '9d1545e1d7142eb4b543be508fc91bcff748ce0782ad24d7982f65a8b33f2fa2','Cut 3 must remain untouched');
assert.equal(await digest(mp4),manifest.outputSha256);
assert.equal(manifest.audio.length,1);
assert.equal(manifest.audio[0].id,'continuous');
assert.equal(manifest.audio[0].offset,3);
assert.equal(manifest.audio[0].sha256,take.sha256);
assert.equal(await digest(manifest.audio[0].file),take.sha256);
assert.equal(await digest(resolve(build,'raw-narration.wav')),take.sha256);
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',mp4],{encoding:'utf8'}));
const video=probe.streams.find(s=>s.codec_type==='video'),audio=probe.streams.find(s=>s.codec_type==='audio');
assert.equal(video.width,1920);assert.equal(video.height,1080);
assert.equal(video.r_frame_rate,'24/1');
assert.equal(Number(video.nb_frames),Math.round(film.output.durationSeconds*24));
assert.ok(Math.abs(Number(video.duration)-film.output.durationSeconds)<.00001);
assert.equal(audio.codec_name,'aac');
assert.equal(probe.streams.filter(s=>s.codec_type==='subtitle').length,0);
const captions=await json('captions.json'),raw=await json('raw-captions.json');
assert.equal(captions.length,raw.length);
for(let i=0;i<raw.length;i++){
  assert.equal(captions[i].text,raw[i].text);
  assert.ok(Math.abs(captions[i].start-raw[i].start-3)<.001);
  assert.ok(Math.abs(captions[i].end-raw[i].end-3)<.001);
}
execFileSync('ffmpeg',['-v','error','-y','-i',resolve(build,'rehearsal.srt'),resolve(build,'rehearsal.vtt')]);
const directory=resolve(build,'encoded');await mkdir(directory,{recursive:true});
const inspected=await json('inspection/report.json');
try{inspected.samples.push(...(await json('inspection/ending-report.json')).samples);}
catch(error){if(error.code!=='ENOENT')throw error;}
const indices=[...new Set(inspected.samples.map(s=>Math.round(s.time*24)))].sort((a,b)=>a-b);
const filter=indices.map(i=>`eq(n,${i})`).join('+');
execFileSync('ffmpeg',['-v','error','-y','-i',mp4,'-vf',`select='${filter}'`,'-fps_mode','vfr',resolve(directory,'frame-%03d.png')]);
const frames=[];
for(let i=0;i<indices.length;i++){
  const file=`frame-${String(i+1).padStart(3,'0')}.png`;
  frames.push({file,index:indices[i],time:indices[i]/24,
    labels:inspected.samples.filter(s=>Math.round(s.time*24)===indices[i]).map(s=>s.id),
    sha256:await digest(resolve(directory,file))});
}
execFileSync('ffmpeg',['-v','error','-y','-i',resolve(directory,'frame-%03d.png'),'-vf','scale=384:216,tile=4x4:padding=4:margin=4:color=0x101419','-fps_mode','vfr',resolve(directory,'sheet-%02d.jpg')]);
const report={status:'decoded; visual and listening reviews separate',outputSha256:manifest.outputSha256,
  video:{width:video.width,height:video.height,fps:video.r_frame_rate,frames:Number(video.nb_frames),duration:Number(video.duration)},
  audio:{codec:audio.codec_name,sampleRate:audio.sample_rate,channels:audio.channels,sourceSha256:take.sha256,offset:3},
  captions:captions.length,frames};
await writeFile(resolve(directory,'index.json'),JSON.stringify(report,null,2)+'\n');
console.log(`Encoded 1080p/24, ${video.nb_frames} frames, cached Jessica narration at +3 s, ${captions.length} shifted captions; ${frames.length} MP4-decoded review frames.`);
