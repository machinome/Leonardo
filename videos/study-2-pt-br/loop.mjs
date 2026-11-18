// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Study 2: a cache-preserving visual loop over the exact approved soundtrack.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir, link, symlink, realpath, copyFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url)), build = resolve(here, '_build');
const recipe = JSON.parse(await readFile(resolve(here, 'loop.json'), 'utf8'));
const base = resolve(here, recipe.base), priorBuild = resolve(base, '_build');
const tool = '/home/asa/devel/machinome/videomaker';
const viewer = '/home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js';
const {loadEpisode} = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const {frameAt} = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const {browserSession} = await import(pathToFileURL(resolve(tool, 'src/render.mjs')));
const {decodePng} = await import(pathToFileURL(resolve(tool, 'src/pixels.mjs')));
const preview = process.argv.includes('--preview');
const hash = b => createHash('sha256').update(b).digest('hex');
const sha = async p => hash(await readFile(p));
const json = async p => JSON.parse(await readFile(p, 'utf8'));
const png = i => String(i).padStart(6, '0') + '.png';
const save = (p, data) => writeFile(p, JSON.stringify(data, null, 2) + '\n');
const scriptSha256 = await sha(fileURLToPath(import.meta.url));
const recipeSha256 = await sha(resolve(here, 'loop.json'));
const run = (name, args) => new Promise((done, fail) => {
  const p = spawn(name, args), output = [], errors = [];
  p.stdout.on('data', x => output.push(x)); p.stderr.on('data', x => errors.push(x));
  p.on('error', fail); p.on('close', code => code === 0 ? done(Buffer.concat(output))
    : fail(new Error(`${name} exited ${code}: ${Buffer.concat(errors)}`)));
});
await mkdir(build, {recursive: true});
for (const [name, target] of Object.entries({
  'shot-cache': '../../study-1-pt-br/_build/shot-cache',
  'source-frames': '../../study-1-pt-br/_build/zoom-pause/frames',
  audio: '../../study-1-pt-br/_build/audio',
  'narration.wav': '../../study-1-pt-br/_build/zoom-pause/narration.wav',
  'captions.json': '../../study-1-pt-br/_build/zoom-pause/captions.json',
})) {
  try { await symlink(target, resolve(build, name)); } catch (e) { if (e.code !== 'EEXIST') throw e; }
  assert.equal(await realpath(resolve(build, name)), await realpath(resolve(build, target)));
}
const sourceMovie = resolve(priorBuild, 'study-1-pt-br.mp4');
const prior = await json(resolve(priorBuild, 'zoom-pause/manifest.json'));
const native = await json(resolve(priorBuild, 'rehearsal-manifest.json'));
assert.equal(await sha(sourceMovie), recipe.baseMovieSha256);
assert.equal(prior.outputSha256, recipe.baseMovieSha256);
assert.equal(await sha(resolve(build, 'narration.wav')), recipe.baseMixSha256);
assert.equal(prior.frames.length, recipe.frames);
assert.equal(await sha(resolve(priorBuild, 'movie.json')), native.provenance.episodeSha256);
const doc = await json(resolve(priorBuild, 'movie.json'));
// Resolve all generated files into the NEW build directory. Stage is read-only.
doc.root = '..';
for (const entry of Object.values(doc.stage.sets)) entry.module = '../study-1-pt-br/' + entry.module;
for (const entry of Object.values(doc.stage.elements)) entry.module = '../study-1-pt-br/' + entry.module;
doc.stage.modules = doc.stage.modules.map(p => '../study-1-pt-br/' + p);
doc.evidence.direction = '../study-1-pt-br/README.md';
doc.release.descriptionTemplate = 'description.md';
await save(resolve(build, 'base-movie.json'), doc);
const film = await loadEpisode(resolve(build, 'base-movie.json'));
const {fps, frames: count, closingStartFrame: closingStart} = recipe;
const first = film.chapters[0].shots[0], closing = film.chapters[0].shots.at(-1);
assert.equal(closingStart, Math.round(closing.start * fps) + 48);
const rate = (first.model.to - first.model.from) / (first.end - first.start);
const initial = frameAt(film, 0).elements['continuous.wheel'];
const from = frameAt(film, closing.start).elements['continuous.whole'];
const modelDuration = film.model.expectedDurationSeconds;
const finalModel = recipe.closingEndModelSeconds;
assert.equal((finalModel - first.model.from) % recipe.wheelPeriodModelSeconds, 0);
const closingFrames = count - closingStart, linearAt = (closingFrames - recipe.constantTailFrames) / fps;
const y0 = closing.model.from, y1 = finalModel - rate * recipe.constantTailFrames / fps;
const initialRate = (closing.model.to - y0) / (closing.end - closing.start);
const smooth = u => u * u * (3 - 2 * u);
const smoother = u => u * u * u * (10 + u * (-15 + 6 * u));
function modelSeconds(local) {
  if (local >= linearAt) return finalModel + rate * (local - closingFrames / fps);
  const u = local / linearAt;
  return (2*u**3 - 3*u**2 + 1)*y0 + (u**3 - 2*u**2 + u)*linearAt*initialRate
    + (-2*u**3 + 3*u**2)*y1 + (u**3 - u**2)*linearAt*rate;
}
function cameraAt(i) {
  const u = Math.min(1, i / recipe.cameraMoveFrames), p = smoother(u);
  if (u === 1) return structuredClone(initial.view);
  const a = from.view.camera.map((v, k) => v - from.view.target[k]);
  const b = initial.view.camera.map((v, k) => v - initial.view.target[k]);
  const angle = Math.atan2(a[1], a[0]);
  const turn = Math.atan2(Math.sin(Math.atan2(b[1], b[0]) - angle), Math.cos(Math.atan2(b[1], b[0]) - angle));
  const target = from.view.target.map((v, k) => v + (initial.view.target[k] - v) * p);
  const radius = Math.hypot(a[0], a[1]) * (1-p) + Math.hypot(b[0], b[1]) * p;
  return {camera: [target[0] + radius*Math.cos(angle + turn*p),
    target[1] + radius*Math.sin(angle + turn*p), target[2] + a[2]*(1-p) + b[2]*p], target};
}
function directedFrame(i) {
  if (i < recipe.openingReplacementFrames) {
    const f = structuredClone(frameAt(film, i / fps)); f.transition = null; return f;
  }
  const local = i - closingStart;
  const f = structuredClone(frameAt(film, closing.start));
  f.time = i / fps; f.transition = null;
  const state = f.elements['continuous.whole'];
  state.view = cameraAt(local); state.time = modelSeconds(local / fps) / modelDuration;
  const outgoing = structuredClone(f);
  const u = Math.max(0, Math.min(1, (local - recipe.backgroundFadeStartFrame)
    / (recipe.backgroundFadeEndFrame - recipe.backgroundFadeStartFrame)));
  if (u > 0) state.hidden = structuredClone(initial.hidden);
  if (u > 0 && u < 1) f.transition = {kind: 'dissolve', progress: smooth(u), outgoing};
  return f;
}
// Pure continuity gates: no stopped/reversed wheel, and no catch-up at the seam.
for (let i = 0; i < closingFrames; i++) assert.ok(modelSeconds((i+1)/fps) > modelSeconds(i/fps));
for (let i = closingFrames - recipe.constantTailFrames; i < closingFrames; i++)
  assert.ok(Math.abs(modelSeconds((i+1)/fps) - modelSeconds(i/fps) - rate/fps) < 1e-10);
assert.deepEqual(cameraAt(closingFrames), initial.view);
assert.equal(modelSeconds(closingFrames / fps), finalModel);
const destination = resolve(build, preview ? 'preview' : 'frames');
await mkdir(destination, {recursive: true});
const samples = new Set([0, 1, 11, 12, 194, 854, 952, 1200, 1900,
  ...[0, 24, 48, 60, 84, 108, 126, 135, 151, 152].map(i => closingStart + i)]);
const selected = preview ? [...samples].sort((a,b) => a-b) : Array.from({length: count}, (_, i) => i);
const frameRecords = [], pixelProofs = [];
const capture = await browserSession(film, viewer, 1080, [], async ({page, pose, info}) => {
  assert.equal(info.browser, native.browser);
  assert.deepEqual(info.hashes, native.hashes, 'Cache reuse requires unchanged stage, model, viewer and page.');
  for (const i of selected) {
    const changed = i < recipe.openingReplacementFrames || i >= closingStart;
    const path = resolve(destination, png(i));
    if (!changed) {
      const source = resolve(build, 'source-frames', png(i)), bytes = await readFile(source);
      assert.equal(hash(bytes), prior.frames[i].sha256);
      assert.equal(bytes.readUInt32BE(16), 1080); assert.equal(bytes.readUInt32BE(20), 1920);
      try { await link(source, path); } catch (e) {
        if (e.code !== 'EEXIST') throw e;
        assert.equal(await sha(path), prior.frames[i].sha256);
      }
      frameRecords.push({index: i, reused: true, sha256: hash(bytes)});
    } else {
      await pose(i < 12 ? i/fps : closing.start, directedFrame(i));
      assert.equal(await page.locator('.portrait').textContent(), '');
      const bytes = await page.screenshot(); await writeFile(path, bytes);
      frameRecords.push({index: i, captured: true, sha256: hash(bytes)});
      if (i % 24 === 0 || i === closingStart) console.log(`Captured loop frame ${i}/${count}`);
    }
  }
  // Prove the branch into the unchanged opening and the start of the new tail.
  for (const [i, f, baseTime] of [[12, {...frameAt(film, .5), transition: null}, .5],
    [closingStart, directedFrame(closingStart), closing.start]]) {
    await pose(baseTime, f);
    const actual = decodePng(await page.screenshot()).rgb;
    const expected = decodePng(await readFile(resolve(build, 'source-frames', png(i)))).rgb;
    assert.ok(actual.equals(expected), `Exact base join at ${i}`);
    pixelProofs.push({kind: 'base-join', index: i, exact: true});
  }
  // Continuing the closing clock must draw opening frames 0 and 1 exactly.
  for (const i of [0, 1]) {
    const f = directedFrame(count + i);
    await pose(closing.start, f);
    const bytes = await page.screenshot();
    await writeFile(resolve(destination, `virtual-${i}.png`), bytes);
    assert.ok(decodePng(bytes).rgb.equals(decodePng(await readFile(resolve(destination, png(i)))).rgb),
      `Loop continuation differs at opening frame ${i}.`);
    pixelProofs.push({kind: 'loop-continuation', index: i, exact: true});
  }
  // Last-to-first is a normal step, not an extra held frame.
  const before = directedFrame(0); before.elements['continuous.wheel'].time = (first.model.from - rate/fps) / modelDuration;
  await pose(0, before);
  const beforeBytes = await page.screenshot();
  await writeFile(resolve(destination, 'virtual-minus-one.png'), beforeBytes);
  assert.ok(decodePng(beforeBytes).rgb.equals(decodePng(await readFile(resolve(destination, png(count-1)))).rgb));
  assert.notEqual(await sha(resolve(destination, png(0))), await sha(resolve(destination, png(1))));
  pixelProofs.push({kind: 'last-is-one-step-before-first', exact: true});
  return {pixelProofs};
});
await save(resolve(build, preview ? 'preview-report.json' : 'capture.json'), {recipe, rate, frameRecords, capture});
if (preview) { console.log('Preview and exact loop pixel proofs passed.'); process.exit(0); }
const output = resolve(build, 'study-2-pt-br.mp4');
console.log('Encoding new picture; copying the original AAC packets unchanged.');
await run('ffmpeg', ['-y','-v','error','-framerate',String(fps),'-i',resolve(destination,'%06d.png'),
  '-i',sourceMovie,'-map','0:v:0','-map','1:a:0','-c:a','copy','-c:v','libx264','-preset','medium',
  '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-t',String(count/fps),output]);
await copyFile(resolve(priorBuild,'study-1-pt-br.srt'),resolve(build,'study-2-pt-br.srt'));
assert.equal(await sha(sourceMovie), recipe.baseMovieSha256, 'Study 1 must remain unchanged.');
await save(resolve(build,'manifest.json'), {schema:'leonardo-loop-edit/1',created:new Date().toISOString(),
  output,outputSha256:await sha(output),recipe,scriptSha256,recipeSha256,
  baseManifest:resolve(priorBuild,'zoom-pause/manifest.json'),baseManifestSha256:await sha(resolve(priorBuild,'zoom-pause/manifest.json')),
  audio:{mode:'AAC stream copy',source:sourceMovie,mixSha256:recipe.baseMixSha256},
  count,fps,duration:count/fps,captured:frameRecords.filter(f=>f.captured).length,
  reused:frameRecords.filter(f=>f.reused).length,frameRecords,capture,
  note:'Local unpublished edit; inherited reconstruction and public-URL limitations remain.'});
console.log(JSON.stringify({output,duration:count/fps,captured:165,reused:1985,sha256:await sha(output)},null,2));
