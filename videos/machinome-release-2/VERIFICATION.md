# Second-cut production evidence

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Production sources: Leonardo commit `48484b56e40c`.
Videomaker: `a2b770d919faf150b57a92e3bbadaf8c91b57647`.
Viewer: API 29, explicit workspace bundle.
Model/export revision: `5b2366460ad3ab20e3cf2682a6ed7b7ec1963e15`.
No model or dependency was changed for this film.

## Passed validation

- The original brief and latest canonical review compare byte-for-byte with
  their cut-2 snapshots. OpenSpec's additional visual role is separately
  recorded in DIRECTION.md from the pilot's explicit clarification.
- Five narration tests pass. One chapter, one approved take, 1,712 characters.
  The raw WAV and cache both hash to
  `e1387135620e02650edea1646e315173fd3a164a16f5f740ecd5726938be8aa3`.
- The raw-audio player passes nine seek/play checks, captions, literal script,
  links, desktop and narrow-screen layout. Its copy and captions are kept
  separately from the film's padded/normalized mix.
- Native check resolves 17 shots to 141.75 seconds. It measures the final
  1920×1080 layouts and the real pinned Python source panels. Source size:
  25.3 px for the import and 20.0 px for the contextual class. The drawing's
  peak enlargement is 1.05×, the photograph's 1.14×, below the declared 1.5×.
- Native preview at 1280×720 passes 336 posed frames with 145 saved samples:
  16 highlight checks, 10 joins/head-tail fades, 15 title fades, one measured
  code emphasis and two picture checks. Replay is pixel-identical and
  invalid-camera refusal preserves the existing view.
- The project inspection checks every output instant for at most one
  highlighted component and identical camera/model states in paired views.
  It verifies the held opening, literal movie-source hash, content bounds
  and exact pixel replay for 16 selected compositions, including OpenSpec's
  incoming position and the rotating technology wheel.
- Inspected the actual preview images: individual pawl, transparent-ratchet
  rope reveal, manuscript/watermark/source, museum photo/source, Python logo,
  full code context, earlier simulation code before the self-reference, and
  clockwise technology arrangement. The source scan is not an AI substitute.

The initial archive-image dissolve failed native replay verification, and a
whole-shot fade exposed a missing incoming-picture measurement in preview.
The production uses native picture/title entrance and exit fades instead;
the complete final native preview passes. No dependency checks were removed
or weakened, and no dependency was patched.

## Encoded artifact

Completed on 3 October 2026: `_build/rehearsal.mp4` is the full narrated cut,
despite the tool's generic output filename.

- SHA-256: `a11d511ae4652cdca84e61178e45eba187af006e6100f4f02b2d789ecf9bbdd8`.
- 1920×1080, 24 fps, 3,402 frames, 141.75 seconds; 20,188,502 bytes.
- H.264 High, yuv420p progressive; AAC, 48 kHz stereo.
- One approved narration input at +3 seconds. The source and preserved raw
  copy retain the approved hash. No speech is cut, stretched or regenerated.
- All 51 caption cues match the approved text and timing shifted by exactly
  three seconds. SRT and WebVTT remain external, optional subtitles.
- Encoded signal inspection finds the expected opening/closing silence and
  the existing narration pauses, with no new mid-film gap.

`postflight.mjs` checks the native manifest hash, stream properties, frame
count, approved audio bytes and caption shift. It decodes 34 selected frames
from the actual MP4, with exact frame indices, timestamps and hashes in
`_build/encoded/index.json`. Reviewed the complete decoded contact sheet and
full-size frames for the pawl, rope reveal, manuscript and museum sources,
Python logo, contextual source and emphasis, earlier simulation excerpt,
self-reference, OpenSpec arrival, clockwise rotation, wheel dissolve and
closing question. This is encoded-film evidence, not just preview imagery.

The local player passes nine seek/play checks, all 51 loaded subtitle cues,
links, desktop and 390-pixel layouts, with no browser errors. HTTP byte-range
serving returns the requested 1,000 bytes with status 206. Desktop and narrow
player screenshots were inspected. Evidence: `_build/player-report.json`,
`_build/player-desktop.png`, `_build/player-mobile.png`.

The native render also completed its review pack at
`_build/review-packs/015e2cdb0942-a11d511ae465-989de1c8-c792-4924-87fe-262531e4292f/`.
Its immutable machine record is preserved; this document records the visual
review separately. No media was uploaded or published.

## Honest limits

The pilot listened to and ratified the raw narration. The agent's checks
cover text, timing, signal, provenance and playback; they do not claim an
independent listening review. The final mix is level-normalized and padded,
not the raw WAV byte stream, but its one input is the unchanged approved take.

The render records three untouched user editor/autosave files in the project,
two unrelated working records in Videomaker, and the model export's existing
dirty flag. These are retained honestly. Unresolved museum/scan audiovisual
rights, public URLs and the production tool's distribution licence are
publication gates. This local build neither clears them nor uploads anything.
