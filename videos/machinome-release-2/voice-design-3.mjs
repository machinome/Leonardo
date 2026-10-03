// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Preserve three existing voices; direct a fresh performance, not a remix.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-3');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const previous = JSON.parse(await readFile(resolve(base, '_build/voice-design-2/manifest.json'), 'utf8'));
const spokenText = previous.candidates[0].request.text;
const displayText = previous.displayText;
const performance = {
  text: '[conversational, confident] ' + spokenText.replace('What do you', '[friendly, direct] What do you'),
  model_id: 'eleven_v3',
  voice_settings: {stability: 0.5, similarity_boost: 0.75, style: 0, speed: 1.05},
  seed: 20261003,
};
assert.equal(performance.text.replace(/\[[^\]]*\]\s*/g, ''), spokenText);
assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(JSON.stringify(performance)));
const selection = [
  ['D3-1', 'C1', 'jtlpSHajhD6dVHux60yP'],
  ['D3-2', 'C3', 'JoOLJ0OHRwCg8Ydjc4IF'],
  ['D3-3', 'C5', 'isdFxhGsw3B4F21g7smQ'],
];
const candidates = [];
for (const [id, sourceId, generatedVoiceId] of selection) {
  const original = previous.candidates.find(c => c.id === sourceId);
  assert.equal(original.generatedVoiceId, generatedVoiceId);
  const sourceFile = `_build/voice-design-2/${original.file}`;
  assert.equal(hash(await readFile(resolve(base, sourceFile))), original.sha256);
  candidates.push({id, sourceId, generatedVoiceId, sourceFile,
    sourceSha256: original.sha256, sourceDuration: original.duration});
}
console.log('Design 3: three existing voice identities; one shared conversational, confident performance direction.');

async function optionalJSON(path) {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
}
async function preserve(path, bytes) {
  try { await writeFile(path, bytes, {flag: 'wx'}); }
  catch (error) {
    if (error.code !== 'EEXIST') throw error;
    assert.equal(hash(await readFile(path)), hash(bytes), 'Cached artifact changed.');
  }
}
let key;
async function recordedRequest(directory, name, endpoint, request) {
  const requestHash = hash(JSON.stringify({endpoint, request}));
  const receiptPath = resolve(directory, `${name}.provider.json`);
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', `No cached ${name}; --generate is required.`);
    if (!key) {
      const {keyFiles} = await import(pathToFileURL(resolve(toolPath, 'src/speech.mjs')));
      key = process.env.ELEVENLABS_API_KEY;
      if (key === undefined) for (const path of keyFiles(resolve(toolPath))) {
        try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
        catch (error) { if (error.code !== 'ENOENT') throw error; }
        if (key) break;
      }
      assert.ok(key, 'No ElevenLabs key configured; no request made.');
    }
    // An unresolved attempt blocks duplicate voice creation or speech charges.
    await writeFile(resolve(directory, `${name}.attempt.json`), JSON.stringify({requestHash, startedAt: new Date().toISOString()}) + '\n', {flag: 'wx'});
    console.log(`${directory.split('/').at(-1)}: ${name} request.`);
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    receipt = {requestHash, endpoint, request, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      createdAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log(`${directory.split('/').at(-1)}: cached ${name}; no request.`);
  assert.equal(receipt.requestHash, requestHash, 'Changed request needs a new audition directory.');
  assert.equal(receipt.status, 200, `${name} HTTP ${receipt.status}; receipt retained, no retry.`);
  return {receipt, data: JSON.parse(receipt.body)};
}

async function perform(candidate) {
  const directory = resolve(build, candidate.id);
  await mkdir(directory, {recursive: true});
  const voiceName = `Machinome audition ${candidate.sourceId}`;
  const saved = await recordedRequest(directory, 'save-voice', 'https://api.elevenlabs.io/v1/text-to-voice', {
    voice_name: voiceName,
    voice_description: `Original gender-neutral Machinome audition ${candidate.sourceId}. Existing designed voice, retained for natural, confident conversational readings. Candidate only, not a final selection.`,
    generated_voice_id: candidate.generatedVoiceId,
  });
  const voiceId = saved.data.voice_id;
  assert.ok(typeof voiceId === 'string' && voiceId.length > 0);
  const speech = await recordedRequest(directory, 'speech', `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}/with-timestamps?output_format=mp3_44100_128`, performance);
  assert.ok(speech.data.audio_base64, 'Provider response retained; missing audio.');
  const audio = Buffer.from(speech.data.audio_base64, 'base64');
  const file = `${candidate.id}/natural-confident.mp3`;
  const path = resolve(build, file);
  await preserve(path, audio);
  const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], {encoding: 'utf8'}));
  assert.equal(probe.streams.length, 1);
  assert.equal(probe.streams[0].codec_name, 'mp3');
  const duration = Number(probe.format.duration);
  assert.ok(duration > 3 && duration < 25);
  execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
  const alignment = speech.data.normalized_alignment ?? speech.data.alignment;
  assert.ok(alignment?.characters?.length);
  const canonical = value => value.replace(/\[[^\]]*\]/g, '').replace(/[^a-z]/gi, '').toLowerCase();
  assert.equal(canonical(alignment.characters.join('')), canonical(spokenText), 'Aligned words differ; inspect retained audio, do not regenerate.');
  const {validateAlignment} = await import(pathToFileURL(resolve(toolPath, 'src/words.mjs')));
  validateAlignment(alignment, candidate.id);
  assert.ok(alignment.character_end_times_seconds.at(-1) <= duration + 0.1);
  await preserve(resolve(directory, 'alignment.json'), JSON.stringify(alignment, null, 2) + '\n');
  const result = {...candidate, voiceName, voiceId, file, sha256: hash(audio), bytes: audio.length,
    duration, requestHash: speech.receipt.requestHash, generatedAt: speech.receipt.createdAt,
    requestId: speech.receipt.requestId, characterCost: speech.receipt.characterCost};
  console.log(`${candidate.id} from ${candidate.sourceId}: ${duration.toFixed(2)} s; decoded and words aligned.`);
  return result;
}

if (mode !== '--check') {
  const results = [await perform(candidates[0])];
  results.push(...await Promise.all(candidates.slice(1).map(perform)));
  assert.equal(new Set(results.map(c => c.voiceId)).size, 3);
  assert.equal(new Set(results.map(c => c.sha256)).size, 3);
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/3', status: 'awaiting-listening-selection',
    displayText, spokenText, performance, candidates: results,
    method: 'Save existing designed identities, then synthesize a new performance. No redesign or remix.',
    processing: 'Unmodified provider MP3s. No splicing, pitch change, effects or post-production time stretching.',
    privateVoicesSaved: 3, finalVoiceSelected: false, filmChanged: false,
  }, null, 2) + '\n');
}
