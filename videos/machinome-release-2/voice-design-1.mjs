// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One original-voice design request, three short closing-line auditions.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-1');
const [toolPath, mode] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 4 && [undefined, '--check', '--generate'].includes(mode));
const displayText = "I'm Machinome, and my purpose is to enable all machines to be open source. What do you want to build next?";
const request = {
  voice_description: 'An original adult androgynous voice, gender-neutral in vocal weight and resonance, neither distinctly masculine nor feminine. Native English with general American pronunciation. Studio quality. Machinome speaks from within the source: profound, grounded, contemplative and quietly alive. A centered middle-to-low register, rounded resonance, luminous upper overtones and a fine natural grain. Depth comes from steady presence, not a booming bass. Close, intimate, clear delivery with precise consonants and measured conversational rhythm. Quiet conviction on purpose; a small, sincere opening of curiosity on the final question. Restrained natural intonation, subtle warmth, a consistent ambiguous-gender identity. No whisper, announcer performance, theatrical gravitas or robotic effects.',
  model_id: 'eleven_ttv_v3',
  // This endpoint has no pronunciation-dictionary field. The listening text
  // retains the brand spelling; this alias follows the approved pronunciation.
  text: displayText.replace('Machinome', 'mah-SHEEN-ohm'),
  auto_generate_text: false,
  loudness: 0.5,
  seed: 20261003,
  guidance_scale: 5,
  stream_previews: false,
  should_enhance: false,
};
const endpoint = 'https://api.elevenlabs.io/v1/text-to-voice/design?output_format=mp3_44100_128';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const requestHash = hash(JSON.stringify({endpoint, request}));
assert.ok(request.text.length >= 100 && request.text.length <= 1000);
assert.ok(request.voice_description.length >= 20 && request.voice_description.length <= 1000);
assert.ok(!('reference_audio_base64' in request), 'Original design, not a clone.');
console.log(`Closing only: ${request.text.length} characters; original voice; film untouched.`);
if (mode !== '--check') {
  await mkdir(build, {recursive: true});
  let receipt;
  try { receipt = JSON.parse(await readFile(resolve(build, 'provider.json'), 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  if (!receipt) {
    assert.equal(mode, '--generate', 'No receipt cached. --generate makes one paid design request.');
    const tool = resolve(toolPath);
    const {keyFiles} = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(tool)) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (error) { if (error.code !== 'ENOENT') throw error; }
      if (key) break;
    }
    assert.ok(key, 'No ElevenLabs key configured; no request made.');
    // An interrupted or ambiguous purchase must be inspected, never retried.
    await writeFile(resolve(build, 'attempt.json'), JSON.stringify({requestHash, startedAt: new Date().toISOString()}) + '\n', {flag: 'wx'});
    console.log('Generating one batch of three closing-line previews. No automatic retry.');
    const response = await fetch(endpoint, {
      method: 'POST', headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000),
    });
    receipt = {requestHash, request, endpoint, status: response.status,
      requestId: response.headers.get('request-id'),
      characterCost: response.headers.get('character-cost'),
      generatedAt: new Date().toISOString(), body: await response.text()};
    // Persist before interpretation so recovery never buys another audition.
    await writeFile(resolve(build, 'provider.json'), JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log('Reusing the saved response; no provider request.');
  assert.equal(receipt.requestHash, requestHash, 'Changed direction requires a new audition batch.');
  assert.equal(receipt.status, 200, `Voice Design HTTP ${receipt.status}; receipt retained, no retry.`);
  const data = JSON.parse(receipt.body);
  assert.equal(data.text, request.text, 'Provider changed the preview text.');
  assert.equal(data.previews.length, 3, 'Inspect saved response; expected three previews.');
  assert.equal(new Set(data.previews.map(p => p.generated_voice_id)).size, 3);
  const candidates = [];
  for (const [index, preview] of data.previews.entries()) {
    assert.ok(preview.audio_base_64 && preview.generated_voice_id);
    const label = 'ABC'[index], file = `voice-${label}.mp3`;
    const bytes = Buffer.from(preview.audio_base_64, 'base64');
    assert.ok(bytes.length > 1000);
    try { await writeFile(resolve(build, file), bytes, {flag: 'wx'}); }
    catch (error) {
      if (error.code !== 'EEXIST') throw error;
      assert.equal(hash(await readFile(resolve(build, file))), hash(bytes));
    }
    const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', resolve(build, file)], {encoding: 'utf8'}));
    assert.equal(probe.streams.length, 1);
    assert.equal(probe.streams[0].codec_name, 'mp3');
    const duration = Number(probe.format.duration);
    assert.ok(duration > 3 && duration < 30);
    execFileSync('ffmpeg', ['-v', 'error', '-i', resolve(build, file), '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
    candidates.push({label, file, generatedVoiceId: preview.generated_voice_id,
      sha256: hash(bytes), duration, bytes: bytes.length});
    console.log(`${label}: ${duration.toFixed(2)} s, decoded successfully.`);
  }
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/1', status: 'awaiting-listening-selection',
    displayText, request, requestHash, generatedAt: receipt.generatedAt,
    requestId: receipt.requestId, characterCost: receipt.characterCost,
    candidates, processing: 'Unmodified provider previews; no effects or pitch changes.',
    filmChanged: false, permanentVoiceCreated: false,
  }, null, 2) + '\n');
}
