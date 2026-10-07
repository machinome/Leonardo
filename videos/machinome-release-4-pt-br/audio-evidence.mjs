// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Signal and alignment checks are evidence, not a substitute for listening.
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const base=dirname(fileURLToPath(import.meta.url));
const take=JSON.parse(await readFile(resolve(base,'_build/narration-manifest.json')));
const record=JSON.parse(await readFile(take.cacheFile+'.json'));
const bytes=await readFile(take.cacheFile);
assert.equal(createHash('sha256').update(bytes).digest('hex'),take.sha256);
assert.equal(take.generation,'one-provider-request');
assert.deepEqual(take.edits,[]);
assert.equal(record.request.text.includes('aberto...\n\nA roda'),true);
assert.equal(record.request.text.includes('O que VOCÊ quer construir agora?'),true);
const alignment=record.alignment,text=alignment.characters.join('');
const span=phrase=>{
  const start=text.lastIndexOf(phrase);assert.ok(start>=0);
  return {phrase,start:alignment.character_start_times_seconds[start],
    end:alignment.character_end_times_seconds[start+phrase.length-1]};
};
const tools=span('aberto...'),next=span('A roda faz revoluções, e os humanos constroem'),you=span('VOCÊ');
const check=spawnSync('ffmpeg',['-hide_banner','-ss',String(tools.start),'-t',String(next.start-tools.start+.2),
  '-i',take.cacheFile,'-af','silencedetect=noise=-42dB:d=0.15','-f','null','-'],{encoding:'utf8'});
assert.equal(check.status,0);
const intervals=[...check.stderr.matchAll(/silence_end: ([\d.]+) \| silence_duration: ([\d.]+)/g)]
  .map(m=>({start:tools.start+Number(m[1])-Number(m[2]),end:tools.start+Number(m[1]),duration:Number(m[2])}));
const pause=intervals.find(p=>p.end>=next.start-.1&&p.end<=next.start+.2);
assert.ok(pause&&pause.duration>=.7,'The requested deliberate pause must be present in the audio.');
const report={status:'signal and alignment checked; listening review remains',sha256:take.sha256,
  generation:take.generation,edits:take.edits,duration:take.duration,tools,next,you,pause,thresholdDb:-42};
await writeFile(resolve(base,'_build/audio-evidence.json'),JSON.stringify(report,null,2)+'\n');
console.log(`Unedited full take ${take.duration.toFixed(2)} s; measured pause ${pause.duration.toFixed(3)} s; VOCÊ emphasis present in provider request.`);
