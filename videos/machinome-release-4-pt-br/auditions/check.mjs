// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile, writeFile} from 'node:fs/promises';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url)),build=resolve(base,'../_build/auditions-1');
const require=createRequire('/home/asa/devel/machinome/videomaker/package.json');
const {chromium}=require('playwright');
const manifest=JSON.parse(await readFile(resolve(build,'manifest.json')));
assert.equal(manifest.voices.length,3);assert.deepEqual(manifest.failures,[]);
const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required']});
try{
  const page=await browser.newPage({viewport:{width:1280,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(`${r.status()} ${r.url()}`)});
  await page.goto('http://127.0.0.1:8785/auditions/');
  await page.waitForFunction(()=>document.querySelectorAll('audio').length===3&&
    [...document.querySelectorAll('audio')].every(a=>a.readyState>=1));
  assert.equal(await page.locator('html').getAttribute('lang'),'pt-BR');
  assert.equal(await page.locator('video').count(),0);
  const played=[];
  for(const voice of manifest.voices){
    const audio=page.locator(`#${voice.id} audio`);
    const actual=await audio.evaluate(a=>a.duration);
    assert.ok(Math.abs(actual-voice.duration)<.2);
    await audio.evaluate(a=>a.play());
    await page.waitForFunction(id=>document.querySelector(`#${id} audio`).currentTime>.1,voice.id);
    assert.equal(await page.locator('audio').evaluateAll(a=>a.filter(e=>!e.paused).length),1);
    await audio.evaluate(a=>{a.currentTime=a.duration/2});
    await page.waitForFunction(id=>{const a=document.querySelector(`#${id} audio`);return !a.seeking&&a.currentTime>=a.duration/2},voice.id);
    played.push({id:voice.id,duration:actual,playbackAndSeek:true});
    const url=await audio.getAttribute('src');
    const response=await fetch(new URL(url,page.url()),{headers:{Range:'bytes=1000-1999'}});
    assert.equal(response.status,206);assert.equal((await response.arrayBuffer()).byteLength,1000);
  }
  await page.locator('audio').evaluateAll(a=>a.forEach(e=>e.pause()));
  for(const a of await page.locator('a').all()){
    const response=await page.request.head(new URL(await a.getAttribute('href'),page.url()).href);
    assert.ok(response.ok());
  }
  await page.screenshot({path:resolve(build,'player-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:resolve(build,'player-mobile.png'),fullPage:true});
  assert.deepEqual(errors,[]);
  await writeFile(resolve(build,'player-report.json'),JSON.stringify({status:'technical checks pass; listening approval pending',played,rangeStatus:206,errors},null,2)+'\n');
  console.log('All three auditions play and seek; exclusive playback, downloads, byte ranges, desktop and mobile pass. No video.');
}finally{await browser.close()}
