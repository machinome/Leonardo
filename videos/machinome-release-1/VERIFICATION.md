# Proposal 1 — verification

Checked 3 October 2026. This records a first-proposal review, not approval to
publish. The rendered source content is project commit
`b75c2781bad9`; this subsequent record does not change the film.

## Delivered encode

- File: `_build/rehearsal.mp4`.
- SHA-256: `7423b8e994b596352b580b649e4d00f0e007b477e7cc067ec8f956ebac3a2028`.
- H.264, 1280 × 720, 24 fps, 3,365 frames, 140.208333 seconds.
- AAC narration track, 140.208 seconds. No music or mechanical sound design.
- Optional subtitles: 49 cues; SRT and player VTT are available.

The current encode's evidence is in `_build/rehearsal-manifest.json` and
`_build/review-packs/7e112c2858b8-7423b8e994b5-0166b6bc-a85e-4671-895b-a578efea882d/`.
These generated files are ignored, not committed.

## Automated checks

The final Videomaker preview passed all 14 shots, including pixel proofs for
the eight mechanical highlight cues. The project inspection passed seven
continuous-camera/model-time boundaries and seven key compositions, text/logo
bounds, exact source identity, and identical pixels after seeking away and back.
The displayed film source has SHA-256
`6a4803cb909f319407f1c1909a8b356b5963b46af53188f22d62381bf33f5bf7`.

The review player passed seven scene seeks, 49 subtitle cues, byte-range
delivery, its linked artifacts, and desktop/narrow layout checks. Its report
and screenshots are in `_build/player-report.json` and `_build/`.

Python formatting/style and Node script syntax checks passed. Authored-file
whitespace checks passed; the two vendored font licence notices retain their
original bytes. The original brief and mechanical sources were not edited.

## Visual sampling

The agent inspected these full-resolution frames decoded from the final MP4:
19, 432, 1332, 1800, 2262, 2484, 2592, 2700, 2952 and 3276.
They cover the opening wheel, full reconstruction, highlighted rope drive,
restored assembly, model source, film source, self-referential narration,
technology ring, return dissolve and closing invitation.

The inspected frames have the intended dark ground, legible text, visible
mechanical emphasis and unclipped focal content. The self-referential scene
shows the literal current Python narration and highlights that sentence.
The ring includes JSCAD, not the separate experimental FreeCAD path. Camera
continuity also has automated endpoint evidence; these stills are not a
claim that the complete film was watched in motion.

## Remaining review

Audio was checked through duration and provider alignment, **not listened to**.
Human review of delivery, pacing and full motion remains. The MP4 is a 720p
proposal; the source composition is 1080p. Existing input-export dirty-state
provenance, unresolved public URLs and the universal open-source line's
licensing scope remain as documented in [README.md](README.md) and
[description.md](description.md). No publication, upload or push occurred.
