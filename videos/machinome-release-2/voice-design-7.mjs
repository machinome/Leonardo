// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Five small J1 variations; Jessica remains the fixed pacing anchor.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';
import {execFileSync} from 'node:child_process';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build/voice-design-7');
const [toolPath, mode, batchArgument] = process.argv.slice(2);
assert.ok(toolPath, 'Pass the explicit Videomaker checkout.');
assert.ok(process.argv.length <= 5 && [undefined, '--check', '--generate'].includes(mode));
assert.ok(mode === '--generate' ? /^[12345]$/.test(batchArgument ?? '') : batchArgument === undefined,
  'Use --generate with a batch number; later batches require an insufficient completed audition pool.');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const json = async file => JSON.parse(await readFile(resolve(base, file), 'utf8'));
const previous = await json('_build/voice-design-6/manifest.json');
const selected = previous.candidates.find(c => c.id === 'J1');
assert.equal(selected.generatedVoiceId, 'YGtltqiF9TGj7nEE9dIi');
const referenceFile = `_build/voice-design-6/${selected.file}`;
const reference = await readFile(resolve(base, referenceFile));
assert.equal(hash(reference), '22779c29223816244a04328860ab44ba61611ba653cac70d16d2cab69d85d545');
assert.equal(hash(reference), selected.sha256);
const paceAnchor = previous.reference;
assert.equal(paceAnchor.label, 'Jessica');
assert.equal(paceAnchor.sha256, '53092b1e8c05ecaf3d661bbe425164fd4aa39921ac5a507a756d4c6638242237');
assert.equal(hash(await readFile(resolve(base, paceAnchor.file))), paceAnchor.sha256);
const displayText = "I'm Machinome, and my purpose is to enable all machines to be open source. What do you want to build next?";
const text = displayText.replace('Machinome', 'mah-SHEEN-ohm');
assert.equal(previous.displayText, displayText);
assert.equal(previous.spokenText, text);
const maximumOverrun = 0.05;
const durationProbe = file => JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', file], {encoding: 'utf8'}));
const referenceDuration = Number(durationProbe(resolve(base, referenceFile)).format.duration);
const anchorDuration = Number(durationProbe(resolve(base, paceAnchor.file)).format.duration);
assert.ok(Math.abs(referenceDuration - selected.duration) < 0.001);
assert.equal(anchorDuration, paceAnchor.duration);
const durationLimit = anchorDuration * (1 + maximumOverrun);
assert.equal(durationLimit, previous.durationLimit, 'Never compound the allowance from J1.');
const endpoint = 'https://api.elevenlabs.io/v1/text-to-voice/design?output_format=mp3_44100_128';
const description = 'Make a small variation of the reference voice, keeping its recognizable character, natural English pronunciation and brisk connected delivery. Move its timbre a little further toward an adult androgynous, gender-ambiguous voice: slightly rounder and firmer resonance, less delicately feminine, while retaining the clear bright edge and comfortable pitch area. Add a modest spark of genuine excitement and eager, confident engagement, like a capable maker inviting someone to build something together. A little more animated melodic movement and a lively lift in the final question, still conversational and unforced. Compact phrases, crisp consonants, brief pauses and forward momentum. Keep the entire reading in the same roughly eight-second span as the reference. Clean dry studio sound.';
assert.ok(description.length >= 20 && description.length <= 1000);
assert.ok(text.length >= 100 && text.length <= 1000);
assert.ok(!/profound|solemn|contemplative|gravitas|whisper|bass|low register/i.test(description));
// Batches 1–2 yielded only one passing preview. Preserve them exactly and make
// the next requests explicit about excitement through momentum, not elongation.
const briskDescription = 'Use the reference voice with only a small timbre change: a little less feminine, more adult androgynous, slightly firmer and rounder resonance, keeping its bright clarity and comfortable pitch. Brisk, energetic, natural and confident. A small spark of excitement about making things together. Speak like a quick spontaneous invitation, with crisp attacks and connected phrases. Express excitement through forward momentum and lively articulation. Short vowels, quick transitions, just one brief pause before the final question. Keep the question quick and inviting. Deliver these exact words in about eight seconds, aiming for 7.8 to 8.2 seconds overall. Retain the reference character and English pronunciation. Clean dry studio sound.';
assert.ok(briskDescription.length >= 20 && briskDescription.length <= 1000);
const requestFor = batch => ({
  voice_description: batch <= 2 ? description : briskDescription, model_id: 'eleven_ttv_v3', text, auto_generate_text: false,
  loudness: 0.5, seed: 202610070 + batch, guidance_scale: 2,
  stream_previews: false, should_enhance: false,
  reference_audio_base64: reference.toString('base64'), prompt_strength: batch <= 2 ? 0.35 : 0.45,
});
const requestHashFor = batch => hash(JSON.stringify({endpoint, request: requestFor(batch)}));
console.log(`J1 reference ${referenceDuration.toFixed(2)} s; Jessica anchor ${anchorDuration.toFixed(2)} s; unchanged limit ${durationLimit.toFixed(2)} s. Same closing words.`);

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
async function decode(batch, receipt) {
  assert.equal(receipt.requestHash, requestHashFor(batch), 'Changed prompt/reference needs a new cache.');
  assert.equal(receipt.status, 200, `Voice Design HTTP ${receipt.status}; receipt retained, no retry.`);
  const data = JSON.parse(receipt.body);
  assert.equal(data.text, text);
  assert.equal(data.previews.length, 3);
  const previews = [];
  for (const [index, preview] of data.previews.entries()) {
    assert.ok(preview.audio_base_64 && preview.generated_voice_id);
    const sourceId = `B${batch}-${index + 1}`;
    const file = `batch-${batch}/${sourceId}.mp3`;
    const bytes = Buffer.from(preview.audio_base_64, 'base64');
    const path = resolve(build, file);
    await preserve(path, bytes);
    const probe = durationProbe(path);
    assert.equal(probe.streams.length, 1);
    assert.equal(probe.streams[0].codec_name, 'mp3');
    const duration = Number(probe.format.duration);
    assert.ok(duration > 3 && duration < 25);
    execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'null', '-'], {stdio: ['ignore', 'pipe', 'pipe']});
    const durationChangePercent = 100 * (duration / anchorDuration - 1);
    const pacePass = duration <= durationLimit;
    previews.push({sourceId, batch, file, generatedVoiceId: preview.generated_voice_id,
      sha256: hash(bytes), bytes: bytes.length, duration, durationChangePercent, pacePass});
    console.log(`${sourceId}: ${duration.toFixed(2)} s (${durationChangePercent >= 0 ? '+' : ''}${durationChangePercent.toFixed(1)}% vs Jessica); duration gate ${pacePass ? 'PASS' : 'FAIL'}.`);
  }
  return previews;
}

if (mode === '--generate') {
  const batch = Number(batchArgument);
  const directory = resolve(build, `batch-${batch}`);
  await mkdir(directory, {recursive: true});
  const receiptPath = resolve(directory, 'provider.json');
  let receipt = await optionalJSON(receiptPath);
  if (!receipt) {
    if (batch >= 3) {
      const completed = [];
      for (const earlier of batch === 5 ? [1, 2, 3, 4] : [1, 2]) {
        const earlierReceipt = await optionalJSON(resolve(build, `batch-${earlier}/provider.json`));
        assert.ok(earlierReceipt, 'Finish the preceding audition batches before considering a reserve.');
        completed.push(...await decode(earlier, earlierReceipt));
      }
      assert.ok(completed.filter(c => c.pacePass).length < 5, 'Five passing previews already exist; no reserve request allowed.');
    }
    const {keyFiles} = await import(pathToFileURL(resolve(toolPath, 'src/speech.mjs')));
    let key = process.env.ELEVENLABS_API_KEY;
    if (key === undefined) for (const path of keyFiles(resolve(toolPath))) {
      try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
      catch (error) { if (error.code !== 'ENOENT') throw error; }
      if (key) break;
    }
    assert.ok(key, 'No ElevenLabs key configured; no request made.');
    const request = requestFor(batch), requestHash = requestHashFor(batch);
    await writeFile(resolve(directory, 'attempt.json'), JSON.stringify({requestHash, startedAt: new Date().toISOString()}) + '\n', {flag: 'wx'});
    console.log(`Generating batch ${batch} from J1 audio; no automatic retry.`);
    const response = await fetch(endpoint, {method: 'POST',
      headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
      body: JSON.stringify(request), signal: AbortSignal.timeout(240000)});
    receipt = {requestHash, endpoint, request: {...request, reference_audio_base64: undefined},
      reference: {file: referenceFile, sha256: hash(reference)}, status: response.status,
      requestId: response.headers.get('request-id'), characterCost: response.headers.get('character-cost'),
      generatedAt: new Date().toISOString(), body: await response.text()};
    await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
  } else console.log(`Using saved batch ${batch}; no provider request.`);
  await decode(batch, receipt);
} else if (mode !== '--check') {
  const previews = [], batches = [];
  for (const batch of [1, 2, 3, 4, 5]) {
    const receipt = await optionalJSON(resolve(build, `batch-${batch}/provider.json`));
    if (!receipt) {
      assert.ok(batch > 2, `Missing batch ${batch}; use --generate ${batch} explicitly.`);
      continue;
    }
    previews.push(...await decode(batch, receipt));
    batches.push({batch, requestHash: receipt.requestHash, request: receipt.request,
      generatedAt: receipt.generatedAt, requestId: receipt.requestId});
  }
  assert.equal(new Set(previews.map(c => c.sha256)).size, previews.length);
  assert.equal(new Set(previews.map(c => c.generatedVoiceId)).size, previews.length);
  const passing = previews.filter(c => c.pacePass);
  assert.ok(passing.length >= 5, `Only ${passing.length} previews meet the unchanged pacing limit; no comparison assembled.`);
  const candidates = passing.slice(0, 5).map((c, i) => ({...c, id: `J1-${'ABCDE'[i]}`}));
  await mkdir(build, {recursive: true});
  for (const candidate of candidates) {
    candidate.sourceFile = candidate.file;
    candidate.file = `${candidate.id}.mp3`;
    await preserve(resolve(build, candidate.file), await readFile(resolve(build, candidate.sourceFile)));
  }
  await writeFile(resolve(build, 'manifest.json'), JSON.stringify({
    schema: 'machinome-voice-audition/7', status: 'awaiting-listening-review',
    displayText, spokenText: text, batches,
    reference: {label: 'J1', file: referenceFile, sha256: hash(reference), duration: referenceDuration, generatedVoiceId: selected.generatedVoiceId},
    paceAnchor, maximumOverrun, durationLimit, previews, candidates,
    rejected: previews.filter(c => !c.pacePass), spare: passing.slice(5),
    selectionRule: 'First five duration-passing previews in batch/response order; not ranked by listening or fastest duration.',
    method: 'J1 audio conditions small variations toward less feminine timbre and modestly more excitement. Batches 1–2 use the initial prompt; later batches explicitly tighten momentum after the first timing results. Jessica anchors the unchanged duration gate.',
    processing: 'Unmodified provider previews; no time stretching, pitch filters, edits or effects.',
    permanentVoicesCreated: 0, filmChanged: false,
    limitations: 'Duration is a pacing gate, not proof of exact cadence, excitement, spoken accuracy or perceived gender neutrality. A selected preview still needs ordinary TTS and full-narration timing verification.',
  }, null, 2) + '\n');
  console.log(`Five variations assembled from ${previews.length} raw previews. ${previews.filter(c => !c.pacePass).length} over-limit, ${passing.length - 5} spare. No provider request during assembly.`);
}
