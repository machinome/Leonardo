// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Import one approved take for this empirical edit. No network or synthesis.
import assert from 'node:assert/strict';
import { readFile, copyFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker repository path');
const tool = resolve(process.argv[2]);
const { loadEpisode } = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const { fileHash, json, duration } = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
const { mixSpeech } = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const { captionsFromAlignment, srt } = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const episode = await loadEpisode(resolve(base, 'episode.yaml'));
assert.equal(episode.shots.length, 1);
assert.equal(episode.output.durationSeconds, 28);
const audition = resolve(base, '../machinome-pronunciation/_build/phoneme');
const take = JSON.parse(await readFile(resolve(audition, 'sample.json'), 'utf8'));
const approvedHash = 'b61dc2bab1c168dfffb4644fac4d6407fff31d7a5ff081adfd2df444af511750';
const source = resolve(audition, 'sample.wav');
assert.equal(await fileHash(source), approvedHash, 'Not the approved take');
assert.equal(take.wavSha256, approvedHash);
assert.equal(take.request.text, episode.shots[0].narration);
assert.equal(take.recipe.audio.voice, episode.audio.voice);
assert.equal(take.request.model_id, episode.audio.model);
assert.deepEqual(take.request.voice_settings, episode.audio.voiceSettings);
assert.deepEqual(episode.audio.replacements, {});
assert.equal(take.request.pronunciation_dictionary_locators.length, 1);
const seconds = await duration(source);
assert.equal(seconds, take.durationSeconds);
const shot = episode.shots[0];
const offset = shot.start + shot.speechOffset;
assert.ok(offset >= 0 && offset + seconds <= shot.end - 0.1, 'Take does not fit');
const dir = resolve(episode.paths.build, 'audio');
await mkdir(dir, { recursive: true });
const file = resolve(dir, `approved-phoneme-${approvedHash.slice(0, 16)}.wav`);
await copyFile(source, file);
await json(file + '.json', {
  importedFrom: source, approval: 'Pilot approved full-context phoneme audition',
  voice: episode.audio.voice, model: episode.audio.model,
  format: take.recipe.audio.outputFormat, request: take.request,
  alignment: take.alignment, sha256: approvedHash, duration: seconds,
});
const records = [{ id: shot.id, file, sha256: approvedHash, duration: seconds, offset }];
const captions = captionsFromAlignment(take.alignment, offset);
await json(resolve(episode.paths.build, 'captions.json'), captions);
await writeFile(resolve(episode.paths.build, 'captions.srt'), srt(captions));
const mix = resolve(episode.paths.build, 'narration.wav');
await mixSpeech(records, episode.output.durationSeconds, mix);
await json(resolve(episode.paths.build, 'audio-manifest.json'), {
  provider: episode.audio.provider, importedApprovedTake: true,
  records, mixSha256: await fileHash(mix),
});
console.log(JSON.stringify({ seconds, offset, approvedHash, mix }));
