# Cut 5 handoff

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Current state — Studio revision, 8 October 2026

Work belongs to the Leonardo repository on **release-video**, checkpoint
`c9c3db6` before this revision. Real root: `/mnt/data/machinome-projects/Leonardo`.
Only `videos/machinome-release-5/` changed. Portuguese cut-4 and review drafts
are unrelated dirty work; do not stage them. No framework, Studio or viewer
source was modified; no push or publication.

Live URL: http://127.0.0.1:8785/#movie (194s).
Log: `/tmp/machinome-release-5-live.log`. Cut 4 stays on 8784.
Studio was already running on http://127.0.0.1:9000; leave it alone.

The pilot corrected the new narration: **remove** “Agents can write mechanical
models because of tests.” After the Studio → testing transition use
“Machinome also lets us test how parts fit together.” This is implemented.

The new take is one unedited 188.72s Jessica/Eleven v3 recording, generated
in one paid request. “Open source technologies” replaces “open source tools”.
The former 1.2s zero-PCM insertion is removed: the natural performed pause is
preserved. Cache `_build/audio/continuous-11e9ec5460036865.wav`, SHA-256
`d656061d09062e49df946f42cee850da48af2b80c2ac24672f8c4848555c569a`.
Its provider receipt, metadata and `provider-original.wav` are retained;
the raw take and provider-original are byte-identical. The mix adds 3s lead-in.
Do not regenerate without direction.

## New scene implementation

- `capture-studio.mjs` captures the real UI with a browser-local mock session
  and fictional completion checklist. All non-GET requests are blocked.
  It loads the real sawmill export and assembly navigator, then hides only
  the model host. A 3000px padding creates the long chat scroll without
  filler text. No agent conversation or broker state was changed.
- `assets/studio-background.png`: 3840×2160, captured at 1280×720 / DPR 3.
  `assets/studio-capture.json` records rectangles, text, scroll and provenance.
- `StudioSurface` is a project element containing the shared model's `Slot`.
  It synchronously moves that box and the screenshot from cue progress; no
  timer, effect-driven layout, alternate simulation or dependency patch.
  Stage set declarations include that nested slot. Empty-set measurement does
  not supply its dynamic box; the new browser checks measure its actual canvas.
- At “Machinome builds” (99.67s), a 1.2s background reveal covers the source
  without moving/fading the model. At 100.875s the Studio shot moves both
  background and model box over 2.8s. The camera stays `Sawmill.source`.
- At 109.79s chat highlights while “There's one more adjustment:” types;
  at 111.32s Code highlights; at 112.83s Build highlights. These are display
  overlays, not clicks/submissions. Testing begins at 114.333s and its code
  types until “This test checks” at 118.17s.

## Preserved direction and verification

Prior opening fades, manuscript/source label, complete rope highlight,
scoped `spoken` highlights, circumference delayed to OpenSCAD, closing hub
zoom, logo entrance on “I'm”, and GitHub/licence fade on “Open Source” remain.
The stream starts 0.85s before Trimesh in this take to retain three seconds
of reading time per label. It runs 171.417–178.32s, over the waterwheel from
173.5s. Wheel acceleration is 45°/s² on the new timing, above one turn/s at
zoom onset and about 1.26 turns/s at its end. Names retain independent clocks.

Fresh local forced alignment pins `drives` to 97.875–98.417s and `crankshaft`
to 98.500–99.333s on the film grid. The take hash guard remains. See
`relation-timing.json`; do not reuse offsets against a different take.

83 existing preview checks, 8 relation-sync checks and 13 Studio-frame
checks pass. Studio transition, full-screen placement, prompt/menu highlights
and representative existing frames were visually inspected. Audio was checked
for integrity and timing, not given a new human listening approval.

The **old MP4 remains unchanged**, 191s / 1080p24, revision `e5e5779`;
SHA-256 `14db64cfa4bb32efeb01cc1586d5ea1aa0f8257770db697c1455997f0fc07d02`.
It does not contain the new scene. No new render was requested or performed.
Previous records are in `_build/revisions/before-studio/`; earlier caches and
MP4 review packs remain. `VERIFICATION.md` keeps the prior review history.

Reproduction commands: `README.md`. Stop only this cut's live server before
movie evaluation → finishing → restart. `finish.mjs` is not idempotent and
requires fresh `movie.py` output. Use `setsid -f` when detaching the live
server so it survives the launching shell. Ordinary composed dissolves still
show as midpoint cuts live; the project-specific Studio reveal is fully live.

The pilot-requested source label and final licence text explicitly override
the Videomaker skill defaults. Gallery licence records remain AGPL-3.0-only;
the closing `GPL-2.0-or-later OR CERN-OHL-S-2.0+` discrepancy and unresolved
publication URLs remain in `description.md`. Do not alter licensing records
or claim this local rehearsal is release-ready.
