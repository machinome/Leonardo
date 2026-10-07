// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Inspect the live preview and its aligned cues; never render a movie.
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const tool=resolve(process.argv[2]);
const origin=process.argv[3]??'http://127.0.0.1:8785';
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const doc=JSON.parse(await readFile(resolve(base,'_build/movie-resolved.json')));
const outline=await (await fetch(`${origin}/film.json`)).json();
const shots=outline.shots;
const browser=await chromium.launch({headless:true});
const output=resolve(base,'_build/inspection');await mkdir(output,{recursive:true});
const checks=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${origin}/#movie`);
  await page.waitForFunction(()=>window.player?.generation()>0);
  const seek=async time=>{
    await page.evaluate(async time=>{window.player.seek(time);await window.player.idle();},time);
    const fault=await page.locator('#fault').textContent();assert.equal(fault,'');
  };
  for(const id of ['document','behind-the-film','mirror','open-source','wheel-returns','invitation']){
    const shot=shots.find(s=>s.id===id);
    for(const fraction of id==='document'||id==='open-source'?[.05,.8]:[.5]){
      const time=shot.start+(shot.end-shot.start)*fraction;
      await seek(time);
      await page.locator('iframe').screenshot({path:resolve(output,`${id}-${fraction}.png`)});
      const overflow=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument.querySelectorAll('.listing')]
        .map(el=>({file:el.querySelector('.listing-file').textContent,
          bottom:el.querySelector('pre').getBoundingClientRect().bottom,
          limit:el.getBoundingClientRect().bottom})));
      for(const item of overflow)assert.ok(item.bottom<=item.limit+1,`Code overflows: ${item.file}`);
      checks.push({id,time,overflow});
    }
  }
  for(const id of ['behind-the-film','mirror']){
    const shot=doc.chapters[0].shots.find(s=>s.id===id);
    for(const cue of shot.cues){
      const action=cue.actions.find(a=>a.action==='blink');if(!action)continue;
      await seek(shot.start+(cue.at+cue.until)/2);
      const tokens=await page.evaluate(()=>[...document.querySelector('iframe').contentDocument.querySelectorAll('.blink-token')].map(x=>x.textContent));
      assert.deepEqual(tokens,[action.params.token]);
      checks.push({id,token:action.params.token,from:shot.start+cue.at,to:shot.start+cue.until});
    }
  }
  await seek(outline.output.duration-1);
  assert.equal(await page.evaluate(()=>document.querySelector('iframe').contentDocument.querySelector('.question')),null);
  assert.deepEqual(errors,[]);
  await writeFile(resolve(output,'checks.json'),JSON.stringify({status:'passed',duration:outline.output.duration,checks},null,2)+'\n');
  console.log(`Preview checked: ${checks.length} frames/cues; no video rendered.`);
}finally{await browser.close();}
