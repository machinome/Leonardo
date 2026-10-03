# Machinome release — proposal 2

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Status: the revised narration has been generated as one continuous take.
The visual second cut has not been built. Listening review is pending.

- [Listen to the full performance](index.html): **2:19.44**, Jessica / Eleven v3.
- [Lossless WAV](_build/narration.wav) · [subtitles](_build/captions.srt).
- [Actual narration source](narration.py) · [timing and provenance](_build/narration-manifest.json).

- [Original brief](brief.md), verbatim snapshot of
  [the canonical brief](../machinome-release.md).
- [Review of proposal 1](review-1.md), verbatim snapshot of
  [the canonical review](../machinome-release-review-1.md).
- [Narration-continuity assessment](NARRATION.md).
- [First proposal and its rendered cut](../machinome-release-1/README.md).

The review supersedes the brief where it changes it. Preserve these human
records exactly, including spelling; corrections belong in a separately
reviewable screenplay, not in the supplied brief or review.

## The continuous take

The pilot accepted the full-take regeneration trade-off on 3 October 2026.
`narration.py` assembles eight source paragraphs into **one** `Narration`;
`speech.mjs` submits the whole 1,694-character text in **one provider request**.
The review player is the raw take, with no cuts, normalization, time stretching
or inserted gaps. Paragraphs are textual organization, not synthesis units.

The revised entrance, technology list, opening and closing use the review's
words. "Five hudreds..." is rendered as "Five hundred years ago"; capitalization
is normalized for names. The brief/review files remain unchanged. The existing
mechanism lesson and permitted film-source explanation are retained. The
rejected "Here is one of its relationships" and "Different ways" additions
are absent. The visual-only OpenSpec/Three.js ambiguity below does not add or
substitute any spoken name.

Voice settings and the previously approved pronunciation dictionary are the
same as proposal 1. The exact paid response is retained before interpreting
it, so an interrupted postprocessing step need not synthesize again. Cached
speech is compatible with Videomaker's chapter cache under chapter ID
`continuous`. The later movie should import `lines` from `narration.py` into
one chapter and use the same audio settings and build directory. Its scenes
remain independent visual shots, all timed from this take. No old shot times
were transferred to the new narration.

There are 29 uniquely resolved phrase anchors and 52 subtitle cues. Every
timestamp is relative to the raw recording; the opening wheel's deliberate
silent lead-in is still a film-placement decision, not silence baked into
the take. Listening is required to judge the delivery and pronunciation;
provider alignment alone does not establish either.

## Reproduce and listen

From the Leonardo repository root:

```sh
/home/asa/devel/machinome/.venv/bin/python videos/machinome-release-2/narration.py
node --test videos/machinome-release-2/speech.test.mjs
node videos/machinome-release-2/speech.mjs /home/asa/devel/machinome/videomaker --check

# Reuse the take. Without --generate, this cannot make a paid request.
node videos/machinome-release-2/speech.mjs /home/asa/devel/machinome/videomaker

# Only when deliberately generating a missing take:
node videos/machinome-release-2/speech.mjs /home/asa/devel/machinome/videomaker --generate

python videos/machinome-revolutions-v2/serve-review.py \
  --port 8782 --directory videos/machinome-release-2
```

Open http://127.0.0.1:8782/. The server is local; nothing is uploaded.
`--generate` also reuses an existing take. There is no automatic retry of a
failed paid request and no overwrite option for its cached audio. Preserve
`_build/audio/`; exact reproduction uses its selected bytes, not a new seed run.

After starting the local server, check its player with:

```sh
node videos/machinome-release-2/check-player.mjs /home/asa/devel/machinome/videomaker
```

The speech is generated media, kept in ignored `_build/`. The original first
cut, its audio and both human-written records are unchanged. Audio-only work
does not resolve the first proposal's public URLs or publication/rights checks.

## Verification

The complete WAV decodes as 24 kHz, mono, 16-bit PCM: 3,346,560 samples,
139.44 seconds. Its SHA-256 is
`00ab8fafdfe778f546150392d4673d7e00a4f84abb9f631700414dba92974e86`.
The review copy is byte-identical to the cached provider take. Signal checks
report a peak of -0.3 dBFS and mean volume of -19.0 dB; there was no mastering
pass. Five sub-threshold intervals longer than one second were detected at
-45 dBFS, the longest 1.217 seconds; these are in the generated audio, not
editorially inserted gaps. They have not been removed.

Four script/anchor tests pass. Reusing the cached take also passed with network
access disabled in the process. The browser passed nine seek/play checks,
captions, literal transcript and download links, with no page errors or narrow
layout overflow; desktop and mobile screenshots were visually inspected.
Python formatting/style and authored-file whitespace checks pass. Reports,
alignment, original provider response and screenshots are retained in `_build/`.
These checks do not constitute a listening review or pronunciation approval.

## Direction carried forward

The first proposal mishandled the reveal: it omitted the spoken import,
covered Machinome's entrance with explanatory copy, added unrequested
narration, and exposed the current narration before the intended meta reveal.
The next cut must follow the supplied lines and preserve that sequence.

The review requires:

- A still wheel accelerating before narration, and the revised opening.
- Context parts opaque where useful, one highlighted component at a time,
  shown normally before and after its speech-synchronized highlight.
- A transparent ratchet when the winding rope is the subject.
- Actual historical drawing and museum images, moving/fading on the relevant
  words, with source identification; provenance and reuse rights checked.
- The supplied spoken import and Machinome introduction as its entrance;
  real surrounding class/source context, not isolated code-shaped captions.
- Simulation/camera/highlight code first; the current scene's narration
  code only at the later self-referential reveal.
- The supplied open-source list, staged around M, and the driven-wheel
  transition into the revised closing lines.
- One continuing vocal performance through the film.

One textual ambiguity remains for the next screenplay: the animation names
"openspec" as the incoming item, while the spoken list names OpenSCAD and
does not name OpenSpec; the visual sequence also starts with Three.js,
which is not in the spoken list. Preserve the review as written and resolve
that mapping with the pilot before inventing a replacement or extra line.
