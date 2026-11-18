// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One complete provider performance. No audio cuts, splices or stretching.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';

const base = dirname(fileURLToPath(import.meta.url));
const [checkout, mode] = process.argv.slice(2);
assert.ok(checkout && (!mode || mode === '--generate'));
const tool = resolve(checkout), build = resolve(base, '_build');
const {speechCacheEntry, spokenChapters, pcmWav, keyFiles} =
  await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const {validateAlignment} = await import(pathToFileURL(resolve(tool, 'src/words.mjs')));
const {hash, fileHash} = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
const doc = JSON.parse(await readFile(resolve(build, 'movie.json'), 'utf8'));
const delivery = JSON.parse(await readFile(resolve(base, 'delivery.json'), 'utf8'));
assert.equal(doc.chapters.length, 1);
assert.equal(doc.audio.voice, 'EbiSUflQjzm4g7S895SC');
assert.equal(doc.audio.model, delivery.model);
assert.equal(doc.audio.model, 'eleven_v3', 'Pilot-fixed model; no substitution.');
assert.deepEqual(doc.audio.voiceSettings, {similarity_boost: 0.75, stability: 0.5});
const text = doc.chapters[0].narration;
const plain = s => s.replace(/\[[^\]]+\]|<break time="[0-9.]+s"\s*\/>/g, '').replace(/\s+/g, ' ').trim();
assert.equal(text, delivery.text);
assert.equal(plain(delivery.directedText), text);
assert.ok(!delivery.directedText.includes('<'), 'v3 uses inline direction, not SSML.');
assert.ok(text.startsWith('A roda faz revoluções, e os humanos dão um propósito.'));
assert.ok(text.endsWith('Uma roda, duas tarefas: cortar e avançar.'));
assert.ok(!/copyright|licen[cs]e|vibecoded|made with|created by/i.test(text));
const entry = speechCacheEntry({...doc, paths: {build}}, spokenChapters(doc), 0);
assert.equal(entry.request.text, delivery.directedText);
assert.equal(entry.format, 'pcm_24000');
await mkdir(resolve(build, 'audio'), {recursive: true});
const optional = async path => {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
};
let record = await optional(entry.meta);
if (record) {
  assert.equal(record.source, 'one complete provider performance');
  assert.equal(await fileHash(entry.file), record.sha256);
  console.log('Reusing the complete new take; no generation.');
} else {
  const receiptPath = entry.file + '.provider.json';
  let receipt = await optional(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', 'No full take cached. Use --generate once.');
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(tool)) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (error) { if (error.code !== 'ENOENT') throw error; }
      if (key) break;
    }
    assert.ok(key, 'ElevenLabs key unavailable; no request made.');
    console.log('Generating the entire directed script in one Leo performance.');
    const response = await fetch(
      'https://api.elevenlabs.io/v1/text-to-speech/' + doc.audio.voice +
      '/with-timestamps?output_format=pcm_24000', {
        method: 'POST', headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
        body: JSON.stringify(entry.request), signal: AbortSignal.timeout(240000),
      });
    const body = await response.text();
    assert.ok(response.ok, 'Speech HTTP ' + response.status + '; no automatic retry.');
    receipt = {cache: entry.cache, request: entry.request, voice: doc.audio.voice,
      requestId: response.headers.get('request-id'), generatedAt: new Date().toISOString(), body};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  }
  assert.equal(receipt.cache, entry.cache);
  const data = JSON.parse(receipt.body);
  assert.ok(data.audio_base64, 'Missing provider audio; receipt preserved.');
  const pcm = Buffer.from(data.audio_base64, 'base64');
  const wav = pcmWav(pcm, 24000);
  const original = data.normalized_alignment ?? data.alignment;
  validateAlignment(original, 'provider');
  const chars = [];
  let tagEnd = null;
  for (let i = 0; i < original.characters.length; i++) {
    const char = original.characters[i];
    if (char === '[') tagEnd = ']';
    if (char === '<') tagEnd = '>';
    if (tagEnd) { if (char === tagEnd) tagEnd = null; continue; }
    const c = {text: /\s/.test(char) ? ' ' : char,
      start: original.character_start_times_seconds[i],
      end: original.character_end_times_seconds[i]};
    if (c.text === ' ' && (!chars.length || chars.at(-1).text === ' ')) continue;
    chars.push(c);
  }
  if (chars.at(-1).text === ' ') chars.pop();
  assert.equal(chars.map(c => c.text).join(''), text, 'Provider transcript must match.');
  const duration = pcm.length / 48000;
  const lastSpoken = chars.filter(c => /[\p{L}\p{N}]/u.test(c.text)).at(-1);
  // A provider terminal estimate may extend slightly beyond the complete PCM.
  // Bound only terminal character metadata by the actual media extent;
  // preserve the provider receipt and every audio sample, with no retiming.
  assert.ok(lastSpoken.start < duration && lastSpoken.end <= duration + .1,
    'More than terminal timing uncertainty; inspect receipt before proceeding.');
  const terminalTimingBounds = chars.filter(c => c.end > duration)
    .map(c => ({...c, boundedStart: Math.min(c.start, duration), boundedEnd: duration}));
  for (const c of chars) {
    c.start = Math.min(c.start, duration);
    c.end = Math.min(c.end, duration);
  }
  const alignment = {characters: chars.map(c => c.text),
    character_start_times_seconds: chars.map(c => c.start),
    character_end_times_seconds: chars.map(c => c.end)};
  validateAlignment(alignment, 'continuous');
  record = {cache: entry.cache, voice: doc.audio.voice, model: doc.audio.model,
    format: entry.format, request: entry.request, alignment,
    sha256: hash(wav), duration, source: 'one complete provider performance',
    requestId: receipt.requestId, generatedAt: receipt.generatedAt,
    alignmentPolicy: 'original provider times; non-spoken direction tags removed',
    terminalTimingBounds,
    audioEdits: []};
  await writeFile(entry.file, wav, {flag: 'wx'});
  await writeFile(entry.meta, JSON.stringify(record, null, 2) + '\n', {flag: 'wx'});
}
await writeFile(resolve(build, 'leo-continuous.wav'), await readFile(entry.file));
await writeFile(resolve(build, 'narration-manifest.json'), JSON.stringify({
  voice: doc.audio, text, duration: record.duration, sha256: record.sha256,
  cacheFile: entry.file, source: record.source, requestId: record.requestId,
  generatedAt: record.generatedAt, audioEdits: [], listeningStatus: 'not listened to by the agent',
}, null, 2) + '\n');
console.log('Complete unedited Leo take: ' + record.duration.toFixed(2) + ' seconds.');
