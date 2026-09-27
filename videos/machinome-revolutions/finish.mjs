// Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
// Original, deterministic electronic score and final mix. No sampled assets.
import {readFile, writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {dirname, resolve} from 'node:path';

const base = dirname(fileURLToPath(import.meta.url));
const build = resolve(base, '_build');
const source = JSON.parse(await readFile(resolve(build, 'rehearsal-manifest.json')));
const episode = source.episode;
const duration = episode.output.durationSeconds;
const sr = 48000;
const frames = Math.round(duration * sr);
const left = new Float32Array(frames);
const right = new Float32Array(frames);
const tau = 2 * Math.PI;
const hz = note => 440 * 2 ** ((note - 69) / 12);
const smooth = x => { x = Math.max(0, Math.min(1, x)); return x*x*(3-2*x); };
const shot = id => {
  const found = episode.shots.find(s => s.id === id);
  if (!found) throw new Error(`Missing score cue: ${id}`);
  return found;
};

// Broad, quietly changing open intervals. Their attacks overlap at each cue.
const harmony = [
  ['revolution', [50, 57, 64]], ['river', [50, 57, 62, 66]],
  ['stroke', [50, 57, 64]], ['relationships', [43, 55, 62, 69]],
  ['machinome', [47, 54, 62, 66]], ['genome', [43, 55, 59, 62]],
  ['corrections', [50, 57, 64]], ['now', [43, 55, 62, 66]],
  ['purpose', [45, 57, 62, 64]], ['next-revolution', [38, 50, 57, 66]],
];
for (let h = 0; h < harmony.length; h++) {
  const [id, notes] = harmony[h];
  const start = shot(id).start;
  const end = h + 1 < harmony.length ? shot(harmony[h+1][0]).start + 2 : duration;
  const a = Math.max(0, Math.floor((start - 2) * sr));
  const b = Math.min(frames, Math.ceil(end * sr));
  for (let n = 0; n < notes.length; n++) {
    const f = hz(notes[n]);
    const pan = notes.length === 1 ? 0 : (n / (notes.length-1) - .5) * .65;
    for (let i = a; i < b; i++) {
      const t = i / sr;
      const env = smooth((t-start+2)/4) * smooth((end-t)/3);
      const breath = .85 + .15 * Math.sin(tau * .065 * t + n);
      const v = .012 * env * breath * (Math.sin(tau*f*t+n) + .12*Math.sin(tau*f*2*t));
      left[i] += v * Math.sqrt((1-pan)/2);
      right[i] += v * Math.sqrt((1+pan)/2);
    }
  }
}

function pluck(start, note, amplitude, decay, pan = 0) {
  const f = hz(note);
  const a = Math.max(0, Math.floor(start * sr));
  const b = Math.min(frames, Math.ceil((start + 6*decay) * sr));
  for (let i = a; i < b; i++) {
    const t = i/sr - start;
    const env = (1-Math.exp(-t/.018)) * Math.exp(-t/decay);
    const fundamental = Math.sin(tau*f*t);
    const overtone = .22 * Math.exp(-t/.3) * Math.sin(tau*f*3*t);
    const v = amplitude * env * (fundamental + overtone);
    left[i] += v * Math.sqrt((1-pan)/2);
    right[i] += v * Math.sqrt((1+pan)/2);
  }
}

// A turn becomes a pulse; the motif opens out when source code enters the film.
for (let t = .6, n = 0; t < shot('relationships').start; t += 2, n++)
  pluck(t, n%2 ? 57 : 50, .029, .36, n%2 ? .22 : -.22);
for (const id of ['revolution', 'river', 'relationships', 'machinome', 'now', 'next-revolution']) {
  const start = shot(id).start;
  [62, 69, 64, 66].forEach((note, n) => pluck(start + .5 + [0, 1.5, 3.5, 6][n], note, .031, 1.5, (n-1.5)*.2));
}
pluck(shot('invitation').start, 74, .025, 2.1);

const wav = Buffer.alloc(44 + frames * 4);
wav.write('RIFF',0); wav.writeUInt32LE(wav.length-8,4); wav.write('WAVEfmt ',8);
wav.writeUInt32LE(16,16); wav.writeUInt16LE(1,20); wav.writeUInt16LE(2,22);
wav.writeUInt32LE(sr,24); wav.writeUInt32LE(sr*4,28);
wav.writeUInt16LE(4,32); wav.writeUInt16LE(16,34);
wav.write('data',36); wav.writeUInt32LE(frames*4,40);
for (let i=0; i<frames; i++) {
  const t = i/sr;
  const envelope = smooth(t/1.4) * smooth((duration-t)/3.5);
  for (const [channel, samples] of [[0,left],[1,right]]) {
    const v = samples[i] * envelope;
    if (!Number.isFinite(v) || Math.abs(v) >= 1) throw new Error('Score clipping');
    wav.writeInt16LE(Math.round(v*32767),44+i*4+channel*2);
  }
}
const score = resolve(build,'score.wav');
await writeFile(score,wav);
const narration = resolve(build,'narration.wav');
const mix = resolve(build,'mix.wav');
const filter = '[0:a]highpass=f=65,asplit=2[voice][key];' +
  '[1:a]loudnorm=I=-28:TP=-6:LRA=8,lowpass=f=5000[bed];' +
  '[bed][key]sidechaincompress=threshold=0.025:ratio=3:attack=40:release=650[ducked];' +
  '[voice][ducked]amix=inputs=2:duration=first:normalize=0[out]';
execFileSync('ffmpeg',['-y','-v','error','-i',narration,'-i',score,
  '-filter_complex',filter,'-map','[out]','-ar','48000','-c:a','pcm_s24le',mix]);

let measurement;
try {
  // ffmpeg emits the measurement on stderr even on success.
  const {spawnSync} = await import('node:child_process');
  const result = spawnSync('ffmpeg',['-hide_banner','-i',mix,'-af',
    'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],{encoding:'utf8'});
  if (result.status !== 0) throw new Error(result.stderr);
  measurement = JSON.parse(result.stderr.slice(result.stderr.lastIndexOf('{')));
} catch (error) { throw new Error('Master loudness measurement failed: '+error.message); }
const master = resolve(build,'master.wav');
const normalize = `loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=${measurement.input_i}:`+
  `measured_TP=${measurement.input_tp}:measured_LRA=${measurement.input_lra}:`+
  `measured_thresh=${measurement.input_thresh}:offset=${measurement.target_offset}:linear=true`;
execFileSync('ffmpeg',['-y','-v','error','-i',mix,'-af',normalize,
  '-ar','48000','-c:a','pcm_s24le',master]);
const output = resolve(build,'machinome-revolutions.mp4');
execFileSync('ffmpeg',['-y','-v','error','-i',source.output,'-i',master,
  '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
  '-t',String(duration),'-movflags','+faststart','-metadata','title=Revolutions | Machinome',output]);
const probe = JSON.parse(execFileSync('ffprobe',['-v','error','-count_frames',
  '-show_streams','-show_format','-of','json',output],{encoding:'utf8'}));
const video = probe.streams.find(s=>s.codec_type==='video');
const sound = probe.streams.find(s=>s.codec_type==='audio');
if (video.width!==episode.output.width || video.height!==episode.output.height ||
    Number(video.nb_read_frames)!==duration*episode.output.fps || !sound ||
    Math.abs(Number(probe.format.duration)-duration)>.1) throw new Error('Final media does not match the edit');
const sha = async path => createHash('sha256').update(await readFile(path)).digest('hex');
await writeFile(resolve(build,'release-manifest.json'),JSON.stringify({
  output, outputSha256:await sha(output), duration, probe,
  narrationSha256:await sha(narration), scoreSha256:await sha(score),
  masterSha256:await sha(master), finishingScriptSha256:await sha(fileURLToPath(import.meta.url)),
  captureManifest:'rehearsal-manifest.json', captureManifestSha256:await sha(resolve(build,'rehearsal-manifest.json')),
  score:'Original deterministic electronic composition, no samples; illustrative soundtrack, not recorded machine sound.',
  loudnessTarget:{integratedLUFS:-16,truePeakDBTP:-1.5},measurement,
  releaseReady:source.releaseReady,published:false,
},null,2)+'\n');
console.log(output);
