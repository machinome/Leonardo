// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// The concluding pullback must not move through the middle of the machine.
import assert from 'node:assert/strict';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
const tool = resolve(process.argv[2]);
const {loadEpisode} = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const {frameAt} = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const film = await loadEpisode(resolve(base, '_build/movie.json'));
const shot = film.chapters[0].shots.at(-1);
const distance = view => Math.hypot(...view.camera.map((v, i) => v - view.target[i]));
const first = frameAt(film, shot.start).elements['continuous.whole'].view;
const minimum = distance(first) * .995;
let checked = 0, nearest = Infinity;
for (let n = Math.round(shot.start * 24); n < Math.round(shot.end * 24); n++) {
  const view = frameAt(film, n / 24).elements['continuous.whole'].view;
  const actual = distance(view);
  nearest = Math.min(nearest, actual);
  assert.ok(actual >= minimum, `Closing camera approaches the machine at ${n / 24}s: ${actual} < ${minimum}`);
  checked++;
}
console.log(`Closing pullback: ${checked} frames remain outside the starting distance; minimum ${nearest.toFixed(2)}.`);
