# Revoluções — estudo em português

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

9 October revision: one freshly generated continuous Leo performance,
approved first sentence, no on-screen text, and the original cut-5 direction
restored. See [direction](DIRECTION.md), [script](roteiro.txt) and
[verification](VERIFICATION.md). Portrait 1080 × 1920, 24 fps.

Delivery: [MP4](_build/study-1-pt-br.mp4), with
[optional separate subtitles](_build/study-1-pt-br.srt) and an
[upload-description draft](description.md). Current complete film: 89.583333
seconds, 2150 frames, with the approved Leo v3 performance and the pilot's
requested two-second extension of the silence before the mechanism explanation.

The opening is “A roda faz revoluções, e os humanos dão um propósito.”
The omitted object preserves the intended ambiguity. Every other word of
the original Portuguese opening and mechanism lesson is unchanged, ending
with “Uma roda, duas tarefas: cortar e avançar.” There is no making-of section.

`delivery.json` holds the unchanged approved script and revised calm delivery
directions. Eleven v3 and Leo are fixed specifications. The pilot rejected
the Multilingual v2 substitution, including `_build/leo-88s.wav`; do not
use that take. The approved performance has emotional direction by passage
and observation pauses. The only later audio edit is the explicitly requested
silence extension; every original PCM sample is preserved. The complete film
stays below 90 seconds. A short duration alone is not a quality criterion.

Approved audio: [Leo v3, 85.52 s](_build/leo-v3-direcao-85s.wav).
Independent transcription recovers the approved words; rendering reused
this exact take without generating speech. The raw take remains immutable.
`speech.mjs` generates the **entire** script in one provider request, retains
the raw receipt, verifies every returned PCM sample, and seeds the native
speech cache. No splice, cut, inserted internal silence or speed change.
A repeated invocation without `--generate` only reuses that complete take.
The separate `pause-transition.mjs` makes the authorized silence edit to the
finished mix, not to this provider recording or its cache/receipt.

All 17 highlights are compared with cut 5 by `verify-direction.mjs`:
same parts, equivalent translated onsets/endings and the original small
gaps. The invented whole-feed highlight is gone. The original 1.2-second
mechanism fade retains the complete machine on the same camera and pose,
covered by an incoming dark plate so it cannot leave a duplicate image.
Portrait cameras remain the only reframing adaptation. The model is unchanged.
The closing camera follows an outward arc between the same endpoints,
avoiding a straight path through the machine; its duration is unchanged.

The mechanism entrance now begins inside the silence after “Vou mostrar como
ela funciona.” The machine holds while the camera moves for 1.583 seconds,
with the original 1.2-second transparency fade. The camera then settles for
0.417 seconds before the mechanism resumes its original unhurried speed;
speech resumes later. No new highlights or words were introduced.
Only 98 entrance frames were captured; 2052 verified lossless PNGs were reused.
The unchanged 87.583333-second base remains `_build/rehearsal.mp4`; its native
manifest still describes that base, not the revised delivery. The final edit
has its own `_build/zoom-pause/manifest.json` and `verification.json`.

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
node videos/study-1-pt-br/pause-transition.mjs
node videos/study-1-pt-br/verify-pause.mjs
# Inspect the encoded transition before replacing the local delivery.
cp videos/study-1-pt-br/_build/zoom-pause/study-1-pt-br.mp4 videos/study-1-pt-br/_build/study-1-pt-br.mp4
cp videos/study-1-pt-br/_build/zoom-pause/study-1-pt-br.srt videos/study-1-pt-br/_build/study-1-pt-br.srt
```

Run `finish.mjs` once per fresh Python evaluation. The empty key makes native
`speech` refuse a missing take instead of purchasing one. Render uses cached
speech and validated frames. A new audition needs explicit authorization.
When the approved base already exists, run only the two pause commands and
the reviewed delivery copies. Passing explicit tool and viewer paths followed
by `--check` checks timing and assets without capture or encoding. This
intentionally targets the exact approved base hash; it is
not an automatic adaptation of an arbitrary new base or changed model.

For the browser continuity checks, start `videomaker live` on this movie
with the same viewer and pass its printed address to:

```sh
node videos/study-1-pt-br/inspect-motion.mjs /home/asa/devel/machinome/videomaker http://127.0.0.1:PORT
```

Generated media remains ignored. Prior deliveries are preserved in
`_build/revisions/fast-58s/` and
`_build/revisions/before-2026-10-09-direction/`.
No CAD, dependency, or other production is modified. Nothing is published.
