// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {test} from 'node:test';
import {verifyInput, resolveBeats} from './speech.mjs';

const input = JSON.parse(await readFile(new URL('./_build/narration-input.json', import.meta.url), 'utf8'));

test('exactly one performance, with the reviewed opening, entrance, list and closing', () => {
  const text = verifyInput(input);
  assert.ok(text.startsWith('The wheel makes revolutions, and humans give it a purpose.'));
  for (const phrase of [
    'From Machinome dot node import...',
    'This is Machinome, the open source CAD framework for building machines...',
    'The waterwheel spin drives the crankshaft.',
    'This is all open source! OpenSCAD, SolidPython, OCCT, CadQuery, Build123d, FreeCAD, JSCAD and so many others...',
    "The wheel makes revolutions, and humans build their own. I'm Machinome.",
  ]) assert.ok(text.includes(phrase), phrase);
  assert.ok(text.endsWith('What do you want to build next?'));
  assert.ok(text.indexOf("This video's source code") < text.indexOf("And here's the code of this exact scene"));
});

test('splitting into a second synthesis chapter is refused', () => {
  assert.throws(() => verifyInput({...input, chapters: [...input.chapters, input.chapters[0]]}), /one take/);
});

test('repeated wheel phrases require their unique opening/closing context', () => {
  assert.throws(() => verifyInput({...input, beats: [{id: 'ambiguous', phrase: 'The wheel makes revolutions'}]}), /ambiguous/);
});

test('all anchors resolve on one clock, including the final word', () => {
  const characters = Array.from(input.chapters[0].narration);
  const alignment = {characters,
    character_start_times_seconds: characters.map((_, i) => i / 100),
    character_end_times_seconds: characters.map((_, i) => (i + 1) / 100)};
  const beats = resolveBeats(alignment, input.beats, characters.length / 100);
  assert.equal(beats.length, 29);
  assert.equal(beats[0].start, 0);
  for (let i = 1; i < beats.length; i++) assert.ok(beats[i].start > beats[i - 1].start);
  assert.throws(() => resolveBeats(alignment, [{id: 'absent', phrase: 'No such line'}], 100), /missing/);
  assert.throws(() => resolveBeats(alignment, input.beats, 1));
});
