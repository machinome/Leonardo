// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Project-owned empirical edit; screenplay remains YAML. No stable tool changes.
import assert from 'node:assert/strict';
import { readFile, writeFile, mkdir, stat, link, rename } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { loadEnvFile } from 'node:process';

const base = dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2], 'Pass the Videomaker repository');
const tool = resolve(process.argv[2]);
const mode = process.argv[3] ?? 'preview';
assert.ok(['speech', 'preview', 'render'].includes(mode));
const require = createRequire(resolve(tool, 'package.json'));
const { chromium } = require('playwright');
const hljs = require('highlight.js/lib/core');
hljs.registerLanguage('python', require('highlight.js/lib/languages/python'));
const { loadEpisode, parseSource, contained } = await import(pathToFileURL(resolve(tool, 'src/episode.mjs')));
const { hash, fileHash, json, command } = await import(pathToFileURL(resolve(tool, 'src/util.mjs')));
const { pcmWav, mixSpeech } = await import(pathToFileURL(resolve(tool, 'src/speech.mjs')));
const { frameAt, captionsFromAlignment, srt } = await import(pathToFileURL(resolve(tool, 'src/timeline.mjs')));
const recipe = parseSource(await readFile(resolve(base, 'rehearsal.yaml'), 'utf8'));
assert.equal(recipe.format, 'machinome-visual-experiment/revolutions-opening');
const episode = await loadEpisode(resolve(base, recipe.episode));
const last = episode.shots.findIndex(s => s.id === recipe.through);
assert.ok(last >= 0);
const shots = episode.shots.slice(0, last + 1);
assert.deepEqual(shots.map(s => s.id), Object.keys(recipe.scenes));
const text = shots.map(s => s.narration).join(' ');
assert.ok(!/name combines|start small|copyright|licen[cs]e|vibecoded|made with|created by/i.test(text));
assert.ok(text.endsWith("And don't forget to leave your like."));
const build = resolve(base, '_build/rehearsal');
await mkdir(build, { recursive: true });
const dictionary = JSON.parse(await readFile(resolve(base, recipe.dictionary), 'utf8'));
assert.equal(dictionary.rules[0].phoneme, 'məˈʃiːnoʊm');
const request = { text, model_id: episode.audio.model,
  voice_settings: episode.audio.voiceSettings, seed: 4217,
  pronunciation_dictionary_locators: [{ pronunciation_dictionary_id: dictionary.id,
    version_id: dictionary.version_id }] };
const inputHash = hash(JSON.stringify({ request, voice: episode.audio.voice, format: episode.audio.outputFormat }));
const audioDir = resolve(build, 'audio');
await mkdir(audioDir, { recursive: true });
const wav = resolve(audioDir, inputHash + '.wav');
const meta = wav + '.json';
let take;
try { take = JSON.parse(await readFile(meta, 'utf8')); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
if (!take) {
  assert.equal(mode, 'speech', 'Missing narration: run speech explicitly');
  loadEnvFile(resolve(tool, '.env'));
  assert.ok(process.env.ELEVENLABS_API_KEY, 'Missing speech key');
  console.log(`Generating one continuous Jessica take (${text.length} characters)`);
  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${episode.audio.voice}/with-timestamps?output_format=pcm_24000`, {
    method: 'POST', headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(request), signal: AbortSignal.timeout(180000),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`ElevenLabs HTTP ${response.status}: ${data.detail?.status ?? 'request_failed'}`);
  assert.ok(data.audio_base64, 'No provider audio');
  const bytes = pcmWav(Buffer.from(data.audio_base64, 'base64'), 24000);
  await writeFile(wav, bytes);
  take = { inputHash, request, voice: episode.audio.voice, sha256: hash(bytes),
    duration: (bytes.length - 44) / 48000, alignment: data.normalized_alignment ?? data.alignment };
  // Cache the paid take before downstream alignment validation.
  await json(meta, take);
}
assert.equal(take.inputHash, inputHash);
assert.equal(await fileHash(wav), take.sha256);
const captions = captionsFromAlignment(take.alignment, recipe.speechOffset);
const aligned = take.alignment.characters.join('');
let position = 0;
const cues = shots.map((shot, index) => {
  const start = aligned.indexOf(shot.narration, position);
  assert.ok(start >= position, `Cannot align scene: ${shot.id}`);
  const end = start + shot.narration.length;
  position = end;
  return { id: shot.id, start: index ? Math.max(0, recipe.speechOffset + take.alignment.character_start_times_seconds[start] - 0.12) : 0,
    spokenStart: recipe.speechOffset + take.alignment.character_start_times_seconds[start],
    spokenEnd: recipe.speechOffset + take.alignment.character_end_times_seconds[end - 1],
    ...recipe.scenes[shot.id] };
});
const fps = recipe.output.fps;
const seconds = Math.ceil((recipe.speechOffset + take.duration + recipe.tailSeconds) * fps) / fps;
for (let i = 1; i < cues.length; i++) cues[i].start = Math.max(cues[i].start, cues[i - 1].spokenEnd);
for (let i = 0; i < cues.length; i++) cues[i].end = cues[i + 1]?.start ?? seconds;
assert.ok(cues.every(c => c.end > c.start));
const mix = resolve(build, 'narration.wav');
const records = [{ file: wav, sha256: take.sha256, duration: take.duration, offset: recipe.speechOffset }];
if (mode === 'speech') {
  await mixSpeech(records, seconds, mix);
  await writeFile(resolve(build, 'rehearsal.srt'), srt(captions));
  await json(resolve(build, 'captions.json'), captions);
  await json(resolve(build, 'audio-manifest.json'), { inputHash, records, seconds, cues, mixSha256: await fileHash(mix) });
  console.log(JSON.stringify({ seconds, cues }, null, 2));
} else {
  const audio = JSON.parse(await readFile(resolve(build, 'audio-manifest.json'), 'utf8'));
  assert.equal(audio.inputHash, inputHash);
  assert.equal(audio.mixSha256, await fileHash(mix));
  assert.deepEqual(audio.cues, cues);
  const viewer = resolve(process.argv[4] ?? '');
  assert.ok(process.argv[4], 'Pass the viewer bundle');
  const manifest = JSON.parse(await readFile(episode.paths.manifest, 'utf8'));
  const paths = new Map([['/viewer.js', viewer], ['/model/manifest.json', episode.paths.manifest]]);
  function collect(value) {
    if (typeof value === 'string' && /\.(stl|png|jpg|jpeg|webp|svg)$/i.test(value)) {
      const file = resolve(dirname(episode.paths.manifest), value);
      assert.ok(contained(dirname(episode.paths.manifest), file));
      paths.set('/model/' + value, file);
    } else if (value && typeof value === 'object') Object.values(value).forEach(collect);
  }
  collect(manifest);
  const modelHashes = {};
  for (const [url, file] of paths) modelHashes[url] = await fileHash(file);
  const html = await readFile(resolve(tool, 'experiments/dark-source/stage.html'), 'utf8');
  const errors = [];
  const server = createServer(async (req, res) => {
    try {
      const path = new URL(req.url, 'http://localhost').pathname;
      if (path === '/') { res.setHeader('Content-Type', 'text/html'); res.end(`<!doctype html><html><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#111519}#viewport{position:absolute;inset:4%}#stage{width:100%;height:100%}canvas{display:block}</style><div id="viewport"><div id="stage"></div></div><script src="/viewer.js"></script></html>`); return; }
      if (path === '/favicon.ico') { res.writeHead(204); res.end(); return; }
      if (!paths.has(path)) { res.writeHead(404); res.end(); return; }
      res.setHeader('Content-Type', path.endsWith('.js') ? 'text/javascript' : path.endsWith('.json') ? 'application/json' : 'application/octet-stream');
      res.end(await readFile(paths.get(path)));
    } catch (error) { errors.push(error.message); res.writeHead(500); res.end(); }
  });
  await new Promise(done => server.listen(0, '127.0.0.1', done));
  const browser = await chromium.launch({ headless: true, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  try {
    const viewport = { width: recipe.output.width, height: recipe.output.height };
    const model = await browser.newPage({ viewport });
    const code = await browser.newPage({ viewport });
    for (const page of [model, code]) {
      page.on('pageerror', e => errors.push(e.message));
      page.on('requestfailed', r => errors.push(r.url()));
      page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    }
    await code.setContent(html);
    await code.evaluate(() => document.fonts.ready);
    await model.goto(`http://127.0.0.1:${server.address().port}/`);
    const first = frameAt(episode, 0);
    await model.evaluate(async f => {
      window.viewer = await MachinomeViewer.mount('#stage', '/model/manifest.json', {
        animation: 'external', autoplay: false, driverControls: 'none', partControls: 'none',
        renderMode: 'on-demand', up: [0, 0, 1], fov: f.fov, view: f.view, time: f.time,
      });
      window.hidden = [];
    }, first);
    let checked = 0;
    const literal = name => { const s = episode.sourceCode[name]; assert.ok(s); return s.text.split('\n').map(line => ' '.repeat(s.dedent) + line).join('\n'); };
    async function pose(time) {
      const cue = cues.find(c => time >= c.start && time < c.end);
      assert.ok(cue);
      let page;
      if (cue.kind === 'code') {
        page = code;
        const source = cue.snippets.map(literal).join('\n\n# …\n\n');
        await code.evaluate(({ source, markup, cue }) => {
          document.querySelector('header').textContent = cue.fileLabel + '   EXCERPTS';
          document.querySelector('pre').style.fontSize = cue.fontSize + 'px';
          document.querySelector('pre').style.lineHeight = cue.lineHeight + 'px';
          document.querySelector('code').innerHTML = markup;
        }, { source, markup: hljs.highlight(source, { language: 'python' }).value, cue });
        assert.equal(await code.locator('code').textContent(), source);
        assert.ok(await code.locator('pre').evaluate(el => el.scrollHeight <= el.clientHeight && el.scrollWidth <= el.clientWidth), 'Source overflows');
        assert.equal(await code.locator('canvas,video,#caption').count(), 0);
      } else {
        page = model;
        const shot = shots.find(s => s.id === cue.id);
        const u = (time - cue.start) / (cue.end - cue.start);
        const frame = frameAt(episode, shot.start + u * (shot.end - shot.start));
        const actual = await model.evaluate(f => {
          if (JSON.stringify(window.hidden) !== JSON.stringify(f.hidden)) {
            for (const path of window.hidden) window.viewer.setVisible(path, true);
            for (const path of f.hidden) window.viewer.setVisible(path, false);
            window.hidden = f.hidden;
          }
          window.viewer.setTime(f.time);
          window.viewer.setView(f.view);
          const v = window.viewer.view();
          return { camera: v.camera.toArray(), target: v.target.toArray() };
        }, frame);
        for (const key of ['camera', 'target']) for (let i = 0; i < 3; i++) assert.ok(Math.abs(actual[key][i] - frame.view[key][i]) < 1e-6);
        assert.equal(await model.locator('pre,code,#caption').count(), 0);
        const box = await model.locator('canvas').boundingBox();
        assert.ok(box.width > viewport.width * .85 && box.height > viewport.height * .85);
      }
      assert.deepEqual(errors, []);
      checked++;
      return page;
    }
    const samples = [];
    for (const cue of cues) {
      const a = cue.start + Math.min(.2, (cue.end - cue.start) / 4);
      const b = cue.start + (cue.end - cue.start) * .6;
      const page = await pose(a), before = await page.screenshot();
      const next = await pose(b), after = await next.screenshot();
      assert.equal(before.equals(after), cue.kind === 'code', 'Expected still code / moving model');
      await pose(a); assert.ok(before.equals(await page.screenshot()), 'Replay differs');
      const file = resolve(build, cue.id + '.png');
      await page.screenshot({ path: file }); samples.push({ cue: cue.id, time: a, file });
    }
    await json(resolve(build, 'preview.json'), { seconds, cues, samples, checks: { literalCode: true, exclusiveScenes: true, pixelReplay: true, machineMotion: true, noCaptions: true } });
    if (mode === 'render') {
      const identity = hash(JSON.stringify({ recipe, shots, sources: episode.sourceCode, cues, modelHashes, html,
        cameras: episode.cameras, layers: episode.layers, model: episode.model, style: episode.style,
        script: await fileHash(fileURLToPath(import.meta.url)), browser: browser.version() }));
      const frames = resolve(build, 'frames', identity.slice(0, 16));
      await mkdir(frames, { recursive: true });
      const count = Math.round(seconds * fps), stills = new Map();
      for (let i = 0; i < count; i++) {
        const time = i / fps, cue = cues.find(c => time >= c.start && time < c.end);
        const file = resolve(frames, String(i).padStart(6, '0') + '.png');
        let exists = false;
        try { exists = (await stat(file)).size > 0; } catch (e) { if (e.code !== 'ENOENT') throw e; }
        if (!exists) {
          if (cue.kind === 'code' && stills.has(cue.id)) await link(stills.get(cue.id), file);
          else {
            const page = await pose(time);
            await page.screenshot({ path: file + '.tmp', type: 'png' });
            await rename(file + '.tmp', file);
          }
        }
        if (cue.kind === 'code' && !stills.has(cue.id)) stills.set(cue.id, file);
        if (i % 120 === 0) console.log(`Frames ${i + 1}/${count}`);
      }
      const output = resolve(build, 'rehearsal.mp4');
      await command('ffmpeg', ['-y', '-v', 'error', '-framerate', String(fps), '-i', resolve(frames, '%06d.png'), '-i', mix,
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-t', String(seconds), '-movflags', '+faststart', output]);
      const probe = JSON.parse(await command('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', output]));
      assert.deepEqual(probe.streams.map(s => s.codec_type).sort(), ['audio', 'video']);
      const video = probe.streams.find(s => s.codec_type === 'video');
      assert.equal(Number(video.nb_read_frames), count);
      assert.equal(video.width, viewport.width); assert.equal(video.height, viewport.height);
      await json(resolve(build, 'rehearsal-manifest.json'), { recipe, shots, cues, seconds, frames, identity, modelHashes,
        sources: episode.sourceCode, audio, outputSha256: await fileHash(output), subtitlesSha256: await fileHash(resolve(build, 'rehearsal.srt')),
        probe, browser: browser.version(), checked, status: 'empirical opening rehearsal, not a release', sourceRevision: episode.model.sourceRevision });
      console.log(output);
    } else console.log('Preview: ' + build);
  } finally { await browser.close(); await new Promise(done => server.close(done)); }
}
