# Machinome release — cut 4, release candidate

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

[Watch locally](http://127.0.0.1:8784/) · [MP4](_build/rehearsal.mp4) ·
[Raw narration](_build/raw-narration.wav) · [Film source](movie.py) ·
[Narration](narration.py) · [Description draft](description.md).

This candidate runs 3:09.042 at 1920×1080, 24 fps. It uses one fresh
Jessica / Eleven v3 performance: eight spoken CAD technologies, then
“And beneath it all, a stream of open source tools...” with a deliberate
pause. The closing question directs emphasis on YOU.

The eight-spoke wheel connects OpenSCAD, SolidPython, CadQuery, Build123d,
FreeCAD, JSCAD, OCCT and Trimesh. Three.js, NumPy, SciPy, Manifold, FastAPI,
React and OpenSpec flow into it as an accelerating stream. The graphic and
physical spokes share one accelerating phase through their handoff.
The literal test excerpt has blank lines before its class and decorator.
The orange closing identity has a larger tagline and the framework GitHub URL.

Release-3 is untouched. [DIRECTION.md](DIRECTION.md) records the latest
commission; [VERIFICATION.md](VERIFICATION.md) records production evidence
and review limits. Nothing is uploaded or published.

## Reproduce

From the Leonardo repository root, using the existing workspace environment:

```sh
node videos/machinome-release-4/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-4/narration.py
node videos/machinome-release-4/speech.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-4/audio-evidence.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-4/movie.py
node videos/machinome-release-4/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/machinome-release-4/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/machinome-release-4/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 1280
node videos/machinome-release-4/inspect.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-4/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/machinome-release-4/postflight.mjs
python videos/machinome-revolutions-v2/serve-review.py --port 8784 --directory videos/machinome-release-4
```

The review server stays in the foreground. In a separate terminal run:
`node videos/machinome-release-4/check-player.mjs /home/asa/devel/machinome/videomaker`.
Run document-loading commands in sequence: each writes its resolved document.
`finish.mjs` follows a fresh evaluation of `movie.py`, never itself twice.

Speech defaults to cache-only. The initial full-script request used
`speech.mjs <videomaker> --generate`; successful provider receipts are saved
before interpretation, and no paid request is automatically retried.
There are no pickups, splices, time stretches or inserted pauses. The
performance is placed at +3 seconds; its final hold comes from the film.

The new audio requires new shot timing and frame capture. Unchanged assets
are reused in place: cut-3's model export, drawing and orange identity;
cut-2's Python logo; cut-1's pinned fonts and pronunciation dictionary.
Native frame and speech caches are retained for subsequent retries. Cache
keys are never substituted to make old frames appear current.

The model export at `../machinome-release-3/_build/model` records revision
`94a8562cc70e96de0cad1b85a4a7c1e092d2ed5c` and its actual dirty-tree flag.
No CAD or test code changes. If that local export is unavailable, export the
same model to a new cut-4 build path and update `Sawmill.export` explicitly;
do not overwrite cut-3's evidence. Generated media stays local and ignored.

The framework URL on the closing card is not the unresolved gallery
source/simulation address. The description keeps those publication blockers,
production disclosure and licensing caveats visible. Human listening review
of pronunciation, delivery and mix remains necessary.
