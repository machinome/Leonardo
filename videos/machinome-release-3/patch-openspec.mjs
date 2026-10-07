// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One bounded correction to the approved cut, not a native cache-key override.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,link,rename} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';

const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'_build');
const tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const {loadEpisode}=await import(pathToFileURL(resolve(tool,'src/episode.mjs')));
const {browserSession}=await import(pathToFileURL(resolve(tool,'src/render.mjs')));
const {command}=await import(pathToFileURL(resolve(tool,'src/util.mjs')));
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
const fileHash=async path=>digest(await readFile(path));
const json=async path=>JSON.parse(await readFile(path,'utf8'));
const manifestPath=resolve(build,'rehearsal-manifest.json');
const old=await json(manifestPath),output=resolve(build,'rehearsal.mp4');
const approved='0f0df5e37a1ec9ecc2a46f74da5de5d13c4d0b4b84a723115496bfc95b7dd6a0';
assert.equal(old.outputSha256,approved,'This patch only applies to the approved original cut 3.');
assert.equal(await fileHash(output),approved);
const originalStage=execFileSync('git',['show',`${old.provenance.projectHead}:videos/machinome-release-3/stage.jsx`],{cwd:base,encoding:'utf8'});
assert.equal(await readFile(resolve(base,'stage.jsx'),'utf8'),originalStage.replace('y={970}>{driver}','y={820}>{driver}'),
  'Only the OpenSpec baseline may differ from the approved stage.');
const film=await loadEpisode(resolve(build,'movie.json'));
for(const key of ['chapters','output','model','cameras','layers','style','audio'])
  assert.deepEqual(film[key],old.episode[key],`${key} changed beyond this correction`);
assert.equal(await fileHash(film.paths.episode),old.provenance.episodeSha256);
const fps=film.output.fps,shots=film.chapters.flatMap(c=>c.shots);
const at=shots.findIndex(s=>s.id==='open-source'),shot=shots[at],next=shots[at+1];
const drive=shot.cues.find(c=>c.actions.some(a=>a.action==='drive'));
const first=Math.round((shot.start+drive.at)*fps);
const end=Math.round((next.start+next.transition.duration)*fps);
const dir=resolve(build,'openspec-contact-patch'),frames=resolve(dir,'frames');
await mkdir(dir);await mkdir(frames);
await link(output,resolve(dir,'source.mp4'));
await writeFile(resolve(dir,'source-manifest.json'),await readFile(manifestPath));
const sourceHashes=new Map();
for(const shot of old.cache.shots){
  const indexPath=resolve(shot.generation,'index.json');
  assert.equal(await fileHash(indexPath),shot.indexSha256);
  const index=await json(indexPath);
  for(const frame of index.frames){
    const path=resolve(old.dir,frame.file);
    assert.equal(await fileHash(path),frame.sha256,`Original frame ${frame.index} was changed`);
    sourceHashes.set(frame.index,frame.sha256);
    if(frame.index<first||frame.index>=end)await link(path,resolve(frames,frame.file));
  }
}
assert.equal(sourceHashes.size,old.count);
console.log(`Reusing ${old.count-(end-first)} verified source frames; capturing only ${first}..${end-1} (${first/fps}–${end/fps} s).`);
const patched=[];
const report=await browserSession(film,viewer,old.width,[],async({page,pose,info})=>{
  assert.equal(info.browser,old.browser);
  assert.equal(info.stage.cssSha256,old.stage.cssSha256);
  const withoutStage=hashes=>Object.fromEntries(Object.entries(hashes).filter(([k])=>k!=='/stage.js'));
  assert.deepEqual(withoutStage(info.hashes),withoutStage(old.hashes),'An asset other than stage JavaScript changed');
  // Exact pixel checks outside the affected interval, including both boundaries.
  const unchanged=[];
  for(const index of [101,240,1400,2352,2750,3344,first-1,end,4260]){
    await pose(index/fps);
    const sha256=digest(await page.screenshot());
    assert.equal(sha256,sourceHashes.get(index),`Unchanged frame ${index} differs`);
    unchanged.push({index,sha256});
  }
  for(let index=first;index<end;index++){
    await pose(index/fps);
    const bytes=await page.screenshot(),sha256=digest(bytes);
    await writeFile(resolve(frames,`${String(index).padStart(6,'0')}.png`),bytes);
    patched.push({index,time:index/fps,sha256,originalSha256:sourceHashes.get(index)});
    if((index-first)%24===0)console.log(`Patched ${index-first+1}/${end-first} frames`);
  }
  return {unchanged};
});
await writeFile(resolve(dir,'capture.json'),JSON.stringify({first,end,report,patched},null,2)+'\n');
const pending=resolve(dir,'patched.mp4');
console.log('Encoding the assembled frames; copying the original AAC track without re-encoding.');
await command('ffmpeg',['-y','-v','error','-framerate',String(fps),'-start_number','0',
  '-i',resolve(frames,'%06d.png'),'-i',resolve(dir,'source.mp4'),'-map','0:v:0','-map','1:a:0',
  '-c:a','copy','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
  '-movflags','+faststart','-t',String(film.output.durationSeconds),pending]);
const probe=JSON.parse(await command('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',pending]));
const video=probe.streams.find(s=>s.codec_type==='video');
assert.equal(Number(video.nb_read_frames),old.count);
assert.equal(video.width,old.width);assert.equal(video.height,old.height);
assert.equal(video.r_frame_rate,'24/1');
assert.equal(video.duration,old.probe.streams.find(s=>s.codec_type==='video').duration);
const audioHash=async path=>(await command('ffmpeg',['-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'])).trim();
assert.equal(await audioHash(pending),await audioHash(resolve(dir,'source.mp4')));
const outputSha256=await fileHash(pending);
const projectHead=(await command('git',['rev-parse','HEAD'],{cwd:base})).trim();
const projectDirty=Boolean((await command('git',['status','--porcelain'],{cwd:base})).trim());
const partialPatch={schema:'leonardo-openspec-contact/1',reason:'Pilot requested OpenSpec above the blue line, contacting the wheel',
  sourceOutputSha256:approved,sourceManifest:resolve(dir,'source-manifest.json'),
  sourceManifestSha256:await fileHash(resolve(dir,'source-manifest.json')),
  sourceVideo:resolve(dir,'source.mp4'),sourceFrames:old.dir,
  baseline:{before:970,after:820,waterline:835},firstFrame:first,endFrameExclusive:end,
  capturedFrames:end-first,reusedFrames:old.count-(end-first),
  sourceFrameChecksumsVerified:sourceHashes.size,unchangedPixelChecks:report.unchanged,
  audioStreamSha256:await audioHash(pending),captureReport:resolve(dir,'capture.json'),
  stageSourceSha256:await fileHash(resolve(base,'stage.jsx')),
  scriptSha256:await fileHash(fileURLToPath(import.meta.url)),createdAt:new Date().toISOString()};
const manifest={...old,...report,identity:digest(JSON.stringify(partialPatch)),dir:frames,
  cache:{schema:partialPatch.schema,capturedFrames:partialPatch.capturedFrames,reusedFrames:partialPatch.reusedFrames,
    note:'Explicit project-owned partial assembly; no native shot-cache keys were overridden.'},
  partialPatch,episode:film,outputSha256,probe,stageSha256:report.stage.sha256,
  provenance:{...old.provenance,projectHead,projectDirty,stageSha256:report.stage.sha256,stageCssSha256:report.stage.cssSha256,
    note:'Mixed capture origins: unchanged frames retain the source manifest provenance; corrected frames use this stage.'}};
manifest.probe.format.filename=output;
await writeFile(resolve(dir,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
// Original MP4/manifest remain in dir if interrupted between these two renames.
await rename(pending,output);
await writeFile(manifestPath+'.pending',JSON.stringify(manifest,null,2)+'\n');
await rename(manifestPath+'.pending',manifestPath);
console.log(`Patched release-3: ${outputSha256}. Original approved film preserved under ${dir}.`);
