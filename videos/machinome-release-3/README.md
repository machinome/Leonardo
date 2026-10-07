# Machinome release — cut 3

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Third version commissioned from [review 2](review-2.md), with Jessica
retained and the opening “AI content” label removed at the pilot's request.
The first and second cuts are preserved. Production evidence and the final
artifact identity are recorded in [VERIFICATION.md](VERIFICATION.md).

- [Local player](index.html) · [MP4](_build/rehearsal.mp4).
- [Edited narration](_build/raw-narration.wav).
- [Film source](movie.py) · [narration](narration.py).
- [Direction](DIRECTION.md) · [description draft](description.md).

The completed movie runs 3:01.833 at 1920×1080 and 24 fps (22.0 MB).
Its local review player is at <http://127.0.0.1:8783/> while the review
server is running. Jessica / Eleven v3 narrates the real testing example,
model-layer technologies and OpenSpec. The latest refinement retains the
approved cut-3 performance except for a short “Manifold 3D” pickup replacing
“Three.js”. It fits the original slot without stretching or changing any
later timing. The raw WAV, provider receipts and character alignment are
retained under ignored `_build/`; the render adds a three-second lead-in
and closing hold. The new pickup remains subject to the pilot's listening
judgment.

The opening orbit is one sampled parametric curve. Code blinks use the
measured start and end of each word and never highlight `water_drive`.
The new scene shows the existing blade-clearance test and thirteen sampled
poses. The requested Commons drawing replaces both prior historical-image
shots. OpenSpec crosses the frame horizontally just above the blue line,
contacting the wheel's lower edge as it starts to turn. It enters slowly
and accelerates. All eight graphic spokes stay phase-aligned with the
physical waterwheel and keep accelerating through their 1.25-second fade.
The hub symbol and closing wordmark use the approved orange assets.

## Reproduce

From the Leonardo repository root, with the existing workspace environment:

```sh
node videos/machinome-release-3/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-3/narration.py
node videos/machinome-release-3/pickup-manifold.mjs /home/asa/devel/machinome/videomaker
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-3/movie.py
node videos/machinome-release-3/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 1280
node videos/machinome-release-3/inspect.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/machinome-release-3/postflight.mjs
python videos/machinome-revolutions-v2/serve-review.py --port 8783 --directory videos/machinome-release-3
```

The review server stays in the foreground. In another terminal, run
`node videos/machinome-release-3/check-player.mjs /home/asa/devel/machinome/videomaker`.
Launch the production commands in the listed order: loading a film writes
its resolved document, so simultaneous command startup can contend on its
temporary output file.

The current refinement used
`render-refinement.mjs <videomaker> <viewer>` instead of the full `render`
command above. It verifies all 4,364 approved source-frame checksums and
all 3,566 unchanged prefix frame requests, then captures only the 798 ending
frames from 148.583333 seconds onward. Nine fresh prefix samples also match
the source PNGs byte for byte. Encoding reuses those lossless PNGs and the
cached edited narration. The previous master and its records remain under
`_build/model-layer-refinement/`. The manifest identifies the mixed capture
origins explicitly; native cache keys are not overridden.

The earlier OpenSpec-only correction used `patch-openspec.mjs <videomaker> <viewer>`
instead of recapturing the full movie. It accepts only the hash-verified
original cut-3 master, verifies the one-line stage change and all cached
source frames, and captures 115 frames from the entrance through the outgoing
transition. It assembles those with the 4,249 unchanged original PNGs and
copies the original AAC track into the new encode. The original MP4 and
manifest remain under `_build/openspec-contact-patch/`; its manifest records
the mixed capture origins explicitly, without overriding native cache keys.
That one-off script is pinned to the earlier source and stage, not intended
for this later refinement. The ordinary reproduction commands above produce
the current stage.

These commands reuse cached speech. `pickup-manifold.mjs --prepare` was a
one-off preservation step before this refinement; it refuses to overwrite
that evidence. One subsequent `--generate` request recorded the 35-character
context “Manifold 3D, OpenSCAD, SolidPython.” Only the first name was used.
Without `--generate`, the script reuses that receipt and preserves all PCM
outside the 1.835-second name slot. `speech.mjs` now refuses to regenerate
the full revised narration. No production command automatically retries an
ambiguous paid request.

The isolated model export is `_build/model`, created with
`machinome export hydraulic_sawmill -o videos/machinome-release-3/_build/model --no-widget`.
It records revision `94a8562cc70e` and the actual dirty-tree flag. The
mechanical source is unchanged. Model and test excerpts are taken from
committed source with original line numbers and whole-file checksums;
film-source classes are AST-extracted from the actual declarations.

Generated media is local and ignored. The description carries the project
attribution, image-source record and production disclosure. Public addresses
remain unresolved; nothing is uploaded or published.
