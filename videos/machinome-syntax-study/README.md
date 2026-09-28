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

Jessica / Eleven v3 now uses the approved explicit IPA dictionary take from
`../machinome-pronunciation/phoneme.yaml`, not the unreliable `Masheenome`
spelling hint. The complete, 23.6-second audition is reused byte-for-byte;
no new speech is purchased and no words are spliced. The written name stays
Machinome. The narration says “the waterwheel drives the crankshaft.”

## Reproduce

From `/home/asa/devel/machinome/videomaker`:

```sh
node ../projects/Leonardo/videos/machinome-syntax-study/prepare-audio.mjs .
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

`prepare-audio.mjs` verifies the approved WAV hash, exact narration, voice,
model, settings and fit, then imports its real request and alignment into
the experiment's audio record. It applies the existing production mix at
the same 0.8-second offset and regenerates separate subtitles. It has no
network access or synthesis step. Do not substitute the ordinary `speech`
command: that stable command does not yet forward pronunciation dictionaries.

Outputs are `_build/dark-source.mp4`, `_build/dark-source.srt`, preview PNGs
and `experiment-manifest.json`. Copy `watch.html` to `_build/index.html` and
serve `_build/` at <http://127.0.0.1:8769/> for the review page. The description
draft carries credits and reconstruction limits; the film does not.

## Approved phoneme rebuild — 28 September 2026

The approved 23.6-second take starts at 0.8 s and ends at 24.4 s, within
the unchanged 28-second edit. The WAV hash is pinned in `prepare-audio.mjs`.
All three emphasis cues were recalculated from this take's actual alignment:
waterwheel 11.910 s, drives 12.540 s, crankshaft 13.110 s, clearing at
14.823 s. Visual onsets are sampled on the 30 fps grid. Separate SRT timing
was regenerated from that same alignment. The old spelling MP4, SRT and
manifest are retained under `_build/previous-spelling-*` for comparison.

The rebuilt encode is 1920×1080, 30 fps, 840 frames and exactly 28 seconds,
with H.264 video and AAC audio only. All 17 Videomaker tests pass. Renderer
checks pass for real mechanism motion at both ends, literal source text,
three measured highlights, pixel-identical seeking and no burned captions.
Decoded MP4 frames were inspected for the unhighlighted/one/two/three-word
sequence and both machine scenes. The approved raw audio hash is unchanged.

MP4 SHA-256: `3352e74bc94e2dbf0c3b4c18076af4ec3882883624e7fb67edc33dab32176a6c`.
SRT SHA-256: `12684073f77d3cf86fcc33c5b7907ada89a9c7e6a165da901909181398b380ac`.

## Previous spelling take — 28 September 2026

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
