// Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.
// Photograph the live preview at chosen film times; never render a movie.
import assert from 'node:assert/strict';
import {mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const [checkout,origin,...times]=process.argv.slice(2);
assert.ok(checkout&&origin&&times.length,'Pass the Videomaker checkout, the live origin and film times.');
const {chromium}=await import(pathToFileURL(resolve(checkout,'node_modules/playwright/index.mjs')));
const output=resolve(base,'_build/inspection');await mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${origin}/#movie`);
  await page.waitForFunction(()=>window.player?.generation()>0,null,{timeout:120000});
  for(const value of times){
    const time=Number(value);
    await page.evaluate(async time=>{window.player.seek(time);await window.player.idle();},time);
    assert.equal(await page.locator('#fault').textContent(),'',`Player fault at ${time}`);
    const name=`frame-${time.toFixed(3).padStart(8,'0')}.png`;
    await page.locator('iframe').screenshot({path:resolve(output,name)});
    console.log(name);
  }
  assert.deepEqual(errors,[]);
}finally{await browser.close();}
