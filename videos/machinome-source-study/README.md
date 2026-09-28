<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# A machine you can read

A 28-second second-pass study for the **Machinome release film**, commissioned
after review of `machinome-revolutions`. It is not a new mechanism tutorial.
The original 177-second master and its screenplay remain untouched.

The pilot requested intact phrase beginnings, a more expressive feminine
narrator, actual highlighted Python typing beside animation, and external
subtitles for YouTube or mplayer. Videomaker implements the reusable features;
this directory owns only the consuming scene, narration and production choices.

## Editorial choices

The real source at `models/hydraulic_sawmill/model.py:200–206` shows named parts
and the wheel-to-crankshaft relationship. Videomaker checks the entire file
against the export's pinned revision before extracting these lines. Typing is
an editorial reveal, not a recording of a live execution or the original session.
The simulation itself is unchanged. Hiding the structural frame makes the moving
relationships visible; the whole assembly still belongs to the source model.

Jessica, a stock feminine voice, uses Eleven v3 with natural stability 0.5.
One continuous take gives the sentences context without separate per-shot starts.
The provider output is lossless PCM at 24 kHz, wrapped without trimming in WAV;
the movie has a 48 kHz AAC track and 0.8 seconds of preroll. There is no music,
voice gate or fade-in. This is an audition, not a claim of human listening approval.

Measured narration is 23.04 seconds. The first three typed lines follow the
waterwheel/saw/carriage phrases. The drive line types from 10.40 to 13.12 seconds,
aligned to “Here, the wheel drives the crankshaft.” The final 4.16 seconds hold
the completed code and moving model. No narration is burned into the picture.

## Reproduce

From `/home/asa/devel/machinome/videomaker`:

```sh
node bin/videomaker.mjs check ../projects/Leonardo/videos/machinome-source-study/episode.yaml
node bin/videomaker.mjs speech ../projects/Leonardo/videos/machinome-source-study/episode.yaml
node bin/videomaker.mjs preview ../projects/Leonardo/videos/machinome-source-study/episode.yaml \
  --width 1920 --viewer ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node bin/videomaker.mjs render ../projects/Leonardo/videos/machinome-source-study/episode.yaml \
  --viewer ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

`speech` only makes a paid request if its verified cache is absent. The existing
export is required; `check` refuses a mismatched revision or duration. Edit
`episode.yaml` for narration/typing and `production.yaml` for source, camera or
voice choices. Camera/typing revisions reuse the cached take.

The ignored `_build/rehearsal.mp4` is the review movie; `_build/rehearsal.srt`
is its optional subtitle upload. Load explicitly with:

```sh
mplayer _build/rehearsal.mp4 -sub _build/rehearsal.srt
```

The same-basename SRT may also be discovered automatically by players. Disable
subtitles there to assess the voice by itself. `description.md` owns credits;
none are on screen. Public links remain unresolved and nothing is published.
