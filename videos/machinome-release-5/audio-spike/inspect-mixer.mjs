// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Real-film listening transport evidence; screenshots only, never a video render.
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const [toolArg,origin,outArg]=process.argv.slice(2);
if(!toolArg||!origin||!outArg)throw Error('Usage: inspect-mixer.mjs TOOL URL OUTPUT');
const tool=resolve(toolArg),out=resolve(outArg);
const {chromium}=await import(pathToFileURL(resolve(tool,'node_modules/playwright/index.mjs')));
const browser=await chromium.launch({headless:true}),errors=[],checks=[];
try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>{
    if(window!==window.top)return;
    const connect=AudioNode.prototype.connect,start=AudioBufferSourceNode.prototype.start;
    const contexts=new WeakMap();let next=0;window.audioStarts=[];
    AudioBufferSourceNode.prototype.start=function(at,offset,...rest){
      if(!contexts.has(this.context))contexts.set(this.context,next++);
      window.audioStarts.push({context:contexts.get(this.context),at,offset,duration:this.buffer?.duration});
      return start.call(this,at,offset,...rest);
    };
    AudioNode.prototype.connect=function(destination,...rest){
      const result=connect.call(this,destination,...rest);
      if(destination instanceof AudioDestinationNode){
        const analyser=this.context.createAnalyser();analyser.fftSize=4096;
        connect.call(this,analyser);window.mixAnalyser=analyser;
      }
      return result;
    };
    window.mixLevel=()=>{
      const a=window.mixAnalyser;if(!a)return null;
      const values=new Float32Array(a.fftSize);a.getFloatTimeDomainData(values);
      let peak=0,sum=0;for(const v of values){peak=Math.max(peak,Math.abs(v));sum+=v*v;}
      return {peak,rms:Math.sqrt(sum/values.length)};
    };
  });
  await page.goto(origin+'/#movie');
  await page.waitForFunction(()=>window.player?.mixer()?.ready,{},{timeout:60000});
  await page.evaluate(()=>window.player.idle());
  const mix=()=>page.evaluate(()=>window.player.mixer());
  const initial=await mix();
  assert.deepEqual(initial.tracks.map(t=>t.id),['narration','water','paddles','wheel','saw']);
  assert.ok(initial.tracks.every(t=>t.duration===203.625));
  assert.equal(initial.playing,false);
  const geometry=await page.locator('#surface').boundingBox();
  const seek=async t=>page.evaluate(async t=>{window.player.seek(t);await window.player.idle();},t);
  for(const t of [0,7.8,12,53,83,107,116,125,149,175,185,195]){
    await seek(t);
    assert.deepEqual(await page.locator('#surface').boundingBox(),geometry,`Stable surface at ${t}`);
    assert.equal(await page.locator('#fault').textContent(),'');
    checks.push({seek:t,clock:(await mix()).time,geometry});
  }
  await seek(12);
  await page.screenshot({path:resolve(out,'mixer-machine.png')});
  await page.locator('[data-play]').click();
  await page.waitForFunction(()=>window.player.mixer().time>12.3);
  const starts=await page.evaluate(()=>window.audioStarts);
  assert.equal(starts.length,5);
  assert.equal(new Set(starts.map(s=>s.context)).size,1);
  assert.equal(new Set(starts.map(s=>s.at)).size,1);
  assert.deepEqual(starts.map(s=>s.offset),[12,12,12,12,12]);
  await page.waitForFunction(()=>window.mixLevel()?.rms>.001);
  checks.push({playingTogether:starts,level:await page.evaluate(()=>window.mixLevel())});
  // Every physical emitter actually reaches the native audio output alone.
  for(const id of ['water','paddles','wheel','saw']){
    await page.locator('[data-reset]').click();
    await page.locator(`[data-solo="${id}"]`).click();
    const changedAt=(await mix()).time;
    await page.waitForFunction(at=>window.player.mixer().time>at+.2,changedAt);
    await page.waitForFunction(()=>window.mixLevel()?.rms>.0001);
    const state=await mix();
    assert.ok(state.tracks.every(t=>t.effectiveGain===(t.id===id?t.gain:0)));
    checks.push({solo:id,time:state.time,level:await page.evaluate(()=>window.mixLevel())});
  }
  await page.locator('[data-reset]').click();
  for(const t of initial.tracks)await page.locator(`[data-mute="${t.id}"]`).click();
  const mutedAt=(await mix()).time;
  await page.waitForFunction(()=>window.mixLevel()?.peak===0);
  await page.waitForFunction(at=>window.player.mixer().time>at+.2,mutedAt);
  assert.ok((await mix()).playing,'Muting every channel does not stop film time');
  await page.locator('[data-reset]').click();
  await page.evaluate(()=>{window.player.seek(40);window.player.seek(120);window.player.seek(185);});
  await page.waitForFunction(()=>window.audioStarts.at(-1)?.offset===185);
  const rapid=await page.evaluate(()=>window.audioStarts.slice(-5));
  assert.equal(new Set(rapid.map(s=>s.at)).size,1);
  assert.deepEqual(rapid.map(s=>s.offset),[185,185,185,185,185]);
  await page.waitForFunction(()=>window.mixLevel()?.rms>.001);
  await page.evaluate(()=>window.player.pause());
  await page.waitForFunction(()=>window.mixLevel()?.peak===0);
  await seek(185);
  await page.screenshot({path:resolve(out,'mixer-ending.png')});
  await page.locator('#title').click();
  await page.keyboard.press('ArrowLeft');await page.evaluate(()=>window.player.idle());
  assert.equal((await mix()).time,183);
  await page.keyboard.press('ArrowRight');await page.evaluate(()=>window.player.idle());
  assert.equal((await mix()).time,185);
  assert.deepEqual(await page.locator('#surface').boundingBox(),geometry);
  await seek(0);
  assert.deepEqual(errors,[]);
  await writeFile(resolve(out,'browser-verification.json'),JSON.stringify({status:'passed',initial,
    checks,rapidSeek:rapid,mutedClockAdvanced:true,shortcutsSeconds:2,errors,
    listening:'Native output measured; no subjective listening assessment by the agent.'},null,2)+'\n');
  console.log(`Full film: ${checks.length} checks, 5 synchronized channels, native output, mute/solo, rapid seek, pause, stable layout and 2-second keys passed.`);
}finally{await browser.close();}
