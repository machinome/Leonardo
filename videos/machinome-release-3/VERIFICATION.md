# Third-cut production evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Production date: 7 October 2026. The pilot commissioned cut 3 from
`review-2.md`, chose Jessica, and removed the opening “AI content” label.
The first two cuts, their narration and their exports remain unchanged.

## Source and checks

The isolated model export records Leonardo source
`94a8562cc70e96de0cad1b85a4a7c1e092d2ed5c`.
Its actual dirty flag is retained. Only video production sources changed.
The movie resolves to one chapter, 17 shots, 181.833333 seconds at 24 fps.
Jessica's new continuous take is 176.48 seconds, 2,115 characters,
67 caption cues and 33 measured navigation beats. The film places it at
+3 seconds without cuts or stretching.
Raw narration SHA-256:
`bc63ebd15746f350edaa6d0a622f141740b7d88fa81cbd2a0e05926d081c4330`.

Videomaker source: `5e91951b98b3ae25cade0353623cfa54d0da3fbc`.
Viewer source: `24d9ad2c0fddb8fdc7a2704e477bdbf7ad88e540`, API 29.
Their existing unrelated working files are not modified by this production.

The native check resolves every cue, verifies the model/source pin and
measures the layouts. The requested Commons image reaches 1.48× enlargement
against its declared 1.5× allowance. Original image bytes are preserved.

The project inspection passes 49 exact pixel replays. It checks every
output frame for at most one highlighted physical component and one blinking
code token; both paired views have identical camera and model states.
The orbit's 160 linear segments sample one analytic curve and never reverse
angular direction. Four separate source pulses light `waterwheel`, the
first `spin`, `drives`, and `crankshaft`; intervening samples have no mark.
No museum photograph or opening “AI content” label is in the rendered data.
OpenSpec has a constant vertical position throughout its passage. A final
composition check found its text crossing CadQuery; its baseline was moved
lower and five new pixel replays passed, with explicit bounding-box checks
that it never overlaps a technology label.

Inspected full-size browser images of the orbit, drawing, literal code and
each test-part highlight. An initial testing camera hid the far timber half;
the native highlight proof rejected it. The final oblique end view exposes
the blade and both halves. The unchanged test itself passes all thirteen
samples with the exact geometry engine through `machinome test`.

The final native preview passes its real-viewer, highlight, picture, fade,
transition and exact-replay checks. The final project inspection repeats
all 49 samples with the corrected OpenSpec position and passes.
Generated reports live under `_build/preview/` and `_build/inspection/`.

The full existing sawmill suite passes on the exact B-rep engine:
**43 passed, 0 failed, 1114.19 seconds**. This includes the featured
thirteen-position blade test, whole-assembly interference, rope geometry,
captured joints and full-pass checks. No mechanical source or test was
changed. Command: `machinome test hydraulic_sawmill --brep`; full output:
`_build/model-test.log`.

## Original full encode and player

The original full render completed successfully from production head
`94de28345e50a2ec6f019037fd477815d9eaad7e`. The delivered local artifact is
`_build/rehearsal.mp4`: 21,804,744 bytes, H.264, 1920×1080, 24 fps,
4,364 frames, 181.833333 seconds. Its SHA-256 is
`0f0df5e37a1ec9ecc2a46f74da5de5d13c4d0b4b84a723115496bfc95b7dd6a0`.
The native render manifest and decoded-video review pack are retained.
The stage JavaScript and CSS hashes match the final preview and inspection:
`f73807570a4b27c211a5ab8857e7f3f00685d943ef80f0260a12ccc3d0dc2178`
and `f2b548253f5de5da7c9f7827840a062362efcda570ed457bc3c51c1a26be1c4a`.

`postflight.mjs` passes against the actual MP4 and native manifest. It
verifies the complete continuous Jessica source by checksum, its +3-second
placement, all 67 captions against the original text and alignment, and
the encoded dimensions, duration, frame count and audio. The film has one
48 kHz stereo AAC track and no embedded subtitle track; the player offers
optional external VTT captions. Decoding the complete audio succeeds;
FFmpeg measures mean volume −19.9 dBFS and maximum −1.1 dBFS.

All 49 selected MP4-decoded frames were inspected on four contact sheets;
additional full-size checks cover the replacement drawing, individual
source-token highlights, both timber-half highlights, complete film-source
class, and OpenSpec's clear horizontal passage. The opening is unlabelled,
the orbit follows one continuous route, and no museum photograph appears.
Frame identities and checksums are in `_build/encoded/index.json`.

`check-player.mjs` passes against `http://127.0.0.1:8783/`: all 14 chapter
jumps seek successfully, 67 subtitle cues load, byte-range requests return
206, and every download/source link resolves. Desktop and 390-pixel-wide
layouts have no page errors or horizontal overflow; their screenshots were
inspected. Evidence is in `_build/player-report.json` and
`_build/player-{desktop,mobile}.png`.

The recorded `releaseReady: false` is preserved: public URLs are unresolved,
the model export records a dirty tree, and unrelated project notes and
Videomaker working files existed at render time. These are not silently
cleared or represented as clean-source publication evidence.

## OpenSpec contact correction

After reviewing the original cut, the pilot requested one correction in
`machinome-release-3`: OpenSpec must travel above the blue line and hit the
wheel, with overlap permitted. Only its baseline changes, from 970 to 820;
the waterline stays at 835. The earlier no-overlap decision above is
superseded. Five new browser samples pass exact replay, all stay above the
line, and the arrival sample intersects the wheel's lower edge. The contact
frame was inspected visually. Narration, captions, motion, timing and all
other stage code remain unchanged.

The partial production uses `patch-openspec.mjs`, scoped to this exact
approved master and one-line source change. It verifies all 4,364 original
PNG checksums, captures only frames 3914–4028 (163.083333–167.875 seconds),
and reuses the other 4,249 lossless source frames. Nine fresh browser samples
outside that interval, including both boundary frames, match the originals
byte for byte. The existing AAC track is copied, not synthesized or
re-encoded. The original MP4 and manifest remain recoverable under
`_build/openspec-contact-patch/`; the new manifest explicitly identifies the
mixed capture origins rather than pretending that a native cache hit occurred.

The corrected master is 21,818,327 bytes, with SHA-256
`2be35f56bb2993b7c0d0bd2530325f56699f33e419ac3b9b5a5628553103a1c6`.
It keeps 4,364 frames, 1920×1080, 24 fps and 181.833333 seconds. Both versions'
copied AAC payload hashes are
`853734d485c12d14d466be84182b2faed779693c43486e61f414a32ed0368065`.
The corrected stage bundle is
`e1b9e8d9ce2c96fbb42b40c1615433f578782112752841918fbbe4db30acc703`;
CSS and other served assets match the original exactly.

Postflight passes again, decoding 49 samples from the corrected MP4.
Full-size decoded frames before contact, at contact and after contact were
inspected: the text travels above the line, overlaps the lower wheel edge,
then continues left while the wheel turns. The player again passes all
14 seeks, 67 subtitle cues, links, range delivery and both viewport checks.

## Review limits

No independent listening review is claimed for the new performance.
Text, character alignment, signal and playback checks do not replace the
pilot's listening judgment. The earlier Jessica take's approval belongs to
cut 2, not this new recording.

The Commons image is recorded with the source's public-domain statement.
The museum photograph and previous manuscript scan are absent. The gallery
source licence does not grant trademark rights in the unchanged identity
assets. The release brief's “all open source” wording still differs from
Videomaker's recorded unselected distribution licence; the description
identifies this existing publication issue. Public source and simulation
URLs remain unresolved. This is a local review film, not a publication.
