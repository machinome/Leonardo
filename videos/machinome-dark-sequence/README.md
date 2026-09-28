<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Dark sequence: machine → source → machine

An actual edit to evaluate the pilot's requested combination, not an isolated
code card. 0–4.5 seconds: complete animated sawmill. 4.5–20.5: source-only scene,
static until the last two lines reveal at 16.5–18.5. 20.5–28: moving mechanism.
Dark background throughout. Code and machine never share the screen.

The same Jessica / Eleven v3 narration and external subtitles are reused.
No new speech purchase, no mechanical changes, no permanent format or specs.
The original release film and prior experiments remain unchanged.

From `/home/asa/devel/machinome/videomaker`:

```sh
node experiments/dark-source/render.mjs \
  ../projects/Leonardo/videos/machinome-dark-sequence/episode.yaml \
  ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

Append `--preview` to inspect the five scene samples without encoding.
Outputs: `_build/dark-source.mp4`, `_build/dark-source.srt`, preview PNGs and
`experiment-manifest.json`. The [recipe](episode.yaml) owns the actual edit.
See the [description](description.md) for attribution and limitations.

Validation, 28 September 2026: rendered 840 frames at 1920×1080, 30 fps,
28 seconds, with audio and no subtitle stream. Inspected decoded MP4 frames
on both sides of both cuts (`_build/encoded-cuts.png`); animation precedes
and follows the full-screen source. Decoded frames at 1/2 seconds and 22/23
seconds differ, and capture checks prove deterministic motion in each shot.
The code reading hold is pixel-static; only the final lines reveal.
All 14 Videomaker tests pass. The cached feminine narration and SRT are
unchanged; audio timing and sample provenance were checked, not listening.
The original release film and previous dark-source film retain their hashes.

MP4 SHA-256: `36a12d3d87be5caf07182a8608baf8eaa589f70da7e489bcaab0b56efee3bb7d`.
This is a visual test awaiting the pilot's judgment, not an approved direction.
