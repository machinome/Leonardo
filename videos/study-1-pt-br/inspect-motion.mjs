// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Browser evidence for the pilot's continuity and no-text requirements.
import assert from 'node:assert/strict';
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const base = dirname(fileURLToPath(import.meta.url));
const tool = resolve(process.argv[2]), origin = process.argv[3];
assert.ok(origin, 'Pass the study live-preview address.');
const {chromium} = await import(pathToFileURL(resolve(tool, 'node_modules/playwright/index.mjs')));
const doc = JSON.parse(await readFile(resolve(base, '_build/movie-resolved.json')));
const output = resolve(base, '_build/motion-inspection');
await mkdir(output, {recursive: true});
const browser = await chromium.launch({headless: true});
const checks = [], errors = [];
try {
  // Keep the 540×960 preview at native CSS pixels; a fitted/scaled iframe
  // introduces a second resampling when a compositing layer is hidden.
  const page = await browser.newPage({viewport: {width: 1000, height: 1500}});
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(origin + '/#movie');
  await page.waitForFunction(() => window.player?.generation() > 0);
  const seek = async time => {
    await page.evaluate(async t => {window.player.seek(t); await window.player.idle();}, time);
    assert.equal(await page.locator('#fault').textContent(), '');
    assert.equal(await page.evaluate(() => document.querySelector('iframe')
      .contentDocument.querySelector('.portrait').textContent.trim()), '');
    return (await fetch(origin + '/frame?t=' + time)).json();
  };
  for (const [id, outgoing, incoming] of [['ancestor', 'wheel', 'mill'], ['water', 'mill', 'detail']]) {
    const shot = doc.chapters[0].shots.find(s => s.id === id);
    assert.equal(shot.transition.kind, 'reframe');
    for (const offset of [0, .3, .6, .9, 1.25]) {
      const frame = await seek(shot.start + offset);
      const a = frame.elements['continuous.' + outgoing], b = frame.elements['continuous.' + incoming];
      assert.deepEqual(a.view, b.view, 'No camera split during ' + id);
      assert.equal(a.time, b.time, 'No mechanical phase split during ' + id);
      if (id === 'water') {
        assert.deepEqual(a.view, frame.elements['continuous.ghost'].view);
        assert.equal(a.time, frame.elements['continuous.ghost'].time);
      }
      const opacity = await page.evaluate(name => {
        const w = document.querySelector('iframe').contentWindow;
        return Number(w.getComputedStyle(w.document.querySelector('[data-element="continuous.' + name + '"]')).opacity);
      }, incoming);
      const p = Math.min(1, offset / 1.2), expected = p * p * (3 - 2 * p);
      assert.ok(Math.abs(opacity - expected) < .06, 'Continuous opacity ramp, not a cut.');
      const before = await page.locator('iframe').screenshot({path: resolve(output, id + '-' + offset + '.png')});
      if (offset === 1.25) {
        await page.evaluate(name => document.querySelector('iframe').contentDocument
          .querySelector('[data-element="continuous.' + name + '"]').style.visibility = 'hidden', outgoing);
        const after = await page.locator('iframe').screenshot({path: resolve(output, id + '-covered.png')});
        await page.evaluate(name => document.querySelector('iframe').contentDocument
          .querySelector('[data-element="continuous.' + name + '"]').style.removeProperty('visibility'), outgoing);
        assert.ok(before.equals(after), 'Old model must be covered after fade: ' + id);
      }
      checks.push({shot: id, offset, opacity, sameCamera: true, samePose: true});
    }
  }
  for (const shot of doc.chapters[0].shots) {
    const time = shot.start + (shot.end - shot.start) / 2;
    const frame = await seek(time);
    const views = Object.values(frame.elements).filter(e => e.kind === 'view');
    if (shot.places.ghost) for (const view of views) {
      assert.deepEqual(view.view, views[0].view);
      assert.equal(view.time, views[0].time);
    }
    await page.locator('iframe').screenshot({path: resolve(output, shot.id + '-middle.png')});
    checks.push({shot: shot.id, noText: true, contextSynchronized: true});
  }
  const closing = doc.chapters[0].shots.at(-1);
  for (const fraction of [0, .2, .4, .6, .8, .92]) {
    const time = closing.start + (closing.end - closing.start) * fraction;
    await seek(time);
    await page.locator('iframe').screenshot({path: resolve(output, 'closing-' + fraction + '.png')});
  }
  assert.deepEqual(errors, []);
  await writeFile(resolve(output, 'report.json'), JSON.stringify(checks, null, 2) + '\n');
  console.log('Both 1.2-second fades, shared camera/pose, covered outgoing views and text-free shots pass.');
} finally { await browser.close(); }
