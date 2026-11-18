// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile, writeFile, stat, realpath} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {decodePng} from '/home/asa/devel/machinome/videomaker/src/pixels.mjs';

const here = dirname(fileURLToPath(import.meta.url)), build = resolve(here, '_build');
const hash = b => createHash('sha256').update(b).digest('hex');
const sha = async p => hash(await readFile(p));
const json = async p => JSON.parse(await readFile(p, 'utf8'));
const png = i => String(i).padStart(6, '0') + '.png';
const pixels = async name => decodePng(await readFile(resolve(build, 'frames', name))).rgb;
const manifest = await json(resolve(build, 'manifest.json'));
const r = await json(resolve(here, 'loop.json'));
assert.deepEqual(r, manifest.recipe);
assert.equal(await sha(resolve(here, 'loop.mjs')), manifest.scriptSha256);
assert.equal(await sha(resolve(here, 'loop.json')), manifest.recipeSha256);
assert.equal(await sha(manifest.output), manifest.outputSha256);
assert.equal(await sha(manifest.audio.source), r.baseMovieSha256, 'Study 1 unchanged.');
assert.equal(await sha(resolve(build, 'narration.wav')), r.baseMixSha256);
assert.equal(await sha(manifest.baseManifest), manifest.baseManifestSha256);
const prior = await json(manifest.baseManifest);
assert.equal(manifest.frameRecords.length, r.frames);
assert.equal(manifest.captured, 165); assert.equal(manifest.reused, 1985);
assert.equal(await realpath(resolve(build, 'shot-cache')),
  await realpath(resolve(here, '../study-1-pt-br/_build/shot-cache')));
for (const [i, frame] of manifest.frameRecords.entries()) {
  assert.equal(frame.index, i);
  const destination = resolve(build, 'frames', png(i));
  assert.equal(await sha(destination), frame.sha256);
  if (i >= r.openingReplacementFrames && i < r.closingStartFrame) {
    assert.equal(frame.reused, true); assert.equal(frame.sha256, prior.frames[i].sha256);
    const a = await stat(destination), b = await stat(resolve(build, 'source-frames', png(i)));
    assert.equal(a.ino, b.ino); assert.equal(a.dev, b.dev, 'Cache is linked, not copied or recaptured.');
  } else assert.equal(frame.captured, true);
}
const first = await pixels(png(0)), next = await pixels(png(1));
assert.ok(!first.equals(next), 'Wheel moves from the first frame.');
let visible = 0;
for (let i = 0; i < first.length; i += 3)
  if (first[i] !== 16 || first[i+1] !== 20 || first[i+2] !== 25) visible++;
assert.ok(visible > 50000, 'First frame cannot be a fade/blank.');
assert.ok(first.equals(await pixels('virtual-0.png')));
assert.ok(next.equals(await pixels('virtual-1.png')));
assert.ok((await pixels(png(r.frames-1))).equals(await pixels('virtual-minus-one.png')));
assert.ok(!(await pixels(png(r.frames-1))).equals(first), 'Do not duplicate the seam frame.');
const subtitle = resolve(build, 'study-2-pt-br.srt');
assert.equal(await sha(subtitle), await sha(resolve(here, '../study-1-pt-br/_build/study-1-pt-br.srt')));

const command = (name, args) => {
  const p = spawnSync(name, args, {maxBuffer: 32*1024*1024});
  assert.equal(p.status, 0, p.stderr?.toString()); return p.stdout;
};
// AAC transport bytes and decoded samples must both remain identical.
const audio = path => command('ffmpeg', ['-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-']);
const sourceAudio = audio(manifest.audio.source), finalAudio = audio(manifest.output);
assert.ok(sourceAudio.equals(finalAudio), 'Exact original AAC packets, not another encoding.');
const decoded = path => command('ffmpeg', ['-v','error','-i',path,'-map','0:a:0','-f','s16le','-']);
assert.ok(decoded(manifest.audio.source).equals(decoded(manifest.output)), 'Decoded audio must be identical too.');
const probe = JSON.parse(command('ffprobe', ['-v','error','-count_frames','-show_streams','-show_format','-of','json',manifest.output]));
const video = probe.streams.find(s=>s.codec_type==='video');
assert.equal(probe.streams.length, 2); assert.equal(video.codec_name,'h264');
assert.equal(video.width,1080); assert.equal(video.height,1920);
assert.equal(video.avg_frame_rate,'24/1'); assert.equal(Number(video.nb_read_frames),r.frames);
assert.ok(Number(probe.format.duration)<90);
assert.ok(Math.abs(Number(probe.format.duration)-r.frames/r.fps)<.001);
command('ffmpeg',['-v','error','-i',manifest.output,'-f','null','-']);
const report = {checkedAt:new Date().toISOString(),output:manifest.output,sha256:manifest.outputSha256,
  duration:Number(probe.format.duration),frames:r.frames,captured:manifest.captured,reused:manifest.reused,
  audioPacketSha256:hash(finalAudio),exactAacCopy:true,exactDecodedAudio:true,
  firstFrameVisiblePixels:visible,firstFrameMoving:true,loopContinuationPixelExact:true,
  lastFrameOneStepBeforeFirst:true,cacheHardLinksVerified:true,baseFilmUnchanged:true,
  externalSubtitlesIdentical:true,fullDecode:true};
await writeFile(resolve(build,'verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
