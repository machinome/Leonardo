// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Verify the delivered local film, subtitles and review navigation.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {writeFile} from 'node:fs/promises';
const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2],'Pass the Videomaker checkout.');
const require=createRequire(resolve(process.argv[2],'package.json'));
const {chromium}=require('playwright');
const url=process.argv[3]??'http://127.0.0.1:8781/';
const range=await fetch(new URL('_build/rehearsal.mp4',url),{headers:{Range:'bytes=1000-1999'}});
assert.equal(range.status,206,'Player server must support byte ranges for seeking.');
assert.equal((await range.arrayBuffer()).byteLength,1000);
const browser=await chromium.launch({headless:true});
try {
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('response',response=>{if(response.status()>=400&&!response.url().endsWith('/favicon.ico'))errors.push(`${response.status()} ${response.url()}`);});
  await page.goto(url);
  await page.waitForFunction(()=>document.querySelector('video').readyState>=2);
  const media=await page.locator('video').evaluate(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight}));
  assert.equal(media.width,1280);
  assert.equal(media.height,720);
  assert.ok(Math.abs(media.duration-140.20833333333334)<.1);
  const seeks=[];
  for(const button of await page.locator('[data-time]').all()) {
    const target=Number(await button.getAttribute('data-time'));
    await button.click();
    await page.waitForFunction(t=>{
      const v=document.querySelector('video');
      return !v.seeking&&v.currentTime>=t&&v.currentTime<t+.8&&v.readyState>=2;
    },target,{timeout:15000});
    const reached=await page.locator('video').evaluate(v=>{v.pause();return v.currentTime;});
    seeks.push({target,reached});
  }
  for(const link of await page.locator('a').all()){
    const destination=new URL(await link.getAttribute('href'),url);
    const response=await page.request.head(destination.href);
    assert.ok(response.ok(),`Broken review link: ${destination.pathname}`);
  }
  await page.locator('video').evaluate(v=>{v.textTracks[0].mode='showing';});
  await page.waitForFunction(()=>document.querySelector('video').textTracks[0].cues?.length>0);
  const cues=await page.locator('video').evaluate(v=>v.textTracks[0].cues.length);
  await page.screenshot({path:resolve(base,'_build/player-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Narrow player overflows.');
  await page.screenshot({path:resolve(base,'_build/player-mobile.png'),fullPage:true});
  assert.deepEqual(errors,[]);
  await writeFile(resolve(base,'_build/player-report.json'),JSON.stringify({url,media,seeks,subtitleCues:cues,rangeStatus:206,errors},null,2)+'\n');
  console.log(`Player passed: ${seeks.length} seeks, ${cues} subtitle cues, range delivery, links, desktop and narrow layout.`);
} finally {await browser.close();}
