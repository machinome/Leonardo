# Restore the code as the character

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot's review of the delivered second cut, 3 October 2026: both video
source panels lost the earlier class context; “How cool is that?” belongs
inside the source, not outside it. Authority: revise these scenes and rebuild.

## Change

- The first panel now shows the complete, executable `CrankStroke` class:
  narration, view, word-timed camera movement and individual highlights.
  The actual earlier crank shot uses this class's view and shot.
- The next panel shows the complete `ThisScene` class. Its full narration,
  including “How cool is that?”, is a literal, highlighted in the source.
  The actual mirror shot uses this class's code element and shot.
- Their narration literals feed the single continuous script through a
  small AST reader. No display-only transcription, comment standing in for
  speech, new synthesis chapter or fictional framework API.
- The first panel highlights one line at a time for the spoken scene,
  camera, voice, word anchor and movement. The mirror highlights its actual
  narration line, not the machinery around it.

These are ordinary Python organizational classes. The native movie still
has one `Continuous` chapter; the approved take is reused unchanged.

## Evidence before encoding

Four initial source regressions failed against the old helper functions.
All six final tests pass: complete class context, literal punchline,
simulation/camera/highlight content, exact approved narration, literal AST
excerpts, and a mutation proving that the class's words feed speech.
The five existing speech tests pass too.

Native check passes at 1920×1080, 24 fps, 17 shots and 141.75 seconds.
The first class-based native preview passes. After refining the focus cues,
the extended browser inspection passes 21 replay-identical compositions,
including all five source highlights and the full self-narration. Source
text stays inside the picture; each source sample highlights exactly one
line. The shared stage script and CSS hashes are unchanged.

Comparing evaluated movie documents, after excluding just the two source
elements and the two source shots' focus cues, gives exact deep equality.
Narration, timings, camera and model requests, every other scene and all
shared stage/style data are unchanged. No dependency or model was edited.

## Rebuild evidence

Pending final render. The original MP4, manifest, movie document and
subtitles are preserved under `_build/before-code-revision-20261003/`.
The render uses Videomaker's shot cache; changed shots and any following
shot that composites one of them must be captured again. Shared stage
changes would invalidate all shots, so the stage is intentionally unchanged.
