// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Refuse stale deliveries and prove the encoded film uses the approved take.
import assert from 'node:assert/strict';
import {readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build');
const json = async path => JSON.parse(await readFile(path, 'utf8'));
const sha = async path => createHash('sha256').update(await readFile(path)).digest('hex');
const approved = 'f237b17e6bc5be12732a8bab81c684bad52903f4212c555cb79bfcac7b582ec6';
const manifest = await json(resolve(build, 'rehearsal-manifest.json'));
const delivery = await json(resolve(base, 'delivery.json'));
assert.equal(await sha(resolve(build, 'leo-v3-direcao-85s.wav')), approved);
assert.equal(manifest.audio.length, 1, 'One whole performance, not spliced clips.');
const audio = manifest.audio[0];
assert.equal(audio.sha256, approved, 'The rendered film must use the approved v3 take.');
assert.equal(await sha(audio.file), approved);
assert.equal(audio.duration, 85.52);
assert.equal(manifest.episode.audio.model, 'eleven_v3');
assert.equal(manifest.episode.audio.voice, 'EbiSUflQjzm4g7S895SC');
assert.equal(manifest.episode.chapters[0].narration, delivery.text);
assert.equal(await sha(resolve(build, 'movie.json')), manifest.provenance.episodeSha256,
  'The encoded film must match the current directed movie, not an earlier render.');
for (const chapter of manifest.episode.chapters) {
  assert.ok(Object.values(chapter.elements).every(e => ['view', 'shade'].includes(e.kind)),
    'No on-screen text elements. Verify pixels separately.');
}
assert.equal(await sha(manifest.output), manifest.outputSha256, 'Stale MP4/manifest pair.');
const probeResult = spawnSync('ffprobe', ['-v', 'error', '-show_streams', '-show_format',
  '-of', 'json', manifest.output], {encoding: 'utf8'});
assert.equal(probeResult.status, 0, probeResult.stderr);
const probe = JSON.parse(probeResult.stdout);
const video = probe.streams.find(s => s.codec_type === 'video');
const sound = probe.streams.find(s => s.codec_type === 'audio');
assert.equal(probe.streams.length, 2, 'Video and audio only, no subtitle stream.');
assert.equal(video.codec_name, 'h264');
assert.equal(sound.codec_name, 'aac');
assert.equal(video.width, 1080);
assert.equal(video.height, 1920);
assert.equal(video.avg_frame_rate, '24/1');
const duration = Number(probe.format.duration);
assert.ok(duration < 90, 'The complete encoded film must be below 90 seconds.');
assert.ok(duration >= audio.offset + audio.duration, 'The complete take must fit.');
assert.equal(Number(video.nb_frames), Math.round(manifest.episode.output.durationSeconds * 24));
assert.equal(manifest.subtitles.burnedIn, false);
const subtitle = await readFile(manifest.subtitles.file, 'utf8');
const subtitleText = subtitle.split(/\r?\n/).filter(line =>
  line.trim() && !/^\d+$/.test(line) && !line.includes('-->')).join(' ');
const plain = text => text.replace(/\s+/g, ' ').trim();
assert.equal(plain(subtitleText), plain(delivery.text));
const decode = spawnSync('ffmpeg', ['-v', 'error', '-i', manifest.output,
  '-f', 'null', '-'], {encoding: 'utf8'});
assert.equal(decode.status, 0, decode.stderr);
const report = {checkedAt: new Date().toISOString(), output: manifest.output,
  sha256: manifest.outputSha256, duration, frames: Number(video.nb_frames),
  width: video.width, height: video.height, fps: 24,
  approvedAudioSha256: approved, completeApprovedTake: true,
  fullDecode: true, externalSubtitlesMatch: true,
  capturedFrames: manifest.cache.capturedFrames, reusedFrames: manifest.cache.reusedFrames,
  note: 'Integrity, transcript and format checks; inspect encoded pixels separately.'};
await writeFile(resolve(build, 'encoded-verification.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
