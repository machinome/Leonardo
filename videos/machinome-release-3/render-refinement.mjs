// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Reuse the approved prefix; capture only the revised model-layer ending.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir,link,rename} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {randomUUID} from 'node:crypto';
import {wheelAngle,driverX} from './ending-motion.mjs';
const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'_build');
const root=resolve(build,'model-layer-refinement'),tool=resolve(process.argv[2]),viewer=resolve(process.argv[3]);
const module=async name=>import(pathToFileURL(resolve(tool,'src',name+'.mjs')));
const {loadEpisode}=await module('episode'),{browserSession}=await module('render');
const {frameAt,srt}=await module('timeline'),{speech}=await module('speech');
const {outputShotUnits}=await module('shot-cache'),{buildReviewSamplePlan}=await module('review-samples');
const {hash,fileHash,command}=await module('util');
const json=async path=>JSON.parse(await readFile(path,'utf8'));
const source=await json(resolve(root,'source-rehearsal-manifest.json'));
assert.equal(await fileHash(resolve(root,'source.mp4')),source.outputSha256);
const film=await loadEpisode(resolve(build,'movie.json')),fps=film.output.fps;
assert.deepEqual(film.output,source.episode.output,'This refinement keeps the original duration and frame grid.');
const shots=film.chapters.flatMap(c=>c.shots),open=shots.find(s=>s.id==='open-source');
const returned=shots.find(s=>s.id==='wheel-returns'),props=film.chapters[0].elements.ecosystem.props;
const first=Math.round(open.start*fps),count=Math.round(film.output.durationSeconds*fps);
const visual=f=>JSON.stringify(f,(key,value)=>key==='digest'?undefined:value);
for(let n=0;n<first;n++)assert.equal(visual(frameAt(film,n/fps)),visual(frameAt(source.episode,n/fps)),`Prefix frame request ${n} differs`);
const driveStart=open.start+open.cues.find(c=>c.actions.some(a=>a.action==='drive')).at;
for(let n=Math.round(returned.start*fps);n<=Math.round((returned.start+1.25)*fps);n++){
  const t=n/fps,frame=frameAt(film,t),actual=(frame.elements['continuous.returned'].time*1460-500)*90;
  const expected=wheelAngle(t-driveStart,props);
  assert.ok(Math.abs(actual-expected)<1e-7,`Spoke phase mismatch at ${t}`);
}
assert.equal(driverX(props.arrival,props),960);
assert.ok(1830-driverX(.25,props)<1830-driverX(.5,props));
assert.ok(driverX(1,props)-driverX(1.25,props)>1830-driverX(.25,props));
const original=await json(source.partialPatch.sourceManifest),hashes=new Map();
for(const shot of original.cache.shots){
  const indexPath=resolve(shot.generation,'index.json');
  assert.equal(await fileHash(indexPath),shot.indexSha256);
  for(const frame of (await json(indexPath)).frames)hashes.set(frame.index,frame.sha256);
}
for(const frame of (await json(source.partialPatch.captureReport)).patched)hashes.set(frame.index,frame.sha256);
const dir=resolve(root,'renders',randomUUID()),frames=resolve(dir,'frames');
await mkdir(frames,{recursive:true});
const frameName=n=>`${String(n).padStart(6,'0')}.png`;
for(let n=0;n<count;n++){
  const path=resolve(source.dir,frameName(n));
  assert.equal(await fileHash(path),hashes.get(n),`Approved source frame ${n} changed`);
  if(n<first)await link(path,resolve(frames,frameName(n)));
}
console.log(`Verified all ${count} source frames. Reusing ${first}; capturing ${count-first} from ${first/fps} s onward.`);
const captures=[];
const report=await browserSession(film,viewer,source.width,[],async({page,pose,info})=>{
  assert.equal(info.browser,source.browser);
  assert.equal(info.stage.cssSha256,source.stage.cssSha256);
  const otherAssets=h=>Object.fromEntries(Object.entries(h).filter(([key])=>key!=='/stage.js'));
  assert.deepEqual(otherAssets(info.hashes),otherAssets(source.hashes));
  const unchanged=[];
  for(const index of [101,240,1400,1991,2352,2750,3344,3518,first-1]){
    await pose(index/fps);const sha256=hash(await page.screenshot());
    assert.equal(sha256,hashes.get(index),`Untouched prefix pixels differ at ${index}`);
    unchanged.push({index,sha256});
  }
  for(let n=first;n<count;n++){
    const posed=await pose(n/fps),bytes=await page.screenshot();
    await writeFile(resolve(frames,frameName(n)),bytes);
    captures.push({index:n,time:n/fps,sha256:hash(bytes),
      motion:Object.fromEntries(Object.entries(posed.observed.elements).filter(([,e])=>e.rotation!==undefined))});
    if((n-first)%90===0)console.log(`Ending frames ${n-first+1}/${count-first}`);
  }
  return {unchanged};
});
await writeFile(resolve(dir,'captures.json'),JSON.stringify({first,count,report,captures},null,2)+'\n');
const audio=await speech(film,{generate:false});
const output=resolve(build,'rehearsal.mp4'),pending=resolve(dir,'refined.mp4');
console.log('Encoding reused prefix plus revised ending, using only cached narration.');
await command('ffmpeg',['-y','-v','error','-framerate',String(fps),'-start_number','0',
  '-i',resolve(frames,'%06d.png'),'-i',audio.mix,'-map','0:v:0','-map','1:a:0',
  '-c:a','aac','-b:a','192k','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
  '-movflags','+faststart','-t',String(film.output.durationSeconds),pending]);
const probe=JSON.parse(await command('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',pending]));
const video=probe.streams.find(s=>s.codec_type==='video');
assert.equal(Number(video.nb_read_frames),count);assert.equal(video.width,1920);assert.equal(video.height,1080);
assert.equal(video.r_frame_rate,'24/1');assert.equal(video.duration,source.probe.streams.find(s=>s.codec_type==='video').duration);
assert.equal(probe.streams.find(s=>s.codec_type==='audio').codec_name,'aac');
const outputSha256=await fileHash(pending),projectHead=(await command('git',['rev-parse','HEAD'],{cwd:base})).trim();
const projectDirty=Boolean((await command('git',['status','--porcelain'],{cwd:base})).trim());
const subtitles=resolve(build,'rehearsal.srt');await writeFile(subtitles,srt(audio.captions));
const partialPatch={schema:'leonardo-model-layer-ending/1',sourceOutputSha256:source.outputSha256,
  sourceManifest:resolve(root,'source-rehearsal-manifest.json'),sourceVideo:resolve(root,'source.mp4'),
  sourceFrameChecksumsVerified:count,prefixFrameRequestsVerified:first,reusedFrames:first,capturedFrames:count-first,
  firstFrame:first,captureReport:resolve(dir,'captures.json'),unchangedPixelChecks:report.unchanged,
  audioEdit:await json(resolve(root,'pickup-edit.json')),handoffPhaseChecks:31,
  scriptSha256:await fileHash(fileURLToPath(import.meta.url)),createdAt:new Date().toISOString()};
const {units}=outputShotUnits(film,fps);
const manifest={...source,...report,identity:hash(JSON.stringify(partialPatch)),dir:frames,count,output,outputSha256,
  reviewSamples:buildReviewSamplePlan(film,units,fps),stageSha256:report.stage.sha256,
  cache:{schema:partialPatch.schema,reusedFrames:first,capturedFrames:count-first,
    note:'Verified approved prefix plus freshly captured ending; native cache keys are not overridden.'},
  partialPatch,audio:audio.records,subtitles:{file:subtitles,sha256:await fileHash(subtitles),burnedIn:false},
  episode:film,probe,releaseReady:false,
  provenance:{...source.provenance,projectHead,projectDirty,episodeSha256:await fileHash(film.paths.episode),
    productionSha256:await fileHash(film.paths.production),stageSha256:report.stage.sha256,stageCssSha256:report.stage.cssSha256,
    note:'Mixed capture: unchanged prefix retains source manifest provenance; new ending and cached pickup use current sources.'}};
manifest.probe.format.filename=output;
await writeFile(resolve(dir,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
await rename(pending,output);
await writeFile(resolve(build,'rehearsal-manifest.json.pending'),JSON.stringify(manifest,null,2)+'\n');
await rename(resolve(build,'rehearsal-manifest.json.pending'),resolve(build,'rehearsal-manifest.json'));
console.log(`Refined cut 3: ${outputSha256}`);
