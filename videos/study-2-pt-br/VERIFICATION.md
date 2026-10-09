# Study 2 — loop verification

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

9 October 2026. The pilot requested a separate second study with the same
audio, a wheel already moving at the opening, and a closing camera/background
fade that joins the opening without a jump. Study 1 is not revised in place.

## Visual edit and preview

The first study's first frame has zero non-background pixels. This study
removes its 12-frame opening fade; its first frame shows 138,986 wheel pixels
and differs from its next frame. The opening already uses linear model time;
that approved rate is retained: 0.685102587 model seconds per video second,
or 61.659233 degrees of wheel rotation per video second. There is no initial
hold or acceleration ramp.

The closing starts at frame 1997 (83.208333 seconds). Its camera follows a
5.25-second eased polar arc around the model to the exact opening wheel view,
instead of interpolating through the machine. Between closing frames 60 and
126 the full assembly dissolves into the wheel-only view; both are real poses
at identical model time and camera, so the wheel is neither doubled nor faded
to black. The camera and wheel-only visibility are settled before the seam.

The closing model clock advances monotonically from 453.08125 to 456 model
seconds. A smooth Hermite segment connects the inherited starting speed to
the opening speed, followed by a constant-speed final 18 frames. At the
exclusive end the isolated wheel differs from the opening's 400 model seconds
by exactly fourteen full turns. Other parts are already invisible; no timber
reset is shown or represented as an automatic mechanism.

The checked browser proved, in decoded full-resolution pixels:

- Opening frame 12 meets the reused opening exactly.
- Closing frame 1997 meets the old closing's first image exactly.
- Continuing past the final timestamp reproduces opening frames 0 and 1
  exactly, including framing, background and wheel phase.
- The actual last frame equals one ordinary animation step before the
  opening, not a duplicate first frame or a stationary seam.

The nineteen numbered images in `_build/preview/` and their overview were
inspected: first-frame wheel visibility, restored context at the closing,
camera route outside the model, gradual background removal and final wheel.
Preview evidence is `_build/preview-report.json`. The production run repeats
the pixel proofs; endpoint captures and continuations remain in `_build/frames/`.

## Preservation and cache

The immutable base delivery is study 1's 89.583333-second pause revision,
SHA-256 `d1f71caf179a3d89b0a8b70ed2851229c40b991c0869572de5aff945408ddf79`.
The unchanged narration mix is
`904eab471094a5dd7b0e47f423f0991d6fec64a1a384c1d6ab207601ff64a371`.
The approved Leo v3 performance and all words, emotional direction and pauses
are unchanged. No voice request, new audition, audio cut or time stretch is made.

Both caches are linked with `ln -s` in this study's own ignored `_build/`.
Rendering verifies all inherited visual-input hashes against the original
manifest. The unchanged middle's PNGs are SHA-256-verified hard links:
frames 12–1996, including the approved silent mechanism transition. New images
are written only in study 2, never through the shared cache links.
Exactly 165 frames require capture and 1985 frames are reused.

The new encode copies the base MP4's AAC stream instead of re-encoding the
voice. `verify-loop.mjs` checks encoded packet identity, decoded PCM identity,
subtitles, every source-frame hash and hard link, the exact loop pixel proofs,
the complete movie's format/duration and full decode. Measured delivery results
are recorded below. No aesthetic claim is inferred from hashes alone.

## Delivered file

`_build/study-2-pt-br.mp4`: 89.583333 seconds, 2150 H.264 frames, 1080 × 1920,
24 fps, AAC stereo, no embedded subtitle stream. SHA-256:
`23da4277b4ae3745e9b75db86a10152d1015beb217f140052179e1c26b4764d7`.

`verify-loop.mjs` passed on 9 October at 17:34 UTC. It verified every PNG,
all 1985 hard links, both pixel-exact base joins and the cyclic motion proofs.
The copied AAC packets are byte-identical to study 1's (ADTS SHA-256
`a47e0d14c7eb4ad7cd4ed816c13a793877ff229f49ba670c67eb1f6b16915b25`),
and the decoded PCM is also byte-identical. No new listening assessment is
claimed or needed to establish that this is the same approved audio.
External subtitles are unchanged, the full MP4 decodes without errors, and
the base study's hash is unchanged. Results: `_build/verification.json`.

The encoded film was inspected via `_build/encoded-overview.png` (12 endpoint
and camera/fade samples) and `_build/encoded-seam.png` (frames 2147, 2148,
2149, 0, 1, 2 in playback order). The latter shows the normal rotational step
across the seam, with no duplicate frame, background flash or framing change.
The former confirms the camera reaches the wheel as the assembly fades away.

The model export, stage, viewer and Videomaker are unchanged. Their inherited
provenance and the unresolved public source/simulation URLs remain limitations;
this is a local study, not a published release. Nothing is pushed or uploaded.
