# Revoluções — estudo em português

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

9 October revision: one freshly generated continuous Leo performance,
approved first sentence, no on-screen text, and the original cut-5 direction
restored. See [direction](DIRECTION.md), [script](roteiro.txt) and
[verification](VERIFICATION.md). Portrait 1080 × 1920, 24 fps.

Delivery: [MP4](_build/study-1-pt-br.mp4), with
[optional separate subtitles](_build/study-1-pt-br.srt) and an
[upload-description draft](description.md). Verified complete film: 87.583333
seconds, 2102 frames, with the approved 85.52-second Leo v3 performance.

The opening is “A roda faz revoluções, e os humanos dão um propósito.”
The omitted object preserves the intended ambiguity. Every other word of
the original Portuguese opening and mechanism lesson is unchanged, ending
with “Uma roda, duas tarefas: cortar e avançar.” There is no making-of section.

`delivery.json` holds the unchanged approved script and revised calm delivery
directions. Eleven v3 and Leo are fixed specifications. The pilot rejected
the Multilingual v2 substitution, including `_build/leo-88s.wav`; do not
use that take. The approved performance has emotional direction by passage
and observation pauses. Its complete film stays below 90 seconds without
audio edits. A short duration alone is not a quality criterion.

Approved audio: [Leo v3, 85.52 s](_build/leo-v3-direcao-85s.wav).
Independent transcription recovers the approved words; rendering reused
this exact take without generating speech.
`speech.mjs` generates the **entire** script in one provider request, retains
the raw receipt, verifies every returned PCM sample, and seeds the native
speech cache. No splice, cut, inserted internal silence or speed change.
A repeated invocation without `--generate` only reuses that complete take.

All 17 highlights are compared with cut 5 by `verify-direction.mjs`:
same parts, equivalent translated onsets/endings and the original small
gaps. The invented whole-feed highlight is gone. The original 1.2-second
mechanism fade retains the complete machine on the same camera and pose,
covered by an incoming dark plate so it cannot leave a duplicate image.
Portrait cameras remain the only reframing adaptation. The model is unchanged.
The closing camera follows an outward arc between the same endpoints,
avoiding a straight path through the machine; its duration is unchanged.

## Reproduce

From the Leonardo repository, after stopping this study's live preview:

```sh
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/study-1-pt-br/movie.py
node videos/study-1-pt-br/speech.mjs /home/asa/devel/machinome/videomaker
node videos/study-1-pt-br/finish.mjs /home/asa/devel/machinome/videomaker
ELEVENLABS_API_KEY='' node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs speech videos/study-1-pt-br/_build/movie.json
node videos/study-1-pt-br/verify-direction.mjs
node videos/study-1-pt-br/check-closing-camera.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js --width 540
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node videos/study-1-pt-br/verify-render.mjs
cp videos/study-1-pt-br/_build/rehearsal.mp4 videos/study-1-pt-br/_build/study-1-pt-br.mp4
cp videos/study-1-pt-br/_build/rehearsal.srt videos/study-1-pt-br/_build/study-1-pt-br.srt
```

Run `finish.mjs` once per fresh Python evaluation. The empty key makes native
`speech` refuse a missing take instead of purchasing one. Render uses cached
speech and validated frames. A new audition needs explicit authorization.

For the browser continuity checks, start `videomaker live` on this movie
with the same viewer and pass its printed address to:

```sh
node videos/study-1-pt-br/inspect-motion.mjs /home/asa/devel/machinome/videomaker http://127.0.0.1:PORT
```

Generated media remains ignored. Prior deliveries are preserved in
`_build/revisions/fast-58s/` and
`_build/revisions/before-2026-10-09-direction/`.
No CAD, dependency, or other production is modified. Nothing is published.
