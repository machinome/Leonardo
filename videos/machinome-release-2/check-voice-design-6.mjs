// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify the Jessica input, same-line comparison and rejection of slow previews.
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
const manifest = await json('_build/voice-design-6/manifest.json');
const previous = await json('_build/voice-design-5/manifest.json');
const oldComparison = await json('_build/voice-design-4/manifest.json');
const receipt = await json('_build/voice-design-6/provider.json');
assert.equal(manifest.displayText, previous.displayText);
assert.equal(manifest.spokenText, previous.spokenText);
assert.equal(receipt.request.text, previous.spokenText);
assert.equal(JSON.parse(receipt.body).text, previous.spokenText);
assert.equal(receipt.reference.sha256, previous.jessica.sha256);
assert.equal(manifest.reference.file, `_build/voice-design-5/${previous.jessica.file}`);
assert.equal(manifest.reference.duration, previous.jessica.duration);
assert.equal(manifest.maximumOverrun, 0.05);
assert.equal(manifest.durationLimit, manifest.reference.duration * 1.05);
assert.deepEqual(manifest.candidates.map(c => c.id), ['J1', 'J2']);
assert.deepEqual(manifest.rejected.map(c => c.id), ['J3']);
assert.equal(manifest.permanentVoicesCreated, 0);
assert.deepEqual(manifest.candidates, manifest.previews.filter(c => c.duration <= manifest.durationLimit));
assert.deepEqual(manifest.rejected, manifest.previews.filter(c => c.duration > manifest.durationLimit));
for (const candidate of manifest.previews) {
  assert.equal(candidate.pacePass, candidate.duration <= manifest.durationLimit);
  assert.ok(Math.abs(candidate.durationChangePercent - 100 * (candidate.duration / manifest.reference.duration - 1)) < 1e-9);
  assert.equal(hash(await readFile(resolve(base, '_build/voice-design-6', candidate.file))), candidate.sha256);
}
const protectedHashes = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  [manifest.reference.file]: manifest.reference.sha256,
  [previous.selectedVoice.referenceFile]: previous.selectedVoice.referenceSha256,
  ...oldComparison.source.sourceHashes,
};
for (const old of previous.candidates) protectedHashes[`_build/voice-design-5/${old.file}`] = old.sha256;
for (const [file, sha256] of Object.entries(protectedHashes)) {
  assert.equal(hash(await readFile(resolve(base, file))), sha256, `Changed original: ${file}`);
}
const url = 'http://127.0.0.1:8782/voice-design-6.html';
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 1000}});
  const errors = [], samples = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && !response.url().endsWith('/favicon.ico')) errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto(url);
  assert.equal(await page.locator('#transcript').textContent(), manifest.displayText);
  assert.equal(await page.locator('audio').count(), 3);
  assert.deepEqual(await page.locator('audio[data-new]').evaluateAll(all => all.map(a => a.dataset.id)), ['J1', 'J2']);
  assert.equal(await page.locator('[src*="J3"], [href*="J3"]').count(), 0);
  await page.waitForFunction(() => [...document.querySelectorAll('audio')].every(a => a.readyState >= 1));
  for (let i = 0; i < 3; i++) {
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
    if (i > 0) assert.ok(sample.duration <= manifest.durationLimit);
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
  await writeFile(resolve(base, '_build/voice-design-6/player-report.json'), JSON.stringify({
    url, samples, protectedHashes, maximumOverrun: manifest.maximumOverrun,
    rejectedNotOffered: ['J3'], rangeStatus: 206, mutualPause: true, links: true, narrowLayout: true,
    errors, listeningJudgment: 'Pending pilot review; duration alone does not prove cadence or timbre.',
  }, null, 2) + '\n');
  console.log('Jessica reference verified; J1/J2 pass +5% duration gate; J3 excluded. Same words, three players, seeking, byte ranges, links and narrow layout pass. Film and earlier audio unchanged.');
} finally {await browser.close();}
