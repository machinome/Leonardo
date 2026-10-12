# Cut 5 handoff

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Main-branch selection — 12 October 2026

The pilot selected the latest descending-stream cut for main with narration
only. Sound-effects sources and their complete listening record are preserved
on release-video-sound-effects (69ea613); the original checkout retains every
ignored audio cache. No effects are loaded by the main preview command.

The recovered model now lives in this cut at _build/model. All 96 assets
match the earlier film checksums; its manifest records the actual recovery
revision. The original continuous narration and visuals are preserved.
The saved 191-second MP4 is historical; the current web preview is 203.625s.
See README.md for the narration-only launch command. No new speech or MP4.

The following sections retain the earlier visual-development history.

## Previous picture state — sequential testing / BUILD emphasis, 8 October 2026

Checkpoint **`efff48d`**, native Firefox version, is committed on
`release-video`. The current timing/narration trial is deliberately left uncommitted
for preview. Only cut-5 production files changed; unrelated Portuguese cut-4,
review drafts and Videomaker working changes belong to others.

Live: http://127.0.0.1:8785/#movie — **203.625s**, authored 1080p24 (live
stage served at 960×540). Studio entrance 102.958s; testing transition 117.417s;
closing question 198.636s. No MP4 render or publication.

Latest follow-up: **mid-right reading hold → curved descending stream**.
Names now hold at (1830,540), then descend smoothly toward (960,820) and
continue left at y820. `driverY(x)` changes only height; `driverX` and every
timing remain untouched. The SVG guide is the matching cubic, 15px below the
text baseline, with level entry/exit tangents. Both graphic and physical-wheel
scenes share this presentation. Movie documents, Studio edit and narration are
unchanged; no evaluation, speech generation or MP4 render. Backup:
`_build/revisions/before-curved-stream/`.

Preceding follow-up: **first pass → graphic spin → waterwheel**. Keep the approved
stream timing/motion unchanged. Graphic spin starts when Three.js passes beneath
the centre at 180.8765s (`streamDelay + arrival` on the drive clock), not at
entry. `HANDOFF` is now the shared spoken anchor “beneath it all” + 2.175s:
the waterwheel begins at 182.125s, after ~1.25s of graphic-only spin. Its fade
still lasts 1.25s, ending at 183.375s. Graphic and real wheel share the new phase;
acceleration is 52°/s² to retain the fast ending after the later start. The hub
zoom's spoken anchors, all seven name holds/launches, Studio and narration are
unchanged. Backup: `_build/revisions/before-later-wheel-handoff/`.
No speech generation or MP4 render.

Preceding follow-up: **individual hold, then accelerating launch**. The pilot
rejected the continuously moving names despite the measured frame occupancy.
Each now holds at x1830 for 14 frames (0.583s), then accelerates from zero speed
to x-110 over 0.5s. Equal entries are ~0.733s apart. The first still appears
on “beneath” at 179.958s; the last leaves at 185.440s before the baseline fade
ends at 185.590s. The readable criterion is now a stationary hold for every
name, not the superseded three-second moving window. `driverX` subtracts
the per-name hold before applying acceleration; the final entry has the same
complete hold/launch. Wheel phase/camera, Studio timing and narration are
unchanged. Backup: `_build/revisions/before-stream-hold-launch/`.
No speech generation or MP4 render.

Preceding follow-up: **stream entrance on “beneath”**. Three.js now enters at
179.958s, the first 24fps frame after the measured onset at 179.950s.
`streamDelay` keeps labels and their baseline absent before that instant,
without shifting the graphic/physical wheel clock or handoff at 179.250s.
`finish.mjs` measures the phrase from the existing take. Labels reach centre
in 1.75s with entry-speed fraction 0.9 and stagger ~0.349s: gentler individual
acceleration and a tighter cadence preserve 3+ seconds of full reading time
and 24+ pixels of spacing. They still clear at 185.590s, before the returning
line at 185.790s. Narration, Studio and the physical wheel shot are unchanged.
Prior sources/documents: `_build/revisions/before-beneath-stream/`.
No speech generation or MP4 render.

Preceding follow-up: **faster testing travel**. The layout move is now 2.75s
instead of 3.625s, arriving at 120.167s. Typing follows the faster move,
beginning at 119.667s (still its final half-second), and completes at the
unchanged 123.958s. Quintic easing, 17% top margin, 0.6s fade, camera, rewind
and narration are unchanged. Prior movie/source documents are retained in
`_build/revisions/before-faster-testing-travel/`. No new speech or MP4.

Preceding follow-up: **testing spacing, easing and earlier typing**. The testing
model lands at y17% rather than y7%, keeping its 36% width / 83% height.
Its layout move now uses quintic smootherstep (zero velocity/acceleration at
both ends); duration and camera are unchanged. Typing now starts at 120.542s,
the final half-second of travel, and still completes at 123.958s. The pilot
explicitly allowed this overlap, superseding the post-landing blank pause.
Source documents before this edit are in `_build/revisions/before-testing-spacing/`.
Fresh evaluation and cache-only finishing preserve the narration hash below;
no speech generation or MP4 render.

Preceding follow-up: **faster Studio fade**, 0.6s instead of the 3.625s travel.
`StudioSurface.departureFade` is authored in movie.py; stage opacity uses that
duration independently of the unchanged layout progress. The photographed
browser, controls and full-machine context are gone by frame 118.042s; the
retained timber/blade stays fully opaque while it travels to the right until
121.042s. Keep code left / model right (code x4%, model x64%, original widths).
At that checkpoint narration, camera, rewind, movement and typing were unchanged. Fresh evaluation
and cache-only finishing were performed; no speech generation or MP4 render.
Only the new fade prop/schema and movie.py provenance hashes changed in the
movie document. Pre-change sources/movie are in
`_build/revisions/before-fast-studio-fade/`; the preceding side-swap records
remain in `_build/revisions/before-code-left/`.

Latest text: “You can build models from your browser, using Machinome Studio”,
continued directly with “where you can prompt your agents…” (no repeated
Studio introduction). Testing: “Machinome also provides a testing framework,
that allows us to test how parts fit together.” Closing: “What do YOU want to
BUILD?” Keep “want to”; both uppercase words request vocal emphasis.
The complete performance was regenerated once for these three edits.

The latest pilot correction supersedes the earlier pointer/long-orbit request:
no pointer; highlight chat, Code, Build, then model. The added line is
“and interact with the model to see different angles and moments of the
animation.” A 110.137° short turn at 112.708–115.083s reaches the test lens,
then holds. Highlight the slider at 115.125s, scrub from model second 479.325
to zero at 115.417–116.792s, hold until testing at 117.417s. Testing is now
**sequential, not a code cross-fade**: Studio and full-machine context fade
in 0.6s while the retained blade/timber view travels right, completing at 120.167s.
Start typing 0.5s before that landing, at 119.667s,
finishing at 123.958s. `Listing.conceal`
hides the entire source panel, filename included, until typing starts.

`studio-motion.mjs` is the project-owned finishing pass. The public movie
format refuses decreasing time inside one shot (confirmed by a read-only
probe). The rewind is therefore 48 single-frame held-pose shots through the
same real export, same View identity and held camera. This is a film edit,
not new geometry or a framework bypass. Each cut uses an absolute spoken
anchor: repeated numeric 1/24 durations accumulated floating-point error,
which the new browser regression caught as stale/missing frame state.
Do not replace these anchors with cumulative additions. `_build/studio-edit.json`
records the measured edit; the slider's `model-clock` action uses exactly
the corresponding model seconds. No mouse or Studio event is dispatched.

One new paid, unedited Jessica/Eleven v3 take: **198.24s**, 2376 characters,
43 beats. Cache `_build/audio/continuous-c4a5bfdf32eede25.wav`; raw SHA-256
`cf456cb9b5f93fd39b288c0d48708d47e5437b471b2deae6d6794a810267efb7`.
Mixed SHA-256 `069804c8984224a171c7dd26641e9475baad5b2b461194e965c50b613efb155c`.
No splicing, added silence, stretching or truncation. Provider receipt and
original WAV retained. `relation-timing.json` was remeasured locally with
PocketSphinx; new film drives 101.417–101.958s, crankshaft 102.042–102.750s.
Never reuse the prior offsets or regenerate without direction.

162 browser samples/checks pass: 118 general, 8 relation, 13 Studio entrance,
23 interaction. The new check additionally examines every camera/scrub frame,
proves the short monotone turn, exact slider/model clock, rewind to zero,
held camera, continuous layout across the testing boundary and pixel-identical
seek replay. It checks every pre-typing frame carries the conceal action,
and verifies blank-left and completed-source browser images. Four additional
travel samples pin the quintic easing at 10%, 25%, 75% and 90% of its duration.
Landing checks pin the 17% top margin with unchanged model size; typing checks
prove source starts while the model is still travelling and continues through
landing. Fast-fade checks
verify half opacity after 0.3s and a fully clear background after 0.75s while
the retained detail stays opaque and continues right. Turn, scrub, departure,
fast-fade, clear-travel, blank-left and completed typing images visually inspected.
Stream entrance checks prove no labels at the old start, phrase start or preceding
frame, then Three.js alone at the first frame after “beneath”. All seven labels
have 14 stationary reading frames, identical accelerating launches from rest
and 24px minimum inter-label gap. Browser checks sample the first/last held
frame and a launch frame for every name, replacing the rejected moving-window
criterion. Before/onset, held-name and last-launch screenshots were inspected.
Five new graphic-spin samples prove no rotation before the first centre pass,
fully opaque graphic-only rotation before handoff, and physical-wheel mounting
only at the new boundary. Stream parameters and Studio timing compare identical
to the preceding backup; wheel model keys change intentionally to the new phase.
At zoom start/end the measured wheel speed is ~411/517° per second. The held
graphic, pre-handoff spin and graphic/waterwheel overlap were visually inspected.
Audio integrity/timing checked; no new human listening approval claimed.

The preceding interaction preview/audio/source files remain in
`_build/revisions/before-sequential-testing/`; earlier preview/audio files
remain in `_build/revisions/before-studio-interaction/`.
The old 191s MP4 still hashes to
`14db64cfa4bb32efeb01cc1586d5ea1aa0f8257770db697c1455997f0fc07d02`.
The screenshot was not recaptured. No Studio, viewer or tool source changed.
Use README's reproduction/check commands; stop only the 8785 process before
fresh movie evaluation → finishing → restart with `setsid -f`. Leave Studio
9000 and cut-4 8784 alone. `finish.mjs` remains non-idempotent.

## Previous checkpoint — Studio revision, 8 October 2026

Work belongs to the Leonardo repository on **release-video**, checkpoint
`c9c3db6` before this revision. Real root: `/mnt/data/machinome-projects/Leonardo`.
Only `videos/machinome-release-5/` changed. Portuguese cut-4 and review drafts
are unrelated dirty work; do not stage them. No framework, Studio or viewer
source was modified; no push or publication.

Live URL: http://127.0.0.1:8785/#movie (194s).
Log: `/tmp/machinome-release-5-live.log`. Cut 4 stays on 8784.
Studio was already running on http://127.0.0.1:9000; leave it alone.

Latest visual follow-up: the screenshot is now a **native Firefox window**
showing `http://localhost:9000/`. Captured on a private 3840×2160 Xvfb display
with Playwright Firefox 153.0 (DPR 3), not a drawn browser mockup. The capture
helper sizes only that isolated window, and FFmpeg captures the full frame.
The page's native offset is 84⅓ CSS pixels; recorded model/menu rectangles
include it. The existing composition uses the new geometry automatically.
All movie fields except the screenshot and capture geometry are identical
to the approved Studio revision (`b7ea1d6`). Narration and MP4 hashes are
unchanged, and no speech generation or MP4 render was performed. Before-frame
records remain under `_build/revisions/before-firefox/`.

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
- `assets/studio-background.png`: 3840×2160, native window 1280×720 / DPR 3;
  its page is 1280×636 beneath the Firefox controls.
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
