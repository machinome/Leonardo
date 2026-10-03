// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify the encoded artifact and decode review frames from that MP4, not preview.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'_build');
const json=async name=>JSON.parse(await readFile(resolve(build,name)));
const digest=async path=>createHash('sha256').update(await readFile(path)).digest('hex');
const manifest=await json('rehearsal-manifest.json'),approved=await json('narration-manifest.json');
const mp4=resolve(build,'rehearsal.mp4');
assert.equal(await digest(mp4),manifest.outputSha256);
assert.equal(manifest.audio.length,1);
assert.equal(manifest.audio[0].id,'continuous');
assert.equal(manifest.audio[0].offset,3);
assert.equal(manifest.audio[0].sha256,approved.sha256);
assert.equal(await digest(manifest.audio[0].file),approved.sha256);
assert.equal(await digest(resolve(build,'approved-narration.wav')),approved.sha256);
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',mp4],{encoding:'utf8'}));
const video=probe.streams.find(s=>s.codec_type==='video'),audio=probe.streams.find(s=>s.codec_type==='audio');
assert.equal(video.width,1920);assert.equal(video.height,1080);
assert.equal(video.r_frame_rate,'24/1');assert.equal(Number(video.nb_frames),3402);
assert.equal(Number(video.duration),141.75);assert.equal(audio.codec_name,'aac');
assert.equal(probe.streams.filter(s=>s.codec_type==='subtitle').length,0);
const captions=await json('captions.json'),raw=await json('approved-captions.json');
assert.equal(captions.length,raw.length);
for(let i=0;i<raw.length;i++){
  assert.equal(captions[i].text,raw[i].text);
  assert.ok(Math.abs(captions[i].start-raw[i].start-3)<.001);
  assert.ok(Math.abs(captions[i].end-raw[i].end-3)<.001);
}
execFileSync('ffmpeg',['-v','error','-y','-i',resolve(build,'rehearsal.srt'),resolve(build,'rehearsal.vtt')]);
const directory=resolve(build,'encoded');await mkdir(directory,{recursive:true});
const times=[1,2.5,13,24,31.5,33.8,34.5,36,43.6,45,48.5,54,59,62,65,67.2,71,77,79.9,81.5,84.5,91.9,101,109.5,115,117,125.5,126.2,127.4,128.5,131.5,135,139.5,141.708333];
const indices=times.map(t=>Math.round(t*24));
const filter=indices.map(i=>`eq(n,${i})`).join('+');
execFileSync('ffmpeg',['-v','error','-y','-i',mp4,'-vf',`select='${filter}'`,'-fps_mode','vfr',resolve(directory,'frame-%02d.png')]);
const frames=[];
for(let i=0;i<indices.length;i++){
  const file=`frame-${String(i+1).padStart(2,'0')}.png`;
  frames.push({file,index:indices[i],time:indices[i]/24,sha256:await digest(resolve(directory,file))});
}
execFileSync('ffmpeg',['-v','error','-y','-i',resolve(directory,'frame-%02d.png'),'-vf','scale=320:180,tile=6x6:padding=4:margin=4:color=0x101419','-frames:v','1',resolve(directory,'overview.jpg')]);
const report={status:'decoded; visual review still required',outputSha256:manifest.outputSha256,
  video:{width:video.width,height:video.height,fps:video.r_frame_rate,frames:Number(video.nb_frames),duration:Number(video.duration)},
  audio:{codec:audio.codec_name,sampleRate:audio.sample_rate,channels:audio.channels,sourceSha256:approved.sha256,offset:3},
  captions:captions.length,frames};
await writeFile(resolve(directory,'index.json'),JSON.stringify(report,null,2)+'\n');
console.log('Encoded 1080p/24, 3402 frames, one approved take at +3 s, 51 shifted captions; 34 MP4-decoded review frames.');
