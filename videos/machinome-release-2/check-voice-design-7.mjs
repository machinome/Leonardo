// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify five J1-derived samples, a fixed Jessica timing gate and preservation.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {createRequire} from 'node:module';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker checkout.');
const require = createRequire(resolve(process.argv[2], 'package.json'));
const {chromium} = require('playwright');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const json = async file => JSON.parse(await readFile(resolve(base, file), 'utf8'));
const manifest = await json('_build/voice-design-7/manifest.json');
const previous = await json('_build/voice-design-6/manifest.json');
const earlier = await json('_build/voice-design-5/manifest.json');
const oldComparison = await json('_build/voice-design-4/manifest.json');
assert.equal(manifest.displayText, previous.displayText);
assert.equal(manifest.spokenText, previous.spokenText);
assert.equal(manifest.reference.label, 'J1');
assert.equal(manifest.reference.file, '_build/voice-design-6/J1.mp3');
assert.equal(manifest.reference.sha256, previous.candidates[0].sha256);
assert.equal(manifest.reference.generatedVoiceId, 'YGtltqiF9TGj7nEE9dIi');
assert.equal(manifest.reference.duration, previous.candidates[0].duration);
assert.deepEqual(manifest.paceAnchor, previous.reference);
assert.equal(manifest.maximumOverrun, 0.05);
assert.equal(manifest.durationLimit, manifest.paceAnchor.duration * 1.05);
assert.equal(manifest.durationLimit, previous.durationLimit);
assert.equal(manifest.permanentVoicesCreated, 0);
assert.equal(manifest.filmChanged, false);
const ids = ['J1-A', 'J1-B', 'J1-C', 'J1-D', 'J1-E'];
assert.deepEqual(manifest.candidates.map(c => c.id), ids);
const passing = manifest.previews.filter(c => c.duration <= manifest.durationLimit);
assert.deepEqual(manifest.candidates.map(c => c.sourceId), passing.slice(0, 5).map(c => c.sourceId));
assert.deepEqual(manifest.spare, passing.slice(5));
assert.deepEqual(manifest.rejected, manifest.previews.filter(c => c.duration > manifest.durationLimit));
for (const batch of manifest.batches) {
  const receipt = await json(`_build/voice-design-7/batch-${batch.batch}/provider.json`);
  assert.equal(receipt.requestHash, batch.requestHash);
  assert.deepEqual(receipt.request, batch.request);
  assert.equal(receipt.request.text, manifest.spokenText);
  assert.equal(JSON.parse(receipt.body).text, manifest.spokenText);
  assert.equal(receipt.reference.sha256, manifest.reference.sha256);
  assert.equal(receipt.reference.file, manifest.reference.file);
  assert.equal(receipt.request.prompt_strength, batch.batch <= 2 ? 0.35 : 0.45);
  assert.equal(receipt.request.model_id, 'eleven_ttv_v3');
  assert.equal(receipt.request.seed, 202610070 + batch.batch);
  assert.equal(receipt.request.auto_generate_text, false);
  const request = {...receipt.request, reference_audio_base64: (await readFile(resolve(base, manifest.reference.file))).toString('base64')};
  // Property order is significant to the original cache hash.
  const {prompt_strength, ...rest} = request;
  assert.equal(hash(JSON.stringify({endpoint: receipt.endpoint, request: {...rest, prompt_strength}})), receipt.requestHash);
  for (const [index, raw] of JSON.parse(receipt.body).previews.entries()) {
    const preview = manifest.previews.find(p => p.sourceId === `B${batch.batch}-${index + 1}`);
    assert.equal(preview.sha256, hash(Buffer.from(raw.audio_base_64, 'base64')));
    assert.equal(preview.generatedVoiceId, raw.generated_voice_id);
  }
}
for (const candidate of [...manifest.previews, ...manifest.candidates]) {
  assert.equal(candidate.pacePass, candidate.duration <= manifest.durationLimit);
  assert.ok(Math.abs(candidate.durationChangePercent - 100 * (candidate.duration / manifest.paceAnchor.duration - 1)) < 1e-9);
  assert.equal(hash(await readFile(resolve(base, '_build/voice-design-7', candidate.file))), candidate.sha256);
  if (candidate.sourceFile) assert.equal(hash(await readFile(resolve(base, '_build/voice-design-7', candidate.sourceFile))), candidate.sha256);
}
const protectedHashes = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  [manifest.reference.file]: manifest.reference.sha256,
  [manifest.paceAnchor.file]: manifest.paceAnchor.sha256,
  [earlier.selectedVoice.referenceFile]: earlier.selectedVoice.referenceSha256,
  ...oldComparison.source.sourceHashes,
};
for (const old of previous.previews) protectedHashes[`_build/voice-design-6/${old.file}`] = old.sha256;
for (const old of earlier.candidates) protectedHashes[`_build/voice-design-5/${old.file}`] = old.sha256;
for (const [file, sha256] of Object.entries(protectedHashes)) {
  assert.equal(hash(await readFile(resolve(base, file))), sha256, `Changed original: ${file}`);
}
const url = 'http://127.0.0.1:8782/voice-design-7.html';
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 1200}});
  const errors = [], samples = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && !response.url().endsWith('/favicon.ico')) errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto(url);
  assert.equal(await page.locator('#transcript').textContent(), manifest.displayText);
  assert.equal(await page.locator('audio').count(), 6);
  assert.deepEqual(await page.locator('audio[data-new]').evaluateAll(all => all.map(a => a.dataset.id)), ids);
  for (const excluded of [...manifest.rejected, ...manifest.spare]) {
    assert.equal(await page.locator(`[src*="${excluded.file}"], [href*="${excluded.file}"]`).count(), 0);
  }
  await page.waitForFunction(() => [...document.querySelectorAll('audio')].every(a => a.readyState >= 1));
  for (let i = 0; i < 6; i++) {
    const player = page.locator('audio').nth(i);
    await player.evaluate(async audio => {audio.currentTime = 2; await audio.play();});
    await page.waitForFunction(index => {
      const audio = document.querySelectorAll('audio')[index];
      return audio.currentTime > 2.1 && !audio.paused && !audio.seeking;
    }, i);
    assert.equal(await page.locator('audio').evaluateAll(all => all.filter(a => !a.paused).length), 1);
    const sample = await player.evaluate(audio => ({id: audio.dataset.id, duration: audio.duration, url: audio.currentSrc,
      displayedDuration: Number(audio.closest('section').querySelector('[data-duration]').dataset.duration)}));
    const expected = i === 0 ? manifest.reference.duration : manifest.candidates[i - 1].duration;
    assert.ok(Math.abs(sample.duration - expected) < 0.1);
    assert.equal(sample.displayedDuration, expected);
    assert.ok(sample.duration <= manifest.durationLimit);
    const range = await fetch(sample.url, {headers: {Range: 'bytes=1000-1999'}});
    assert.equal(range.status, 206);
    assert.equal((await range.arrayBuffer()).byteLength, 1000);
    samples.push(sample);
  }
  await page.locator('audio').evaluateAll(all => all.forEach(a => a.pause()));
  for (const link of await page.locator('a').all()) {
    const href = new URL(await link.getAttribute('href'), url).href;
    assert.ok((await page.request.head(href)).ok(), `Broken link: ${href}`);
  }
  await page.setViewportSize({width: 390, height: 844});
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  assert.deepEqual(errors, []);
  await writeFile(resolve(base, '_build/voice-design-7/player-report.json'), JSON.stringify({
    url, samples, protectedHashes, maximumOverrun: manifest.maximumOverrun,
    excludedNotOffered: [...manifest.rejected, ...manifest.spare].map(c => c.sourceId),
    rangeStatus: 206, mutualPause: true, links: true, narrowLayout: true, errors,
    listeningJudgment: 'Pending pilot review; duration alone does not prove cadence, excitement or timbre.',
  }, null, 2) + '\n');
  console.log('Five J1 variations verified against the unchanged Jessica pacing limit. Same words, six players, seeking, byte ranges, links and narrow layout pass. Film and earlier audio unchanged.');
} finally {await browser.close();}
