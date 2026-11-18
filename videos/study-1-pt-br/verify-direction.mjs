// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Compare every explanatory highlight with the pilot-directed cut 5.
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
const read = async path => JSON.parse(await readFile(resolve(base, path), 'utf8'));
const original = await read('../machinome-release-5/_build/movie.json');
const study = await read('_build/movie.json');
const chapter = study.chapters[0];
const translation = {
  'the wheel turns': 'roda gira', 'this shaft': 'este eixo',
  'A crank': 'Uma manivela', 'connecting rod': 'uma biela',
  'turn that rotation': 'transformam esse giro',
  "the saw's up-and-down stroke": 'no movimento de subida e descida da serra',
  'But the timber': 'Mas a tora', 'this long lever': 'esta alavanca',
  'pulls a pawl': 'puxa uma lingueta', 'one tooth': 'um dente',
  'A second pawl': 'Uma segunda lingueta',
  'while the first returns': 'enquanto a primeira retorna',
  'winds a rope': 'enrola uma corda nesse eixo', 'Follow it': 'Siga a corda',
  'down, and across': 'para baixo e para o outro lado', 'It turns': 'Ela gira',
  'a compound shaft': 'um eixo composto', 'a broad drum': 'um tambor largo',
  'while a thinner': 'enquanto uma seção mais fina',
  'The second rope': 'A segunda corda', 'draws the timber': 'puxa a tora',
  'towards the blade': 'em direção à lâmina',
};
const anchor = value => {
  const copy = {...value};
  for (const key of ['spoken', 'spokenEnd']) if (key in copy) {
    assert.ok(translation[copy[key]], 'Unmapped source anchor: ' + copy[key]);
    copy[key] = translation[copy[key]];
  }
  return copy;
};
const highlights = shot => shot.cues.flatMap(c => c.actions
  .filter(a => a.action === 'highlight')
  .map(({element, ...a}) => ({at: c.at, until: c.until, action: a})));
const report = [];
for (const [sourceId, studyId] of [['water', 'water'], ['crank', 'stroke'],
  ['feed-motion', 'feed'], ['transmission', 'transmission'], ['consequence', 'consequence']]) {
  const source = original.chapters[0].shots.find(s => s.id === sourceId);
  const target = chapter.shots.find(s => s.id === studyId);
  const expected = highlights(source).map(c => ({...c, at: anchor(c.at), until: anchor(c.until)}));
  assert.deepEqual(highlights(target), expected, 'Highlight drift in ' + studyId);
  report.push({shot: studyId, sourceShot: sourceId, highlights: expected});
}
assert.equal(report.reduce((n, r) => n + r.highlights.length, 0), 17);
assert.ok(Object.values(chapter.elements).every(e => ['view', 'shade'].includes(e.kind)),
  'The film must contain no titles, notes, captions, or other text elements.');
assert.deepEqual(chapter.shots.find(s => s.id === 'water').transition,
  original.chapters[0].shots.find(s => s.id === 'water').transition);
assert.deepEqual(study.layers['drive-context'], original.layers['drive-context']);
const delivery = await read('delivery.json');
const opening = await read('../machinome-release-4-pt-br/auditions/opening.json');
const mechanical = await read('../machinome-release-4-pt-br/delivery.json');
const plain = s => s.replace(/\[[^\]]+\]/g, '').replace(/\s+/g, ' ').trim();
const expectedText = plain(opening.directedText + ' ' + mechanical.sectionsAfterOpening[0])
  .replace('dão a ela um propósito', 'dão um propósito');
assert.equal(chapter.narration, expectedText);
assert.equal(delivery.text, expectedText);
assert.equal(plain(await readFile(resolve(base, 'roteiro.txt'), 'utf8')), expectedText);
const manifest = await read('_build/narration-manifest.json');
assert.equal(manifest.source, 'one complete provider performance');
assert.deepEqual(manifest.audioEdits, []);
const provider = JSON.parse((await readFile(manifest.cacheFile + '.provider.json', 'utf8')));
const pcm = Buffer.from(JSON.parse(provider.body).audio_base64, 'base64');
const wav = await readFile(manifest.cacheFile);
assert.ok(wav.subarray(44).equals(pcm), 'Every provider PCM sample must survive unchanged.');
await writeFile(resolve(base, '_build/direction-comparison.json'), JSON.stringify({
  source: '../machinome-release-5/_build/movie.json',
  originalHighlights: 17, studyHighlights: 17, noText: true,
  onlyTextEdit: 'dão a ela um propósito -> dão um propósito',
  uneditedContinuousAudio: true, checks: report,
}, null, 2) + '\n');
console.log('17/17 original highlights and timing anchors restored; no text; full unedited audio.');
