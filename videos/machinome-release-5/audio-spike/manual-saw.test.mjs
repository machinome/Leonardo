// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createManualSaw} from './manual-saw.mjs';
import {rms} from './synthesis.mjs';
const sampleRate=8000,duration=8;
const strokes=[173,347].map(f=>Float32Array.from({length:3200},(_,i)=>.2*Math.sin(2*Math.PI*f*i/sampleRate)));
const recipe={topMm:170,bottomMm:122,startProgress:.25,returnGain:.18,edgeSeconds:.008};
function render({rate=1,engaged=1,blocks=128,jump=false}={}){
  const controls={sample(i){const t=i/sampleRate,a=Math.PI/2*t*rate;
    return {phase:90*t*rate+(jump&&t>=4?10000:0),phaseRate:90*rate,
      bladePosition:146+24*Math.cos(a),velocity:-24*Math.sin(a)*Math.PI/2*rate,
      engaged,continuous:!(jump&&i===4*sampleRate),sawGain:1};}};
  const r=createManualSaw({sampleRate,duration,controls,strokes,recipe});while(r.process(blocks)){}return r;
}
test('each audible scrape preserves the source samples and original pitch',()=>{
  const r=render(),e=r.events[0],source=strokes[e.variant];
  for(let i=200;i<2500;i++)assert.equal(r.audio[e.startSample+i],source[i]);
  assert.equal(e.playbackRate,1);assert.equal(e.sourceSamples,3200);
});
test('faster motion changes event timing, never stretches or pitch-sweeps a hand stroke',()=>{
  const a=render(),b=render({rate:2});
  assert.equal(a.events.length,4);assert.equal(b.events.length,8);
  const x=a.events[0],y=b.events[0];assert.ok(Math.abs(x.at/2-y.at)<1/sampleRate);
  for(let i=200;i<2500;i++)assert.equal(a.audio[x.startSample+i],b.audio[y.startSample+i]);
});
test('a short native scrape is followed by silence, not repeated to fill the half-cycle',()=>{
  const r=render(),e=r.events[0];
  assert.ok(rms(r.audio.subarray(e.startSample,e.startSample+3200))>.05);
  assert.equal(rms(r.audio.subarray(e.startSample+3300,e.startSample+7000)),0);
  assert.ok(r.events[1].gain<r.events[0].gain*.2);
});
test('stopped or disengaged manual tools are silent',()=>{
  assert.equal(rms(render({rate:0}).audio),0);assert.equal(rms(render({engaged:0}).audio),0);
});
test('a time jump cancels the sounding stroke instead of playing a backlog',()=>{
  const r=render({jump:true});assert.equal(r.audio[4*sampleRate],0);assert.ok(r.events.length<=5);
});
test('native-stroke playback is identical across audio block sizes',()=>{
  const a=render({blocks:127}),b=render({blocks:4096});assert.deepEqual(a.audio,b.audio);assert.deepEqual(a.events,b.events);
});
