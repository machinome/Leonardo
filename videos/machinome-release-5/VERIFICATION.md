# Cut 5 preview and rehearsal evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

8 October 2026. Status: one narrated MP4 rehearsal rendered after the pilot
approved the current preview and requested it. No publication.

## Post-rehearsal relation sync correction

The pilot heard delayed `drives` and much later `crankshaft` highlights.
The provider assigned raw-take spans 99.371–100.171s and 101.130–101.140s;
with the three-second film lead-in these appeared at about 102.37s and
104.08s (the latter had an inadequate one-frame-early workaround).

Local forced alignment used PocketSphinx 5.1.1, its bundled English acoustic
model, 16 kHz mono PCM decoded by FFmpeg from the existing take, and 100 Hz
alignment frames. `Decoder.set_align_text` aligned the known transcript in
`relation-timing.json`, not a guessed speaking rate. The crop 97.4–104.25s
gave `drives` 98.90–99.37s and `crankshaft` 99.46–100.23s. Two shifted crop
starts (97.3 and 97.5s) and the sentence-only crop 97.4–100.8s agreed within
10 ms. The installed diagnostic was isolated by `uv run --no-project --with
pocketsphinx==5.1.1`; it is not a production dependency or paid service.

`finish.mjs` applies only take-bound visual offsets, rejecting a different
audio SHA-256. The resulting 24 fps film spans are:

| Token | Start | End |
| --- | ---: | ---: |
| spin | 101.500 | 101.917 |
| drives | 101.917 | 102.375 |
| crankshaft | 102.458 | 103.250 |

Waterwheel and spin onsets stay unchanged. Shortening spin's end is necessary:
the stage selects one active blink, so overlapping it with the earlier drives
would hide that correction. No relation highlights overlap. The prior
one-frame crankshaft workaround is removed.

`inspect-relation-sync.mjs` failed before the change on the late spin boundary.
Afterward it checks all corrected endpoints within half an output frame and
passes eight live browser checks: before, onset, middle and clearing of both
words, including exact marked text and no page errors. The two word screenshots
were visually inspected. All 78 existing browser/frame checks also pass.
Run both from the project root with the live server online:

```sh
node videos/machinome-release-5/inspect-relation-sync.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-5/inspect-preview.mjs /home/asa/devel/machinome/videomaker
```

Comparison with `_build/revisions/before-relation-sync/movie.json` confirms
only these three cue spans and the updated movie.py source-provenance hashes
changed; every other movie field, including code excerpts, model clocks and
scene boundaries, is identical. Mixed narration SHA-256 remains
`e93ac2c2c7c549da87b8638d65e188096b5438f93728925487338328a1d07848`.
The existing MP4 and its hash below are unchanged and predate this correction.
The live server answers HTTP 200 at port 8785. No audio synthesis, provider
alignment rewrite, MP4 render or fresh human listening pass was performed.
This is a measured acoustic-model correction ready for the pilot's listening
check, not a claim of sample-exact phonetic boundaries.

## Encoded rehearsal

`_build/rehearsal.mp4`: H.264, 1920×1080, 24 fps, 4,584 frames,
191.000 seconds, 25,464,703 bytes. AAC narration also spans 191.000 seconds.
The separate SRT is not burned into the picture. Render used cached speech
only; no synthesis, retiming, source edit or extra silent MP4 was made.
The captured cut-5 source revision is `e5e577931bb0`.

SHA-256, independently checked against `_build/rehearsal-manifest.json`:
`14db64cfa4bb32efeb01cc1586d5ea1aa0f8257770db697c1455997f0fc07d02`.
All frames were newly captured. The render and encoded review-pack generation
completed successfully. The review pack decoded all 4,584 frames and verified
their dimensions and increasing presentation timestamps. It is retained at
`_build/review-packs/1eef183e87bb-14db64cfa4bb-79ab3332-733d-4002-9f00-5585e3f11376/`.

All four decoded overview sheets were visually inspected, plus full-resolution
frames at the 104s and 131s crossfade midpoints, the late tool stream over the
physical wheel, and the settled closing logo/address/licence. The code-scene
crossfades do blend both pictures, unlike the live player's midpoint cuts;
overlapping code is transient during those authored dissolves. This is sampled
visual inspection and technical audio verification, not a fresh listening pass.
The existing provider-alignment caveat below remains.

The manifest correctly says `releaseReady: false`: public simulation/source
URLs are unresolved, unrelated project and Videomaker files were dirty, and
the reused model export records dirty provenance. No unrelated edits were
included in a commit. The pilot's displayed closing licence still differs
from the gallery's AGPL-3.0-only record; see `description.md` before publication.
The cut-5 live server was stopped during rendering and restored afterward.

## Preview evidence retained

The resolved movie is 191 seconds at 24 fps, with a 185.68-second edited
Jessica take, a three-second lead-in and a final hold. One new provider
request generated this revision's narration. Its receipt and untouched WAV remain in
the ignored build directory. A byte comparison confirmed every original
PCM sample is preserved and exactly 1.2 seconds of zeros were inserted
before the return line; no speech is stretched or truncated. All subsequent
alignment timestamps shift by 1.2 seconds. The returning sentence is
5.02 seconds, compared with 3.66 seconds in cut 4. The previous cut-5 take
and documents remain in `_build/revisions/before-second-review/`, as well
as their original keyed speech cache entries.

The standard check passes, including the drawing's peak enlargement of
3.36 against its explicit 3.4 allowance. This is the requested close crop of
the existing 1000×1000 image, not a higher-resolution replacement. The movie
reuses the existing cut-3 export.
`inspect-preview.mjs` passes 78 browser frame/cue checks: five opening-spin
positions (including the second frame), five positions each
for the opening and 32s fades, a later orbit frame, manuscript coverage and
edge-aligned source plate, code bounds, two five-sample typing passes, seven
enumeration cues and four meta-scene tokens, returning-pawl and complete-rope
highlights, circle easing, stream/wheel overlap, seven tool-reading windows,
two late-stream samples, five ending angular-speed
samples, four hub-zoom positions, five
logo-approach positions, two blank pre-logo positions, four synchronized
URL/licence-fade positions, and no closing question.
At each typing onset the incoming source state is checked, because the live
player still displays the outgoing composed transition; the remaining eight
typing samples check actual browser text. Screenshots of the fades,
manuscript, code, rope, easing, overlap, zoom and logo were inspected.
No page errors were reported. `git diff --check` passes.

Immediate opening motion: a new assertion failed against the old first-second
hold. The film now advances linearly from model second 400 on its first frame,
reaching second 432 at the unchanged start of the pawl lesson. Both model time
and actual browser pixels change at all five sampled opening instants. This
retimes the posed reconstruction, not its physical dynamics.

Opening-reveal correction: the original `Dissolve(1.2)` was present in the
movie; the live player's documented midpoint-cut approximation caused the
abrupt appearance. A browser assertion for half-opacity at the reveal's
midpoint failed before the correction. The opening now uses `Reframe(1.2)`
with a shared, fully visible wheel in an identical backdrop box and the full
machine fading over it from 7.292 to 8.492 seconds. Both views have the same
camera and model time throughout the fade. Screenshot inspection caught a
duplicate background wheel during the later orbit: the incoming view now
fades its opaque background plate too. A pixel comparison that hides the old
wheel at the orbit midpoint failed before that fix and passes afterward.
Opening fade and orbit screenshots were inspected. This is an episode edit,
not a general live-player dissolve fix; no narration was regenerated.

The follow-up 32s fade similarly failed a midpoint half-opacity assertion
before its edit. It now uses a 1.2-second live reframe starting at 32.458s.
The outgoing full machine, incoming drive and faint context share camera and
model time; a fading dark plate covers the old full machine. Hiding that
base after the fade makes no pixel difference. The highlighted second rope
now includes its central take-up, upper-roller span and carriage haul; the
browser image shows the highlight reaching the timber cart. The source plate
names Wikimedia Commons and touches both the right and bottom edges; its
width now equals measured text width plus the authored padding within one pixel.

Key locations in the revised film:

| Scene | Starts | Ends |
| --- | ---: | ---: |
| Historical drawing | 79.458 | 85.500 |
| Import and assembly | 87.583 | 104.125 |
| Testing | 104.125 | 131.083 |
| Film-code enumeration | 131.083 | 143.458 |
| The code of this scene | 143.458 | 148.667 |
| Open-source wheel | 148.667 | 168.792 |
| Returning physical wheel | 168.792 | 179.833 |
| Closing identity | 179.833 | 191.000 |

The stream starts at 167.750 seconds, under “Trimesh”. Its seven labels
share one accelerating trajectory and a 0.533-second stagger; the handoff
starts on “And beneath it all” at 168.792, before the last label is released.
The graphic wheel fades over 1.25 seconds while labels remain independent.
The stream now finishes at 174.621, 0.2 seconds before the returning sentence
at 174.821. Its duration grows from 4.651 to 6.871 seconds, giving every name
about 48% longer to cross. The pilot explicitly extended streaming through
the pause after “tools”. An endpoint assertion failed against the earlier
short stream. Browser checks now measure each label's actual text width and
verify at least three seconds fully inside the frame with a 48-unit inset;
the last name remains visible after the circle has disappeared, and all names
are gone before the returning sentence. This checks available reading time,
not a claim that every viewer has read the names.
The graphic and physical wheel phases are checked against the same motion law.
Separating `spinDelay` from label `arrival` preserves the approved wheel clock:
the complete resolved waterwheel model-key record retains SHA-256
`6d7029e0046d4f4bfd55e85259c6c7ccccafd0d4755a41cdbc48cfb70667b7f4`.

The ending wheel now uses 42 degrees/s², six times the previous acceleration,
and keeps gaining speed through the hub zoom. A speed assertion failed against
the prior approximately 75 degrees/s ending. Independent differences between
the actual posed model times now show over 360 degrees/s at zoom onset and
over 440 degrees/s at the final sample (about 1.25 turns/s), increasing at
every sampled point. Each authored 24 fps angular step remains below 22.5°,
half the eight-spoke interval; live playback dropping frames can still affect
perceived motion. The graphic and physical wheels remain phase-aligned; the
tool-label trajectory is now slower, while all cuts, zoom and logo timing are unchanged. The wheel's phase law
is faster; this is editorial retiming, not simulated acceleration dynamics.

The camera moves directly towards the hub from 177.958 (“and humans”) to
179.833 (end of “their own”), with a dark fade over its last half-second.
The wheel is entirely gone before the boundary. Following the pilot's latest
direction, the logo waits for “I'm” at 180.521s, rather than entering at the
shot boundary. An onset assertion failed before this delay; browser checks
now verify zero logo width at the boundary and immediately before “I'm”.
The logo does not fade: it approaches from the screen-centre
vanishing point at constant opacity, growing from 0.002 to full scale over
1.2 seconds. A constant-opacity/scale assertion failed against the earlier
fade and passes now. The logo settles around 181.72s; the URL waits for the
closing “Open Source” at 185.607–186.487s (placed on the 24 fps grid), below
it and about 18% wider. The pilot's exact licence line appears beneath it.
Browser checks verify both lines' equal opacity, the licence's exact text and
bounds, and the fade's measured speech anchors. The URL is outside the logo's
transformed layer; its width stays fixed throughout the approach and fade.
No tagline remains. These actions
are visible and checked in the live player.

The circle's cubic ease-out advances promptly and ends at the first
technology's measured onset (scale 0.523 at 150.17s).
The enumeration is 12.375 seconds, down from 41.708. Its token flashes use
recorded first-word start/end times,
displayed on the movie's 24 fps grid. The real CrankStroke source now inlines
its stroke and end anchors; all four `Cue` calls, all three `highlight`
calls and all eight `spoken` calls flash on their respective words. Browser
readback checks both the exact token and occurrence count. “A shot” now marks
`Shot`, the constructor, instead of its variable. Testing source
types from 105 to 110s, as clarified by the pilot; film source types from
131.083 to 133.083s. Both reveal exact prefixes of the real source and finish
with the complete source. No narration or duration changed for this review.

Limits: the live player approximates composed dissolves as midpoint cuts;
this applies to the other scene joins, not the two live reframes or the custom
closing actions above.
The original preview run verified those joins' declared timings, not final
blended pixels; the encoded rehearsal inspection above now adds sampled
blended-pixel evidence.
The provider assigned only 10 ms to “crankshaft” and 4 ms to the following
“With”. A separate forced-alignment request was refused with HTTP 401 by the
configured key; no retry or second synthesis was made. The final relation
flash starts one frame earlier to remain visible before the testing cut.
Those two word timings remain uncertain and need listening review; do not
call that cue acoustically verified. No audio bytes or alignment data were
silently repaired. Other cue alignment and PCM integrity were checked;
pronunciation and delivery still need the pilot's listening review. Existing export provenance
and unresolved publication URLs remain as recorded in the earlier cuts.
