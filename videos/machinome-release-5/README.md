# Machinome release — cut 5 preview

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Live preview of the edits in [DIRECTION.md](DIRECTION.md), with new Jessica
narration, brief word-synced code enumeration, a narrated stream/wheel overlap,
and a closing zoom into the wheel followed by the logo fade.
No MP4 is rendered. [Narration](narration.py), [movie](movie.py),
[upload description draft](description.md).

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

The live player shows composed dissolves as midpoint cuts. Review their
timing here; this player does not yet show their final blended appearance.
The opening machine reveal now uses a live reframe from 7.29s to 8.49s:
the wheel stays solid and the full machine fades in. The stream/wheel overlap
and closing zoom/fade are project-owned live actions and also display their
blending. Current duration: 191 seconds. The second
wheel line starts around 174.8s, its zoom starts at 177.96s, and the logo
begins fading in at 179.83s. See [VERIFICATION.md](VERIFICATION.md) for checks
and the known provider-alignment issue.
