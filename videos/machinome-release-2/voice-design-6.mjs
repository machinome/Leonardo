// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Start from Jessica's actual performance; alter timbre and check duration.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-6');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const previous = JSON.parse(await readFile(resolve(base, '_build/voice-design-5/manifest.json'), 'utf8'));
const referenceFile = `_build/voice-design-5/${previous.jessica.file}`;
const reference = await readFile(resolve(base, referenceFile));
assert.equal(hash(reference), '53092b1e8c05ecaf3d661bbe425164fd4aa39921ac5a507a756d4c6638242237');
assert.equal(hash(reference), previous.jessica.sha256);
assert.equal(previous.jessica.voiceId, 'cgSgspJ2msm6clMCkdW9');
const displayText = "I'm Machinome, and my purpose is to enable all machines to be open source. What do you want to build next?";
assert.equal(previous.displayText, displayText);
const text = displayText.replace('Machinome', 'mah-SHEEN-ohm');
assert.equal(text, previous.spokenText);
const maximumOverrun = 0.05;
const request = {
  voice_description: 'Use the reference performance as the foundation. Preserve its lively, alert conversational delivery, compact phrase lengths, brisk connected speech, brief pauses, clear consonants and confident friendly invitation. Keep the same English pronunciation and expressive melodic movement. Change the vocal timbre toward an adult androgynous, gender-ambiguous voice: a slightly fuller, balanced resonance with both bright and rounded overtones and a clear, lightly textured tone. Keep the comfortable pitch area and forward placement of the reference. Natural, capable and engaged, enjoying the prospect of building something. Retain the reference tempo and energy throughout the sentence. The complete reading should fit the same roughly eight-second span as the reference. Clean dry studio sound.',
  model_id: 'eleven_ttv_v3', text, auto_generate_text: false,
  loudness: 0.5, seed: 20261006, guidance_scale: 2,
  stream_previews: false, should_enhance: false,
  reference_audio_base64: reference.toString('base64'), prompt_strength: 0.35,
};
assert.ok(text.length >= 100 && text.length <= 1000);
assert.ok(request.voice_description.length >= 20 && request.voice_description.length <= 1000);
assert.ok(!/profound|solemn|contemplative|gravitas|whisper|bass|low register/i.test(request.voice_description));
const endpoint = 'https://api.elevenlabs.io/v1/text-to-voice/design?output_format=mp3_44100_128';
const requestHash = hash(JSON.stringify({endpoint, request}));
const durationProbe = file => JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', file], {encoding: 'utf8'}));
const referenceDuration = Number(durationProbe(resolve(base, referenceFile)).format.duration);
assert.ok(Math.abs(referenceDuration - previous.jessica.duration) < 0.001);
const durationLimit = referenceDuration * (1 + maximumOverrun);
console.log(`Jessica reference ${referenceDuration.toFixed(2)} s; audition limit ${durationLimit.toFixed(2)} s (+5%). Same closing words.`);

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

if (mode !== '--check') {
  await mkdir(build, {recursive: true});
  const receiptPath = resolve(build, 'provider.json');
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', 'No response cached. --generate makes one paid design request.');
    const {keyFiles} = await import(pathToFileURL(resolve(toolPath, 'src/speech.mjs')));
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(resolve(toolPath))) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (error) { if (error.code !== 'ENOENT') throw error; }
      if (key) break;
    }
    assert.ok(key, 'No ElevenLabs key configured; no request made.');
    await writeFile(resolve(build, 'attempt.json'), JSON.stringify({requestHash, startedAt: new Date().toISOString()}) + '\n', {flag: 'wx'});
    console.log('Generating three candidates from Jessica audio; no C3 input, no automatic retry.');
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    receipt = {requestHash, endpoint, request: {...request, reference_audio_base64: undefined},
      reference: {file: referenceFile, sha256: hash(reference)}, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      generatedAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log('Using the saved design response; no provider request.');
  assert.equal(receipt.requestHash, requestHash, 'Changed prompt/reference needs a new cache.');
  assert.equal(receipt.status, 200, `Voice Design HTTP ${receipt.status}; receipt retained, no retry.`);
  const data = JSON.parse(receipt.body);
  assert.equal(data.text, text);
  assert.equal(data.previews.length, 3);
  const candidates = [];
  for (const [index, preview] of data.previews.entries()) {
    assert.ok(preview.audio_base_64 && preview.generated_voice_id);
    const id = `J${index + 1}`, file = `${id}.mp3`;
    const bytes = Buffer.from(preview.audio_base_64, 'base64');
    const path = resolve(build, file);
    await preserve(path, bytes);
    const probe = durationProbe(path);
    assert.equal(probe.streams.length, 1);
    assert.equal(probe.streams[0].codec_name, 'mp3');
    const duration = Number(probe.format.duration);
    assert.ok(duration > 3 && duration < 25);
    execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
    const durationChangePercent = 100 * (duration / referenceDuration - 1);
    const pacePass = duration <= durationLimit;
    candidates.push({id, file, generatedVoiceId: preview.generated_voice_id,
      sha256: hash(bytes), bytes: bytes.length, duration, durationChangePercent, pacePass});
    console.log(`${id}: ${duration.toFixed(2)} s (${durationChangePercent >= 0 ? '+' : ''}${durationChangePercent.toFixed(1)}%); duration gate ${pacePass ? 'PASS' : 'FAIL'}.`);
  }
  assert.equal(new Set(candidates.map(c => c.sha256)).size, 3);
  assert.equal(new Set(candidates.map(c => c.generatedVoiceId)).size, 3);
  const priorDurations = previous.candidates.map(c => ({id: c.id, duration: c.duration,
    durationChangePercent: 100 * (c.duration / referenceDuration - 1)}));
  const accepted = candidates.filter(c => c.pacePass);
  const rejected = candidates.filter(c => !c.pacePass);
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/6', status: accepted.length ? 'awaiting-timbre-listening-review' : 'duration-gate-failed',
    displayText, spokenText: text, requestHash, request: receipt.request,
    reference: {label: 'Jessica', file: referenceFile, sha256: hash(reference), duration: referenceDuration},
    maximumOverrun, durationLimit, previews: candidates, candidates: accepted, rejected, priorDurations,
    generatedAt: receipt.generatedAt, requestId: receipt.requestId,
    method: 'Jessica audio conditions a new androgynous-timbre design. C3 is not a reference.',
    processing: 'Unmodified provider previews; no time stretching, pitch filters, edits or effects.',
    permanentVoicesCreated: 0, filmChanged: false,
    limitations: 'Duration is a pacing gate, not proof of exact cadence, alertness, spoken accuracy or perceived gender neutrality. Preview pacing must later be verified in ordinary TTS and full narration.',
  }, null, 2) + '\n');
  assert.ok(accepted.length > 0, 'No preview passed the duration gate; all media retained, no automatic retry.');
  console.log(`${accepted.length} candidates meet the duration gate; ${rejected.length} excluded from the listening comparison. No threshold changes or additional requests.`);
}
