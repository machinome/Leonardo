// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Project-owned projection master: 4K captures, Full HD lossless-source encode.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const use=path=>import(pathToFileURL(resolve(tool,path)));
const {loadEpisode}=await use('src/episode.mjs');
const {prepareWordTimingForCommand}=await use('src/command-timing.mjs');
const {speech}=await use('src/speech.mjs');
const {render}=await use('src/render.mjs');
const {command,fileHash}=await use('src/util.mjs');
const film=await loadEpisode(resolve(base,'_build/movie.json'));
assert.equal(film.output.width,1920);
assert.equal(film.output.height,1080);
assert.equal(film.output.fps,24);
await prepareWordTimingForCommand(film,{command:'render',silent:false,fps:24});
const audio=await speech(film,{generate:false});
const approved=JSON.parse(await readFile(resolve(base,'_build/reading-pauses-12/narration-manifest.json')));
assert.equal(audio.records[0].sha256,approved.sha256);
assert.equal(await fileHash(audio.mix),
  await fileHash(resolve(base,'_build/before-projection-render/narration.wav')));
await render(film,{viewer,width:3840,fps:24,audio,label:'projection-4k'});
const capturePath=resolve(base,'_build/projection-4k-manifest.json');
const capture=JSON.parse(await readFile(capturePath));
const output=resolve(base,'_build/machinome-pythonbrasil-pt-br-fullhd-projection.mp4');
// Encode from original PNGs, never from the compressed 4K intermediate.
// Copy the approved AAC packets unchanged from the previous delivery.
const args=['-y','-v','error','-framerate','24','-start_number','0',
  '-i',resolve(capture.dir,'%06d.png'),
  '-i',resolve(base,'_build/before-projection-render/rehearsal.mp4'),
  '-map','0:v:0','-map','1:a:0','-vf','scale=1920:1080:flags=lanczos',
  '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',
  '-c:a','copy','-movflags','+faststart','-t',String(film.output.durationSeconds),output];
console.log('Encoding projection Full HD from 4K PNGs');
await command('ffmpeg',args);
const probe=JSON.parse(await command('ffprobe',
  ['-v','error','-count_frames','-show_streams','-show_format','-of','json',output]));
const video=probe.streams.find(s=>s.codec_type==='video');
assert.equal(video.width,1920);assert.equal(video.height,1080);
assert.equal(Number(video.nb_read_frames),capture.count);
assert.equal(video.r_frame_rate,'24/1');
const audioHash=async file=>(await command('ffmpeg',
  ['-v','error','-i',file,'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'])).trim();
const copiedAudio=await audioHash(output);
assert.equal(copiedAudio,await audioHash(resolve(base,'_build/before-projection-render/rehearsal.mp4')));
await writeFile(resolve(base,'_build/projection-master.json'),JSON.stringify({
  schema:'leonardo-projection-master/1',output,outputSha256:await fileHash(output),
  captureManifest:capturePath,captureManifestSha256:await fileHash(capturePath),
  sourceResolution:[3840,2160],outputResolution:[1920,1080],
  frames:capture.count,fps:24,duration:film.output.durationSeconds,
  audioPackets:copiedAudio,approvedTake:approved.sha256,ffmpegArgs:args,probe,
},null,2)+'\n');
console.log('Projection master verified: '+output);
