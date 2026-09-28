<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Dark, source-only study

The pilot rejected simultaneous code and animation: too much competing motion,
too little architectural context. This experiment starts with the actual
`machinome` imports and `LeonardoHydraulicSawmill(AssemblyNode)` visible. Only
the final `simulate` method reveals at 23.8–26.2 seconds. Everything else stays
still; the charcoal background lasts for the whole 28-second sample.

The feminine Jessica / Eleven v3 take is reused unchanged to isolate the visual
decision. No new synthesis was purchased. Subtitles remain separate. The code
is selected from the actual pinned model, with omission markers, not rewritten
as a complete executable example. Nothing represents the historical typing session.

This is explicitly an empirical test **before specs**, not a ratified interface
or a redesign of the full release movie. The full movie has not been rerendered;
dark is the requested overall direction, being tested here first. Earlier
white-background studies and the original release master remain untouched.

From `/home/asa/devel/machinome/videomaker`:

```sh
node experiments/dark-source/render.mjs \
  ../projects/Leonardo/videos/machinome-dark-source/episode.yaml
```

Outputs: `_build/dark-source.mp4`, `_build/dark-source.srt`, three preview PNGs
and `experiment-manifest.json`. The [episode](episode.yaml) is editable prose
and settings; the isolated renderer is disposable, not the supported CLI.
The [upload description](description.md) holds credits and limitations.

Review evidence: 28.000 seconds, 1920×1080, 30 fps, 840 H.264 frames and AAC
audio; no embedded subtitle stream. Static-hold and exact replay checks pass.
The complete source was inspected both in the preview and decoded from the
actual MP4 at 26.8 seconds; no clipping or overlapping content. Narration is
unchanged from the previous study and was not newly auditioned. Video SHA-256:
`06e198177fefbb690ebba254bda7286ac433f25e0cf8090870fa1ba1bd1b1cfd`.
