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

The pilot has not yet approved this revision or listened to its new performance.
Review the full-frame manuscript reveal and bottom-right source label, shorter
code enumeration, token flashes, faster stream overlapping the physical wheel,
short pause, and closing zoom on “and humans”. The wheel disappears by the end
of “their own”, then the logo fades in. The closing question remains speech
only. No MP4 has been rendered. Twenty-eight live browser checks pass.

The live player still shows composed dissolves as cuts at their midpoint.
Cut 5 declares a 1.8-second transition starting on “With Machinome” and a
0.9-second dissolve into the film-code enumeration, but the live
player cannot demonstrate their final blended appearance. The pilot was
told this limitation during work. Do not claim the crossfades were visually
reviewed as rendered, or silently expand this into a Videomaker change.
The wheel/stream overlap and ending zoom/fade instead use project-owned live
actions and have been inspected in the browser.

This revision's narration was generated once. `speech.mjs` retains the provider
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
