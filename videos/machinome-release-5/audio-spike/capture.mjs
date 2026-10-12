// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const base=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const out=resolve(process.argv[2]),tool=resolve(process.argv[3]);
const {chromium}=await import(`${tool}/node_modules/playwright/index.mjs`);
const sha=b=>createHash('sha256').update(b).digest('hex');
const inputs=['stage.jsx','stage.css','ending-motion.mjs','finish.mjs','movie.py',
  '_build/movie.json','_build/movie-resolved.json','_build/narration.wav','_build/rehearsal.mp4'];
const before=Object.fromEntries(await Promise.all(inputs.map(async f=>[f,sha(await readFile(resolve(base,f)))])));
const origin='http://127.0.0.1:8785',outline=await(await fetch(`${origin}/film.json`)).json();
assert.equal(outline.refusal,null);assert.equal(outline.output.fps,24);
await writeFile(resolve(out,'movie-resolved.json'),await readFile(resolve(base,'_build/movie-resolved.json')));
await writeFile(resolve(out,'outline.json'),JSON.stringify(outline,null,2)+'\n');
await writeFile(resolve(out,'source-hashes.json'),JSON.stringify(before,null,2)+'\n');
const fps=24,duration=17,frames=resolve(out,'frames');await mkdir(frames);
const browser=await chromium.launch({headless:true});const checks=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'/#movie');await page.waitForFunction(()=>window.player?.generation()>0);
  await page.evaluate(()=>window.player.pause());
  const generation=await page.evaluate(()=>window.player.generation());let first;
  for(let i=0;i<fps*duration;i++){
    const t=i/fps;
    await page.evaluate(async t=>{window.player.seek(t);await window.player.idle();},t);
    assert.equal(await page.locator('#fault').textContent(),'');
    assert.equal(await page.evaluate(()=>window.player.generation()),generation);
    const png=await page.locator('iframe').screenshot({path:resolve(frames,`frame-${String(i).padStart(6,'0')}.png`)});
    if(i===0)first=sha(png);if(i===1)assert.notEqual(sha(png),first);
    if(i%fps===0){checks.push({time:t,sha256:sha(png)});console.log(`Capture ${t+1}/${duration}s`);}
  }
  assert.deepEqual(errors,[]);
}finally{await browser.close();}
execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-n','-framerate',String(fps),
  '-i',resolve(frames,'frame-%06d.png'),'-vf','crop=960:540:0:0','-an','-c:v','libx264','-preset','fast','-crf','18',
  '-pix_fmt','yuv420p','-movflags','+faststart',resolve(out,'opening-silent.mp4')]);
for(const f of inputs)assert.equal(sha(await readFile(resolve(base,f))),before[f],f);
await writeFile(resolve(out,'capture.json'),JSON.stringify({origin,duration,fps,
  livePreviewCapture:true,checks,sha256:sha(await readFile(resolve(out,'opening-silent.mp4')))},null,2)+'\n');
console.log('Captured the unchanged opening, 408 frames.');
