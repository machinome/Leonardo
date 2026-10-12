// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import assert from 'node:assert/strict';
import {readFile,writeFile,readdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const out=resolve(process.argv[2]),base=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const sha=b=>createHash('sha256').update(b).digest('hex');
const artifacts={};
for(const [label,audio] of [['opening-with-effects','mix.wav'],['opening-effects-only','effects.wav']]){
  const file=resolve(out,`${label}.mp4`);
  execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',resolve(out,'opening-silent.mp4'),
    '-i',resolve(out,audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
    '-t','17','-movflags','+faststart',file]);
  const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file]));
  const v=probe.streams.find(s=>s.codec_type==='video'),a=probe.streams.find(s=>s.codec_type==='audio');
  assert.equal(v.width,960);assert.equal(v.height,540);assert.equal(v.nb_frames,'408');
  assert.equal(v.avg_frame_rate,'24/1');assert.equal(Number(v.duration),17);
  assert.equal(a.sample_rate,'48000');assert.ok(Math.abs(Number(a.duration)-17)<.025);
  execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-i',file,'-f','null','-']);
  artifacts[label]={sha256:sha(await readFile(file)),probe};
}
const frames=(await readdir(resolve(out,'frames'))).filter(f=>f.endsWith('.png'));
assert.equal(frames.length,408);
const saved=JSON.parse(await readFile(resolve(out,'source-hashes.json')));
for(const [f,digest] of Object.entries(saved))
  assert.equal(sha(await readFile(resolve(base,f))),digest,`${f} remains unchanged`);
const recordedSaw={title:'Hand Saw Sawing Wood',author:'deleted_user_7146007',
  page:'https://freesound.org/people/deleted_user_7146007/sounds/383725/',
  url:'https://cdn.freesound.org/previews/383/383725_7146007-hq.mp3',
  license:'CC0 (as stated on the sound page)',
  sha256:sha(await readFile(resolve(out,'saw-recording.mp3'))),
  use:'25 seconds from 5s; filtered, broken into 65ms overlapping grains, and driven by model blade velocity.'};
await writeFile(resolve(out,'manifest.json'),JSON.stringify({created:new Date().toISOString(),
  type:'project-local-simulation-audio-spike',interval:[0,17],releaseReady:false,
  capture:'Existing live stage, 408 frames; bottom CSS rounding row cropped from 960x541 to 960x540.',
  preservedSourceHashes:saved,recordedSaw,water:'Earlier anonymous MMAudio water audition; provider provenance retained beside original.',
  wheel:'Seeded procedural friction and wooden resonances; no generated axle sample was obtained.',
  failedGeneration:'Two text requests and one video request rejected by MMAudio with null error; records retained.',
  effects:'Model-timed, not a speed-adjusted mixed recording.',
  listeningReview:'Not performed by the agent; ready for pilot review.',artifacts},null,2)+'\n');
console.log(`Ready: ${resolve(out,'opening-with-effects.mp4')}`);
console.log(`Effects only: ${resolve(out,'opening-effects-only.mp4')}`);
