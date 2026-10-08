# Cut 5 preview evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

8 October 2026. Status: ready for the pilot's live viewing and listening
review. No MP4 rendered; no publication.

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
`inspect-preview.mjs` passes 34 browser frame/cue checks: five opening fade
positions and a later orbit frame, manuscript coverage
and source-label placement, code bounds, seven enumeration tokens and four
meta-scene tokens, returning-pawl highlight, stream/wheel overlap, four zoom
positions, three logo-fade positions, and absence of the closing question.
Screenshots of the manuscript, code, overlap, zoom and logo were inspected.
No page errors were reported. `git diff --check` passes.

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
share one accelerating trajectory and a 0.361-second stagger; the handoff
starts on “And beneath it all” at 168.792, before the last label is released.
The graphic wheel fades over 1.25 seconds while labels remain independent.
They finish at 172.401, with the end of “tools”; the returning sentence starts
at 174.821, after 2.42 seconds on the wheel without streaming.
The graphic and physical wheel phases are checked against the same motion law.

The camera moves directly towards the hub from 177.958 (“and humans”) to
179.833 (end of “their own”), with a dark fade over its last half-second.
The wheel is entirely gone before the boundary. The logo starts at zero
opacity at that boundary and fades in over approximately 0.8 seconds.
These actions are visible and checked in the live player.

The circle's approach ends at the first technology's measured onset.
The enumeration is 12.375 seconds, down from 41.708. Its token flashes use
recorded first-word start/end times,
displayed on the movie's 24 fps grid. Cue readback matches the intended
token in the actual browser.

Limits: the live player approximates composed dissolves as midpoint cuts;
this applies to the other scene joins, not the opening reframe or the custom
closing actions above.
This run verified those joins' declared timings, not final blended pixels.
The provider assigned only 10 ms to “crankshaft” and 4 ms to the following
“With”. A separate forced-alignment request was refused with HTTP 401 by the
configured key; no retry or second synthesis was made. The final relation
flash starts one frame earlier to remain visible before the testing cut.
Those two word timings remain uncertain and need listening review; do not
call that cue acoustically verified. No audio bytes or alignment data were
silently repaired. Other cue alignment and PCM integrity were checked;
pronunciation and delivery still need the pilot's listening review. Existing export provenance
and unresolved publication URLs remain as recorded in the earlier cuts.
