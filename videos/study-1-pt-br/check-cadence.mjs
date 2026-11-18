// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Read-only audio acceptance evidence against the pilot-approved calm take.
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
const read = async p => JSON.parse(await readFile(p, 'utf8'));
const manifest = await read(resolve(base, process.argv[2] ?? '_build/narration-manifest.json'));
assert.equal(manifest.voice.model, 'eleven_v3', 'The model is fixed by the pilot.');
assert.equal(manifest.voice.voice, 'EbiSUflQjzm4g7S895SC', 'Keep Leo.');
const reference = await read(resolve(base,
  '_build/revisions/before-2026-10-09-direction/narration-manifest.json'));
const detector = 'silencedetect=noise=-40dB:d=0.15';
const inspect = async m => {
  const record = await read(m.cacheFile + '.json');
  const pcm = Buffer.from(JSON.parse((await read(m.cacheFile + '.provider.json')).body).audio_base64, 'base64');
  assert.ok((await readFile(m.cacheFile)).subarray(44).equals(pcm));
  return measure(m, record);
};
const measure = async (m, record) => {
  record ??= await read(m.cacheFile + '.json');
  // FFmpeg diagnostics are captured, not sent to the console.
  const {spawnSync} = await import('node:child_process');
  const r = spawnSync('ffmpeg', ['-hide_banner', '-i', m.cacheFile, '-af', detector, '-f', 'null', '-'], {encoding: 'utf8'});
  assert.equal(r.status, 0, r.stderr);
  const pauses = [...r.stderr.matchAll(/silence_duration: ([\d.]+)/g)].map(m => Number(m[1]));
  const a = record.alignment, text = a.characters.join('');
  const at = phrase => {
    const i = text.indexOf(phrase);
    assert.ok(i >= 0 && text.lastIndexOf(phrase) === i, 'Unique phrase: ' + phrase);
    return a.character_start_times_seconds[i];
  };
  const anchors = ['A roda', 'Há cinco séculos', 'Máquinas como', 'Eu também',
    'Vou mostrar', 'A água sob', 'Uma manivela', 'Mas a tora', 'Durante o corte',
    'Uma segunda lingueta', 'Esse pequeno passo', 'Siga a corda', 'Ela gira',
    'A segunda corda', 'Uma roda,'];
  return {duration: m.duration, sha256: m.sha256, cacheFile: m.cacheFile,
    silenceSeconds: pauses.reduce((a, b) => a + b, 0), pauseCount: pauses.length,
    onsets: Object.fromEntries(anchors.map(p => [p, at(p)]))};
};
const actual = await inspect(manifest), original = await measure(reference);
const sections = [
  ['História e apresentação', 'Há cinco séculos', 'A água sob'],
  ['Roda e biela', 'A água sob', 'Mas a tora'],
  ['Linguetas e catraca', 'Mas a tora', 'Esse pequeno passo'],
  ['Transmissão pelas cordas', 'Esse pequeno passo', 'Uma roda,'],
].map(([name, from, to]) => {
  const seconds = actual.onsets[to] - actual.onsets[from];
  const referenceSeconds = original.onsets[to] - original.onsets[from];
  return {name, seconds, referenceSeconds, ratio: seconds / referenceSeconds};
});
const failures = [];
// The pilot specifies a 90-second target and a hard maximum, not a minimum.
// Keep the earlier 86-second heuristic visible as a target warning, while
// retaining the speech, pauses and per-mechanism tests unchanged.
const warnings = [];
if (actual.duration > 90) failures.push('The whole take must not exceed 90 seconds.');
if (actual.duration < 86) warnings.push('Below the internal 86-second target band; disclose actual duration.');
if (actual.silenceSeconds < 24) failures.push('Observation pauses must total at least 24 s, compared with 28.17 s in the reference.');
const voicedRatio = (actual.duration - actual.silenceSeconds) /
  (original.duration - original.silenceSeconds);
if (voicedRatio < .94) failures.push('Non-silent speech is too compressed versus the original; pauses alone do not fix rushed articulation.');
for (const s of sections) if (s.ratio < .90) failures.push(s.name + ': more than 10% shorter than the approved reference.');
const report = {status: failures.length ? 'rejected' : warnings.length ? 'timing-passed-with-target-warning' : 'timing-passed', detector,
  note: 'Timing and sample integrity only; not an auditory or emotion judgement.',
  original, actual, voicedRatio, sections, failures, warnings};
await writeFile(resolve(base, '_build/cadence-check.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
assert.deepEqual(failures, [], 'Do not deliver or render a failed take.');
