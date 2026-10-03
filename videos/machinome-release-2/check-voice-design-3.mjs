// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify saved identity bindings, shared performance, playback and preservation.
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
const manifest = await json('_build/voice-design-3/manifest.json');
const previous = await json('_build/voice-design-2/manifest.json');
assert.equal(manifest.candidates.length, 3);
assert.equal(manifest.privateVoicesSaved, 3);
assert.equal(manifest.finalVoiceSelected, false);
assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(JSON.stringify(manifest.performance)));
const protectedHashes = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  [previous.reference.file]: previous.reference.sha256,
};
for (const old of previous.candidates) protectedHashes[`_build/voice-design-2/${old.file}`] = old.sha256;
for (const [file, sha256] of Object.entries(protectedHashes)) {
  assert.equal(hash(await readFile(resolve(base, file))), sha256, `Changed original: ${file}`);
}
for (const candidate of manifest.candidates) {
  const prefix = `_build/voice-design-3/${candidate.id}/`;
  const saved = await json(prefix + 'save-voice.provider.json');
  const speech = await json(prefix + 'speech.provider.json');
  assert.equal(saved.request.generated_voice_id, candidate.generatedVoiceId);
  assert.equal(JSON.parse(saved.body).voice_id, candidate.voiceId);
  assert.ok(speech.endpoint.includes(`/text-to-speech/${candidate.voiceId}/`));
  assert.deepEqual(speech.request, manifest.performance);
  assert.equal(hash(await readFile(resolve(base, '_build/voice-design-3', candidate.file))), candidate.sha256);
}
const url = 'http://127.0.0.1:8782/voice-design-3.html';
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 1000}});
  const errors = [], samples = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.status() >= 400 && !response.url().endsWith('/favicon.ico')) errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto(url);
  for (const summary of await page.locator('summary').all()) await summary.click();
  assert.equal(await page.locator('audio[data-new]').count(), 3);
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
    const candidate = manifest.candidates[Math.floor(i / 2)];
    assert.ok(Math.abs(sample.duration - (i % 2 === 0 ? candidate.duration : candidate.sourceDuration)) < 0.1);
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
  await writeFile(resolve(base, '_build/voice-design-3/player-report.json'), JSON.stringify({
    url, samples, protectedHashes, voiceIdentityBindings: 'verified', samePerformanceDirection: true,
    rangeStatus: 206, mutualPause: true, links: true, narrowLayout: true, errors,
    listeningJudgment: 'Pending pilot review; timing is not proof of naturalness or perceived identity.',
  }, null, 2) + '\n');
  console.log('Three saved identities and matching TTS bindings verified. Six players passed playback, seeking, range delivery, mutual pause, links and mobile layout. Film and earlier samples unchanged.');
} finally {await browser.close();}
