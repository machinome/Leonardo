# Study 1 — approved v3 performance and portrait film

Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.

## Current delivery — 9 October 2026

The pilot requested a longer silence during the mechanism entrance, explicitly
allowing this local audio edit without regenerating the approved performance.
The current `_build/study-1-pt-br.mp4` is **89.583333 seconds**, 2150 frames,
1080 × 1920 at 24 fps, H.264/AAC, without on-screen text or embedded subtitles.
SHA-256: `d1f71caf179a3d89b0a8b70ed2851229c40b991c0869572de5aff945408ddf79`.
Its own edit manifest and verification are under `_build/zoom-pause/`.
The base `_build/rehearsal.mp4` and native manifest remain unchanged below.

`pause-transition.mjs` inserts 96,000 zero PCM sample frames (two seconds,
stereo 48 kHz) at sample 1,708,000 of the finished mix. Every original sample
before and after is byte-identical, in the same order and at the same rate.
No word, breath, delivery, synthesis setting or approved raw recording changed.
No voice request or purchase was made. Independent silence detection at
-45 dB measures the target gap expanding from 35.3375–36.1372 seconds
(0.7997 s) to 35.3375–38.1372 seconds (2.7997 s).

The machine holds from 35.583333 to 37.583333. The zoom to the original
crank camera ends at 37.166667, leaving 0.416667 seconds with both camera
and mechanism still. The original 1.2-second fade is preserved inside this
move. Motion then resumes at its original rate; speech follows at 38.1372.
No phase jump or accelerated catch-up is used. Existing highlights and all
later images/cues shift by exactly two seconds, with no new highlighting.

Only 98 entrance frames were captured through Videomaker's checked browser;
2052 lossless PNGs were reused after their manifest hashes were verified.
`verify-pause.mjs` independently verifies the complete PCM insertion,
every output frame/hash/mapping, unchanged caption words and shifted timings,
2150 encoded frames, the under-90-second duration and full video decode.
Both replacement endpoints match the base images **pixel for pixel**.
Frames 892–902 are pixel-identical, proving the settled camera/model hold;
frame 910 differs, confirming motion resumes. The 12-image contact sheet
`_build/zoom-pause/encoded-transition.png`, extracted from the finished MP4,
was inspected for the fade, framing and both joins. Audio was not re-auditioned:
the approved performance is preserved rather than replaced.

The edit recipe and independent verifier preserve the base and its cache;
the native `movie.json` intentionally still describes that base. Reproduction
must finish with the pause-edit command in `README.md`, not stop at the base
render. The model, viewer, video tool and unrelated productions are unchanged.

## Approved base film — 9 October 2026

The pilot approved the 85.52-second Leo v3 audition and requested rendering.
The complete film is 87.583333 seconds: 2102 H.264 frames, 1080 × 1920,
24 fps, stereo AAC, no subtitle stream and no on-screen text.
The then-delivered `_build/study-1-pt-br.mp4` was byte-identical to `_build/rehearsal.mp4`,
12,424,856 bytes, SHA-256:
`1ef4847a8ea0246a4ad38275008bfa22bbf774ab6fd6e042eb5a043e53812d28`.

The exact approved audio remains the complete provider performance:
`continuous-f5670ed891a3674c.wav`, request `g2t6jQk8ABrawMG2rkCn`,
Leo `EbiSUflQjzm4g7S895SC`, `eleven_v3`, stability 0.5 and similarity 0.75.
SHA-256: `f237b17e6bc5be12732a8bab81c684bad52903f4212c555cb79bfcac7b582ec6`.
No speech requests, audio cuts, phrase patches or speed changes were made
for this render. Native mixing adds the declared 0.6-second lead-in,
resampling and loudness normalization. The complete take fits before the
closing image and fade. The agent has not listened; the pilot approved the
take, and independent transcription previously recovered all 175 words.

`verify-direction.mjs` passes all 17 original cut-5 highlight targets and
translated anchors, the approved opening, absence of text elements and
byte-for-byte provider PCM preservation. Preview verified 154 frames,
17 highlights, four transition/fade checks and exact pixel replay.
`inspect-motion.mjs` rechecks both 1.2-second fades, synchronized camera and
model time, outgoing-image coverage and all text-free shots. Its six
closing-path images were also inspected. The preview contact sheet can
include old PNGs left by earlier passes; exact report-listed stills and
the encoded review pack, not that mixed sheet, were used for inspection.

The first encoded pass exposed a straight closing camera path through the
model, producing an unintended zoom. It is preserved under
`_build/revisions/rejected-closing-camera/`, not delivered. The replacement
keeps the camera endpoints and 6.375-second shot but uses an outward arc.
`check-closing-camera.mjs` failed on the old path and passes every one of
the 153 closing frames. The final render reused all 1949 earlier frames;
their seven shot keys and the common cache key are unchanged.

`verify-render.mjs` first rejected the old recording and then rejected the
stale closing-path render. It passes the delivery: current movie-document
hash, approved audio hash, full take extent, dimensions/rate/frame count,
under-90-second duration, external subtitle text and full FFmpeg decode.
Evidence: `_build/encoded-verification.json` and `rehearsal-manifest.json`.
All four encoded overview pages and the join samples were inspected on the
first pass; the corrected closing was inspected in the final pack:
`_build/review-packs/2a4633f6efff-1ef4847a8ea0-296c7577-997b-42f6-a01b-48bc2803a523/`.

The model export, viewer, tool and other productions are unchanged. Their
pre-existing dirty state and unresolved public URLs remain explicit in the
manifest; this is a local delivery, not a published release. Nothing was
pushed or uploaded. The workspace videomaker skill was separately updated
and integrated at `66bf15c` before production, covering emotional direction
by passage and preservation of approved voice, model, text and performance.

## Historical delivery — 8 October (superseded)

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
