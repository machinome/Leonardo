# Study 1 — production evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

8 October 2026. This is an independent portrait adaptation, not a replacement
of cut 5 or the Portuguese cut 4. Only `videos/study-1-pt-br/` was authored.
The gallery's pre-existing edits were retained.

## Narration and editorial boundary

- Leo Antonio — Welcoming & Serene, `EbiSUflQjzm4g7S895SC`, the exact voice
  recorded by `machinome-release-4-pt-br/voice.json`.
- One new continuous ElevenLabs `eleven_v3` performance, 805 characters,
  57.12 seconds; lossless 24 kHz provider audio retained in `_build/audio/`.
- Brazilian Portuguese, with no Machinome character, implementation lesson,
  source code, Studio sequence, product attribution or closing invitation.
- Ends with “Uma roda, duas funções: cortar e avançar.” The 0.35-second
  lead-in and 1.07-second tail give a 58.541667-second film, 1405 frames.
- No speech trimming, stretching or splicing. Final mix peaks at -1.5 dBFS;
  mean level -20.3 dBFS, measured with FFmpeg `volumedetect`.
- The spoken text, closing shot and visible titles were inspected for
  credits. Attribution remains in `description.md` and operator metadata.
- Audio duration, alignment and levels were checked. The agent did not
  listen to the performance; human listening review remains outstanding.

## Picture and timing

1080 × 1920, 24 fps. The model is rendered again with portrait cameras,
not cropped from the earlier landscape MP4. The dark stage uses the existing
local Space Grotesk font. Machine details remain opaque against a faint
complete assembly; moving views share exactly the same camera and pose.

The opening wheel moves immediately. A live 0.8-second reveal retains the
wheel while the whole machine appears. A continuous arc orbits around it.
`finish.mjs` fits that arc and a continuous model clock to the cached take.
The pawl sequence retains the source film's actual model-phase anchors:
436–438 model seconds for the pull, 438–440 for the return.

The final portrait preview at 540 × 960 checked 186 frames, 18 highlights,
13 title-fade checks, opening/closing fades, the assembly reveal, deterministic
pixel replay and invalid-camera rejection. All passed. Each highlight changed
the intended part's pixels, including the previously obscured input winding.
The output and per-part difference images are in `_build/preview/`.

The agent inspected opening, orbit, linkage, pawl, winding, compound-shaft,
carriage and closing images for framing and text. Close-ups deliberately
exclude surrounding structure while preserving faint assembly context.

Python formatting/PEP 8 and JavaScript syntax checks pass for the new sources.
No CAD, dependency, framework or production-tool source was changed.

## Provenance and release limits

The existing model export is cut 3's `_build/model`, also used by cut 5.
Its recorded source is `94a8562cc70e96de0cad1b85a4a7c1e092d2ed5c`, with
`dirty: true`. Its 1460-second posed timeline and Viewer API 29 are reused.
The gallery was at `efff48d7ae2e` and Videomaker at `1617f8184acd` when
rendering began, both with pre-existing uncommitted changes. The actual
asset and stage hashes are recorded in the generated manifests; those
commit IDs alone are not the content rendered.

Public source/simulation URLs remain unresolved. The description follows
the gallery's AGPL-3.0-only NOTICE; there is no conflicting licence line
in this cut. These facts make the production manifest's `releaseReady`
false, without preventing a local study. Nothing was published.

## Completed MP4

`_build/study-1-pt-br.mp4` is the byte-identical named delivery copy of
`_build/rehearsal.mp4`, the output recorded by `rehearsal-manifest.json`.
SHA-256: `09f47b8854d9c90a10800e1f6579503f0a40fc680dce52e7eb8870eaa40e8118`.

FFprobe confirms 58.541667 seconds, 1405 H.264 frames at 24 fps,
1080 × 1920, with stereo AAC at 48 kHz. File size: 9,379,570 bytes.
A complete FFmpeg decode of video and audio finishes without errors.
All 1405 frames were captured for this film; none came from a landscape
video or a previous shot cache.

The renderer generated and verified an encoded-film review pack under
`_build/review-packs/597304a56ef1-09f47b8854d9-599ecff1-95db-44d6-901c-af50047dbee7/`.
Its decoded frame count and dimensions agree with FFprobe. The agent also
inspected `_build/encoded-overview.jpg`, twelve chronological samples
decoded from the actual MP4, including the mechanism sequence and closing.
The automatic pack's “generated, not reviewed” status is retained; it does
not substitute for the pilot's review or imply listening approval.

`_build/study-1-pt-br.srt` is a copy of the renderer's separate Portuguese
subtitles. No captions or credits are burned into the film.
