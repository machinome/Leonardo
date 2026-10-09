# Revoluções — estudo 2, loop

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Second portrait study, commissioned on 9 October 2026. Preserve study 1 and
its exact 89.583333-second soundtrack, including the mechanism-entrance pause.
No new synthesis, change of voice/model/text, audio cut or speed adjustment.
Only remove the opening fade and replace the closing camera/visibility/motion
direction. No on-screen text. No model, viewer or Videomaker modifications.

Delivered: [study-2-pt-br.mp4](_build/study-2-pt-br.mp4), 89.583333 seconds,
1080 × 1920 at 24 fps. [Verification](VERIFICATION.md) confirms the seamless
wheel motion and byte-identical audio; study 1 remains intact.

The wheel is fully visible and already moving on the first frame. The closing
camera travels around the model to that same wheel view. The rest of the
assembly fades away, not the wheel. The isolated wheel then continues at the
opening speed. At the exclusive end its phase matches the opening modulo a
complete wheel revolution; the last frame is one normal step **before** the
first, never a duplicate held frame. This is an editorial loop, not a claim
that the sawmill automatically reloads its timber.

`loop.json` is the editable local timing recipe; `loop.mjs` resolves it against
the approved base and renders through Videomaker's checked browser. It reads
the original stage and model without modifying them. `_build/source-frames`
and `_build/shot-cache` are symbolic links to study 1's lossless frame caches.
New endpoint captures go only in this study's own `_build/frames/`; unchanged
middle frames are hard-linked after SHA-256 verification. The existing pause
is among those unchanged frames. Do not run a native full render into the
linked shot cache: its global first-frame key would invalidate the middle.
The frame count, opening replacement span and closing boundary are the fixed
cache contract for this edit. If a later study changes those ranges, use a new
build directory: never overwrite an inherited hard-linked PNG with a capture.

The base document staged under `_build/base-movie.json` is deliberately still
the original timing context. It is not the complete new edit: the two-second
pause is in the linked middle frames, and `loop.json` plus `loop.mjs` own the
loop endpoints. The new edit has its own manifest. No old manifest is relabelled.

## Reproduce

From the Leonardo repository, with study 1's verified artifacts available:

```sh
node videos/study-2-pt-br/loop.mjs --preview
node videos/study-2-pt-br/loop.mjs
node videos/study-2-pt-br/verify-loop.mjs
```

The script creates missing build links without overwriting existing paths.
The source MP4's AAC stream is copied directly, not regenerated or re-encoded.
Optional separate subtitles retain their exact bytes. The final MP4 remains
1080 × 1920 at 24 fps and below 90 seconds. See `VERIFICATION.md` for completed
checks and review evidence, and [description draft](description.md) for credits
and unresolved public URLs. Nothing is published or uploaded.
