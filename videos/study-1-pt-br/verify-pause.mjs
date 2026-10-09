// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Independent checks on the files produced by pause-transition.mjs.
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), build = resolve(here, '_build');
const out = resolve(build, 'zoom-pause');
const tool = resolve(process.argv[2] ?? '/home/asa/devel/machinome/videomaker');
const {decodePng} = await import(pathToFileURL(resolve(tool, 'src/pixels.mjs')));
const json = async p => JSON.parse(await readFile(p, 'utf8'));
const hash = b => createHash('sha256').update(b).digest('hex');
const sha = async p => hash(await readFile(p));
const png = i => String(i).padStart(6, '0') + '.png';
const report = await json(resolve(out, 'manifest.json'));
const base = await json(report.baseManifest);
assert.equal(await sha(report.baseManifest), report.baseManifestSha256);
assert.equal(await sha(base.output), report.baseMovieSha256);
assert.equal(await sha(report.output), report.outputSha256);
assert.equal(await sha(resolve(here, 'pause-transition.mjs')), report.scriptSha256);
assert.equal(await sha(base.audio[0].file), report.approvedRawAudioSha256);

function pcm(wav) {
  for (let p = 12; p < wav.length;) {
    const size = wav.readUInt32LE(p + 4);
    if (wav.toString('ascii', p, p + 4) === 'data') return wav.subarray(p + 8, p + 8 + size);
    p += size + 8 + size % 2;
  }
  throw new Error('No PCM chunk.');
}
const original = await readFile(resolve(build, 'narration.wav'));
const revised = await readFile(resolve(out, 'narration.wav'));
assert.equal(hash(original), report.sourceMixSha256); assert.equal(hash(revised), report.mixSha256);
const a = pcm(original), b = pcm(revised), cut = 1708000 * 4, added = 96000 * 4;
assert.equal(b.length, a.length + added);
assert.ok(a.subarray(0, cut).equals(b.subarray(0, cut)));
assert.ok(a.subarray(cut).equals(b.subarray(cut + added)));
assert.ok(b.subarray(cut, cut + added).every(x => x === 0));

const baseFrames = new Map();
for (const shot of base.cache.shots) {
  assert.equal(await sha(resolve(shot.generation, 'index.json')), shot.indexSha256);
  const index = await json(resolve(shot.generation, 'index.json'));
  for (const f of index.frames) baseFrames.set(f.index, {...f, path: resolve(shot.generation, f.file)});
}
assert.equal(report.frames.length, 2150);
assert.equal(report.capturedFrames, 98); assert.equal(report.reusedFrames, 2052);
for (const [i, f] of report.frames.entries()) {
  assert.equal(f.index, i);
  assert.equal(await sha(resolve(out, 'frames', png(i))), f.sha256);
  if (i < 854 || i >= 952) {
    assert.equal(f.baseIndex, i < 854 ? i : i - 48);
    assert.equal(f.sha256, baseFrames.get(f.baseIndex).sha256);
  } else assert.equal(f.captured, true);
}
const pixels = async p => decodePng(await readFile(p)).rgb;
assert.ok((await pixels(resolve(out, 'frames', png(854)))).equals(await pixels(baseFrames.get(854).path)),
  'Entry must match the original image pixel for pixel.');
assert.ok((await pixels(resolve(out, 'join-check.png'))).equals(await pixels(baseFrames.get(904).path)),
  'End of replacement must match the original cached image pixel for pixel.');
const settled = await pixels(resolve(out, 'frames', png(892)));
for (let i = 893; i <= 902; i++) assert.ok(settled.equals(await pixels(resolve(out, 'frames', png(i)))),
  'Both camera and model must hold after zoom and before motion.');
assert.ok(!settled.equals(await pixels(resolve(out, 'frames', png(910)))), 'Model must resume moving.');

function silenceAt(path, at) {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', path,
    '-af', 'silencedetect=noise=-45dB:d=0.1', '-f', 'null', '-'], {encoding: 'utf8'});
  assert.equal(r.status, 0, r.stderr);
  const starts = [...r.stderr.matchAll(/silence_start: ([\d.]+)/g)].map(x => +x[1]);
  const ends = [...r.stderr.matchAll(/silence_end: ([\d.]+)/g)].map(x => +x[1]);
  const index = starts.findIndex((s, i) => s <= at && ends[i] >= at);
  assert.ok(index >= 0, 'Insertion must be in detected silence.');
  return {start: starts[index], end: ends[index], duration: ends[index] - starts[index]};
}
const before = silenceAt(resolve(build, 'narration.wav'), 854 / 24);
const after = silenceAt(resolve(out, 'narration.wav'), 854 / 24);
assert.equal(before.start, after.start);
assert.ok(Math.abs(after.end - before.end - 2) < .001);
assert.ok(after.end > report.timing.motionResumes);
assert.ok(report.timing.zoomEnds < report.timing.motionResumes);
const oldCaptions = await json(resolve(build, 'captions.json'));
const newCaptions = await json(resolve(out, 'captions.json'));
assert.equal(oldCaptions.length, newCaptions.length);
for (const [i, c] of oldCaptions.entries()) {
  assert.equal(newCaptions[i].text, c.text);
  const shift = c.start >= 854 / 24 ? 2 : 0;
  assert.equal(newCaptions[i].start, c.start + shift);
  assert.equal(newCaptions[i].end, c.end + shift);
}
const probe = spawnSync('ffprobe', ['-v', 'error', '-show_streams', '-show_format', '-of', 'json', report.output], {encoding: 'utf8'});
assert.equal(probe.status, 0, probe.stderr);
const media = JSON.parse(probe.stdout), v = media.streams.find(s => s.codec_type === 'video');
assert.equal(Number(v.nb_frames), 2150); assert.equal(v.width, 1080); assert.equal(v.height, 1920);
assert.equal(v.avg_frame_rate, '24/1'); assert.equal(media.streams.length, 2);
assert.ok(Number(media.format.duration) < 90);
const decode = spawnSync('ffmpeg', ['-v', 'error', '-i', report.output, '-f', 'null', '-'], {encoding: 'utf8'});
assert.equal(decode.status, 0, decode.stderr);
const verification = {output: report.output, sha256: report.outputSha256,
  duration: Number(media.format.duration), frames: 2150, captured: 98, reused: 2052,
  originalPcmSamplesPreserved: true, insertedSilenceSeconds: 2,
  measuredSilenceBefore: before, measuredSilenceAfter: after,
  exactPixelJoins: true, settledFramesPixelIdentical: [892, 902],
  fullDecode: true, captionWordsUnchanged: true, checkedAt: new Date().toISOString()};
await writeFile(resolve(out, 'verification.json'), JSON.stringify(verification, null, 2) + '\n');
console.log(JSON.stringify(verification, null, 2));
