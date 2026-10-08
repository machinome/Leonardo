# Cut 5 handoff

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Status: on 8 October 2026 the pilot approved the current preview and requested
one MP4 rehearsal. It is built at `_build/rehearsal.mp4`, with separate
`_build/rehearsal.srt`: 191 seconds, 1080p/24 fps, existing narration.
The cut-5 live preview was restored after rendering. No publication.
Further renders or content changes require the pilot's direction.

Subsequent pilot review: the live preview now corrects `drives` and
`crankshaft` in the assembly-code sentence. Local PocketSphinx forced
alignment of the unchanged recording puts their visual spans at
101.917–102.375s and 102.458–103.250s on the 24 fps grid. `spin` clears at
101.917s to avoid masking `drives`. `relation-timing.json` binds these
corrections to the exact take; `finish.mjs` applies visual offsets without
modifying the provider alignment, audio or cuts. The original MP4 and its
manifest remain unchanged and **do not contain this follow-up fix**.
Eight new browser boundary checks and all 78 prior checks pass. Review from
100s at the same live URL. No further synthesis or render was performed.

Next two live-only refinements: at 142.292–142.637s, “spoken” lights only
the seven calls inside the four highlighted `Cue` declarations, excluding
the earlier `Shot.until` call. The targets come from the actual Python AST;
the listing now draws simultaneous per-line blink actions. At 148.667–157.75s
the M/title approach has no circumference. The circumference appears with
OpenSCAD and its spoke, sharing their 0.35s fade starting at 157.75s.
Both new expectations failed against the old preview. All 83 preview checks
and the eight relation-sync checks now pass; screenshots were inspected.
The live server is online at the same address. Audio and MP4 hashes are unchanged.

## Preview and records

- Cut 5: http://127.0.0.1:8785/#movie (detached live server).
- Cut 4 remains at http://127.0.0.1:8784/#movie for comparison.
- Cut-5 server log: `/tmp/machinome-release-5-live.log`.
- Duration: 191 seconds. Sources and reproduction commands: `README.md`.
- Commission and implementation choices: `DIRECTION.md`.
- Checks, revised scene times and limits: `VERIFICATION.md`.
- Rehearsal source revision: `e5e5779`. Reproduction command: `README.md`.
  Output hash and decoded review-pack identity: `VERIFICATION.md`.
- Generated movie, audio, provider receipt, screenshots and browser check
  results are local and ignored under `_build/`. They are required to reuse
  this precise performance; do not discard or regenerate them casually.

## What remains for review

The pilot reviewed the cut-5 changes and requested the rehearsal after the
final stream slowdown. The current cut includes a matching fade at 32.46s,
the complete second rope highlighted up to the cart, the source plate flush
right/bottom and naming Wikimedia Commons, testing code typed over 105–110s
(explicitly clarified), and film source typed over 131.08–133.08s. CrankStroke's
stroke/end anchors are inline in its actual source; all `Cue` and `highlight`
identifiers flash as groups. The `spoken` group is now restricted to those
Cue arguments. The open-source M/title approach uses cubic ease-out; the
circumference waits for OpenSCAD.
Latest refinements: the opening wheel turns from the first frame; the
manuscript source plate hugs its text; “a shot” highlights `Shot`, not `shot`.
The latest wheel-speed review raises its ending acceleration from 7 to 42
degrees/s², shared by the graphic and physical wheel. It reaches just over
one turn per second as the hub zoom starts and about 1.25 turns/s by its end,
still accelerating. This is film playback timing, not a CAD or dynamics change.

Latest stream review: slow the tool names uniformly by extending the stream
from 4.651 to 6.871 seconds (167.75–174.621s). It continues over the physical
wheel after the graphic circle disappears and clears 0.2s before the returning
sentence at 174.821s. Each name has at least three seconds wholly inside the
frame. This supersedes the previous no-silent-streaming-tail direction.
The separate `spinDelay` preserves every approved waterwheel model key exactly;
do not tie it back to label `arrival`. Camera, narration, logo and closing
text timings remain unchanged.

The latest instruction supersedes the former closing logo fade: after the
wheel disappears at the end of “their own”, the screen stays clear until
“I'm” starts at 180.521s. Then the logo approaches from the screen centre
at constant opacity over 1.2s, as if the camera continued
through the wheel hole. It settles, then the GitHub address fades in beneath
it on the closing “Open Source” (185.607–186.487s), about 18% wider than the
logo. The exact requested `GPL-2.0-or-later OR CERN-OHL-S-2.0+` appears below
it in the same fade. Both lines are outside the zooming layer and never scale.
The requested purpose sentence was already recorded, so no synthesis was
needed. The licence overlay is explicit pilot direction overriding the skill's
no-licence-text default; gallery records remain AGPL-3.0-only and were not changed.
There is no tagline or drawn question. Seventy-eight live browser checks pass,
including no duplicate wheels and the new code/ending behavior. Screenshots
were inspected. The subsequent MP4 request was fulfilled using this source
unchanged and without regenerating narration.

The live player still shows composed dissolves as cuts at their midpoint.
Cut 5 declares a 1.8-second transition starting on “With Machinome” and a
0.9-second dissolve into the film-code enumeration, but the live
player cannot demonstrate their final blended appearance. The MP4 now
contains the blends; decoded midpoint frames at both joins were visually
inspected, along with all four overview sheets, the late stream and closing
identity. This is sampled visual review, not a complete real-time viewing or
new listening pass. Do not expand it into a Videomaker change.
The opening reveal uses a supported live reframe, with the complete
incoming view (including its opaque background) fading over a shared wheel.
The 32s reveal also uses a live reframe and an opaque incoming plate. The
wheel/stream overlap, approaching logo and URL fade use project-owned actions.
These have been inspected in the browser. This is not a tool-wide dissolve fix.

The current narration was generated once in the earlier review. `speech.mjs` retains the provider
original and inserts a documented 1.2-second silence before the return
line, shifting alignment with it. `finish.mjs` must follow a fresh movie
evaluation; it adjusts the document, then mixes cached speech with the
three-second lead-in. It generates no speech. The live server watches the
movie document, so stop that specific server before future rebuilds if
avoiding transient intermediate loads is important.

The provider collapsed “crankshaft” and “With” to implausibly short timestamps;
its remote forced-alignment endpoint was unavailable (HTTP 401). The later
local forced alignment above replaces the old one-frame-early workaround for
the relation highlights. Raw provider timing and the “With Machinome” cut
remain unchanged. This is acoustic-model alignment, not a new human listening
approval; the pilot requested the live server to check it. See `VERIFICATION.md`.

The initial cut-5 sources are in commit `c8b9f7b`; its local movie/audio backup
is `_build/revisions/before-second-review/`. Preserve both speech generations.

## Repository boundaries

This is the Leonardo Git repository (real root
`/mnt/data/machinome-projects/Leonardo`). Only `videos/machinome-release-5/`
belongs to this change. Existing dirty Portuguese cut-4 files and review
drafts belong to other work and were not staged or edited.

Earlier in this conversation, Videomaker received three committed and
integrated player fixes: stable caption/readout height (`0eb777b`), left
arrow back two seconds (`b5f1ec0`), and right arrow forward two seconds
(`1617f81`). The live bundles contain those fixes. Shift+arrow remains one
second; Space plays/pauses. Videomaker has unrelated dirty workflow files.
No repository was pushed or published.
