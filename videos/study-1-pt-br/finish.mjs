// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Measured continuity and the portrait opening orbit; no speech generation.
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker checkout.');
const tool = resolve(process.argv[2]);
const {readMovie, resolveMovie} = await import(pathToFileURL(resolve(tool, 'src/movie.mjs')));
const {cachedTake} = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const file = resolve(base, '_build/movie.json');
const {doc, build} = await readMovie(file);
const take = await cachedTake({audio: doc.audio, chapters: doc.chapters, paths: {build}}, 0);
assert.ok(take, 'Run speech first; this command never purchases audio.');
const measured = resolveMovie(doc, {continuous: take});
const chapter = doc.chapters[0];
// The faint assembly provides context at exactly the mechanism's camera.
for (const shot of chapter.shots) {
  if (!shot.places.ghost) continue;
  for (const cue of shot.cues) {
    for (const action of [...cue.actions]) {
      if (action.action === 'move' && action.element !== 'mill')
        cue.actions.push({...action, element: 'ghost'});
    }
  }
}
const feed = measured.chapters[0].shots.find(s => s.id === 'feed');
const clock = t => t <= feed.start ? 400 + 32 * t / feed.start :
  440 + (t - feed.end) * .65;
for (const [i, shot] of chapter.shots.entries()) {
  if (shot.id === 'feed') continue; // Keep the spoken pull/return phase keys.
  const timing = measured.chapters[0].shots[i];
  shot.model = {from: clock(timing.start), to: clock(timing.end)};
}
const ancestor = chapter.shots.find(s => s.id === 'ancestor');
const timing = measured.chapters[0].shots.find(s => s.id === 'ancestor');
const orbit = ancestor.cues.find(c => c.actions.some(a => a.action === 'move'));
assert.ok(orbit && typeof orbit.at === 'object', 'Run on a fresh movie evaluation.');
const timedOrbit = timing.cues.find(c => c.actions.some(a => a.action === 'move'));
const start = timedOrbit.at, end = timedOrbit.actions[0].until;
ancestor.cues = ancestor.cues.filter(c => c !== orbit);
// One smooth arc goes around the machine rather than through its centre.
for (let i = 1; i <= 120; i++) {
  const u = i / 120, p = u * u * u * (10 + u * (-15 + 6 * u));
  const theta = -Math.PI / 2 + 3 * Math.PI / 4 * p;
  const radius = 710 + (Math.hypot(1320, 1320) - 710) * p + 600 * Math.sin(Math.PI * p);
  const name = `portrait-orbit-${String(i).padStart(3, '0')}`;
  doc.cameras[name] = {position: [radius * Math.cos(theta), radius * Math.sin(theta),
    120 + 850 * p + 180 * Math.sin(Math.PI * p)],
    target: [0, -151 * (1 - p), 120 + 165 * p], up: [0, 0, 1], fov: 37};
  if (i === 120) doc.cameras[name] = structuredClone(doc.cameras.rear);
  ancestor.cues.push({at: start + (end - start) * (i - 1) / 120,
    actions: [{element: 'mill', action: 'move', camera: name, ease: 'linear',
      until: start + (end - start) * u}]});
}
// Preserve the closing cameras and timing, but pull back around the model.
// A straight Cartesian interpolation crosses its centre and creates a zoom.
const closing = chapter.shots.find(s => s.id === 'two-jobs');
const closingTime = measured.chapters[0].shots.find(s => s.id === 'two-jobs');
const closingMove = closing.cues.find(c => c.actions.some(a => a.action === 'move'));
const closingEnd = closingTime.cues[0].actions[0].until;
closing.cues = closing.cues.filter(c => c !== closingMove);
const from = doc.cameras.carriage, to = doc.cameras.wide;
const relative = camera => camera.position.map((v, i) => v - camera.target[i]);
const a = relative(from), b = relative(to);
const angle = Math.atan2(a[1], a[0]);
const turn = Math.atan2(Math.sin(Math.atan2(b[1], b[0]) - angle),
  Math.cos(Math.atan2(b[1], b[0]) - angle));
for (let i = 1; i <= 120; i++) {
  const u = i / 120, p = u * u * u * (10 + u * (-15 + 6 * u));
  const target = from.target.map((v, k) => v + (to.target[k] - v) * p);
  const radius = Math.hypot(a[0], a[1]) * (1 - p) + Math.hypot(b[0], b[1]) * p;
  const theta = angle + turn * p;
  const name = `portrait-closing-${String(i).padStart(3, '0')}`;
  doc.cameras[name] = {position: [target[0] + radius * Math.cos(theta),
    target[1] + radius * Math.sin(theta), target[2] + a[2] * (1 - p) + b[2] * p],
    target, up: from.up, fov: from.fov};
  if (i === 120) doc.cameras[name] = structuredClone(to);
  closing.cues.push({at: closingEnd * (i - 1) / 120,
    actions: [{element: 'whole', action: 'move', camera: name, ease: 'linear',
      until: closingEnd * u}]});
}
await writeFile(file, JSON.stringify(doc, null, 2) + '\n');
console.log('Continuous model clock and portrait orbit fitted to the cached Leo take.');
