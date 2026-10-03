// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Five lighter variations, all conditioned on the actual audition C audio.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-2');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const referencePath = '_build/voice-design-1/voice-C.mp3';
const referenceBytes = await readFile(resolve(base, referencePath));
const referenceHash = 'e0419c7622fce4b39a87f1f8cbb487504105c7adec2dd28e2d7beb5bff3eddfc';
assert.equal(hash(referenceBytes), referenceHash, 'The reference must be the original C.');
const previous = JSON.parse(await readFile(resolve(base, '_build/voice-design-1/manifest.json'), 'utf8'));
const displayText = previous.displayText;
const text = previous.request.text;
const common = 'Keep the reference voice recognizable: its timbre, English pronunciation and adult gender-neutral identity. Lighten the vocal weight into a comfortable middle register, with an easy conversational flow and clear natural articulation. Machinome is the code, the making and the mechanism speaking as one curious collaborator. It enjoys understanding how things work and helping people build. Speak with everyday presence, modest confidence and an open, living quality. Studio quality, dry close recording. ';
const variations = [
  {id: 'C1', title: 'At the workbench', strength: 0.30,
    direction: 'Conversational and easy, as if working beside the listener.',
    prompt: 'A relaxed conversation between two people at a workbench. Keep the voice particularly close to the reference, but release its solemn weight and deliberate dramatic pauses. Unforced, unhurried, candid. Say the purpose plainly; ask the final question with genuine interest in the answer.'},
  {id: 'C2', title: 'A spark of curiosity', strength: 0.40,
    direction: 'Brighter and more animated, with the pleasure of discovery.',
    prompt: 'Let curiosity lift the voice: a slightly brighter forward resonance, nimble rhythm and small, lively changes of intonation. The pleasure is in discovery, like a mechanism suddenly making sense. The final question is eager and inquisitive. Keep the energy contained and adult, with the same gender ambiguity.'},
  {id: 'C3', title: 'Clear thinking', strength: 0.35,
    direction: 'Clean, precise and quietly alert.',
    prompt: 'A lucid, precise voice with a light, clean tone and economical phrasing. Sound quietly alert, as if understanding each connection while speaking. Smooth, even flow, lightly articulated consonants, natural small inflections. Purpose is a simple statement of what you do; the final question opens a possibility.'},
  {id: 'C4', title: 'A little play', strength: 0.40,
    direction: 'A subtle smile and a gently playful invitation.',
    prompt: 'Add a small audible smile, lightly elastic timing and understated playfulness. The voice enjoys being both the machine and the explanation of the machine. Warm wit rather than a joke, a friendly glint rather than a performance. Let the last question feel like an intriguing challenge offered to a friend.'},
  {id: 'C5', title: 'Build with me', strength: 0.35,
    direction: 'Warm, approachable and collaborative.',
    prompt: 'Round, approachable warmth and easy companionship. Speak as a capable collaborator sharing a purpose, with a slightly softer edge and comfortable conversational pace. The invitation matters more than the declaration. Let the final question sound open and welcoming, leaving space for the listener to imagine an answer.'},
];
assert.equal(variations.length, 5);
assert.ok(text.length >= 100 && text.length <= 1000);
const endpoint = 'https://api.elevenlabs.io/v1/text-to-voice/design?output_format=mp3_44100_128';
const jobs = variations.map(variation => {
  const request = {voice_description: common + variation.prompt,
    model_id: 'eleven_ttv_v3', text, auto_generate_text: false,
    loudness: 0.5, seed: 20261004, guidance_scale: 2,
    stream_previews: false, should_enhance: false,
    reference_audio_base64: referenceBytes.toString('base64'),
    prompt_strength: variation.strength};
  assert.ok(request.voice_description.length >= 20 && request.voice_description.length <= 1000);
  return {variation, request, requestHash: hash(JSON.stringify({endpoint, request}))};
});
console.log(`Five C-referenced directions; same ${text.length}-character closing; film untouched.`);

async function optionalJSON(path) {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
}
async function preserve(path, bytes) {
  try { await writeFile(path, bytes, {flag: 'wx'}); }
  catch (error) {
    if (error.code !== 'EEXIST') throw error;
    assert.equal(hash(await readFile(path)), hash(bytes), `Cached bytes changed: ${path}`);
  }
}
let key;
async function generate({variation, request, requestHash}) {
  const directory = resolve(build, variation.id);
  await mkdir(directory, {recursive: true});
  const receiptPath = resolve(directory, 'provider.json');
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    assert.equal(mode, '--generate', `No cached ${variation.id}; no paid request allowed without --generate.`);
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
    console.log(`${variation.id}: generating ${variation.title}, using original C audio.`);
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    // Store the full response before parsing; never automatically retry a purchase.
    receipt = {requestHash, endpoint, request: {...request, reference_audio_base64: undefined},
      reference: {file: referencePath, sha256: referenceHash}, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      generatedAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log(`${variation.id}: using saved response, no request.`);
  assert.equal(receipt.requestHash, requestHash, 'Changed direction needs a new audition directory.');
  assert.equal(receipt.status, 200, `Voice Design HTTP ${receipt.status}; receipt retained, no automatic retry.`);
  const data = JSON.parse(receipt.body);
  assert.equal(data.text, text);
  assert.ok(data.previews?.length > 0);
  const previews = [];
  for (const [index, preview] of data.previews.entries()) {
    assert.ok(preview.audio_base_64 && preview.generated_voice_id);
    const bytes = Buffer.from(preview.audio_base_64, 'base64');
    const file = `${variation.id}/preview-${index + 1}.mp3`;
    await preserve(resolve(build, file), bytes);
    previews.push({file, generatedVoiceId: preview.generated_voice_id, sha256: hash(bytes), bytes: bytes.length});
  }
  // One sample per direction, chosen by stable provider order, not a claim
  // of auditory curation. Every extra preview remains in the original receipt.
  const selected = previews[0], path = resolve(build, selected.file);
  const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], {encoding: 'utf8'}));
  assert.equal(probe.streams.length, 1);
  assert.equal(probe.streams[0].codec_name, 'mp3');
  const duration = Number(probe.format.duration);
  assert.ok(duration > 3 && duration < 30);
  execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
  console.log(`${variation.id}: ${duration.toFixed(2)} s; decoded successfully.`);
  return {...variation, ...selected, duration, requestHash, request: receipt.request,
    generatedAt: receipt.generatedAt, requestId: receipt.requestId, characterCost: receipt.characterCost,
    selection: 'First provider preview; listening decision remains with pilot.', previews};
}

if (mode !== '--check') {
  // Confirm the first request succeeds before starting the remaining pairs.
  const candidates = [await generate(jobs[0])];
  for (let i = 1; i < jobs.length; i += 2) {
    candidates.push(...await Promise.all(jobs.slice(i, i + 2).map(generate)));
  }
  assert.equal(new Set(candidates.map(c => c.sha256)).size, 5);
  assert.equal(new Set(candidates.map(c => c.generatedVoiceId)).size, 5);
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/2', status: 'awaiting-listening-selection',
    displayText, reference: {file: referencePath, sha256: referenceHash, label: 'Original C'},
    candidates, processing: 'Unmodified reference-conditioned provider previews; no effects or pitch changes.',
    filmChanged: false, permanentVoiceCreated: false,
  }, null, 2) + '\n');
}
