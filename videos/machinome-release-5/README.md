# Machinome release — cut 5

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Live preview of the edits in [DIRECTION.md](DIRECTION.md), with new Jessica
narration, brief word-synced code enumeration, a narrated stream/wheel overlap,
and a closing zoom through the wheel towards the approaching logo.
One narrated [MP4 rehearsal](_build/rehearsal.mp4) was rendered on the pilot's
request on 8 October 2026: 191 seconds, 1920×1080, 24 fps. Optional
[subtitles](_build/rehearsal.srt) are separate, not burned in.
[Narration](narration.py), [movie](movie.py),
[upload description draft](description.md).

The live preview now includes the subsequent relation-word sync correction:
`drives` at 101.917s and `crankshaft` at 102.458s. The existing MP4 predates
this correction and is retained unchanged; no replacement render was requested.
The preview also confines “spoken” to the seven calls inside the displayed
`Cue`s (142.3s), and delays the circumference until the OpenSCAD label and
spoke appear (157.75s). Only the M and title approach beforehand.

From the Leonardo repository:

```sh
node videos/machinome-release-5/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-5/narration.py
node videos/machinome-release-5/speech.mjs /home/asa/devel/machinome/videomaker
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-5/movie.py
node videos/machinome-release-5/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs live videos/machinome-release-5/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --port 8785
```

Speech is cache-only by default; the initial take requires `--generate`.
The provider receipt and untouched provider WAV are retained. The preview
take inserts 1.2 seconds of silence before the returning wheel line;
its metadata records the edit and all following timestamps shift with it.
`finish.mjs` follows a fresh movie evaluation and mixes the cached audio at
the film's three-second lead-in. It does not request speech or render video.

To reproduce the rehearsal from the finished movie and cached narration,
stop this film's live server first, then run from the Leonardo repository:

```sh
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-5/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

This uses cached speech only. The rendered source revision is `e5e5779`;
the manifest and decoded review pack remain in `_build/`. This is a local
rehearsal, not a release-ready publication. See [VERIFICATION.md](VERIFICATION.md).

The live player shows composed dissolves as midpoint cuts. The MP4 contains
their final blends, inspected in decoded midpoint and end frames.
The opening wheel turns from the first frame, without the former one-second hold.
The opening machine reveal now uses a live reframe from 7.29s to 8.49s:
the wheel stays solid and the full machine fades in. The mechanism change
at 32.46s also fades live over 1.2 seconds. Testing code types from 105–110s;
the film source types from 131.08–133.08s before the word-synced enumeration.
The stream/wheel overlap and closing motion are project-owned live actions.
The slower tool stream lasts 167.75–174.62s, continuing over the waterwheel
after the graphic circle fades and clearing 0.2s before the returning speech.
Each name stays fully in frame for at least three seconds.
The ending wheel keeps accelerating through the hub zoom, from just over
one turn per second at zoom onset to about 1.25 turns/s at its end.
Current duration: 191 seconds. The second
wheel line starts around 174.8s, its zoom starts at 177.96s, and the logo
waits for “I'm”, then approaches from the distance at approximately
180.52–181.72s without fading. Its GitHub
address and the pilot-supplied licence line fade in together on the closing
“Open Source” at about 185.61–186.49s, both at fixed size, with no tagline.
See [VERIFICATION.md](VERIFICATION.md) for checks
and the take-bound local correction of the provider-alignment issue.
