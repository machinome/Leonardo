# Machinome release — cut 5

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Main-branch **narration-only live preview**: http://127.0.0.1:8785/#movie — 203.625 seconds,
1920×1080, 24 fps. The sequential testing revision has a new continuous Jessica take.
[Narration](narration.py), [movie](movie.py), [direction](DIRECTION.md),
[upload description draft](description.md), [verification](VERIFICATION.md).

“You can build models from your browser, using Machinome Studio” replaces
the JavaScript-application introduction; it continues “where you can prompt
your agents…”, without a repeated Studio introduction.
At 102.958s, the assembly source fades into the Studio background while the
model keeps moving without a camera change. At 104.167–106.967s, the whole
composition translates and scales into the full-screen Studio layout.
The chat prompt types on “prompt your agents”; Code and Build highlight
on their spoken phrases. The new line is “and interact with the model to see
different angles and moments of the animation.” There is no mouse pointer.
Highlight the model, take the short camera turn at 112.708–115.083s, then
highlight the timeline at 115.125s. Scrub the actual model from 479.325s back
to zero at 115.417–116.792s; the overlaid slider reads that same model clock.
Testing begins at 117.417s with “Machinome also provides a testing framework,
that allows us to test how parts fit together.” Studio fades out as the model
travels right, arriving at 120.167s. Code starts typing at 119.667s, during
the final half-second of travel, and completes at 123.958s. Studio and full-machine
context now fade out in **0.6s**, fully clear by the 118.042s frame, leaving
the opaque timber/blade travelling across the clear background. The move
now takes 2.75s instead of 3.625s, retaining the quintic ease-in/out. Neither code nor filename
appears during the fade; no cross-fade into the code. The discarded sentence
about agents and tests is absent.

The layout restores code on the left (4–64% of the frame) and model on the
right (64–100%). The testing model's top margin is now 17% (formerly 7%),
moving it down without shrinking it. The 0.6s fade, camera, rewind and narration
are unchanged. No new speech was generated.

The closing request is now “What do YOU want to BUILD?” Both uppercase words
request vocal emphasis; no closing question is drawn on screen.

The screenshot includes a real Mozilla Firefox window with the address
`http://localhost:9000/`, around the real Studio UI and existing sawmill export,
a **browser-only staged** completion message, and a long scroll created
by spacing rather than filler text. The actual model was hidden for the
capture and is composed as a live View in the film. No broker session was
opened, no message submitted and no build dispatched by the capture.
The screenshot, geometry and provenance are under [assets/](assets/).

“Open source technologies” replaces “open source tools”. Speech is one
unedited provider recording, including its natural pause before the returning
wheel line. No zero-PCM block, splice, stretching or truncation is applied.
The stream waits for “beneath it all”, with Three.js entering at 179.958s (the first frame after
the measured “beneath” onset at 179.950s). No stream label appears before it.
Each name holds still at **right/mid-height** (x1830, y540) for **0.583s
(14 frames)**, then accelerates from rest across the screen in **0.5s**.
The names and their guide line curve downward like water from higher ground,
levelling out beneath the wheel at the original y820 text baseline. Horizontal
motion and all approved timings are unchanged. Entries are spaced about
0.733s apart, so the names read as separate launches. OpenSpec completes the
same motion by 185.440s; the baseline fades out by 185.590s, before the
returning sentence. This replaces the rejected continuously moving stream;
time inside the frame alone was not sufficient reading time. The graphic wheel
waits until Three.js passes below its centre at 180.877s, then spins alone for
about 1.25s. The fade to the physical wheel starts at 182.125s and finishes at
183.375s while names continue launching. The shared wheel phase accelerates
at 52°/s² to preserve the fast hub-zoom ending despite the later spin start;
the zoom, narration and all name timings are unchanged.

The original [MP4 rehearsal](_build/rehearsal.mp4) and separate
[subtitles](_build/rehearsal.srt) remain **unchanged**: 191 seconds, rendered
from `e5e5779`. They do not include the Studio scene or subsequent live fixes.
No replacement MP4 was requested. Previous preview/audio records are retained
under `_build/revisions/before-studio/`; keyed speech caches are also retained.

## Reproduce the live preview

This is the selected main-branch cut: the descending technology stream,
Studio sequence and continuous Jessica narration, without sound effects.
The experimental effects sources, recipes and listening history are preserved
on the local `release-video-sound-effects` branch. Its ignored audio caches
remain in the original Leonardo checkout; they are not part of this soundtrack.
To reopen the completed preview, run **only the final `live` command** below.
The preceding commands rebuild the film using the existing speech cache.

The model export now belongs to this cut at `_build/model`. The missing cut-3
export was recovered on 12 October: all 96 model assets match the earlier
film's recorded SHA-256 checksums. If that local export is absent, first run
`machinome export hydraulic_sawmill -o videos/machinome-release-5/_build/model --no-widget`.

Stop this film's live server before evaluating/finishing; leave Studio and
the cut-4 server alone. From the Leonardo repository:

```sh
node videos/machinome-release-5/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-5/narration.py
node videos/machinome-release-5/speech.mjs /home/asa/devel/machinome/videomaker
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-5/movie.py
node videos/machinome-release-5/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs live videos/machinome-release-5/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --port 8785
```

Speech is cache-only unless explicitly passed `--generate`; generation costs
money and is not required for reuse. `finish.mjs` must follow a **fresh** movie
evaluation. It mixes the take with the three-second lead-in and applies the
take-bound relation timing in `relation-timing.json`; a new take requires
remeasuring that timing. It does not generate speech or render video.

To recapture the staged Studio UI, with Studio already running at port 9000:
the capture uses Playwright's Firefox, Xvfb, xwininfo, FFmpeg, and Python's
standard-library ctypes with the system libX11. It captures a private virtual
display, never the user's desktop. Install the capture browser only if missing:

```sh
PLAYWRIGHT_SKIP_BROWSER_GC=1 node /home/asa/devel/machinome/videomaker/node_modules/playwright/cli.js install firefox
```

Then capture the native tab/address bars and the staged page together:

```sh
node videos/machinome-release-5/capture-studio.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

Do not recapture casually: a different Studio layout changes the recorded
geometry and screenshot. The script blocks all non-GET requests and serves
the fixture session/model only to its isolated capture browser.

The Studio reveal and exit, opening reveals and ending motion are visible live.
Other ordinary composed dissolves still appear as midpoint cuts in the live
player; a future requested render supplies their final blend. No tool-wide
transition behavior was changed.

`studio-motion.mjs` compiles the short turn and scrub. Since the public movie
format forbids decreasing model time within a shot, the scrub is a sequence
of held real-model poses, one per 24fps frame, with the same view and camera.
Absolute spoken anchors prevent cumulative frame-boundary rounding drift.
This is a playback demonstration, not a physically reversing sawmill.

Browser checks (with the live server running):

```sh
node videos/machinome-release-5/inspect-preview.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-5/inspect-relation-sync.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-5/inspect-studio.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-5/inspect-studio-interaction.mjs /home/asa/devel/machinome/videomaker
```
