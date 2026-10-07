# Machinome release — cut 3

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Third version commissioned from [review 2](review-2.md), with Jessica
retained and the opening “AI content” label removed at the pilot's request.
The first and second cuts are preserved. Production evidence and the final
artifact identity are recorded in [VERIFICATION.md](VERIFICATION.md).

- [Local player](index.html) · [MP4](_build/rehearsal.mp4).
- [Raw continuous narration](_build/raw-narration.wav).
- [Film source](movie.py) · [narration](narration.py).
- [Direction](DIRECTION.md) · [description draft](description.md).

The movie uses 1920×1080 at 24 fps. One new Jessica / Eleven v3 take
includes the real testing example, Three.js and OpenSpec. Its raw WAV,
provider receipt and character alignment are retained under ignored
`_build/`; the render adds a three-second lead-in and closing hold.
It neither splices nor stretches the performance. Listening approval of
cut 2 does not imply approval of this new take.

The opening orbit is one sampled parametric curve. Code blinks use the
measured start and end of each word and never highlight `water_drive`.
The new scene shows the existing blade-clearance test and thirteen sampled
poses. The requested Commons drawing replaces both prior historical-image
shots. OpenSpec crosses the frame horizontally and sets the graphic wheel
moving as it passes underneath.

## Reproduce

From the Leonardo repository root, with the existing workspace environment:

```sh
node videos/machinome-release-3/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-3/movie.py
node videos/machinome-release-3/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 1280
node videos/machinome-release-3/inspect.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-3/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/machinome-release-3/postflight.mjs
python videos/machinome-revolutions-v2/serve-review.py --port 8783 --directory videos/machinome-release-3
```

These commands reuse cached speech. To deliberately generate a revised take,
first evaluate `narration.py`, then call `speech.mjs <videomaker> --check`,
review its script, and use `--generate` for one paid request. The command
without `--generate` is cache-only; it retains successful receipts before
interpretation and does not automatically retry an ambiguous request.

The isolated model export is `_build/model`, created with
`machinome export hydraulic_sawmill -o videos/machinome-release-3/_build/model --no-widget`.
It records revision `94a8562cc70e` and the actual dirty-tree flag. The
mechanical source is unchanged. Model and test excerpts are taken from
committed source with original line numbers and whole-file checksums;
film-source classes are AST-extracted from the actual declarations.

Generated media is local and ignored. The description carries the project
attribution, image-source record and production disclosure. Public addresses
remain unresolved; nothing is uploaded or published.
