// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createMechanics} from './mechanics.mjs';
import {rms} from './synthesis.mjs';
const sampleRate=8000,duration=8;
const tone=(seconds,f)=>Float32Array.from({length:seconds*sampleRate},(_,i)=>.1*Math.sin(2*Math.PI*f*i/sampleRate));
const assets={saw:[tone(2,300),tone(2,350)],iron:[tone(.55,700),tone(.45,800)]};
const recipe={topMm:170,bottomMm:122,referenceVelocity:24,returnGain:.1,turnaroundFraction:.07,
  ironOffsetDeg:60,ironEveryDeg:180,ironReferenceRate:70.75};
function render({rate=1,blocks=128,engaged=1,jump=false}={}){
  const controls={sample(i){const t=i/sampleRate,phase=90*t*rate+(jump&&t>=4?10000:0),a=90*t*rate*Math.PI/180;
    return {phase,phaseRate:90*rate,bladePosition:146+24*Math.cos(a),velocity:-24*Math.sin(a)*Math.PI/2*rate,
      engaged,continuous:!(jump&&i===4*sampleRate),sawGain:1,wheelGain:1};}};
  const r=createMechanics({sampleRate,duration,controls,assets,recipe});while(r.process(blocks)){}return r;
}
test('hacksaw has quiet turnarounds, a strong cutting stroke and a light return',()=>{
  const a=render().stems.saw;
  assert.ok(rms(a.subarray(0,400))<.0001);
  assert.ok(rms(a.subarray(15600,16400))<.0001);
  assert.ok(rms(a.subarray(8000,10000))>.025);
  assert.ok(rms(a.subarray(24000,26000))<rms(a.subarray(8000,10000))*.2);
});
test('hacksaw sample position follows blade displacement, doubling pitch/cadence at twice the speed',()=>{
  const a=render().stems.saw,b=render({rate:2}).stems.saw;
  // Both peak velocities saturate the same gain, so compare the actual waveform.
  for(let i=3500;i<4500;i++)assert.ok(Math.abs(b[i]-a[i*2])<1e-6);
});
test('disengaged blade and stopped iron mechanism are silent',()=>{
  assert.equal(rms(render({engaged:0}).stems.saw),0);
  const stopped=render({rate:0});assert.equal(rms(stopped.stems.saw),0);assert.equal(rms(stopped.stems.wheel),0);
});
test('iron friction is discrete and phase-driven, not a continuous synthetic drone',()=>{
  const a=render(),b=render({rate:2});
  assert.equal(a.events.length,4);assert.equal(b.events.length,8);
  assert.ok(Math.abs(a.events[0].at-60/90)<1/sampleRate);
  assert.equal(rms(a.stems.wheel.subarray(0,4000)),0);
  assert.equal(rms(a.stems.wheel.subarray(12000,18000)),0);
  assert.ok(rms(a.stems.wheel)>0);
  assert.ok(b.events.every(e=>e.pitch<=1.3));
});
test('a model-time jump cancels old friction and does not schedule skipped turns',()=>{
  const r=render({jump:true});assert.ok(r.events.length<=5);
  assert.equal(r.stems.wheel[4*sampleRate],0);
});
test('mechanical replacement is identical across audio block sizes',()=>{
  const a=render({blocks:127}),b=render({blocks:4096});
  assert.deepEqual(a.stems,b.stems);assert.deepEqual(a.events,b.events);
});
