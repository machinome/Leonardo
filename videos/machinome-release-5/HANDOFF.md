# Cut 5 handoff

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Status: stopped at the pilot's request on 7 October 2026. The requested
cut-5 live preview is built and running; no further edits are in progress.
Do not resume production or render an MP4 without the pilot's direction.

## Preview and records

- Cut 5: http://127.0.0.1:8785/#movie (detached live server).
- Cut 4 remains at http://127.0.0.1:8784/#movie for comparison.
- Cut-5 server log: `/tmp/machinome-release-5-live.log`.
- Duration: 225 seconds. Sources and reproduction commands: `README.md`.
- Commission and implementation choices: `DIRECTION.md`.
- Checks, revised scene times and limits: `VERIFICATION.md`.
- Generated movie, audio, provider receipt, screenshots and browser check
  results are local and ignored under `_build/`. They are required to reuse
  this precise performance; do not discard or regenerate them casually.

## What remains for review

The pilot has not yet approved cut 5 or listened to its new performance.
Review the complete import pronunciation, fuller code explanation, token
flashes, individual technology entries, silent wheel buildup, slower
returning line and spoken-only closing question. No MP4 has been rendered.

The live player still shows composed dissolves as cuts at their midpoint.
Cut 5 declares a 1.8-second transition starting on “With Machinome” and a
0.9-second dissolve into the expanded film-code explanation, but the live
player cannot demonstrate their final blended appearance. The pilot was
told this limitation during work. Do not claim the crossfades were visually
reviewed as rendered, or silently expand this into a Videomaker change.

The new narration was generated once. `speech.mjs` retains the provider
original and inserts a documented seven-second silence before the return
line, shifting alignment with it. `finish.mjs` must follow a fresh movie
evaluation; it adjusts the document, then mixes cached speech with the
three-second lead-in. It generates no speech. The live server watches the
movie document, so stop that specific server before future rebuilds if
avoiding transient intermediate loads is important.

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
