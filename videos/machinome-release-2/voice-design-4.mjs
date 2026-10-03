// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Five performances of the film's actual words, using the selected C3 voice.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-4');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const readJSON = async file => JSON.parse(await readFile(resolve(base, file), 'utf8'));
const previous = await readJSON('_build/voice-design-3/manifest.json');
const selected = previous.candidates.find(c => c.sourceId === 'C3');
assert.equal(selected.id, 'D3-2', 'C3 is proposal 2 of design 3, not proposal 3.');
assert.equal(selected.voiceId, 'JoOLJ0OHRwCg8Ydjc4IF');
const saved = await readJSON('_build/voice-design-3/D3-2/save-voice.provider.json');
assert.equal(JSON.parse(saved.body).voice_id, selected.voiceId);
assert.equal(hash(await readFile(resolve(base, '_build/voice-design-3', selected.file))), selected.sha256);

const inputPath = '_build/narration-input.json';
const input = await readJSON(inputPath);
assert.equal(input.chapters.length, 1);
const fullText = input.chapters[0].narration;
const start = 'With Machinome, machines can have a source code.';
const reveal = "And here's the code of this exact scene!";
const ending = 'And the best part is: this is all open source!';
for (const anchor of [start, reveal, ending]) assert.equal(fullText.split(anchor).length, 2);
const begin = fullText.indexOf(start), end = fullText.indexOf(ending) + ending.length;
assert.ok(begin < end);
const displayText = fullText.slice(begin, end);
assert.ok(displayText.includes('How cool is that?'));
const spokenText = displayText.replace('Machinome', 'mah-SHEEN-ohm');
const spokenReveal = spokenText.indexOf(reveal), spokenEnding = spokenText.indexOf(ending);
const sections = [spokenText.slice(0, spokenReveal).trimEnd(),
  spokenText.slice(spokenReveal, spokenEnding).trimEnd(), spokenText.slice(spokenEnding)];
assert.equal(sections.join(' '), spokenText);
const sourceHashes = {};
for (const path of [inputPath, 'narration.py', 'movie.py', 'scene_source.py']) {
  sourceHashes[path] = hash(await readFile(resolve(base, path)));
}
const directions = [
  {id: 'D4-1', title: 'A spark of excitement',
    intent: 'Engaged explanation, then an audible lift of delight at the reveal.',
    tags: ['conversational, enthusiastic', 'excited, delighted', 'happy, confident']},
  {id: 'D4-2', title: 'Discovering it together',
    intent: 'Curiosity becomes a small discovery shared with the listener.',
    tags: ['curious, conversational', 'surprised, delighted', 'pleased, assured']},
  {id: 'D4-3', title: 'Warm conviction',
    intent: 'Assured, approachable and glad to share what this makes possible.',
    tags: ['warm, confident', 'friendly, smiling', 'warm, inviting']},
  {id: 'D4-4', title: 'A knowing smile',
    intent: 'Enjoy the self-reference with gentle playfulness and an audible smile.',
    tags: ['conversational, lightly amused', 'playful, smiling', 'pleased, confident']},
  {id: 'D4-5', title: 'Understated confidence',
    intent: 'Plainspoken and self-assured, with a little dry amusement at the reveal.',
    tags: ['conversational, confident', 'understated, amused', 'confident, satisfied']},
];
const jobs = directions.map(direction => {
  const request = {...previous.performance,
    text: sections.map((section, i) => `[${direction.tags[i]}] ${section}`).join(' ')};
  assert.equal(request.text.replace(/\[[^\]]*\]\s*/g, ''), spokenText);
  assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(request.text));
  return {direction, request};
});
const endpoint = `https://api.elevenlabs.io/v1/text-to-speech/${selected.voiceId}/with-timestamps?output_format=mp3_44100_128`;
console.log(`Design 4: five performances, fixed C3 identity/settings; ${displayText.length} verbatim script characters.`);

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
async function perform({direction, request}) {
  const directory = resolve(build, direction.id);
  await mkdir(directory, {recursive: true});
  const requestHash = hash(JSON.stringify({endpoint, request}));
  const receiptPath = resolve(directory, 'speech.provider.json');
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', `No cached ${direction.id}; --generate is required.`);
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
    console.log(`${direction.id}: ${direction.title}; one fresh performance of C3.`);
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    receipt = {requestHash, endpoint, request, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      createdAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log(`${direction.id}: cached; no provider request.`);
  assert.equal(receipt.requestHash, requestHash, 'Changed performance needs a new audition directory.');
  assert.equal(receipt.status, 200, `Speech HTTP ${receipt.status}; receipt retained, no automatic retry.`);
  const data = JSON.parse(receipt.body);
  assert.ok(data.audio_base64);
  const bytes = Buffer.from(data.audio_base64, 'base64');
  const file = `${direction.id}/performance.mp3`, path = resolve(build, file);
  await preserve(path, bytes);
  const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], {encoding: 'utf8'}));
  assert.equal(probe.streams.length, 1);
  assert.equal(probe.streams[0].codec_name, 'mp3');
  const duration = Number(probe.format.duration);
  assert.ok(duration > 8 && duration < 60);
  execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
  const alignment = data.normalized_alignment ?? data.alignment;
  assert.ok(alignment?.characters?.length);
  const canonical = value => value.replace(/\[[^\]]*\]/g, '').replace(/[^a-z]/gi, '').toLowerCase();
  assert.equal(canonical(alignment.characters.join('')), canonical(spokenText), 'Aligned words differ; inspect saved response, do not regenerate.');
  const {validateAlignment} = await import(pathToFileURL(resolve(toolPath, 'src/words.mjs')));
  validateAlignment(alignment, direction.id);
  assert.ok(alignment.character_end_times_seconds.at(-1) <= duration + 0.1);
  await preserve(resolve(directory, 'alignment.json'), JSON.stringify(alignment, null, 2) + '\n');
  console.log(`${direction.id}: ${duration.toFixed(2)} s; decoded and script words aligned.`);
  return {...direction, voiceId: selected.voiceId, request, requestHash, file, sha256: hash(bytes),
    duration, bytes: bytes.length, generatedAt: receipt.createdAt,
    requestId: receipt.requestId, characterCost: receipt.characterCost};
}

if (mode !== '--check') {
  const candidates = [await perform(jobs[0])];
  for (let i = 1; i < jobs.length; i += 2) candidates.push(...await Promise.all(jobs.slice(i, i + 2).map(perform)));
  assert.equal(new Set(candidates.map(c => c.voiceId)).size, 1);
  assert.equal(new Set(candidates.map(c => c.sha256)).size, 5);
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/4', status: 'awaiting-performance-selection',
    selectedVoice: {label: 'C3', previousProposal: selected.id, voiceId: selected.voiceId,
      referenceFile: `_build/voice-design-3/${selected.file}`, referenceSha256: selected.sha256,
      referenceDuration: selected.duration},
    displayText, spokenText, source: {input: inputPath, begin, end, sourceHashes}, candidates,
    method: 'One existing selected voice. Same model, settings, seed and script; only audio direction tags vary.',
    processing: 'Unmodified provider MP3s; no effects, edits, pitch changes or post-production time stretching.',
    newVoicesCreated: 0, filmChanged: false,
  }, null, 2) + '\n');
}
