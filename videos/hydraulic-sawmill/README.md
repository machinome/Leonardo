# Leonardo’s Sawmill: One Wheel, Two Jobs

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

An 84-second educational rehearsal, built by the independent Videomaker tool.
Read [episode.yaml](episode.yaml) as a screenplay: each shot puts its narration
beside plain-language visual directions, timing and camera cues.
[production.yaml](production.yaml) holds model paths, camera presets, voice
settings, evidence and credits. [description.md](description.md) is release copy
that still needs verified public source and interactive-simulation URLs.

## Editorial plan

One lesson: the same waterwheel reciprocates the saw and times the carriage
feed. Show the input, uncover the transmission, then show the consequence.
The cut uses the model's own shrinking uncut-timber insert; the video does not
fake material removal with an independent masking animation.

| Video seconds | Beat | Model seconds | View |
| --- | --- | --- | --- |
| 0–8 | Who moves the log? | 8–16 | Saw and timber |
| 8–16 | Introduce the reconstruction | 16–24 | Pull out to whole assembly |
| 16–28 | Rotation becomes reciprocation | 24–32 | Wheel, then saw; hide structure |
| 28–37 | Hold on downstroke, feed on return | 32–36 | Saw close-up, timed to narration |
| 37–50 | Driving and holding pawls | 36–44 | Rear feed close-up |
| 50–60 | Winding rope pulls the carriage | 44–52 | Drum to rope/pulley overview |
| 60–69 | Cut / advance | 52–64 | Overhead cut, sash frame hidden |
| 69–84 | Credits and invitation | 64–80 | Whole assembly, visibility restored |

The landscape film has 2,520 frames at 1920×1080 and 30 fps. It uses model
seconds 8–80 of the completed 296-second pass, never rewinding or wrapping.
Video and model clocks are independent. Explicit model keyframes in the hold
and rhythm shots align the half-strokes with measured speech timestamps.
Visibility changes are explanatory reveals, not physical disassembly.

## Build

From the workspace's `videomaker/` repository, after its documented setup:

```sh
node bin/videomaker.mjs check ../projects/Leonardo/videos/hydraulic-sawmill/episode.yaml
node bin/videomaker.mjs build ../projects/Leonardo/videos/hydraulic-sawmill/episode.yaml \
  --viewer ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

The viewer must support API 21 (`setView` and on-demand rendering). That local
viewer capability is not yet released. The export is pinned to model revision
`0904386e9c5c876c51337d704da7b94304b2ee1d`; stale exports are refused.

ElevenLabs George narrates using `eleven_multilingual_v2`. The pilot confirmed
“mah-SHEEN-ohm” (machine + genome); a spoken alias leaves the written name
Machinome intact in captions. The API key belongs only in Videomaker's ignored
`.env`. Eight audio segments and their character timestamps are cached, so
camera/timing revisions do not regenerate unchanged narration.

Generated output belongs only in ignored `_build/`: `rehearsal.mp4`,
`narration.wav`, captions, thumbnail, storyboard, frames, audio caches and
provenance manifests. `preview` makes stills without speech generation;
`render --width 960 --fps 10 --silent` makes a quick silent film.

## Revise and release

Edit each shot's `narration`, `direction`, time mapping and overlays in YAML.
Named cameras and assembly layers are defined in `production.yaml`. The `>-`
marker folds a readable paragraph; `|-` preserves credit-card line breaks.
Speech overflow stops production with a measured duration, never truncation.

Review the MP4, especially pronunciation, caption timing, mechanism phases and
framing. Supply and verify the public simulation/source URLs before publishing.
The build marks unresolved URLs explicitly and sets `releaseReady: false`.
No video is uploaded automatically. This first rehearsal is landscape, not a
vertical Shorts export.
