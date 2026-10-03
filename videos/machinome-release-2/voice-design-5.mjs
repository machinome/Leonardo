// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Restore the comparison line: five C3 deliveries and a matched Jessica control.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-5');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const readJSON = async file => JSON.parse(await readFile(resolve(base, file), 'utf8'));
const previous = await readJSON('_build/voice-design-3/manifest.json');
const selected = previous.candidates.find(c => c.sourceId === 'C3');
assert.equal(selected.id, 'D3-2');
assert.equal(selected.voiceId, 'JoOLJ0OHRwCg8Ydjc4IF');
const referenceFile = `_build/voice-design-3/${selected.file}`;
assert.equal(hash(await readFile(resolve(base, referenceFile))), selected.sha256);
const displayText = "I'm Machinome, and my purpose is to enable all machines to be open source. What do you want to build next?";
assert.equal(displayText, previous.displayText, 'Never change the comparison line.');
const spokenText = displayText.replace('Machinome', 'mah-SHEEN-ohm');
assert.equal(spokenText, previous.spokenText, 'Retain pronunciation and punctuation too.');
const jessicaId = (await readJSON('_build/narration-input.json')).audio.voice;
assert.equal(jessicaId, 'cgSgspJ2msm6clMCkdW9');
const {text: oldDirection, ...settings} = previous.performance;
const directions = [
  {id: 'D5-1', title: 'Natural baseline', cue: '', intent: 'Let the voice read the line without an imposed emotion.'},
  {id: 'D5-2', title: 'Easy confidence', cue: 'confident', intent: 'A clear purpose, said straightforwardly.'},
  {id: 'D5-3', title: 'Warm invitation', cue: 'warm, conversational', intent: 'A capable collaborator inviting you to build.'},
  {id: 'D5-4', title: 'Genuine interest', cue: 'curious, engaged', intent: 'Interested in the possibilities and in your answer.'},
  {id: 'D5-5', title: 'A little more energy', cue: 'enthusiastic, conversational', intent: 'Enjoy the possibilities with a little more forward energy.'},
];
const jobs = directions.map(direction => ({...direction, voiceId: selected.voiceId,
  request: {...settings, text: (direction.cue ? `[${direction.cue}] ` : '') + spokenText}}));
const jessicaJob = {id: 'jessica', title: 'Jessica — same-line control', cue: '', voiceId: jessicaId,
  intent: 'A fresh untagged reading, matched to C3 natural baseline; not a crop of the film.',
  request: {...settings, text: spokenText}};
assert.deepEqual(jobs[0].request, jessicaJob.request);
for (const job of [...jobs, jessicaJob]) {
  assert.equal(job.request.text.replace(/\[[^\]]*\]\s*/g, ''), spokenText);
  assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(job.request.text));
  assert.ok((job.request.text.match(/\[/g) ?? []).length <= 1);
}
console.log('Design 5: original closing restored; five fixed-C3 deliveries, one matched Jessica control.');

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
async function perform(job) {
  const directory = resolve(build, job.id);
  await mkdir(directory, {recursive: true});
  const endpoint = `https://api.elevenlabs.io/v1/text-to-speech/${job.voiceId}/with-timestamps?output_format=mp3_44100_128`;
  const request = job.request, requestHash = hash(JSON.stringify({endpoint, request}));
  const receiptPath = resolve(directory, 'speech.provider.json');
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', `No cached ${job.id}; --generate is required.`);
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
    await writeFile(resolve(directory, 'attempt.json'), JSON.stringify({requestHash, startedAt: new Date().toISOString()}) + '\n', {flag: 'wx'});
    console.log(`${job.id}: ${job.title}; original comparison words.`);
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    receipt = {requestHash, endpoint, request, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      createdAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log(`${job.id}: cached; no provider request.`);
  assert.equal(receipt.requestHash, requestHash, 'Changed request requires a new cache.');
  assert.equal(receipt.status, 200, `Speech HTTP ${receipt.status}; receipt retained, no automatic retry.`);
  const data = JSON.parse(receipt.body);
  assert.ok(data.audio_base64);
  const bytes = Buffer.from(data.audio_base64, 'base64');
  const file = `${job.id}/closing.mp3`, path = resolve(build, file);
  await preserve(path, bytes);
  const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], {encoding: 'utf8'}));
  assert.equal(probe.streams.length, 1);
  assert.equal(probe.streams[0].codec_name, 'mp3');
  const duration = Number(probe.format.duration);
  assert.ok(duration > 3 && duration < 25);
  execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
  const alignment = data.normalized_alignment ?? data.alignment;
  assert.ok(alignment?.characters?.length);
  const canonical = value => value.replace(/\[[^\]]*\]/g, '').replace(/[^a-z]/gi, '').toLowerCase();
  assert.equal(canonical(alignment.characters.join('')), canonical(spokenText), 'Aligned text differs; inspect saved response, do not regenerate.');
  const {validateAlignment} = await import(pathToFileURL(resolve(toolPath, 'src/words.mjs')));
  validateAlignment(alignment, job.id);
  assert.ok(alignment.character_end_times_seconds.at(-1) <= duration + 0.1);
  await preserve(resolve(directory, 'alignment.json'), JSON.stringify(alignment, null, 2) + '\n');
  console.log(`${job.id}: ${duration.toFixed(2)} s; decoded and words aligned.`);
  return {...job, requestHash, file, sha256: hash(bytes), duration, bytes: bytes.length,
    generatedAt: receipt.createdAt, requestId: receipt.requestId, characterCost: receipt.characterCost};
}

if (mode !== '--check') {
  const results = [await perform(jobs[0])];
  const remaining = [...jobs.slice(1), jessicaJob];
  for (let i = 0; i < remaining.length; i += 2) results.push(...await Promise.all(remaining.slice(i, i + 2).map(perform)));
  const candidates = results.filter(c => c.id !== 'jessica');
  const jessica = results.find(c => c.id === 'jessica');
  assert.equal(candidates.length, 5);
  assert.equal(new Set(candidates.map(c => c.voiceId)).size, 1);
  assert.equal(new Set(results.map(c => c.sha256)).size, 6);
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/5', status: 'awaiting-performance-selection',
    displayText, spokenText, fixedSettings: settings,
    selectedVoice: {label: 'C3', previousProposal: selected.id, voiceId: selected.voiceId,
      referenceFile, referenceSha256: selected.sha256, referenceDuration: selected.duration},
    candidates, jessica,
    comparisonContract: 'Every sample uses the unchanged design-3 closing words and pronunciation. C3 reference bytes are untouched. Jessica and C3 natural baseline use identical TTS requests except voice ID.',
    processing: 'Raw provider MP3s. No edits, effects, pitch changes or post-production time stretching.',
    newVoicesCreated: 0, filmChanged: false,
  }, null, 2) + '\n');
}
