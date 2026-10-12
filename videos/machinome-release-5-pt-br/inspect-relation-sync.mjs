// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Compare corrected word boundaries with the resolved film and live pixels.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2],'Pass Videomaker checkout.');
const tool=resolve(process.argv[2]),origin=process.argv[3]??'http://127.0.0.1:8785';
const timing=JSON.parse(await readFile(resolve(base,'relation-timing.json')));
const doc=JSON.parse(await readFile(resolve(base,'_build/movie-resolved.json')));
const meta=JSON.parse(await readFile(resolve(base,'_build/narration-manifest.json')));
assert.equal(createHash('sha256').update(await readFile(meta.cacheFile)).digest('hex'),timing.audioSha256);
const chapter=doc.chapters[0],shot=chapter.shots.find(s=>s.id==='face-reveal');
const fps=doc.output.fps,checks=[];
for(const [token,word] of Object.entries(timing.words)){
  const cue=shot.cues.find(c=>c.actions.some(a=>a.action==='blink'&&a.params.token===token));
  assert.ok(cue,`Missing ${token} cue`);
  for(const [edge,field] of [['start','at'],['end','until']])if(word[edge]!==undefined){
    const actual=shot.start+cue[field],expected=chapter.speechOffset+word[edge];
    console.log(`${token} ${edge}: film ${actual.toFixed(3)}s; aligned ${expected.toFixed(3)}s`);
    assert.ok(Math.abs(actual-expected)<=.5/fps+1e-6,`${token} ${edge} must follow the locally aligned recording`);
  }
}
const cues=shot.cues.filter(c=>c.actions.some(a=>a.action==='blink'));
for(let i=1;i<cues.length;i++)assert.ok(cues[i-1].until<=cues[i].at,'Relation highlights never overlap');
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const browser=await chromium.launch({headless:true});
const output=resolve(base,'_build/inspection/relation-sync');await mkdir(output,{recursive:true});
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(`${origin}/#movie`);
  await page.waitForFunction(()=>window.player?.generation()>0);
  for(const token of ['drives','crankshaft']){
    const cue=cues.find(c=>c.actions[0].params.token===token);
    const start=shot.start+cue.at,end=shot.start+cue.until;
    for(const [phase,time] of [['before',start-1/fps],['start',start],['middle',(start+end)/2],['end',end]]){
      await page.evaluate(async time=>{window.player.seek(time);await window.player.idle();},time);
      assert.equal(await page.locator('#fault').textContent(),'');
      const marks=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument
        .querySelectorAll('[data-element="continuous.assembly"] .blink-token')].map(m=>m.textContent));
      if(phase==='start'||phase==='middle')assert.deepEqual(marks,[token]);
      else assert.ok(!marks.includes(token),`${token} is clear ${phase}`);
      if(phase==='middle')await page.locator('iframe').screenshot({path:resolve(output,`${token}.png`)});
      checks.push({token,phase,time,marks});
    }
  }
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({audioSha256:timing.audioSha256,checks,errors},null,2)+'\n');
  console.log(`${checks.length} live relation-highlight checks passed.`);
}finally{await browser.close();}
