// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Full-film audition: one provider request, untouched PCM, no retries.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';

const base = dirname(fileURLToPath(import.meta.url));
const [checkout, mode] = process.argv.slice(2);
assert.ok(checkout && (!mode || ['--check', '--generate'].includes(mode)),
  'Pass the Videomaker checkout, then --check or --generate; without either, reuse only.');
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
assert.ok(!/</.test(directedText), 'v3 takes bracketed directions, not markup.');
assert.ok(!/©|copyright|licen[cs]e|vibecoded|made with|created by|written by|\b(?:AGPL|GPL|MIT|BSD|CERN-OHL)\b/i.test(text),
  'Credit in spoken text.');
// The film shows these scene literals as its own source; they are spoken verbatim.
for (const line of ['From Machinome dot node dot assembly import AssemblyNode.',
  'The waterwheel spin drives the crankshaft.',
  "A crank and connecting rod turn that rotation into the saw's up-and-down stroke.",
  "And here's the code of this exact scene! How cool is that?"]) assert.ok(text.includes(line), line);
assert.equal(delivery.audio.model, 'eleven_v3');
assert.equal(delivery.audio.voice, 'cgSgspJ2msm6clMCkdW9');
const dictionary = JSON.parse(await readFile(resolve(base, delivery.pronunciation), 'utf8'));
assert.equal(dictionary.rules[0].phoneme, 'məˈʃiːnoʊm');
const audio = {...delivery.audio, replacements: {[text]: directedText}};
const doc = {audio, chapters: [{id: 'continuous', narration: text}], paths: {build}};
const entry = speechCacheEntry(doc, spokenChapters(doc), 0);
assert.equal(entry.request.text, directedText, 'Direction must actually reach the provider.');
const request = {...entry.request, pronunciation_dictionary_locators: [{
  pronunciation_dictionary_id: dictionary.id, version_id: dictionary.version_id,
}]};
assert.ok(!request.previous_text && !request.next_text);
const requestHash = hash(JSON.stringify({request, voice: delivery.audio.voice, format: entry.format}));
console.log(`${text.length} spoken characters; ${directedText.length} with direction; ${delivery.audio.voiceLabel} / eleven_v3.`);
if (mode === '--check') process.exit(0);
await mkdir(resolve(build, 'audio'), {recursive: true});
const optional = async path => {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (e) { if (e.code !== 'ENOENT') throw e; return null; }
};
let record = await optional(entry.meta);
if (record) {
  assert.equal(record.requestHash, requestHash, 'Request changed; keep the old take and choose a new cache.');
  assert.equal(record.sha256, await fileHash(entry.file), 'Cached speech bytes changed.');
  console.log('Reusing the continuous take; no request made.');
} else {
  const receiptPath = entry.file + '.provider.json';
  let receipt = await optional(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', 'No cached take; use --generate for the single paid request.');
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(tool)) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (e) { if (e.code !== 'ENOENT') throw e; }
      if (key) break;
    }
    assert.ok(key, 'No ElevenLabs key configured; no request made.');
    console.log('Generating one continuous directed performance.');
    // No automatic retry: a failed or ambiguous paid call must be inspected.
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${delivery.audio.voice}/with-timestamps?output_format=pcm_24000`, {
      method: 'POST', headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000),
    });
    const body = await response.text();
    assert.ok(response.ok, `Speech HTTP ${response.status}; no automatic retry (key and response omitted).`);
    // Keep the exact successful response before interpreting it, so recovery
    // never buys the same performance twice.
    receipt = {requestHash, request, voice: delivery.audio.voice,
      requestId: response.headers.get('request-id'),
      characterCost: response.headers.get('character-cost'),
      generatedAt: new Date().toISOString(), body};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  }
  assert.equal(receipt.requestHash, requestHash);
  const data = JSON.parse(receipt.body);
  assert.ok(data.audio_base64, 'No audio; receipt retained.');
  const pcm = Buffer.from(data.audio_base64, 'base64'), wav = pcmWav(pcm, 24000);
  await writeFile(resolve(build, 'provider-original.wav'), wav);
  // Drop the bracketed directions from the provider's clock, keeping the words.
  const spokenCharacters = original => {
    if (!original?.characters) return null;
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
    return chars;
  };
  const chars = [data.normalized_alignment, data.alignment].map(spokenCharacters)
    .find(c => c && c.map(x => x.text).join('') === text);
  assert.ok(chars, 'Transcript mismatch; inspect the retained receipt, no retry.');
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
  record = {cache: entry.cache, request, requestHash, voice: delivery.audio.voice,
    model: delivery.audio.model, format: entry.format, pronunciation: dictionary,
    sha256: hash(wav), duration, alignment, alignmentWarning, audioEdits: [],
    source: 'one complete provider performance', requestId: receipt.requestId,
    characterCost: receipt.characterCost, generatedAt: receipt.generatedAt};
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
