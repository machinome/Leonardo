# Machinome release — proposal 1

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

**Revolutions** — a narrated, 2 minute 20 second first proposal from
[the release brief](brief.md). Machinome speaks as the
machine, framework, foundry, agent and film. The visual world is dark,
with warm timber, amber attention and real Python source.

- [Watch the proposal](index.html)
- [MP4](_build/rehearsal.mp4) · [optional subtitles](_build/rehearsal.srt)
- [Visual direction and sequence](DIRECTION.md)
- [Contact sheet](_build/storyboard.jpg)
- [Film declarations and narration](movie.py)
- [Stage](stage.jsx) · [stage styling](stage.css)
- [Upload-description draft](description.md)

The declarations target 1920×1080 at 24 fps. The first review encode is
1280×720 at the same frame rate, with complete narration and no burned
captions. Generated media, speech caches and proofs live in ignored
`_build/`. Keep them to reproduce this exact voice; synthesis can vary.

## Reproduce

Run from the Leonardo repository root, using the explicit workspace tools:

```sh
node videos/machinome-release-1/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python \
  videos/machinome-release-1/movie.py

# Generates only missing takes; makes paid requests when they are absent.
node videos/machinome-release-1/speech.mjs \
  /home/asa/devel/machinome/videomaker

# Match the two wheel reveals to the measured speech clock.
node videos/machinome-release-1/finish.mjs \
  /home/asa/devel/machinome/videomaker

node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check \
  videos/machinome-release-1/_build/movie.json \
  --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview \
  videos/machinome-release-1/_build/movie.json \
  --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render \
  videos/machinome-release-1/_build/movie.json --width 1280 \
  --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

`prepare.mjs` embeds the unchanged, locally bundled fonts. `movie.py`
evaluates the Python declarations. `speech.mjs` uses the pronunciation
dictionary previously approved for Revolutions, and records the actual
provider request, dictionary version, audio checksum and alignment. It
refuses a cache made with another dictionary. No credential enters the
sources, stage or manifest. `finish.mjs` changes only generated model-time
endpoints so wheel-only and full-machine images agree during their two
visibility dissolves; it never modifies the model or export.

Use the project speech adapter for new takes: the normal tool command
does not currently forward the approved dictionary. `render` reuses
cached speech and makes no synthesis requests. After any declaration
edit, reevaluate and run `finish.mjs` before preview/render.

To serve the player with video seeking, from this directory:

```sh
python ../machinome-revolutions-v2/serve-review.py --port 8781 --directory .
```

Open http://127.0.0.1:8781/. The server is local; it publishes nothing.

## Evidence and remaining review

The first preview exercised all 14 shots with the real Viewer API 29
bundle: replay, camera placement, arrows, highlights, speech-based source
emphasis, fades and the live source/model reframe passed. Selected frames
were visually inspected, then the wheel framing, code size and phase
continuity were refined for the render. The generated render manifest
and review pack are the authoritative encoded-film evidence.

The project inspection also checks all seven camera/model boundaries in
the initial continuous take and seven key compositions. It measures the
custom text and logo boxes, verifies the shown film-source checksum, and
compares pixels after seeking away and back. Reproduce it with:

```sh
node videos/machinome-release-1/inspect.mjs \
  /home/asa/devel/machinome/videomaker \
  /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

Audio was checked by cached waveform duration and provider alignment,
not by a listening review. The film is voice only; music and mechanical
sound design are not present. The source is a proposal, not a ratified
release or a promise that every filmed development API is published.

The input model export records revision
`5b2366460ad3ab20e3cf2682a6ed7b7ec1963e15` **and a dirty source tree**.
The actual selected model-code file matches that revision. Videomaker
also has pre-existing untracked working notes. Those facts remain in
the build records; no provenance is rewritten to claim a clean release.

Public source/simulation addresses are unresolved. Videomaker records no
selected distribution licence, so the brief's universal open-source line
needs a scope/licensing decision before publication. The identity artwork
also has its own rights boundary. Details are in the description draft.
No upload, push, dependency change or mechanical-model edit is part of
this proposal.
