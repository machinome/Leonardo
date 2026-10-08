# Study 1 — restored original script and Leo performance

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

8 October 2026. The pilot rejected the rewritten, hurried 58-second version
and explicitly requested the original script. That rejected render and its
evidence are retained under `_build/revisions/fast-58s/`. This revision changes
only `videos/study-1-pt-br/`; existing work in other productions is untouched.

## Text and recording

`delivery.json` preserves the directed opening from cut 4's
`auditions/opening.json` and the first mechanical section of its
`delivery.json`. Removing non-spoken direction tags and normalizing whitespace
produces the exact text of `narration.py` and the readable `roteiro.txt`.
This equality was checked programmatically. No sentences were shortened,
rephrased or replaced. The first-person machine narrator is retained.
The final sentence is “Uma roda, duas tarefas: cortar e avançar.”

The revised film uses the **original Leo audio**, not another generation:

- Voice `EbiSUflQjzm4g7S895SC`, model `eleven_v3`.
- Source receipt: cut 4's
  `_build/audio/continuous-5c0fb0eadc157e2b.wav.provider.json`.
- Original request ID `6fNdExDYiSpe0v0Gy9Fl`, generated 7 October 2026.
- The original request begins with this exact directed script.
- The excerpt contains the original mono 24 kHz PCM samples 0–2147795,
  unchanged: 89.4915 seconds of the 220.32-second source recording.
- Excerpt WAV SHA-256:
  `8f315504745ecbbf66d10bace511041b19bc690155052c929b45b5c015720777`.
- No stretching, inserted internal silence, internal cuts, or regenerated
  words. The only edit to the source take is its ending, in the pause before
  “Para reconstruir”. FFmpeg silence detection at -40 dB confirms the excerpt
  ends in 0.677 seconds of silence following the last audible phrase.
- Source character alignment is retained with only non-spoken tags removed.
  A fresh alignment request was refused with HTTP 401 and was not retried.
  Timings are therefore the original provider's estimates, not independently
  verified forced alignment. No key or response secrets are recorded here.

The native film mix adds a 0.6-second lead-in, resamples and normalizes
loudness, but does not alter performance speed. The closing image continues
after the voice, with a one-second fade. Total timeline: 91.958333 seconds.

A failed new take of the rejected wording, attempted before the pilot's
explicit restoration instruction, is not used. Its raw receipt remains in
the ignored audio evidence. Recovery now runs entirely offline through the
project-owned `speech.mjs`; native speech generation is unnecessary.

The agent has not listened to the recording. The recovery proves audio and
text provenance, not human listening approval. Listening and final editorial
approval remain with the pilot.

## Picture and timing

Portrait 1080 × 1920, 24 fps, 2207 frames. Original mechanism explanation,
with the study's portrait cameras retimed to the restored performance.
The invented hook and closing slogan are removed. The opening title is
“Serraria hidráulica / LEONARDO DA VINCI”. No author/product/licence credits
appear in the film; historical subject naming and reconstruction limits
remain. Attribution is in `description.md`.

The preview at 960 × 1706 checked 162 frames, 18 highlights, five title-fade
checks and three transition checks. All passed, including deterministic pixel
replay and invalid-camera rejection. Every highlight changes the intended
part and can be restored and reapplied. Framing was inspected for the full
machine, saw linkage, holding pawl and compound winding shaft.

Model phases remain 436–438 seconds for the ratchet pull and 438–440 for
its return. No model, framework, viewer or production-tool code is changed.
Python PEP 8 and JavaScript syntax checks pass. The original text equality
and sample-preserving recovery assertions pass.

## Provenance and release limits

The existing cut-3 model export is reused, as in cut 5. Its recorded source
is `94a8562cc70e96de0cad1b85a4a7c1e092d2ed5c`, with `dirty: true`, a
1460-second posed timeline and Viewer API 29. The project and Videomaker
checkouts also contain pre-existing changes; generated manifests retain
content hashes, rather than pretending their Git heads fully describe them.

The upload description remains a draft. Public source/simulation URLs are
unresolved; `releaseReady` remains false. Nothing was published or pushed.

## Encoded delivery

`_build/study-1-pt-br.mp4` is a byte-identical copy of the new
`_build/rehearsal.mp4`; its optional SRT is copied alongside it.
SHA-256: `2aa36b10856cb29f03d1d73c1d793a311526a0ece56a12f7c452a74ce7195f5f`.

FFprobe confirms 91.958333 seconds, 2207 H.264 frames at 24 fps,
1080 × 1920, with stereo AAC at 48 kHz. File size: 13,251,516 bytes.
Full FFmpeg decode of audio and video completed without errors.
Decoded AAC peak: -1.2 dBFS; mean: -20.4 dBFS. The subtitle text matches
the restored script exactly, with no direction tags.

The encoded review pack is retained at
`_build/review-packs/29080a67d913-2aa36b10856c-b8d02439-76a6-4e72-a58b-f7bd1e7c7ad1/`.
The agent inspected chronological samples decoded from the actual MP4
in `_build/encoded-overview.jpg`, plus the closing at 88 seconds in
`_build/encoded-closing.png`. These image and technical checks do not
constitute listening approval; that limitation remains as stated above.
