// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Disposable pronunciation audition, not a new Videomaker source format.
import assert from 'node:assert/strict';
import { loadEnvFile } from 'node:process';
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker repository path');
const tool = resolve(process.argv[2]);
const { parseSource } = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const { pcmWav } = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const { captionsFromAlignment, srt } = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const recipeName = process.argv[3] ?? 'sample';
assert.match(recipeName, /^(sample|phoneme)$/);
const recipe = parseSource(await readFile(resolve(base, `${recipeName}.yaml`), 'utf8'));
assert.equal(recipe.format, 'machinome-audio-experiment/pronunciation');
assert.ok(!/copyright|licen[cs]e|created by|made with/i.test(recipe.text));
const build = resolve(base, '_build', recipeName === 'sample' ? '.' : recipeName);
await mkdir(build, { recursive: true });
loadEnvFile(resolve(tool, '.env'));
const key = process.env.ELEVENLABS_API_KEY;
assert.ok(key, 'Missing ElevenLabs key');
const hash = data => createHash('sha256').update(data).digest('hex');
const json = (name, value) => writeFile(resolve(build, name), JSON.stringify(value, null, 2) + '\n');
async function cached(name) {
  try { return JSON.parse(await readFile(resolve(build, name), 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
}
async function request(path, body) {
  const response = await fetch(`https://api.elevenlabs.io/v1/${path}`, {
    method: 'POST', headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify(body), signal: AbortSignal.timeout(120000),
  });
  const data = await response.json();
  if (!response.ok) {
    // Never print headers or credentials, even on provider failures.
    throw new Error(`ElevenLabs HTTP ${response.status}: ${data.detail?.status ?? 'request_failed'}`);
  }
  return data;
}
// Preserve the original spelling audition; test explicit phonemes separately.
const phonetic = recipe.pronunciation.method === 'phoneme-dictionary';
assert.ok(phonetic || recipe.pronunciation.method === 'continuous-spelling-audition');
let dictionary;
if (phonetic) {
  const rules = [{ type: 'phoneme', string_to_replace: recipe.pronunciation.word,
    alphabet: recipe.pronunciation.alphabet, phoneme: recipe.pronunciation.phoneme }];
  const rulesHash = hash(JSON.stringify(rules));
  dictionary = await cached('dictionary.json');
  if (!dictionary) {
    const result = await request('pronunciation-dictionaries/add-from-rules', {
      name: 'Machinome release pronunciation audition', rules,
      description: 'Explicit English phonemes; pronunciation awaiting listening approval.',
    });
    assert.ok(result.id && result.version_id, 'Missing dictionary locator');
    dictionary = { id: result.id, version_id: result.version_id, rules, rulesHash };
    await json('dictionary.json', dictionary);
    console.log('Pronunciation dictionary created successfully');
  }
  assert.equal(dictionary.rulesHash, rulesHash, 'Dictionary rules changed: refusing stale cache');
}
const spokenText = phonetic ? recipe.text : recipe.text.replaceAll(
  recipe.pronunciation.word, recipe.pronunciation.spokenAlias,
);
const body = {
  text: spokenText, model_id: recipe.audio.model,
  voice_settings: recipe.audio.voiceSettings, seed: 4217,
  ...(phonetic ? { pronunciation_dictionary_locators: [{
    pronunciation_dictionary_id: dictionary.id, version_id: dictionary.version_id,
  }] } : {}),
};
const inputHash = hash(JSON.stringify({ body, voice: recipe.audio.voice, format: recipe.audio.outputFormat }));
let record = await cached('sample.json');
if (!record) {
  console.log(`Generating Jessica pronunciation sample (${recipe.text.length} characters)`);
  const data = await request(
    `text-to-speech/${recipe.audio.voice}/with-timestamps?output_format=${recipe.audio.outputFormat}`, body,
  );
  assert.ok(data.audio_base64, 'Provider returned no audio');
  const alignment = data.normalized_alignment ?? data.alignment;
  const cues = captionsFromAlignment(alignment);
  for (const cue of cues) {
    if (!phonetic) {
      cue.text = cue.text.replaceAll(recipe.pronunciation.spokenAlias, recipe.pronunciation.word);
    }
  }
  const wav = pcmWav(Buffer.from(data.audio_base64, 'base64'), 24000);
  await writeFile(resolve(build, 'sample.wav'), wav);
  await writeFile(resolve(build, 'sample.srt'), srt(cues));
  record = { status: recipe.status, recipe, request: body, inputHash,
    wavSha256: hash(wav), durationSeconds: (wav.length - 44) / 48000, alignment };
  await json('sample.json', record);
}
assert.equal(record.inputHash, inputHash, 'Sample inputs changed: refusing stale cache');
assert.equal(hash(await readFile(resolve(build, 'sample.wav'))), record.wavSha256);
if (!phonetic) await copyFile(resolve(base, 'listen.html'), resolve(build, 'index.html'));
console.log(JSON.stringify({ file: resolve(build, 'sample.wav'), seconds: record.durationSeconds, status: record.status }));
