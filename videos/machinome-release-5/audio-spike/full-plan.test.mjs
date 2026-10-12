// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createFilmPlan,createControls} from './full-plan.mjs';
const shots=[
  {id:'revolution',start:0,end:7},
  {id:'ancestor',start:7,end:32,transition:{duration:1.2}},
  {id:'two-jobs',start:32,end:80},
  {id:'document',start:80,end:86,transition:{duration:.4}},
  {id:'python-language',start:86,end:88},
  {id:'face-reveal',start:88,end:104,transition:{duration:.4}},
  {id:'studio',start:104,end:115},
  {id:'studio-rewind-000',start:115,end:117},
  {id:'testing',start:117,end:143},
  {id:'behind-the-film',start:143,end:155},
  {id:'mirror',start:155,end:160},
  {id:'open-source',start:160,end:182},
  {id:'wheel-returns',start:182,end:191},
  {id:'invitation',start:191,end:204},
];
const plan=createFilmPlan({output:{durationSeconds:204},chapters:[{shots}]});
test('opening retains water, wheel introduction and saw reveal',()=>{
  assert.equal(plan.gains(0).waterGain,0);
  assert.equal(plan.gains(1).sawGain,0);
  assert.equal(plan.gains(7).sawGain,0);
  assert.ok(plan.gains(7.6).sawGain>.49);
  assert.equal(plan.gains(9).sawGain,1);
});
test('documents, rewind, tests, film explanation and logo have silent effects',()=>{
  for(const t of [81,87,115,116,120,150,165,191,203])
    assert.deepEqual(plan.gains(t),{waterGain:0,wheelGain:0,sawGain:0},String(t));
});
test('model returns with browser scene, then fades before rewind',()=>{
  assert.equal(plan.gains(88).sawGain,0);
  assert.equal(plan.gains(100).sawGain,.65);
  assert.equal(plan.gains(110).sawGain,.65);
  assert.ok(plan.gains(114.85).sawGain>0&&plan.gains(114.85).sawGain<.65);
});
test('ending introduces only water and wheel, fading out through hole',()=>{
  assert.equal(plan.gains(182).waterGain,0);
  assert.equal(plan.gains(185).waterGain,1);
  assert.equal(plan.gains(185).sawGain,0);
  assert.ok(plan.gains(190.7).waterGain>0&&plan.gains(190.7).waterGain<1);
  assert.equal(plan.gains(191).waterGain,0);
});
test('interpolates source joint values and suppresses time jumps',()=>{
  const rows=[[400,36000,170,1,1],[400.01,36000.9,169.8,1,1],
    null,[0,0,170,0,0],[.01,.9,169.8,0,0]];
  const c=createControls({rows,controlHz:100,sampleRate:1000,plan});
  assert.ok(Math.abs(c.sample(5).velocity+20)<1e-9);
  assert.ok(Math.abs(c.sample(5).phase-36000.45)<1e-9);
  assert.equal(c.sample(15).continuous,false);
  assert.equal(c.sample(15).velocity,0);
  assert.equal(c.sample(25).continuous,false);
  assert.equal(c.sample(30).continuous,false);
});
