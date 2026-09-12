/* Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. */
'use strict';
const $ = id => document.getElementById(id);
const views = {
  whole: {camera: [620,-910,630], target: [0,-30,200]},
  drive: {camera: [360,-660,320], target: [0,-120,170]},
  saw: {camera: [335,-430,405], target: [-5,0,349]},
  feed: {camera: [515,470,495], target: [200,35,330]},
};
let viewer, phase = 0, playing = !matchMedia('(prefers-reduced-motion: reduce)').matches;
let revealed = false, mounting = false, previousTime;
let currentView = 'whole';
const stage = $('stage');
const controls = document.querySelectorAll('button, input, select');
const rad = Math.PI / 180;
const height = a => 24 * Math.cos(a * rad) + Math.sqrt(146 ** 2 - (24 * Math.sin(a * rad)) ** 2);
const curve = Array.from({length:121}, (_,i) => `${i?'L':'M'}${i*280/120},${14+(170-height(i*3))*56/48}`).join(' ');
$('stroke-curve').setAttribute('d', curve);

function setPlaying(value) {
  playing = value;
  $('play').textContent = playing ? 'Ⅱ' : '▶';
  $('play').setAttribute('aria-label', playing ? 'Pause animation' : 'Play animation');
  $('status').textContent = playing ? 'THE MILL IS RUNNING' : 'PAUSED FOR A CLOSER LOOK';
}
function pose() {
  if (!viewer) return;
  viewer.setTime(phase / 1440);
  $('timeline').value = phase;
  const a = phase % 360;
  const q = (phase - Math.asin(Math.sin((phase - 90) * rad)) / rad - 90) / 360;
  const feed = 8 * (q - Math.sin(360*q*rad)/(2*Math.PI));
  $('angle').textContent = `${Math.round(a)}°`;
  $('feed').innerHTML = `${feed.toFixed(1)} <i>mm</i>`;
  $('cycle').textContent = `${String(Math.min(4,Math.floor(phase/360)+1)).padStart(2,'0')} / 04`;
  $('stroke-label').textContent = a < 180 ? 'CUTTING STROKE' : 'RETURN & FEED';
  $('trace-dot').setAttribute('cx', a*280/360);
  $('trace-dot').setAttribute('cy', 14+(170-height(a))*56/48);
}
function applyReveal() {
  const names = new Set(['timber_structure','foundation','flume_water','tailrace','plaque']);
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
    if (viewer) viewer.dispose();
    const chosen = views[name];
    const factor = Math.max(1, 560 / stage.clientWidth);
    const view = {target:chosen.target, camera:chosen.camera.map((v,i) => chosen.target[i]+(v-chosen.target[i])*factor)};
    viewer = await SolidNodeWidget.mount(stage, 'export/manifest.json', {
      animation: 'external', driverControls: 'none', autoplay: false,
      time: phase / 1440, view, up: [0,0,1], fov: 37,
      ariaLabel: 'Interactive three-dimensional reconstruction of Leonardo’s hydraulic sawmill',
    });
    applyReveal(); pose(); setPlaying(playing);
    $('loading').hidden = true;
    document.querySelectorAll('.view-tabs button').forEach(b => b.classList.toggle('active',b.dataset.view===name));
    document.body.dataset.ready = 'true';
    currentView = name;
    // Read-only observability for the project's browser acceptance check.
    window.exhibit = {get phase(){return phase}, get playing(){return playing}, get revealed(){return revealed}, get view(){return viewer.view()}};
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
$('reset').addEventListener('click', () => {phase=0;pose()});
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
  if (viewer && playing && !mounting && !document.hidden) {phase=(phase+elapsed*90*Number($('speed').value))%1440;pose()}
  requestAnimationFrame(frame);
}
mount();requestAnimationFrame(frame);
