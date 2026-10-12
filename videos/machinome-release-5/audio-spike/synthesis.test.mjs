// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {createRenderer,texture,random,rms} from './synthesis.mjs';
const recipe=JSON.parse(readFileSync(new URL('./sawmill.json',import.meta.url)));
const sampleRate=8000,duration=2,noise=random(1);
const assets={water:Float32Array.from({length:4096},()=>noise()-.5),
  saw:Float32Array.from({length:4096},()=>noise()-.5)};
function render(rate=1,{engaged=1,blocks=128,jump=false}={}){
  const controls={sample(i){const t=i/sampleRate;return {phase:t*90*rate+(jump&&t>=1?10000:0),
    phaseRate:90*rate,velocity:-12*rate,engaged,continuous:!jump||i!==sampleRate,
    waterGain:1,wheelGain:1,sawGain:1};}};
  const r=createRenderer({sampleRate,duration,controls,assets,recipe});
  while(r.process(blocks)){}return r;
}
test('water texture keeps the same pitch and samples when motion is accelerated',()=>{
  assert.deepEqual(render(1).stems.water,render(2).stems.water);
});
test('phase-linked splash cadence doubles when the motion rate doubles',()=>{
  const a=render(1).telemetry.events,b=render(2).telemetry.events;
  assert.equal(a.length,3);assert.equal(b.length,7);
  assert.ok(Math.abs(a[0].at-.5)<1/sampleRate);
  assert.ok(Math.abs(b[0].at-.25)<1/sampleRate);
});
test('saw pitch responds to blade velocity independently from splash pitch',()=>{
  const a=render(1),b=render(2);
  assert.ok(b.telemetry.pitchMax>a.telemetry.pitchMax);
  assert.ok(b.telemetry.events.every(e=>e.pitch===1));
});
test('disengaged saw and zero-speed mechanism have no mechanical output',()=>{
  assert.equal(rms(render(1,{engaged:0}).stems.saw),0);
  const stopped=render(0);assert.equal(rms(stopped.stems.saw),0);
  assert.equal(rms(stopped.stems.wheel),0);assert.equal(stopped.telemetry.events.length,0);
  assert.ok(rms(stopped.stems.water)>0);
});
test('output is deterministic and independent of audio block boundaries',()=>{
  const a=render(1,{blocks:127}),b=render(1,{blocks:2048});
  assert.deepEqual(a.stems,b.stems);assert.deepEqual(a.telemetry,b.telemetry);
});
test('a declared time discontinuity does not emit skipped paddle crossings',()=>{
  const result=render(1,{jump:true});
  assert.ok(result.telemetry.events.length<=4);
});
test('sample-texture extraction is seeded and refuses silence',()=>{
  const a=texture(assets.water,sampleRate,1,17),b=texture(assets.water,sampleRate,1,17);
  assert.deepEqual(a,b);assert.ok(Math.abs(rms(a)-.15)<1e-6);
  assert.throws(()=>texture(new Float32Array(8000),sampleRate,1,17),/No active/);
});
