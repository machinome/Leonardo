# Revoluções — estudo em português

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Revised study: [MP4](_build/study-1-pt-br.mp4), 91.96 seconds,
1080 × 1920 at 24 fps, with Leo's Brazilian Portuguese narration.
[Optional subtitles](_build/study-1-pt-br.srt),
[upload description](description.md), [verification](VERIFICATION.md).
The named delivery copies are byte-identical to the renderer's
`_build/rehearsal.mp4` and `_build/rehearsal.srt`.

Commissioned on 8 October 2026: a standalone Brazilian Portuguese social
video adapted from the opening and mechanical lesson of
`machinome-release-5`, ending after “one wheel, two jobs”. Leo Antonio is
the voice selected in `machinome-release-4-pt-br/voice.json`.

1080 × 1920 portrait, 24 fps. New portrait cameras and a minimal dark stage;
no code, Studio scene, brand or closing invitation. The original script is
preserved word for word, including its first-person machine narrator, from
“A roda faz revoluções” through “Uma roda, duas tarefas: cortar e avançar.”
`delivery.json` snapshots the original Portuguese opening and first mechanical
section, with their original performance directions. No paraphrase or new hook.
Narration and titles are in Brazilian Portuguese. Subtitles remain
an optional separate SRT, as in the source film.

The production reuses cut 3's existing sawmill export, as cut 5 does.
No mechanical model is changed. The source film's phase anchors remain:
the ratchet pull is 436–438 model seconds and its return 438–440.
The description retains attribution and reconstruction limits.

From the Leonardo repository:

```sh
node videos/study-1-pt-br/prepare.mjs
PYTHONPATH=. /home/asa/devel/machinome/.venv/bin/python videos/study-1-pt-br/movie.py
node videos/study-1-pt-br/speech.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs speech videos/study-1-pt-br/_build/movie.json
node videos/study-1-pt-br/finish.mjs /home/asa/devel/machinome/videomaker
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs check videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs preview videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node /home/asa/devel/machinome/videomaker/bin/videomaker.mjs render videos/study-1-pt-br/_build/movie.json --viewer /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
cp videos/study-1-pt-br/_build/rehearsal.mp4 videos/study-1-pt-br/_build/study-1-pt-br.mp4
cp videos/study-1-pt-br/_build/rehearsal.srt videos/study-1-pt-br/_build/study-1-pt-br.srt
```

The project-owned `speech.mjs` recovers the actual original Leo recording
from cut 4's preserved provider receipt, named in `delivery.json`. It requires
that local receipt and makes no network or synthesis request. It preserves
every original PCM sample until an end cut in the pause before “Para
reconstruir”. The provider's original character timestamps are reused with
non-spoken direction tags removed. It checks text, voice and audio identity
before seeding the native speech cache. Run it BEFORE the tool's `speech`
command; the latter can purchase missing speech and must only mix this cache.
`render` uses cached audio. Generated media and evidence stay in `_build/`.
Run `finish.mjs` once after each fresh Python evaluation: it fits a continuous
model clock and a smooth opening camera orbit to the measured narration.
Nothing is uploaded or published. Prior productions and their ongoing edits
are retained. Listening review is separate from encoded/timing checks.
The rejected 58-second edit is preserved under `_build/revisions/fast-58s/`.
