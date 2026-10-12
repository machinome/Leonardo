// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Full-film audition: one provider request, untouched PCM, no retries.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';

const base = dirname(fileURLToPath(import.meta.url));
const [checkout, mode] = process.argv.slice(2);
assert.ok(checkout && (!mode || ['--check', '--generate'].includes(mode)));
const tool = resolve(checkout), build = resolve(base, '_build');
const {speechCacheEntry, spokenChapters, pcmWav, keyFiles} =
  await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const {hash, fileHash} = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
const {validateAlignment} = await import(pathToFileURL(resolve(tool, 'src/words.mjs')));
const {captionsFromAlignment, srt} = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const delivery = JSON.parse(await readFile(resolve(base, 'delivery.json'), 'utf8'));
const plain = s => s.replace(/\[[^\]]+\]/g, '').replace(/\s+/g, ' ').trim();
const directedText = delivery.sections.map(s => s.directedText).join('\n\n');
const text = plain(directedText);
assert.ok(directedText.length <= 5000, 'One v3 request must fit the validated limit.');
assert.ok(!/<|em português:|in Portuguese:/i.test(directedText));
assert.ok(!/copyright|vibecoded|created by|\b(?:AGPL|GPL|CERN-OHL)\b/i.test(text));
for (const line of ['From Machinome dot node dot assembly import AssemblyNode.',
  'The waterwheel spin drives the crankshaft.']) assert.ok(text.includes(line));
assert.equal(delivery.audio.model, 'eleven_v3');
assert.equal(delivery.audio.voice, 'EbiSUflQjzm4g7S895SC');
const audio = {...delivery.audio, replacements: {[text]: directedText}};
const doc = {audio, chapters: [{id: 'continuous', narration: text}], paths: {build}};
const entry = speechCacheEntry(doc, spokenChapters(doc), 0);
assert.equal(entry.request.text, directedText, 'Direction must actually reach the provider.');
console.log(`${text.length} spoken characters; ${directedText.length} with direction; Leo / eleven_v3.`);
if (mode === '--check') process.exit(0);
await mkdir(resolve(build, 'audio'), {recursive: true});
const optional = async path => {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (e) { if (e.code !== 'ENOENT') throw e; return null; }
};
let record = await optional(entry.meta);
if (record) {
  assert.equal(record.sha256, await fileHash(entry.file));
  assert.equal(record.cache, entry.cache);
} else {
  const receiptPath = entry.file + '.provider.json';
  let receipt = await optional(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', 'No cached take; use --generate for one request.');
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(tool)) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (e) { if (e.code !== 'ENOENT') throw e; }
      if (key) break;
    }
    assert.ok(key, 'No ElevenLabs key configured; no request made.');
    console.log('Generating one continuous directed performance.');
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${delivery.audio.voice}/with-timestamps?output_format=pcm_24000`, {
      method: 'POST', headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(entry.request), signal: AbortSignal.timeout(240000),
    });
    const body = await response.text();
    assert.ok(response.ok, `Speech HTTP ${response.status}; no automatic retry.`);
    receipt = {cache: entry.cache, request: entry.request, voice: delivery.audio.voice,
      requestId: response.headers.get('request-id'), generatedAt: new Date().toISOString(), body};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  }
  assert.equal(receipt.cache, entry.cache);
  const data = JSON.parse(receipt.body);
  assert.ok(data.audio_base64, 'No audio; receipt retained.');
  const pcm = Buffer.from(data.audio_base64, 'base64'), wav = pcmWav(pcm, 24000);
  await writeFile(resolve(build, 'provider-original.wav'), wav);
  const original = data.normalized_alignment ?? data.alignment;
  validateAlignment(original, 'provider');
  const chars = [];
  let tag = false;
  for (let i = 0; i < original.characters.length; i++) {
    const ch = original.characters[i];
    if (ch === '[') tag = true;
    if (tag) { if (ch === ']') tag = false; continue; }
    const c = {text: /\s/u.test(ch) ? ' ' : ch,
      start: original.character_start_times_seconds[i],
      end: original.character_end_times_seconds[i]};
    if (c.text === ' ' && (!chars.length || chars.at(-1).text === ' ')) continue;
    chars.push(c);
  }
  if (chars.at(-1)?.text === ' ') chars.pop();
  assert.equal(chars.map(c => c.text).join(''), text, 'Transcript mismatch; inspect retained receipt.');
  const duration = pcm.length / 48000;
  let alignmentWarning = null;
  if (chars.at(-1).end > duration + .1) {
    const review = await optional(resolve(build, 'ending-check.json'));
    assert.ok(review?.completeEnding && review.audioSha256 === hash(wav),
      'Alignment extends beyond audio; verify the retained recording independently.');
    alignmentWarning = 'Provider terminal times extend past the PCM; independent ASR verifies the complete ending. Navigation is approximate; captions withheld pending realignment.';
  }
  const alignment = {characters: chars.map(c => c.text),
    character_start_times_seconds: chars.map(c => c.start),
    character_end_times_seconds: chars.map(c => c.end)};
  validateAlignment(alignment, 'continuous');
  record = {cache: entry.cache, request: entry.request, voice: delivery.audio.voice,
    model: delivery.audio.model, format: entry.format, sha256: hash(wav), duration,
    alignment, alignmentWarning, audioEdits: [], source: 'one complete provider performance',
    requestId: receipt.requestId, generatedAt: receipt.generatedAt};
  await writeFile(entry.file, wav, {flag: 'wx'});
  await writeFile(entry.meta, JSON.stringify(record, null, 2) + '\n', {flag: 'wx'});
}
const sections = [];
let offset = 0;
for (const section of delivery.sections) {
  const words = plain(section.directedText), start = text.indexOf(words, offset);
  assert.ok(start >= 0);
  const first = Array.from(text.slice(0, start)).length;
  const last = first + Array.from(words).length - 1;
  sections.push({id: section.id, emotion: section.emotion, text: words,
    start: record.alignment.character_start_times_seconds[first],
    end: record.alignment.character_end_times_seconds[last]});
  offset = start + words.length;
}
await writeFile(resolve(build, 'narration.wav'), await readFile(entry.file));
await writeFile(resolve(build, 'narration.txt'), text + '\n');
if (!record.alignmentWarning) {
  const captions = captionsFromAlignment(record.alignment);
  await writeFile(resolve(build, 'captions.srt'), srt(captions));
}
await writeFile(resolve(build, 'narration-manifest.json'), JSON.stringify({
  id: delivery.id, text, audio, sections, duration: record.duration,
  sha256: record.sha256, cacheFile: entry.file, audioEdits: [],
  alignmentWarning: record.alignmentWarning,
  source: record.source, requestId: record.requestId, generatedAt: record.generatedAt,
  listeningStatus: 'awaiting pilot review; no subjective listening claim',
}, null, 2) + '\n');
console.log(`Complete untouched narration: ${record.duration.toFixed(2)} seconds.`);
