// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Playback checks are not a listening or performance-quality review.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker checkout.');
const require = createRequire(resolve(process.argv[2], 'package.json'));
const {chromium} = require('playwright');
const url = process.argv[3] ?? 'http://127.0.0.1:8782/';
const manifest = JSON.parse(await readFile(resolve(base, '_build/narration-manifest.json'), 'utf8'));
const range = await fetch(new URL('_build/narration.wav', url), {headers: {Range: 'bytes=1000-1999'}});
assert.equal(range.status, 206);
assert.equal((await range.arrayBuffer()).byteLength, 1000);
const browser = await chromium.launch({headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 960}});
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  await page.goto(url);
  await page.waitForFunction(() => document.body.dataset.ready === 'true' && document.querySelector('audio').readyState >= 1);
  const duration = await page.locator('audio').evaluate(a => a.duration);
  assert.ok(Math.abs(duration - manifest.duration) < 0.01);
  assert.equal((await page.locator('#script').innerText()).replace(/\s+/gu, ' ').trim(), manifest.text.replace(/\s+/gu, ' ').trim());
  assert.equal(await page.locator('#script p').count(), 8);
  const seeks = [];
  for (const button of await page.locator('[data-time]').all()) {
    const target = Number(await button.getAttribute('data-time'));
    await button.click();
    await page.waitForFunction(t => {
      const a = document.querySelector('audio');
      return !a.seeking && !a.paused && a.currentTime > t + 0.05 && a.readyState >= 2;
    }, target, {timeout: 15000});
    const reached = await page.locator('audio').evaluate(a => { a.pause(); return a.currentTime; });
    assert.ok(reached < target + 1, 'A chapter seek overshot its requested passage.');
    seeks.push({target, reached});
  }
  assert.equal(seeks.length, 9);
  const importTime = manifest.beats.find(b => b.id === 'import').start + 0.5;
  await page.locator('audio').evaluate((a, t) => { a.currentTime = t; }, importTime);
  await page.waitForFunction(() => document.querySelector('#caption').textContent.includes('Machinome'));
  for (const link of await page.locator('a').all()) {
    const destination = new URL(await link.getAttribute('href'), url);
    assert.ok((await page.request.head(destination.href)).ok(), destination.pathname);
  }
  await page.screenshot({path: resolve(base, '_build/listening-desktop.png'), fullPage: true});
  await page.setViewportSize({width: 390, height: 844});
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.screenshot({path: resolve(base, '_build/listening-mobile.png'), fullPage: true});
  assert.deepEqual(errors, []);
  await writeFile(resolve(base, '_build/player-report.json'), JSON.stringify({
    url, duration, sha256: manifest.sha256, rangeStatus: 206, seeks,
    captions: manifest.captions, scriptMatches: true, errors,
    listeningReview: 'not performed by this test',
  }, null, 2) + '\n');
  console.log('Audio player passed: 9 seek/play checks, captions, literal script, links and both layouts.');
} finally { await browser.close(); }
