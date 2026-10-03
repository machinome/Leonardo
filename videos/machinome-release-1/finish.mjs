// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Measure speech first, then match the model clock through the two reveals.
// This edits only the generated movie document, never the model or its export.
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
assert.ok(process.argv[2],'Pass the Videomaker checkout.');
const tool=resolve(process.argv[2]);
const {readMovie,resolveMovie}=await import(pathToFileURL(resolve(tool,'src/movie.mjs')));
const {cachedTake}=await import(pathToFileURL(resolve(tool,'src/speech.mjs')));
const file=resolve(base,'_build/movie.json');
const {doc,build}=await readMovie(file);
const pending={audio:doc.audio,chapters:doc.chapters,paths:{build}};
const takes={};
for(const [i,chapter] of doc.chapters.entries()) {
  const take=await cachedTake(pending,i);
  assert.ok(take,`Missing ${chapter.id} narration.`);
  takes[chapter.id]=take;
}
const measured=resolveMovie(doc,takes);
for(const name of ['encounter','intention']) {
  const original=doc.chapters.find(c=>c.id===name);
  const timed=measured.chapters.find(c=>c.id===name);
  const [first,second]=timed.shots;
  const from=original.shots[0].model.from;
  const to=original.shots[1].model.to;
  const cut=from+(to-from)*(first.end-first.start)/(second.end-first.start);
  original.shots[0].model={from,to:cut};
  original.shots[1].model={from:cut,to};
  console.log(`${name}: wheel and machine share a continuous model clock through the reveal.`);
}
await writeFile(file,JSON.stringify(doc,null,2)+'\n');
