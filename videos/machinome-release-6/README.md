# Revolutions — final English cut

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The English release film with everything approved for the Brazilian cut
(`../machinome-release-5-pt-br/`). [DIRECTION.md](DIRECTION.md) records what
was carried over, [delivery.json](delivery.json) holds the approved text and
voice directions, and [description.md](description.md) is the draft upload
description. Nothing has been published.

## Delivered file

`_build/machinome-revolutions-en-fullhd.mp4`, rendered on 17 November 2026:

- 1920×1080, 24 fps, 5294 frames, 220.583 s (3 min 40.6 s), H.264 CRF 14
  with AAC stereo sound;
- captured at 3840×2160 and reduced with Lanczos from the lossless frames;
- SHA-256 `6f8237d33053e370bc6157361e7cb4d12aae744cc9a26b434fdf9ef9978ca341`;
- `_build/projection-master.json` records the capture, the encode and the
  probe.

The narration is one continuous Jessica take (207.36 s), approved by the
pilot by listening on 17 November 2026, SHA-256
`cc80a2c9f0ddde3fa7d7e27372d852decfe0296d67acb32a8cda4a3663361613`. The film
plays its derivative with four three-second reading pauses (215.177 s,
SHA-256 `1efb964a65fc47dc31f68b0ec99737757793f610506e76c4107bdeb78bcd356d`);
every spoken sample is preserved.

Checked on the delivered file: frame count, size and rate; decoded frames at
21 moments across the film; silence of three seconds at each of the four
code transitions (107.85, 153.96, 170.12 and 178.05 s). The agent did not
listen to it. Word timing inside a phrase is approximate.

## Reproduce from the approved take

Do not generate speech again: `audition.mjs --generate` is a new paid
audition and needs the pilot's request. The untouched take and its receipt
are in `_build/audition-1/`. `_build/model` is a byte copy of the Brazilian
cut's model export. From this repository's root:

```sh
node videos/machinome-release-6/prepare.mjs
python3 videos/machinome-release-6/calibrate.py
node videos/machinome-release-6/reading-pauses.mjs
PYTHONPATH=.:/home/asa/devel/machinome/videomaker/python /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-6/movie.py
node videos/machinome-release-6/finish.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-6/check-reading-pauses.mjs
node videos/machinome-release-6/render-projection.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

`finish.mjs` needs a fresh evaluation of `movie.py` and is not idempotent.
It and the render use cached speech only. The render took about 85 minutes
on this machine, which has no GPU.

`calibrate.py` reads `_build/audition-1/ending-check.json`, the independent
transcription written by `verify-ending.py` (faster-whisper, local model).
That transcription only tells which measured silence belongs to which
sentence boundary; it gives the film no timestamp.

## Preview

```sh
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs live videos/machinome-release-6/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --port 8785
```

`inspect-frames.mjs` photographs that preview at chosen film times.
`python3 videos/machinome-release-6/serve-listening.py --port 8786` serves
the listening page for the take.
