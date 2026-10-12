// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// One full-script request, using Videomaker's cache and alignment contracts.
import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {parseEnv} from 'node:util';

const base = dirname(fileURLToPath(import.meta.url));

export function verifyInput(input) {
  assert.equal(input.format, 'machinome-release-narration/1');
  assert.equal(input.chapters.length, 1, 'The performance must be one take.');
  assert.equal(input.chapters[0].id, 'continuous');
  const text = input.chapters[0].narration;
  assert.ok(typeof text === 'string' && text.length > 0 && text.length <= 5000);
  assert.equal(input.audio.model, 'eleven_v3');
  assert.equal(input.audio.outputFormat, 'pcm_24000');
  assert.ok(!/©|copyright|licen[cs]e|vibecoded|made with|created by|written by|\b(?:AGPL|GPL|MIT|BSD|CERN-OHL)\b/i.test(text), 'Credit in spoken text.');
  assert.ok(!/Here is one of its relationships|Different ways to describe/.test(text));
  assert.equal(new Set(input.beats.map(b => b.id)).size, input.beats.length);
  for (const beat of input.beats) {
    assert.equal(text.split(beat.phrase).length, 2, `Missing/ambiguous beat: ${beat.id}`);
  }
  return text;
}

export function resolveBeats(alignment, beats, duration) {
  const text = alignment.characters.join('');
  return beats.map(beat => {
    const at = text.indexOf(beat.phrase);
    assert.ok(at >= 0 && text.indexOf(beat.phrase, at + 1) < 0, `Recorded beat missing/ambiguous: ${beat.id}`);
    const first = Array.from(text.slice(0, at)).length;
    const last = first + Array.from(beat.phrase).length - 1;
    const start = alignment.character_start_times_seconds[first];
    const end = alignment.character_end_times_seconds[last];
    assert.ok(Number.isFinite(start) && start >= 0 && end >= start && end <= duration + 0.05);
    return {...beat, start, end};
  });
}

async function optionalJSON(path) {
  try { return JSON.parse(await readFile(path, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; return null; }
}

export async function main(args) {
  assert.ok(args[0], 'Pass the explicit Videomaker checkout.');
  assert.ok(args.length <= 2 && (!args[1] || ['--check', '--generate'].includes(args[1])), 'Use --check or --generate; without either, reuse only.');
  const tool = resolve(args[0]), build = resolve(base, '_build');
  const {speechCacheEntry, spokenChapters, pcmWav, keyFiles} = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
  const {hash, fileHash} = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
  const {validateAlignment} = await import(pathToFileURL(resolve(tool, 'src/words.mjs')));
  const {captionsFromAlignment, srt} = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
  const input = JSON.parse(await readFile(resolve(build, 'narration-input.json'), 'utf8'));
  const text = verifyInput(input);
  assert.ok(text.includes('What do YOU want to BUILD?'));
  assert.ok(text.includes('And beneath it all, a stream of open source technologies... The wheel... makes revolutions'));
  assert.ok(text.includes('Machinome also provides a testing framework, that allows us to test how parts fit together.'));
  assert.ok(text.includes('You can build models from your browser, using Machinome Studio'));
  assert.ok(!text.includes('Agents can write mechanical models because of tests'));
  const dictionary = JSON.parse(await readFile(resolve(base, input.pronunciation), 'utf8'));
  assert.equal(dictionary.rules[0].phoneme, 'məˈʃiːnoʊm');
  const film = {...input, paths: {build}};
  const entry = speechCacheEntry(film, spokenChapters(film), 0);
  const request = {...entry.request, pronunciation_dictionary_locators: [{
    pronunciation_dictionary_id: dictionary.id, version_id: dictionary.version_id,
  }]};
  assert.ok(!request.previous_text && !request.next_text);
  assert.ok(request.text.includes('technologies...\n\nThe wheel'));
  const productionRequestHash = hash(JSON.stringify({request, voice: input.audio.voice, format: entry.format}));
  console.log(`One ${text.length}-character request; ${input.beats.length} unique beats; Jessica / eleven_v3.`);
  if (args[1] === '--check') return;
  await mkdir(resolve(build, 'audio'), {recursive: true});
  const receiptPath = entry.file + '.provider.json';
  let record = await optionalJSON(entry.meta);
  if (record) {
    assert.equal(record.productionRequestHash, productionRequestHash, 'Request/dictionary changed; retain the old take and choose a new cache.');
    assert.equal(record.sha256, await fileHash(entry.file), 'Cached speech bytes changed.');
    console.log('Reusing the continuous take; no request made.');
  } else {
    let receipt = await optionalJSON(receiptPath);
    if (!receipt) {
      assert.equal(args[1], '--generate', 'No take cached. Use --generate to make the single paid request.');
      let key = process.env.ELEVENLABS_API_KEY;
      if (key === undefined) for (const path of keyFiles(tool)) {
        try { key = parseEnv(await readFile(path, 'utf8')).ELEVENLABS_API_KEY; }
        catch (error) { if (error.code !== 'ENOENT') throw error; }
        if (key) break;
      }
      assert.ok(key, 'No ElevenLabs key configured; no request made.');
      console.log('Generating the entire performance in one provider request.');
      // No automatic retry: a failed/ambiguous paid call must be inspected.
      const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(input.audio.voice)}/with-timestamps?output_format=pcm_24000`, {
        method: 'POST', headers: {'xi-api-key': key, 'Content-Type': 'application/json'},
        body: JSON.stringify(request), signal: AbortSignal.timeout(240000),
      });
      const body = await response.text();
      assert.ok(response.ok, `Speech HTTP ${response.status}; no automatic retry (key and response omitted).`);
      // Keep the exact successful response before interpretation. Recovery
      // uses this receipt rather than purchasing the same performance again.
      receipt = {productionRequestHash, request, voice: input.audio.voice,
        requestId: response.headers.get('request-id'),
        characterCost: response.headers.get('character-cost'),
        generatedAt: new Date().toISOString(), body};
      await writeFile(receiptPath, JSON.stringify(receipt) + '\n', {flag: 'wx'});
    }
    assert.equal(receipt.productionRequestHash, productionRequestHash);
    const data = JSON.parse(receipt.body);
    assert.ok(data.audio_base64, 'Provider returned no audio; response retained.');
    const originalPCM = Buffer.from(data.audio_base64, 'base64');
    const canonical = value => value.replace(/\s+/gu, ' ').trim();
    const alignment = [data.normalized_alignment, data.alignment].find(a =>
      a?.characters && canonical(a.characters.join('')) === canonical(text));
    assert.ok(alignment, 'Provider text differs from the script; response retained, no retry.');
    validateAlignment(alignment, 'continuous');
    // The pause belongs to the performance. Never splice digital silence into
    // a breath or phoneme: the film follows this continuous provider signal.
    await writeFile(resolve(build, 'provider-original.wav'), pcmWav(originalPCM, 24000));
    const pcm = originalPCM;
    const wav = pcmWav(pcm, 24000);
    const edits = [];
    const duration = pcm.length / 48000;
    assert.ok(alignment.character_end_times_seconds.at(-1) <= duration + 0.05);
    resolveBeats(alignment, input.beats, duration);
    await writeFile(entry.file, wav, {flag: 'wx'});
    record = {cache: entry.cache, voice: input.audio.voice, model: input.audio.model,
      format: entry.format, request, productionRequestHash, pronunciation: dictionary,
      alignment, sha256: hash(wav), duration, requestId: receipt.requestId,
      generatedAt: receipt.generatedAt, source: 'one-provider-request-unedited', edits};
    await writeFile(entry.meta, JSON.stringify(record, null, 2) + '\n', {flag: 'wx'});
  }
  validateAlignment(record.alignment, 'continuous');
  const beats = resolveBeats(record.alignment, input.beats, record.duration);
  const captions = captionsFromAlignment(record.alignment);
  // This listening copy is byte-identical to the provider's continuous take.
  await writeFile(resolve(build, 'narration.wav'), await readFile(entry.file));
  await writeFile(resolve(build, 'captions.srt'), srt(captions));
  await writeFile(resolve(build, 'captions.json'), JSON.stringify(captions, null, 2) + '\n');
  const manifest = {schema: 'continuous-narration-review/1', status: 'awaiting-listening-review',
    source: 'narration.py', sourceSha256: await fileHash(resolve(base, 'narration.py')),
    text, characters: text.length, generation: record.source, edits: record.edits,
    duration: record.duration, sha256: record.sha256, cacheFile: entry.file,
    productionRequestHash, providerRequestId: record.requestId, generatedAt: record.generatedAt,
    voice: input.audio, audioTimeOrigin: 0, filmLeadIn: 'not yet placed',
    captions: captions.length, beats};
  await writeFile(resolve(build, 'narration-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(`Continuous WAV: ${record.duration.toFixed(2)} s; ${captions.length} captions; ${beats.length} measured beats.`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main(process.argv.slice(2));
}
