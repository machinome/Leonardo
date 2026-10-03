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

## Completed rebuild

Rendered and verified on 3 October 2026 from production commit
`8bc6a70a2ca7936fb5259a91e4a517b051e54d3f`.
Current output: `_build/rehearsal.mp4`, 20,246,699 bytes, SHA-256
`18b0830df9c442cb23ff8d19794d721afdc603e1aad9dc04431e43555dc9be3f`.
The format remains 1920×1080, 24 fps, 3,402 frames, 141.75 seconds.

Videomaker's incremental render reused **14 of 17 shots**, 2,690 frames.
It recaptured only `behind-the-film` (240 frames), `mirror` (115) and
`open-source` (357), whose incoming dissolve contains the outgoing mirror.
The 14 reused shots retain their exact previous keys and cache generations;
the common key and both shared stage hashes are unchanged. This proves the
partial-rebuild behavior on this film, not just from the documentation.

The approved raw narration hash is unchanged. Independently extracting the
AAC packets from the previous and new MP4 gives the same SHA-256:
`bf1ba381899498f5107695085adc9153cef4c0b37ca346ca462895c0bc7edae0`.
No listening reapproval or paid generation was needed; no new independent
listening review is claimed. All 51 external captions keep their exact text
and +3-second offset from the approved performance.

The final native preview passes, as do postflight and all nine player
seek/play checks, subtitle loading, byte-range delivery, links and desktop/
narrow layouts. Six source tests, five speech tests and PEP 8 checks for
the new source-reader/test modules pass. The final follow-up commit only
shortens three reader docstrings and records this evidence; it changes no
movie input.

Inspected full-resolution frames decoded from the new MP4: the complete
classes at 101 and 109.5 seconds, then each of the five source highlights
and the punchline. Additional decoded samples are in
`_build/encoded-code-revision/frame-01.png` through `frame-06.png`, selected
at zero-based frame indices 2455, 2481, 2504, 2530, 2570 and 2676.
Every sample keeps the complete class context visible, and the last shows
the full literal narration still highlighted at 111.5 seconds.
The native encoded review pack also completes at
`_build/review-packs/f8a113c9ff58-18b0830df9c4-0d3e0e1a-e209-47d1-93c4-ee2138dc1657/`.

The original MP4, manifest, movie document, subtitles, decoded-frame set
and player evidence remain under `_build/before-code-revision-20261003/`.
Nothing was published. The original image-rights, public-link, tool-licence
and provenance publication checks remain unchanged.
