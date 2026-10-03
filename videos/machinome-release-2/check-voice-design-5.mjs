// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Pin the comparison words, selected C3 recording and matched Jessica control.
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
const manifest = await json('_build/voice-design-5/manifest.json');
const previous = await json('_build/voice-design-3/manifest.json');
const wrongTextRound = await json('_build/voice-design-4/manifest.json');
assert.equal(manifest.displayText, "I'm Machinome, and my purpose is to enable all machines to be open source. What do you want to build next?");
assert.equal(manifest.displayText, previous.displayText);
assert.equal(manifest.spokenText, previous.spokenText);
assert.equal(manifest.candidates.length, 5);
assert.equal(manifest.newVoicesCreated, 0);
assert.equal(manifest.selectedVoice.voiceId, 'JoOLJ0OHRwCg8Ydjc4IF');
assert.equal(manifest.jessica.voiceId, 'cgSgspJ2msm6clMCkdW9');
assert.deepEqual(manifest.candidates[0].request, manifest.jessica.request);
assert.equal(manifest.candidates[0].request.text, manifest.spokenText);
const {text: oldDirection, ...oldSettings} = previous.performance;
assert.deepEqual(manifest.fixedSettings, oldSettings);
const protectedHashes = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  ...wrongTextRound.source.sourceHashes,
};
for (const old of previous.candidates) protectedHashes[`_build/voice-design-3/${old.file}`] = old.sha256;
for (const old of wrongTextRound.candidates) protectedHashes[`_build/voice-design-4/${old.file}`] = old.sha256;
for (const [file, sha256] of Object.entries(protectedHashes)) {
  assert.equal(hash(await readFile(resolve(base, file))), sha256, `Changed original: ${file}`);
}
const allNew = [...manifest.candidates, manifest.jessica];
for (const candidate of allNew) {
  const receipt = await json(`_build/voice-design-5/${candidate.id}/speech.provider.json`);
  assert.ok(receipt.endpoint.includes(`/text-to-speech/${candidate.voiceId}/`));
  if (candidate.id !== 'jessica') assert.equal(candidate.voiceId, manifest.selectedVoice.voiceId);
  assert.deepEqual(receipt.request, candidate.request);
  const {text, ...settings} = candidate.request;
  assert.deepEqual(settings, manifest.fixedSettings);
  assert.equal(text.replace(/\[[^\]]*\]\s*/g, ''), manifest.spokenText);
  assert.ok((text.match(/\[/g) ?? []).length <= 1);
  assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(text));
  assert.equal(hash(await readFile(resolve(base, '_build/voice-design-5', candidate.file))), candidate.sha256);
}
const url = 'http://127.0.0.1:8782/voice-design-5.html';
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
  assert.equal(await page.locator('audio[data-new]').count(), 5);
  assert.equal(await page.locator('audio').count(), 7);
  await page.waitForFunction(() => [...document.querySelectorAll('audio')].every(a => a.readyState >= 1));
  for (let i = 0; i < 7; i++) {
    const player = page.locator('audio').nth(i);
    await player.evaluate(async audio => {audio.currentTime = 2; await audio.play();});
    await page.waitForFunction(index => {
      const audio = document.querySelectorAll('audio')[index];
      return audio.currentTime > 2.1 && !audio.paused && !audio.seeking;
    }, i);
    assert.equal(await page.locator('audio').evaluateAll(all => all.filter(a => !a.paused).length), 1);
    const sample = await player.evaluate(audio => ({id: audio.dataset.id, duration: audio.duration, url: audio.currentSrc}));
    const expected = sample.id === 'reference' ? manifest.selectedVoice.referenceDuration : allNew.find(c => c.id === sample.id).duration;
    assert.ok(Math.abs(sample.duration - expected) < 0.1);
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
  await writeFile(resolve(base, '_build/voice-design-5/player-report.json'), JSON.stringify({
    url, samples, protectedHashes, exactOriginalComparisonWords: true, selectedC3Untouched: true,
    jessicaMatchedToNaturalBaseline: true, rangeStatus: 206, mutualPause: true,
    links: true, narrowLayout: true, errors, listeningJudgment: 'Pending pilot review.',
  }, null, 2) + '\n');
  console.log('Exact original closing, C3 identity/reference and matched Jessica control verified. Seven players pass playback, seeking, range delivery, mutual pause, links and narrow layout. Film unchanged.');
} finally {await browser.close();}
