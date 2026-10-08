// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Recover the actual original Leo recording; never synthesize new speech.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const base = dirname(fileURLToPath(import.meta.url));
const [checkout] = process.argv.slice(2);
assert.ok(checkout);
const tool = resolve(checkout), build = resolve(base, '_build');
const {speechCacheEntry, spokenChapters, pcmWav} =
  await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const {validateAlignment} = await import(pathToFileURL(resolve(tool, 'src/words.mjs')));
const {hash, fileHash} = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
const doc = JSON.parse(await readFile(resolve(build, 'movie.json'), 'utf8'));
const delivery = JSON.parse(await readFile(resolve(base, 'delivery.json'), 'utf8'));
const source = JSON.parse(await readFile(resolve(base, delivery.sourceReceipt), 'utf8'));
assert.equal(doc.chapters.length, 1);
assert.equal(source.voice, 'EbiSUflQjzm4g7S895SC');
assert.equal(doc.audio.voice, source.voice);
const text = doc.chapters[0].narration;
const plain = s => s.replace(/\[[^\]]+\]/g, '').replace(/\s+/g, ' ').trim();
assert.equal(text, delivery.text);
assert.equal(plain(delivery.directedText), text);
assert.ok(text.endsWith('Uma roda, duas tarefas: cortar e avançar.'));
assert.ok(!/copyright|licen[cs]e|vibecoded|made with|created by/i.test(text));
assert.ok(source.request.text.startsWith(delivery.directedText),
  'The original recording must contain the exact directed script as its prefix.');
const fullText = plain(source.request.text);
const data = JSON.parse(source.body);
const originalPCM = Buffer.from(data.audio_base64, 'base64');
const originalWAV = pcmWav(originalPCM, 24000);
await mkdir(resolve(build, 'audio'), {recursive: true});
const optional = async path => {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
};
// Retain the original provider timestamps, removing only non-spoken tags.
// No API access, retiming, or new synthesis is needed to recover this take.
const originalAlignment = data.normalized_alignment ?? data.alignment;
validateAlignment(originalAlignment, 'original Leo');
assert.equal(originalAlignment.characters.join(''), source.request.text);
const characters = [];
let inTag = false;
for (let i = 0; i < originalAlignment.characters.length; i++) {
  const char = originalAlignment.characters[i];
  if (char === '[') inTag = true;
  if (inTag) { if (char === ']') inTag = false; continue; }
  const c = {text: /\s/.test(char) ? ' ' : char,
    start: originalAlignment.character_start_times_seconds[i],
    end: originalAlignment.character_end_times_seconds[i]};
  if (c.text === ' ' && (!characters.length || characters.at(-1).text === ' ')) continue;
  characters.push(c);
}
if (characters.at(-1).text === ' ') characters.pop();
const aligned = {characters};
assert.equal(aligned.characters.map(c => c.text).join(''), fullText);
assert.ok(fullText.startsWith(text + ' Para reconstruir'));
const count = Array.from(text).length;
assert.ok(aligned.characters.every(c => Array.from(c.text).length === 1));
const selected = aligned.characters.slice(0, count);
assert.equal(selected.map(c => c.text).join(''), text);
const spokenEnd = selected.filter(c => /[\p{L}\p{N}]/u.test(c.text)).at(-1).end;
const nextStart = aligned.characters.slice(count).find(c => /[\p{L}\p{N}]/u.test(c.text)).start;
assert.ok(nextStart > spokenEnd + .15, 'No clear pause at the requested end.');
// Cut within the original natural pause. All samples before it stay identical.
const cut = Math.min(spokenEnd + .75, (spokenEnd + nextStart) / 2);
const endSample = Math.floor(cut * 24000);
const pcm = originalPCM.subarray(0, endSample * 2), wav = pcmWav(pcm, 24000);
const alignment = {characters: selected.map(c => c.text),
  character_start_times_seconds: selected.map(c => c.start),
  character_end_times_seconds: selected.map(c => c.end)};
validateAlignment(alignment, 'continuous');
const entry = speechCacheEntry({...doc, paths: {build}}, spokenChapters(doc), 0);
const record = {cache: entry.cache, voice: doc.audio.voice, model: doc.audio.model,
  format: entry.format, request: entry.request, alignment, sha256: hash(wav),
  duration: pcm.length / 48000, source: 'sample-exact excerpt of the original cut-4 Leo take',
  sourceReceipt: delivery.sourceReceipt, sourceRequestId: source.requestId,
  sourceAudioSha256: hash(originalWAV), sourceGeneratedAt: source.generatedAt,
  alignmentSource: 'original provider timestamps; non-spoken tags removed',
  excerpt: {startSample: 0, endSample, sampleRate: 24000,
    spokenEnd, nextSentenceStart: nextStart}, speechGenerated: false};
const previous = await optional(entry.meta);
if (previous) {
  assert.equal(previous.sha256, record.sha256);
  assert.equal(await fileHash(entry.file), record.sha256);
} else {
  await writeFile(entry.file, wav, {flag: 'wx'});
  await writeFile(entry.meta, JSON.stringify(record, null, 2) + '\n', {flag: 'wx'});
}
await writeFile(resolve(build, 'leo-original.wav'), wav);
await writeFile(resolve(build, 'narration-manifest.json'), JSON.stringify({
  voice: doc.audio.voice, text, duration: record.duration, sha256: record.sha256,
  cacheFile: entry.file, source: record.source, sourceRequestId: source.requestId,
  originalDuration: originalPCM.length / 48000, excerpt: record.excerpt,
  speechGenerated: false, audioEdits: ['End cut in the natural pause before Para reconstruir'],
  listeningStatus: 'not listened to by the agent',
}, null, 2) + '\n');
console.log('Original Leo excerpt: ' + record.duration.toFixed(2) +
  ' seconds; every spoken word restored, original PCM preserved.');
