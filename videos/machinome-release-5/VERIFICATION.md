# Cut 5 preview evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

7 October 2026. Status: ready for the pilot's live viewing and listening
review. No MP4 rendered; no publication.

The resolved movie is 225 seconds at 24 fps, with a 219.72-second edited
Jessica take, a three-second lead-in and a final hold. One new provider
request generated the narration. Its receipt and untouched WAV remain in
the ignored build directory. A byte comparison confirmed every original
PCM sample is preserved and exactly seven seconds of zeros were inserted
before the return line; no speech is stretched or truncated. All subsequent
alignment timestamps shift by seven seconds. The returning sentence is
4.78 seconds, compared with 3.66 seconds in cut 4.

The standard check passes, including the drawing's peak enlargement of
1.45 against its 1.5 allowance. The movie reuses the existing cut-3 export.
`inspect-preview.mjs` passes 21 browser frame/cue checks: the zoom's endpoints,
code layout bounds, all nine explanatory highlights and four meta-scene
highlights, scene captures and absence of the closing question. Screenshot
inspection caught crowded stream entries; spacing was increased and the
browser checks rerun. Final screenshots were inspected.

Key locations in the revised film:

| Scene | Starts | Ends |
| --- | ---: | ---: |
| Historical drawing | 80.625 | 86.458 |
| Import and assembly | 88.500 | 103.167 |
| Testing | 103.167 | 130.583 |
| How the film's code works | 130.583 | 172.292 |
| The code of this scene | 172.292 | 177.708 |
| Open-source wheel and stream | 177.708 | 205.083 |
| Returning physical wheel | 205.083 | 214.000 |
| Closing identity | 214.000 | 225.000 |

The return narration begins at 208.602 seconds: 3.52 seconds after the
physical-wheel shot starts, including its 1.25-second graphical handoff.
The circle's approach ends at the first technology's measured onset.
Each stream label has the same entry trajectory, staggered by 0.85 seconds.
Explanatory token highlights use recorded first-word start/end times,
displayed on the movie's 24 fps grid. Cue readback matches the intended
token in the actual browser.

Limits: the live player approximates composed dissolves as midpoint cuts;
this run verified their declared timings, not their final blended pixels.
Narration alignment and PCM integrity were checked; pronunciation and
delivery still need the pilot's listening review. Existing export provenance
and unresolved publication URLs remain as recorded in the earlier cuts.
