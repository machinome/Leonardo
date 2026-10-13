// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const read=async file=>JSON.parse(await readFile(resolve(base,file)));
const doc=await read('_build/movie-resolved.json');
const manifest=await read('_build/reading-pauses/narration-manifest.json');
const original=await read('auditions/proposal-8/_build/narration-manifest.json');
assert.equal(manifest.text,original.text,'Spoken text must remain approved.');
const chapter=doc.chapters[0],fps=doc.output.fps;
const pauses=manifest.pauses.filter(p=>p.minimum===5);
assert.equal(pauses.length,4);
for(const pause of pauses){
  const shot=chapter.shots.find(s=>s.id===pause.shot);
  const end=chapter.speechOffset+pause.voiceEnd;
  const next=chapter.speechOffset+pause.nextVoiceStart;
  assert(next-end>=5&&shot.end-end>=5);
  // The browser layout starts arriving before the next shot's formal cut.
  const reveal=shot.cues.find(c=>c.actions.some(a=>a.element==='studio-ui'&&a.action==='reveal'));
  if(reveal)assert(shot.start+reveal.at-end>=5);
  if(shot.id==='testing'){
    const keys=shot.model.keys.filter(k=>shot.start+k.at>end);
    assert(new Set(keys.map(k=>k.seconds)).size>=3,'Keep stepping in the silent tail.');
    const lastChange=keys.findLast(k=>k.seconds!==keys[keys.indexOf(k)-1]?.seconds);
    assert(shot.end-shot.start-lastChange.at<=2/fps,'No frozen tail after the steps.');
  }
  console.log(`${shot.id}: ${end.toFixed(3)}–${next.toFixed(3)}s without narration; cut ${shot.end.toFixed(3)}s`);
}
assert(!chapter.elements.limits);
assert.equal(chapter.elements['ai-notice'].text,'Conteúdo de IA');
const studio=manifest.sections.find(s=>s.id==='studio');
assert(studio.end-studio.start>original.sections.find(s=>s.id==='studio').end-original.sections.find(s=>s.id==='studio').start);
assert(doc.output.durationSeconds<270,'Leave at least half a minute for the live introduction.');
console.log(`Duration ${doc.output.durationSeconds}s; ${300-doc.output.durationSeconds}s available in five minutes.`);
