# Cut 5 handoff

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Status: revised in place on 8 October 2026 after the pilot resumed work and
gave another review. The requested cut-5 live preview is built and running.
Do not render an MP4 without the pilot's direction.

## Preview and records

- Cut 5: http://127.0.0.1:8785/#movie (detached live server).
- Cut 4 remains at http://127.0.0.1:8784/#movie for comparison.
- Cut-5 server log: `/tmp/machinome-release-5-live.log`.
- Duration: 191 seconds. Sources and reproduction commands: `README.md`.
- Commission and implementation choices: `DIRECTION.md`.
- Checks, revised scene times and limits: `VERIFICATION.md`.
- Generated movie, audio, provider receipt, screenshots and browser check
  results are local and ignored under `_build/`. They are required to reuse
  this precise performance; do not discard or regenerate them casually.

## What remains for review

The pilot has reviewed the earlier cut-5 changes and confirmed the opening
fade worked. This latest batch awaits their viewing: a matching fade at 32.46s,
the complete second rope highlighted up to the cart, the source plate flush
right/bottom and naming Wikimedia Commons, testing code typed over 105–110s
(explicitly clarified), and film source typed over 131.08–133.08s. CrankStroke's
stroke/end anchors are inline in its actual source; all `Cue`, `highlight`,
and `spoken` identifiers flash as groups on their respective spoken words.
The open-source circle now approaches with cubic ease-out.
Latest refinements: the opening wheel turns from the first frame; the
manuscript source plate hugs its text; “a shot” highlights `Shot`, not `shot`.
The latest wheel-speed review raises its ending acceleration from 7 to 42
degrees/s², shared by the graphic and physical wheel. It reaches just over
one turn per second as the hub zoom starts and about 1.25 turns/s by its end,
still accelerating. Stream-label speed, cameras, narration and logo timing
are unchanged. This is film playback timing, not a CAD or dynamics change.

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
There is no tagline or drawn question. Sixty-nine live browser checks pass,
including no duplicate wheels and the new code/ending behavior. Screenshots
were inspected. No MP4 rendered and no narration regenerated for this batch.

The live player still shows composed dissolves as cuts at their midpoint.
Cut 5 declares a 1.8-second transition starting on “With Machinome” and a
0.9-second dissolve into the film-code enumeration, but the live
player cannot demonstrate their final blended appearance. The pilot was
told this limitation during work. Do not claim the crossfades were visually
reviewed as rendered, or silently expand this into a Videomaker change.
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
forced alignment was unavailable (HTTP 401). Only that relation flash has a
one-frame early entrance to remain visible before the scene cut. The recorded
timing itself was not changed. See `VERIFICATION.md`; do not claim acoustic
review or regenerate the whole performance casually to work around this.

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
