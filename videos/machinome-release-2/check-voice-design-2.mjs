// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Technical playback and preservation checks; not an auditory assessment.
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
const url = 'http://127.0.0.1:8782/voice-design-2.html';
const manifest = JSON.parse(await readFile(resolve(base, '_build/voice-design-2/manifest.json'), 'utf8'));
assert.equal(manifest.candidates.length, 5);
const expected = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  '_build/voice-design-1/voice-C.mp3': manifest.reference.sha256,
};
for (const [file, sha256] of Object.entries(expected)) {
  assert.equal(createHash('sha256').update(await readFile(resolve(base, file))).digest('hex'), sha256, `Changed original: ${file}`);
}
for (const candidate of manifest.candidates) {
  assert.notEqual(candidate.sha256, manifest.reference.sha256);
  const actual = createHash('sha256').update(await readFile(resolve(base, '_build/voice-design-2', candidate.file))).digest('hex');
  assert.equal(actual, candidate.sha256);
}
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 1000}});
  const errors = [], samples = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && !response.url().endsWith('/favicon.ico')) errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto(url);
  await page.locator('summary').click();
  assert.equal(await page.locator('audio').count(), 6);
  await page.waitForFunction(() => [...document.querySelectorAll('audio')].every(a => a.readyState >= 1));
  for (let i = 0; i < 6; i++) {
    const player = page.locator('audio').nth(i);
    await player.evaluate(async audio => {audio.currentTime = 2; await audio.play();});
    await page.waitForFunction(index => {
      const audio = document.querySelectorAll('audio')[index];
      return audio.currentTime > 2.1 && !audio.paused && !audio.seeking;
    }, i);
    assert.equal(await page.locator('audio').evaluateAll(all => all.filter(a => !a.paused).length), 1);
    const sample = await player.evaluate(audio => ({label: audio.getAttribute('aria-label'), duration: audio.duration, url: audio.currentSrc}));
    assert.ok(Math.abs(sample.duration - (i === 0 ? 11.15425 : manifest.candidates[i - 1].duration)) < 0.1);
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
  const report = {url, samples, originalHashes: expected, rangeStatus: 206, mutualPause: true,
    links: true, narrowLayout: true, errors, listeningJudgment: 'Pending pilot review'};
  await writeFile(resolve(base, '_build/voice-design-2/player-report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log('Five variations and original C passed playback, seeking, mutual pause, range delivery, links and mobile layout. Film, narration and C unchanged.');
} finally {await browser.close();}
