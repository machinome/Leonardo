<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Source syntax study

The next 28-second release-film segment after the dark-sequence study.
The pilot approved the continuous Machinome pronunciation, then requested
word-synced emphasis to demonstrate the expressiveness of the actual syntax.

The dark machine → source → machine sequence is retained. Real PEP 8 source
comes from the same committed revision as the freshly regenerated export.
In line 376, `waterwheel`, `drives` and `crankshaft` receive cumulative
highlights at their measured spoken onsets. All three hold briefly, then
clear. No code scrolling, split-screen animation or burned subtitles.
The final simulation lines still reveal near the end of the code scene.

Jessica / Eleven v3 uses the approved `Masheenome` spoken alias. The written
name stays Machinome. The one changed narration phrase now explicitly says
“the waterwheel drives the crankshaft.” A new continuous take is cached;
it is not assembled from separately synthesized words.

## Reproduce

From `/home/asa/devel/machinome/videomaker`:

```sh
node bin/videomaker.mjs speech \
  ../projects/Leonardo/videos/machinome-syntax-study/episode.yaml
node experiments/dark-source/render.mjs \
  ../projects/Leonardo/videos/machinome-syntax-study/visual.yaml \
  ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

`episode.yaml` and `production.yaml` own narration and model settings;
`visual.yaml` owns the empirical edit. This remains an isolated visual
experiment, not a ratified new Videomaker format. Append `--preview` to
the experimental renderer for stills. It checks alignment against the actual
cached take and fails if source words, the spoken phrase or timing no longer
match. It never purchases speech.

Outputs are `_build/dark-source.mp4`, `_build/dark-source.srt`, preview PNGs
and `experiment-manifest.json`. Copy `watch.html` to `_build/index.html` and
serve `_build/` at <http://127.0.0.1:8769/> for the review page. The description
draft carries credits and reconstruction limits; the film does not.

## Verification — 28 September 2026

Rendered with Videomaker `fb1956c`: 840 frames, 1920×1080, 30 fps, 28 seconds,
H.264 video plus AAC audio, no subtitle stream. All 17 tool tests pass.
Browser checks verify literal source equality, highlight boundaries and
pixel-identical seeking, a still reading hold outside emphasis, and real
mechanism motion before and after the code scene. Decoded MP4 frames show
the progression from no highlight to one, two and three highlighted words.

Measured narration onsets are 11.200 s for waterwheel, 11.897 s for drives,
and 12.387 s for crankshaft; highlights clear at 14.100 s. Rendering samples
those times on the 30 fps grid. The full 23.28-second take starts at 0.8 s,
with no truncation or time stretching. Speech timing and sample provenance
were checked; no claim of auditory review is made for this new take.

The review page and its replay-line button pass a real browser check at the
same port, 8769. Separate SRT downloads correctly. Earlier MP4s and the
approved pronunciation audition WAV are unchanged.

MP4 SHA-256: `cfb69bfe89418ed8726a696d5d984bae59c3b959a719862f7e1cd346f827f2b6`.
