// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Local editorial revision of the approved film, not a new voice generation.
// Keep the base film/cache immutable; replace only the mechanism entrance.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir, link, copyFile, access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const build = resolve(here, '_build'), out = resolve(build, 'zoom-pause');
const tool = resolve(process.argv[2] ?? '/home/asa/devel/machinome/videomaker');
const viewer = resolve(process.argv[3] ?? '/home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js');
const checkOnly = process.argv.includes('--check');
const {loadEpisode} = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const {frameAt, reframeAt} = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const {browserSession} = await import(pathToFileURL(resolve(tool, 'src/render.mjs')));
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const sha = async file => digest(await readFile(file));
const json = async file => JSON.parse(await readFile(file, 'utf8'));
const save = (name, data) => writeFile(resolve(out, name), JSON.stringify(data, null, 2) + '\n');
const pngName = i => String(i).padStart(6, '0') + '.png';
const command = (name, args) => new Promise((done, fail) => {
  const p = spawn(name, args), chunks = [], errors = [];
  p.stdout.on('data', x => chunks.push(x)); p.stderr.on('data', x => errors.push(x));
  p.on('error', fail); p.on('close', code => code === 0 ? done(Buffer.concat(chunks).toString())
    : fail(new Error(`${name} exited ${code}: ${Buffer.concat(errors)}`)));
});

const fps = 24, insert = 854, added = 48, resumeBase = 904, count = 2150;
const start = insert / fps, seconds = added / fps, end = resumeBase + added;
const zoomFrames = 38; // 1.583 s zoom, then 0.417 s stationary before motion.
const approvedMovie = '1ef4847a8ea0246a4ad38275008bfa22bbf774ab6fd6e042eb5a043e53812d28';
const approvedVoice = 'f237b17e6bc5be12732a8bab81c684bad52903f4212c555cb79bfcac7b582ec6';
const manifest = await json(resolve(build, 'rehearsal-manifest.json'));
assert.equal(manifest.outputSha256, approvedMovie, 'Wrong base film; do not adapt a rejected take.');
assert.equal(await sha(manifest.output), approvedMovie);
assert.equal(await sha(resolve(build, 'movie.json')), manifest.provenance.episodeSha256);
assert.equal(await sha(manifest.audio[0].file), approvedVoice);
const film = await loadEpisode(resolve(build, 'movie.json'));
assert.equal(film.output.fps, fps);
assert.equal(Math.round(film.output.durationSeconds * fps), count - added);
assert.ok(count / fps < 90);

// Insert zeros in PCM silence only. All original samples, including breaths
// and room tone, retain their order, level and sample rate. No time stretching.
const sourceMix = await readFile(resolve(build, 'narration.wav'));
assert.equal(sourceMix.toString('ascii', 0, 4), 'RIFF');
let dataOffset, dataLength, rate, block;
for (let p = 12; p < sourceMix.length;) {
  const size = sourceMix.readUInt32LE(p + 4), kind = sourceMix.toString('ascii', p, p + 4);
  if (kind === 'fmt ') {
    assert.equal(sourceMix.readUInt16LE(p + 8), 1, 'PCM only');
    assert.equal(sourceMix.readUInt16LE(p + 10), 2);
    rate = sourceMix.readUInt32LE(p + 12); block = sourceMix.readUInt16LE(p + 20);
    assert.equal(sourceMix.readUInt16LE(p + 22), 16);
  }
  if (kind === 'data') { dataOffset = p + 8; dataLength = size; }
  p += 8 + size + size % 2;
}
assert.equal(rate, 48000); assert.equal(block, 4);
assert.equal(dataLength / block, Math.round((count - added) / fps * rate));
const cutSample = Math.round(start * rate), cut = dataOffset + cutSample * block;
// Both sides are below -70 dBFS, so inserting zero introduces no audible edge.
for (let p = cut - block; p < cut + block; p += 2) assert.ok(Math.abs(sourceMix.readInt16LE(p)) <= 8);
const silenceBytes = seconds * rate * block;
const padded = Buffer.concat([sourceMix.subarray(0, cut), Buffer.alloc(silenceBytes), sourceMix.subarray(cut)]);
padded.writeUInt32LE(sourceMix.readUInt32LE(4) + silenceBytes, 4);
padded.writeUInt32LE(dataLength + silenceBytes, dataOffset - 4);
assert.ok(padded.subarray(dataOffset, cut).equals(sourceMix.subarray(dataOffset, cut)));
assert.ok(padded.subarray(cut + silenceBytes).equals(sourceMix.subarray(cut)));
assert.ok(padded.subarray(cut, cut + silenceBytes).every(x => x === 0));

const captions = await json(resolve(build, 'captions.json'));
const shifted = captions.map(c => {
  assert.ok(c.end <= start || c.start >= start, 'Never split a caption/phrase at the insertion.');
  return c.start >= start ? {...c, start: c.start + seconds, end: c.end + seconds} : c;
});
const water = film.chapters[0].shots.find(s => s.id === 'water');
const held = frameAt(film, start).elements['continuous.mill'];
const crank = film.cameras.crank;
const smooth = x => x * x * (3 - 2 * x);

function editedFrame(i) {
  const oldTime = Math.max(start, (i - added) / fps);
  const old = frameAt(film, oldTime);
  const f = structuredClone(frameAt(film, Math.max(water.start, oldTime)));
  const elapsed = (i - insert) / fps;
  const w = smooth(Math.min(1, (i - insert) / zoomFrames));
  const mix = (a, b) => a.map((v, k) => v + (b[k] - v) * w);
  const camera = {camera: mix(held.view.camera, crank.position), target: mix(held.view.target, crank.target)};
  const poseTime = old.elements['continuous.mill'].time;
  for (const [key, state] of Object.entries(f.elements)) if (state.kind === 'view') {
    state.view = structuredClone(camera); state.time = poseTime;
    state.up = [...held.up]; state.fov = held.fov;
    state.highlight = old.elements[key]?.highlight ?? null;
    state.marks = old.elements[key]?.marks ?? [];
  }
  f.time = i / fps;
  f.transition = elapsed < water.transition.duration ? reframeAt(film, 'water', elapsed) : null;
  if (f.transition) f.transition.start = start;
  return f;
}

if (!checkOnly) await mkdir(resolve(out, 'frames'), {recursive: true});
const baseFrames = new Map();
for (const shot of manifest.cache.shots) {
  assert.equal(await sha(resolve(shot.generation, 'index.json')), shot.indexSha256);
  const index = await json(resolve(shot.generation, 'index.json'));
  assert.equal(index.width, 1080); assert.equal(index.height, 1920);
  for (const frame of index.frames) baseFrames.set(frame.index, {...frame, path: resolve(shot.generation, frame.file)});
}
assert.equal(baseFrames.size, count - added);
const frames = [], checks = [];
const report = await browserSession(film, viewer, 1080, [], async ({page, pose, info}) => {
  assert.equal(info.browser, manifest.browser);
  assert.equal(info.stage.sha256, manifest.stage.sha256);
  assert.deepEqual(info.hashes, manifest.hashes, 'Same stage, viewer and model assets are required for reuse.');
  for (let i = insert; i <= end; i++) {
    const f = editedFrame(i), views = Object.values(f.elements).filter(e => e.kind === 'view');
    for (const state of views) {
      assert.deepEqual(state.view, views[0].view); assert.equal(state.time, views[0].time);
      if (i <= insert + added) assert.equal(state.time, held.time, 'Hold every moving part through zoom/settle.');
      if (i >= insert + zoomFrames) assert.deepEqual(state.view, {camera: crank.position, target: crank.target});
    }
    if (i === end) {
      const base = frameAt(film, resumeBase / fps);
      assert.deepEqual(f.elements, base.elements, 'Exact camera, phase, highlights and visibility at cache join.');
      assert.deepEqual(f.slots, base.slots); assert.equal(f.transition, base.transition);
    }
    if (i < end) checks.push({index: i, time: i / fps, modelTime: views[0].time,
      camera: views[0].view, fade: f.transition?.progress ?? 1,
      highlight: f.elements['continuous.detail'].highlight});
  }
  console.log(`Timing and continuity pass: ${seconds}s silence; ${end - insert} replacement frames; ${count - (end - insert)} reused.`);
  if (checkOnly) return {checks};
  for (let i = 0; i < count; i++) {
    const path = resolve(out, 'frames', pngName(i));
    if (i < insert || i >= end) {
      const oldIndex = i < insert ? i : i - added, source = baseFrames.get(oldIndex);
      const bytes = await readFile(source.path);
      assert.equal(digest(bytes), source.sha256, `Base PNG ${oldIndex} changed.`);
      assert.equal(bytes.readUInt32BE(16), 1080); assert.equal(bytes.readUInt32BE(20), 1920);
      try { await link(source.path, path); } catch (e) {
        if (e.code !== 'EEXIST') throw e;
        assert.equal(await sha(path), source.sha256);
      }
      frames.push({index: i, baseIndex: oldIndex, sha256: source.sha256});
    } else {
      // Each new image is posed through the tool's normal checked browser.
      const f = editedFrame(i);
      await pose(Math.max(water.start, (i - added) / fps), f);
      assert.equal(await page.locator('.portrait').textContent(), '');
      const bytes = await page.screenshot(); await writeFile(path, bytes);
      frames.push({index: i, captured: true, sha256: digest(bytes)});
      if ((i - insert) % 24 === 0) console.log(`Transition captured ${i - insert + 1}/${end - insert}`);
    }
  }
  // Capture the exact join state independently, not just a mathematical check.
  await pose(resumeBase / fps, editedFrame(end));
  const endpoint = await page.screenshot();
  await writeFile(resolve(out, 'join-check.png'), endpoint);
  return {checks, join: {index: end, baseIndex: resumeBase, sha256: digest(endpoint),
    sourceSha256: baseFrames.get(resumeBase).sha256}};
});
if (checkOnly) { console.log('Check only: no voice call, frame capture, encoding or delivery changes.'); process.exit(0); }

await writeFile(resolve(out, 'narration.wav'), padded);
await save('captions.json', shifted);
const stamp = t => {
  const ms = Math.round(t * 1000), pad = (n, width = 2) => String(n).padStart(width, '0');
  return `${pad(Math.floor(ms / 3600000))}:${pad(Math.floor(ms / 60000) % 60)}:${pad(Math.floor(ms / 1000) % 60)},${pad(ms % 1000, 3)}`;
};
await writeFile(resolve(out, 'study-1-pt-br.srt'), shifted.map((c, i) =>
  `${i + 1}\n${stamp(c.start)} --> ${stamp(c.end)}\n${c.text}\n`).join('\n'));
const output = resolve(out, 'study-1-pt-br.mp4');
console.log('Encoding revised film from lossless frames and sample-preserved audio.');
await command('ffmpeg', ['-y', '-v', 'error', '-framerate', String(fps), '-start_number', '0',
  '-i', resolve(out, 'frames/%06d.png'), '-i', resolve(out, 'narration.wav'),
  '-map', '0:v:0', '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
  '-movflags', '+faststart', '-t', String(count / fps), output]);
const probe = JSON.parse(await command('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', output]));
const video = probe.streams.find(s => s.codec_type === 'video');
assert.equal(probe.streams.length, 2); assert.equal(video.codec_name, 'h264');
assert.equal(video.width, 1080); assert.equal(video.height, 1920);
assert.equal(video.avg_frame_rate, '24/1'); assert.equal(Number(video.nb_read_frames), count);
assert.equal(probe.streams.find(s => s.codec_type === 'audio').codec_name, 'aac');
assert.ok(Math.abs(Number(probe.format.duration) - count / fps) < .001);
assert.ok(Number(probe.format.duration) < 90);
await command('ffmpeg', ['-v', 'error', '-i', output, '-f', 'null', '-']);
await save('manifest.json', {schema: 'leonardo-local-pause-edit/1', created: new Date().toISOString(),
  scriptSha256: await sha(fileURLToPath(import.meta.url)), baseManifest: resolve(build, 'rehearsal-manifest.json'),
  baseManifestSha256: await sha(resolve(build, 'rehearsal-manifest.json')), baseMovieSha256: approvedMovie,
  approvedRawAudioSha256: approvedVoice, sourceMixSha256: digest(sourceMix), mixSha256: digest(padded),
  audioEdit: {kind: 'insert-silence', atSample: cutSample, sampleRate: rate, addedSamples: seconds * rate,
    seconds, originalSamplesPreserved: true, speedChanged: false, speechGenerated: false},
  timing: {start, zoomEnds: (insert + zoomFrames) / fps, motionResumes: (insert + added) / fps,
    detectedSpeechResumes: 35.53721 + .6 + seconds, duration: count / fps},
  output, outputSha256: await sha(output), count, fps, capturedFrames: end - insert,
  reusedFrames: frames.filter(f => !f.captured).length, fullDecode: true,
  subtitlesBurnedIn: false, frames, capture: report, probe});
console.log(JSON.stringify({output, duration: count / fps, captured: end - insert,
  reused: frames.filter(f => !f.captured).length, sha256: await sha(output)}, null, 2));
console.log('Staged only. Inspect the encoded transition before copying to the delivery path.');
