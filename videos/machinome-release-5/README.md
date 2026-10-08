# Machinome release — cut 5

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Current **live preview**: http://127.0.0.1:8785/#movie — 194 seconds,
1920×1080, 24 fps. The Studio revision has a new continuous Jessica take.
[Narration](narration.py), [movie](movie.py), [direction](DIRECTION.md),
[upload description draft](description.md), [verification](VERIFICATION.md).

At 99.7s, the assembly source fades into the Studio background while the
model keeps moving without a camera change. At 100.875–103.675s, the whole
composition translates and scales into the full-screen Studio layout.
The chat prompt types on “prompt your agents”; Code and Build highlight
on their spoken phrases. Testing begins at 114.333s with “Machinome also
lets us test how parts fit together.” The discarded sentence about agents
and tests is absent.

The screenshot is the real Studio UI with the existing sawmill export,
a **browser-only staged** completion message, and a long scroll created
by spacing rather than filler text. The actual model was hidden for the
capture and is composed as a live View in the film. No broker session was
opened, no message submitted and no build dispatched by the capture.
The screenshot, geometry and provenance are under [assets/](assets/).

“Open source technologies” replaces “open source tools”. Speech is one
unedited provider recording, including its natural pause before the returning
wheel line. No zero-PCM block, splice, stretching or truncation is applied.
The stream overlaps the physical wheel from 173.5s and clears at 178.32s,
0.2s before the returning sentence. Every name remains fully visible for
at least three seconds. The wheel keeps accelerating through its hub zoom.

The original [MP4 rehearsal](_build/rehearsal.mp4) and separate
[subtitles](_build/rehearsal.srt) remain **unchanged**: 191 seconds, rendered
from `e5e5779`. They do not include the Studio scene or subsequent live fixes.
No replacement MP4 was requested. Previous preview/audio records are retained
under `_build/revisions/before-studio/`; keyed speech caches are also retained.

## Reproduce the live preview

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

```sh
node videos/machinome-release-5/capture-studio.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

Do not recapture casually: a different Studio layout changes the recorded
geometry and screenshot. The script blocks all non-GET requests and serves
the fixture session/model only to its isolated capture browser.

The Studio reveal, opening reveals and ending motion are visible live.
Ordinary composed dissolves (including Studio → testing) still appear as
midpoint cuts in the live player; a future requested render supplies their
final blend. No tool-wide transition behavior was changed.
