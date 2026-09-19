# Leonardo’s Sawmill: One Wheel, Two Jobs

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

**Rehearsal sources only. No audio or video has been generated.**
Entry point: [episode.mjs](episode.mjs). Spoken text lives only in
[narration.mjs](narration.mjs); camera/visibility/time directions live in
[shots.mjs](shots.mjs). [description.md](description.md) is draft release copy.

## Editorial plan

One lesson: the same waterwheel reciprocates the saw and times the carriage
feed. Show the input, uncover the transmission, then show the consequence.
The visual cut uses the model's own shrinking uncut-timber insert; the video
must not fake removal with an independent masking animation.

| Video seconds | Beat | Model seconds | View |
| --- | --- | --- | --- |
| 0–8 | Who moves the log? | 8–16 | Saw and timber |
| 8–16 | Introduce Leonardo's reconstruction | 16–24 | Pull out to whole assembly |
| 16–28 | Rotation becomes reciprocation | 24–32 | Wheel, then saw; reveal structure |
| 28–36 | Hold on downstroke, feed on return | 32–36 | Fixed saw close-up, half speed |
| 36–50 | Rocker, driving pawl and holding pawl | 36–44 | Rear feed close-up |
| 50–60 | Winding rope pulls the carriage | 44–52 | Drum to rope/pulley overview |
| 60–68 | Cut / advance twice | 52–60 | Fixed saw close-up |
| 68–84 | Credits and invitation | 60–76 | Whole assembly, frame restored |

The 84-second landscape rehearsal has 2,520 frames at 30 fps. It uses model
seconds 8–76 of the upcoming 108-second pass, never rewinding or wrapping.
All shot mappings are linear; video and model clocks are independent.
At four model seconds per revolution, the cut/advance labels in the hold and
rhythm shots match the model's two half-strokes. Align spoken words after TTS.

Camera presets originate in the current exhibit, except the proposed rope
overview. Their coordinates and transitions need image review at 1920×1080.
Visibility paths were checked against the in-progress export, not a released
model. Hiding structure is an explanatory reveal, not physical disassembly.

## Before rendering

- Finish and validate the model's full-timber-pass work independently. Its
  current uncommitted edits are not owned by this episode.
- Regenerate the export from the tested model revision and set `sourceRevision`.
  Verify the loop remains 108 seconds, the named parts resolve, and the visual
  cut opens correctly at the chosen times. Do not reuse old four-cycle evidence.
- Build Videomaker and the viewer capabilities the shots require. The draft
  contract is recorded in that repository's `docs/FORMAT.md`.
- Select the synthetic narrator and confirm the pronunciation of Machinome.
  Generate beats into `_build/`, measure speech, align captions and inspect the
  result before fixing the final timing. Eight seconds may need revision for
  a longer line; these are editorial targets, not measured speech durations.
- Supply public simulation/source URLs. Current gallery metadata describes an
  intended source destination, not verified publication. No URL is invented here.

## Inspect the source without rendering

From the gallery root (Node, no package installation):

```sh
node --input-type=module -e 'import episode from "./videos/hydraulic-sawmill/episode.mjs"; console.log(JSON.stringify(episode, null, 2))'
```

Future build output goes only in `_build/`: resolved episode/provenance,
per-beat audio and alignment, frames, captions, thumbnail, MP4 and release copy.
Pin viewer and browser versions and font assets when building the renderer.
