# Machinome release — cut 2

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Status: built and verified on 3 October 2026. The completed cut is
1920×1080, 24 fps, 141.75 seconds, with the approved single narration.
[Verification](VERIFICATION.md) records the initial cut. The completed
[code-scene revision](CODE-REVISION.md) records the current checksum,
restores complete classes and keeps the self-narration inside its source.

- [Local video player](index.html) · [MP4](_build/rehearsal.mp4).
- [Approved raw narration](narration.html) · [lossless take](_build/approved-narration.wav).
- [Film source](movie.py) · [narration source](narration.py).
- [Visual direction](DIRECTION.md) · [upload-description draft](description.md).
- [Original brief](brief.md) and [review](review-1.md), verbatim snapshots
  of the canonical human records in the parent directory.
- [Narration history and trade-off](NARRATION.md).
- [Voice design 6: starting from Jessica](voice-design-6.html) · [previous C3/Jessica comparison](voice-design-5.html) · [voice direction and earlier rounds](VOICE-DESIGN.md); timbre selection pending, film unchanged.
- [First proposal](../machinome-release-1/README.md), preserved unchanged.

With the review server running, open <http://127.0.0.1:8782/>. The player
offers optional subtitles and seeks to each major sequence.

The pilot ratified the corrected single narration and added the Python logo
after the museum photograph. The later clarification explicitly chose
**OpenSpec as an additional visual element**, arriving along the watercourse.
It adds no speech and does not replace the spoken OpenSCAD.

## Edit and reproduction

One chapter, continuous, uses the exact approved 1,712-character performance,
Jessica / Eleven v3. Its raw duration is 136.40 seconds; its SHA-256 is
`e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3`.
The current provider WAV and original request/alignment remain under
`_build/audio/continuous-be56771bde523273.wav`; the previous take remains too.

The 17-shot movie is 141.75 seconds at 24 fps. There is a three-second silent
lead-in: one second held, two accelerating. The render places the unchanged
take at +3 s, level-normalizes the final mix, and adds the closing hold.
It never splices, stretches or resynthesizes speech. The raw listening copy
and raw captions have their own approved-* paths, independent of the film mix.

Run from the Leonardo project root, using the existing workspace environment:

```sh
node videos/machinome-release-2/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/machinome-release-2/movie.py
node videos/machinome-release-2/finish.mjs /home/asa/devel/machinome/videomaker
node --test videos/machinome-release-2/speech.test.mjs
/home/asa/devel/machinome/.venv/bin/python videos/machinome-release-2/test_code_scenes.py
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/machinome-release-2/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/machinome-release-2/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 1280
node videos/machinome-release-2/inspect.mjs /home/asa/devel/machinome/videomaker /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/machinome-release-2/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/machinome-release-2/postflight.mjs
python videos/machinome-revolutions-v2/serve-review.py --port 8782 --directory videos/machinome-release-2
node videos/machinome-release-2/check-player.mjs /home/asa/devel/machinome/videomaker
```

The server stays in the foreground; run the player check in another terminal.
Postflight verifies the encoded MP4 and unchanged narration input, produces
WebVTT, and decodes 34 review frames. Its report deliberately leaves visual
judgment to the reviewer; the completed inspection is in VERIFICATION.md.

The commands above cannot purchase speech. Do not use build or regenerate
the ratified take. finish.mjs restores the original voice-setting property
order (the existing cache hashes JSON order), sets the continuous model
clock and measured pawl phases, and preserves the raw listening assets.

`CrankStroke` and `ThisScene` in movie.py own the literal narration they
show. scene_source.py reads these declarations without executing the movie;
narration.py includes those words in the one continuous performance. The
same reader extracts the complete classes for the source panels. The
source tests verify this link and the exact approved script.

## Boundaries

The source and simulation are local development artifacts, not a published
URL promise. The museum photo and manuscript scan are private research
downloads, with native picture rights deliberately unset. Their requested
on-frame source labels and watermark remain. Clear audiovisual reuse rights
before publication. The Python logo is the unchanged official PSF asset.

The model, viewer and Videomaker are unchanged. Model source/export revision:
`5b2366460ad3ab20e3cf2682a6ed7b7ec1963e15`; its existing export records a
dirty tree, retained honestly. User editor backups and unrelated Videomaker
working records remain untouched. These provenance flags, unresolved URLs,
image rights and the production tool's distribution licence are publication
checks, separate from whether the film renders and plays correctly.

The videomaker skill supplied the cache-only production and encoded-film
inspection procedure. Original brief and review are preserved as human
records; AI direction and production decisions live separately.
