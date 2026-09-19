/* Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. */
'use strict';
const $ = id => document.getElementById(id);
const views = {
  whole: {camera: [940,-1260,940], target: [0,-20,290]},
  drive: {camera: [330,-630,300], target: [0,-135,145]},
  saw: {camera: [335,-470,505], target: [0,0,445]},
  feed: {camera: [180,720,480], target: [-105,115,337]},
};
let viewer, navigator, phase = 0, playing = !matchMedia('(prefers-reduced-motion: reduce)').matches;
let revealed = false, mounting = false, previousTime, measurements, resetUntil = 0;
let currentView = 'whole';
const stage = $('stage');
const controls = document.querySelectorAll('button, input, select');
// This table is measured from the Python CAD. It changes labels only;
// machinome's exported relations drive every solid and the flexible rope.
function reading(angle) {
  const x = Math.max(0,Math.min(360,angle)) / measurements.step;
  const i = Math.min(measurements.rows.length-2, Math.floor(x));
  return measurements.rows[i].map((v,j) => v+(measurements.rows[i+1][j]-v)*(x-i));
}
function status() {
  $('status').textContent = performance.now() < resetUntil
    ? 'REPLAY RESET · CARRIAGE RETURNED'
    : playing ? 'THE MILL IS RUNNING' : 'PAUSED FOR A CLOSER LOOK';
}

function setPlaying(value) {
  playing = value;
  $('play').textContent = playing ? 'Ⅱ' : '▶';
  $('play').setAttribute('aria-label', playing ? 'Pause animation' : 'Play animation');
  status();
}
function pose() {
  if (!viewer || !measurements) return;
  viewer.setTime(phase / measurements.pass_angle);
  $('timeline').value = phase;
  const a = phase % 360;
  const [drop,increment] = reading(a);
  const turn = Math.min(measurements.pass_turns-1, Math.floor(phase/360));
  const startFeed = measurements.turn_feed[turn];
  const turnFeed = measurements.turn_feed[turn+1]-startFeed;
  const feed = phase >= measurements.pass_angle ? measurements.turn_feed.at(-1)
    : startFeed + turnFeed*increment/measurements.feed_per_turn;
  $('angle').textContent = `${Math.round(a)}°`;
  $('feed').innerHTML = `${feed.toFixed(1)} <i>mm</i>`;
  $('cycle').textContent = `${String(Math.min(measurements.pass_turns,Math.floor(phase/360)+1)).padStart(2,'0')} / ${measurements.pass_turns}`;
  $('stroke-label').textContent = a < 180 ? 'CUTTING STROKE' : 'RETURN & FEED';
  $('trace-dot').setAttribute('cx', a*280/360);
  $('trace-dot').setAttribute('cy', 14+drop*56/48);
  status();
}
function applyReveal() {
  const names = new Set(['Frame and guides','Water channel','Water surface']);
  const walk = node => { if (names.has(node.name)) viewer.setVisible(node.path, !revealed); node.children.forEach(walk); };
  walk(viewer.assembly());
  $('reveal').setAttribute('aria-pressed',String(revealed));
  $('reveal').textContent = revealed ? '◇ Restore timber frame' : '◇ Reveal mechanism';
}
async function mount(name='whole') {
  if (mounting) return;
  mounting = true;
  controls.forEach(c => c.disabled = true);
  try {
    if (!measurements) {
      const response = await fetch('readouts.json');
      if (!response.ok) throw new Error('CAD measurement table unavailable');
      measurements = await response.json();
      $('timeline').max = measurements.pass_angle;
      document.querySelector('.transport-note').textContent = `${measurements.pass_turns} turns · ${measurements.pass_seconds} seconds`;
      const curve = Array.from({length:121}, (_,i) => `${i?'L':'M'}${i*280/120},${14+reading(i*3)[0]*56/48}`).join(' ');
      $('stroke-curve').setAttribute('d', curve);
    }
    if (navigator) navigator.dispose();
    if (viewer) viewer.dispose();
    const chosen = views[name];
    const factor = Math.max(1, 560 / stage.clientWidth);
    const view = {target:chosen.target, camera:chosen.camera.map((v,i) => chosen.target[i]+(v-chosen.target[i])*factor)};
    viewer = await MachinomeViewer.mount(stage, '../../export/hydraulic_sawmill/manifest.json', {
      animation: 'external', driverControls: 'none', autoplay: false,
      time: phase / measurements.pass_angle, view, up: [0,0,1], fov: 37,
      ariaLabel: 'Interactive three-dimensional reconstruction of Leonardo’s hydraulic sawmill',
    });
    navigator = MachinomeViewer.mountNavigator('#assembly-tree', viewer, {label: 'Sawmill assembly'});
    applyReveal(); pose(); setPlaying(playing);
    $('loading').hidden = true;
    document.querySelectorAll('.view-tabs button').forEach(b => b.classList.toggle('active',b.dataset.view===name));
    document.body.dataset.ready = 'true';
    currentView = name;
    // Read-only observability for the project's browser acceptance check.
    window.exhibit = {get phase(){return phase}, get playing(){return playing}, get revealed(){return revealed}, get view(){return viewer.view()}, get assembly(){return viewer.assembly()}};
  } catch(error) {
    $('loading').hidden = false;
    $('loading').textContent = `The model could not open: ${error.message}`;
    $('status').textContent = 'MODEL UNAVAILABLE';
    console.error(error);
  } finally {
    mounting = false;
    controls.forEach(c => c.disabled = false);
  }
}
$('play').addEventListener('click', () => setPlaying(!playing));
$('reset').addEventListener('click', () => {phase=0;resetUntil=performance.now()+1800;pose()});
$('timeline').addEventListener('input', e => {setPlaying(false);phase=Number(e.target.value);pose()});
$('reveal').addEventListener('click', () => {revealed=!revealed;applyReveal()});
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => mount(button.dataset.view)));
let resizeTimer;
window.addEventListener('resize', () => {clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>mount(currentView),250)});
document.addEventListener('keydown', e => {
  if (e.code==='Space' && e.target===document.body) {e.preventDefault();setPlaying(!playing)}
});
function frame(now) {
  const elapsed = previousTime === undefined ? 0 : Math.min((now-previousTime)/1000,0.1);
  previousTime = now;
  if (viewer && playing && !mounting && !document.hidden) {
    const next=phase+elapsed*(measurements.pass_angle/measurements.pass_seconds)*Number($('speed').value);
    if (next>=measurements.pass_angle) resetUntil=now+1800;
    phase=next%measurements.pass_angle;pose();
  }
  requestAnimationFrame(frame);
}
mount();requestAnimationFrame(frame);
