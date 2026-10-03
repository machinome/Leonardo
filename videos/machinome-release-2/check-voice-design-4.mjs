// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Same voice, same script, five directions; verify media and the comparison page.
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
const manifest = await json('_build/voice-design-4/manifest.json');
const previous = await json('_build/voice-design-3/manifest.json');
assert.equal(manifest.candidates.length, 5);
assert.equal(manifest.newVoicesCreated, 0);
assert.equal(manifest.selectedVoice.voiceId, 'JoOLJ0OHRwCg8Ydjc4IF');
assert.equal(manifest.selectedVoice.previousProposal, 'D3-2');
const script = (await json(manifest.source.input)).chapters[0].narration;
assert.equal(script.slice(manifest.source.begin, manifest.source.end), manifest.displayText);
assert.equal(manifest.spokenText, manifest.displayText.replace('Machinome', 'mah-SHEEN-ohm'));
const protectedHashes = {
  '_build/rehearsal.mp4': '18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f',
  '_build/audio/continuous-be56771bde523273.wav': 'e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3',
  ...manifest.source.sourceHashes,
};
for (const old of previous.candidates) protectedHashes[`_build/voice-design-3/${old.file}`] = old.sha256;
for (const [file, sha256] of Object.entries(protectedHashes)) {
  assert.equal(hash(await readFile(resolve(base, file))), sha256, `Changed original: ${file}`);
}
for (const candidate of manifest.candidates) {
  const receipt = await json(`_build/voice-design-4/${candidate.id}/speech.provider.json`);
  assert.ok(receipt.endpoint.includes(`/text-to-speech/${manifest.selectedVoice.voiceId}/`));
  assert.equal(candidate.voiceId, manifest.selectedVoice.voiceId);
  assert.deepEqual(receipt.request, candidate.request);
  const {text, ...settings} = candidate.request;
  const {text: previousText, ...previousSettings} = previous.performance;
  assert.deepEqual(settings, previousSettings);
  assert.equal(text.replace(/\[[^\]]*\]\s*/g, ''), manifest.spokenText);
  assert.ok(!/profound|solemn|contemplative|gravitas|whisper|slow|\.\.\.|…/i.test(text));
  assert.equal(hash(await readFile(resolve(base, '_build/voice-design-4', candidate.file))), candidate.sha256);
}
const url = 'http://127.0.0.1:8782/voice-design-4.html';
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
  await page.locator('summary').click();
  assert.equal(await page.locator('audio[data-new]').count(), 5);
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
    const expected = i < 5 ? manifest.candidates[i].duration : manifest.selectedVoice.referenceDuration;
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
  await writeFile(resolve(base, '_build/voice-design-4/player-report.json'), JSON.stringify({
    url, samples, protectedHashes, sameVoiceAndSettings: true, verbatimScript: true,
    rangeStatus: 206, mutualPause: true, links: true, narrowLayout: true, errors,
    listeningJudgment: 'Pending pilot review; labels describe direction, not an auditory quality assessment.',
  }, null, 2) + '\n');
  console.log('Fixed C3 identity/settings and verbatim script verified. Six players passed playback, seeking, byte ranges, mutual pause, links and mobile layout. Script, film and previous readings unchanged.');
} finally {await browser.close();}
