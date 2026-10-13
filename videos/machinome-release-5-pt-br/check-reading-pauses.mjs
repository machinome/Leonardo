// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const read=async file=>JSON.parse(await readFile(resolve(base,file)));
const doc=await read('_build/movie-resolved.json');
const selection=await read('preview-take.json');
const manifest=await read(selection.manifest);
const original=await read('auditions/proposal-8/_build/narration-manifest.json');
assert.equal(manifest.text,original.text.replace('Eu sou o Machinome.','Eu sou Machinome!'),
  'Only the requested closing declaration changes.');
const chapter=doc.chapters[0],fps=doc.output.fps;
const pauses=manifest.pauses.filter(p=>['face-reveal','testing','behind-the-film','mirror'].includes(p.shot));
assert.equal(pauses.length,4);
for(const pause of pauses){
  const shot=chapter.shots.find(s=>s.id===pause.shot);
  const end=chapter.speechOffset+pause.voiceEnd;
  const next=chapter.speechOffset+pause.nextVoiceStart;
  assert.equal(pause.minimum,3);
  assert(next-end>=3&&shot.end-end>=3);
  // The browser layout starts arriving before the next shot's formal cut.
  const reveal=shot.cues.find(c=>c.actions.some(a=>a.element==='studio-ui'&&a.action==='reveal'));
  if(reveal)assert(shot.start+reveal.at-end>=3);
  if(shot.id==='testing'){
    const keys=shot.model.keys.filter(k=>shot.start+k.at>end);
    assert(new Set(keys.map(k=>k.seconds)).size>=2,'Keep stepping in the silent tail.');
    const lastChange=keys.findLast(k=>k.seconds!==keys[keys.indexOf(k)-1]?.seconds);
    assert(shot.end-shot.start-lastChange.at<=2/fps,'No frozen tail after the steps.');
  }
  console.log(`${shot.id}: ${end.toFixed(3)}–${next.toFixed(3)}s without narration; cut ${shot.end.toFixed(3)}s`);
}
assert(!chapter.elements.limits);
assert.equal(chapter.elements['ai-notice'].text,'Conteúdo de IA');
assert(!manifest.audioEdits.some(e=>e.shot.startsWith('studio')),'Never splice the Studio phrase.');
for(const p of manifest.pauses){
  assert(p.acousticSilence.end-p.acousticSilence.start>=.12);
  assert(p.at>p.acousticSilence.start&&p.at<p.acousticSilence.end);
  assert(p.nextVoiceStart-p.voiceEnd>=p.minimum);
}
const identity=manifest.pauses.find(p=>p.shot==='identity');
assert(identity.nextVoiceStart-identity.voiceEnd>=1.5);
const purpose=manifest.pauses.find(p=>p.shot==='purpose');
assert(purpose.nextVoiceStart-purpose.voiceEnd>=2);
const studio=manifest.sections.find(s=>s.id==='studio');
assert(studio.end-studio.start>original.sections.find(s=>s.id==='studio').end-original.sections.find(s=>s.id==='studio').start);
assert(doc.output.durationSeconds<270,'Leave at least half a minute for the live introduction.');
console.log(`Duration ${doc.output.durationSeconds}s; ${300-doc.output.durationSeconds}s available in five minutes.`);
