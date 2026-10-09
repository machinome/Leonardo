# Pilot corrections — 9 October 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Current authority — v3 restored

The pilot approved the 85.52-second v3 take below ("great") and then
requested rendering. Reuse this exact approved audio; no new synthesis.
The audio-only restriction below records the preceding audition task and
is now superseded by that explicit render request. Preserve the corrected
text-free portrait staging, cut-5 highlights and gradual mechanism reveal.

Delivered on 9 October: `_build/study-1-pt-br.mp4`, 87.583333 seconds,
1080 × 1920 at 24 fps, using that unchanged take. See `VERIFICATION.md`.
Encoded review exposed a closing camera path through the machine's centre;
only that path was corrected to an outward arc with the same endpoints and
timing. A distance check failed on the old path and passes all 153 closing
frames. The other 1949 frames were verified cache hits. No speech was generated.

The pilot explicitly rejected changing the synthesis model. Eleven v3,
Leo and the approved words are fixed specifications. The Multilingual v2
take described below is rejected, not a completed correction. Never use it.
`speech.mjs` and `check-cadence.mjs` now enforce the original model and voice;
generation also enforces original stability 0.5 and similarity 0.75.

The new request is AUDIO ONLY: one whole take near 90 seconds, never over,
with reflection at the opening, restrained historical admiration, warmth in
the ancestry passage, an explicit transition into clear patient explanation,
and restrained satisfaction at the conclusion. Observation pauses support
the mechanical explanation. Do not render images, splice, accelerate or
stretch audio, change the words, or substitute another model. Actual spoken
performance remains for the pilot to hear; measurements do not prove emotion.
`delivery.json` contains the exact inline directions sent to the provider.

Selected v3 candidate for this request: `_build/leo-v3-direcao-85s.wav`,
85.52 seconds, one whole provider performance; request `g2t6jQk8ABrawMG2rkCn`.
SHA-256: `f237b17e6bc5be12732a8bab81c684bad52903f4212c555cb79bfcac7b582ec6`.
Its non-silent duration is 60.91 seconds versus 61.32 in the approved
reference; detected pauses total 24.61 versus 28.17 seconds. The four
explanatory sections retain 92–97% of the reference's time. Every PCM sample
is preserved; peak is -1.11 dBFS with no full-scale clipped samples.

The 90-second upper limit is hard. The earlier 86-second lower bound was an
agent-authored heuristic, not a pilot requirement; the pilot explicitly says
emotion and observation time matter more than hitting an exact number.
The checker now keeps that lower-band miss visible as a warning, retaining
all per-section, pause and non-silent-duration checks. This candidate is
85.52 seconds, not a claimed 90-second take. No padding was added to satisfy
the heuristic. Five whole v3 attempts in this request lasted 81.44, 82.80,
85.52, 80.80 and 76.48 seconds. Only the 85.52-second candidate is selected.

No images, previews, mixes or movies were rendered for this audio-only
request. Older resolved timing, narration mix and MP4 files remain stale;
do not confuse them with the selected raw WAV. The agent has not listened
to the performance; duration and transcript checks cannot certify emotion.

Independent Whisper large-v3-turbo transcription, without a script prompt,
recovers all 175 approved words after ignoring punctuation and orthographic
a/à. Small and medium recognizers had transcription disagreements, retained
in their own reports; the final recognizer resolves them, including Vinci,
tora and recolhe. No voice-generation model was changed during recognition.
Full WAV decode and FFprobe confirm mono 24 kHz PCM, exactly 85.520 seconds.

## Earlier production record (superseded where noted)

The original film is the editorial authority. The study adapts its framing
to portrait and ends at “one wheel, two jobs”; it does not invent a new lesson.

The pilot approved “A roda faz revoluções, e os humanos dão um propósito.”
Do not reintroduce “ela”: the English “it” may refer to the wheel making
revolutions, not only to the wheel. All remaining spoken words stay intact.

The pilot explicitly requested a fresh **whole** voice take. Never replace
only the first sentence or splice narration. Preserve Leo's original calm,
thoughtful direction; do not speed up speech to target a short duration.
Frame capture is the expensive operation where valid caching is appropriate.

The pilot rejected the fresh 77.60-second take: it lost observation time.
Measured with the same silence detector, the original 89.49-second excerpt
has 28.17 seconds of pauses, versus 16.97 in the rejected take. This is timing
evidence, not an assessment of emotion or a substitute for listening.
Keep that rejected take under `_build/revisions/rejected-77s/`.
The next take is an audio-only audition. Preserve all approved words and
obtain listening approval before any frame rendering. Do not force the
under-90-second goal by rushing the explanation.

An attempted stronger-tag take (receipt `tQDxOGk9NK9sDAZXhhB4`, 77.04 seconds)
failed the terminal-alignment check: the last words have zero-duration
timestamps beyond the PCM end. Retain its provider receipt, but do not use
it or bypass the check. The replacement uses simpler calm, measured delivery
directions throughout, with the same voice, model and spoken text.

Replacement audition: `_build/leo-audition-76s.wav`, 76.32 seconds, generated
as one complete performance. Its PCM is byte-identical to the provider's
receipt. The same detector finds 30 pauses totaling 17.61 seconds; it still
does not recover the original's observation time. Do not mark this as a
successful cadence correction or render it automatically. It has not been
listened to by the agent. `_build/audio-audition-comparison.json` records the
three measured takes. The approved film remains unchanged.

## Completed narration correction — 9 October

The pilot rejected further short auditions and requested a properly completed
take, not more broken samples to test. The selected whole take is now
`_build/leo-88s.wav`, also `_build/leo-continuous.wav`: 88.142958 seconds.
Same Leo voice ID, with `eleven_multilingual_v2` replacing v3 so native SSML
pauses can be directed reliably. Synthesis settings and the exact SSML are
in `delivery.json`; native speech speed is 0.88. No audio post-stretching,
cuts, splices or added internal silence. Every PCM sample matches the receipt.

SHA-256: `1154c88bf33fd87bac67a4269ef614c33a884115880ba80d8cff66c367b6a8d5`.
Provider request: `BqXURm1CC19Xx2PZmWKi`.
Silence is 28.134327 seconds versus 28.172823 in the approved reference.
Non-silent duration is 60.01 versus 61.32 seconds. Mechanical sections are
96–106% of their original durations. `check-cadence.mjs` passes this take
and rejects the known bad 77.60-second take.
Local Whisper small, without the script as a prompt, independently recovers
all 175 words (ignoring punctuation and orthographic a/à). Evidence is beside
the cached audio as `.whisper.json`; the agent has not listened to the audio.
An attempted hosted transcription returned HTTP 401; local verification
replaced it, without changing credentials or requesting more permissions.

The movie is retimed to 89.875 seconds. Only the closing visual hold is
0.3 seconds shorter (2.2 instead of 2.5); the complete audio fits. All 17
original highlight anchors pass. Both 1.2-second fades pass camera/pose,
opacity, outgoing-view coverage and no-text checks at native preview size.
The prior apparent coverage mismatch was caused by the scaled iframe; native
pixel comparison is exact. Images were inspected, but no new MP4 rendered.
The pilot asked whether those images were part of narration; they are not.
The additional preview was stopped and no frame-by-frame render started.
`VERIFICATION.md` and the existing MP4 still describe the old delivered film,
not this corrected audio. Finish visual preview/render only when continuing
the movie task; do not present the old MP4 as containing this new take.

The frame contains only the model: no heading, historical subtitle,
reconstruction label, burned caption, logo or closing text. Reconstruction
limits and credits stay in the upload description, outside the film.

Restore the original 1.2-second live fade after “Vou mostrar como ela
funciona”. Keep the old complete machine, ghost context and detailed
mechanism on the same camera and model time throughout. Fade in the opaque
background plate, ghost and mechanism together. Cover the old machine after
the fade; otherwise a second model survives behind the moving view.

Remove the invented whole-feed highlight on “Mas a tora também precisa
avançar”. Audit all other cues, not just those the pilot happened to name:

- Start the opening orbit on “projetou”, equivalent to “designed”.
- Show water and channel in the drive view, as in cut 5.
- Highlight the wheel on “roda gira” and the shaft on “este eixo”.
- End the connecting-rod highlight before “transformam esse giro”.
- Preserve the original small gaps before successive highlights.
- Light the returning pawl only through “enquanto a primeira retorna”.
- Start the winding highlight on “enrola”, not “Esse pequeno passo”.
- Start the first-rope highlight on “para baixo e para o outro lado”.
- Start the compound-shaft highlight on “um eixo composto”.
- Keep the whole second-rope path, then light the timber only until
  “em direção à lâmina”, clearing it before the conclusion.
- Let the returning whole-machine camera move through the conclusion.

`verify-direction.mjs` compares all 17 highlighting intervals with cut 5,
including their exact part paths and translated anchors. `inspect-motion.mjs`
checks the two fades in the browser, synchronized cameras/poses, coverage of
the outgoing model and absence of text in every shot.
