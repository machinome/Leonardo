# Continuous narration — technical assessment

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Assessed 3 October 2026 against proposal 1 at Leonardo
`ebf6c01fa57bdd108073b4f619032cdac27123c4`, and Videomaker
`a2b770d919faf150b57a92e3bbadaf8c91b57647`.
This is a recommendation, not an implemented tool change or listening test.

Implementation update: the pilot accepted the one-take approach and its
trade-off. The first revised script was generated in one request on 3 October
2026: 1,694 characters, 139.44 seconds, 29 measured anchors. After listening,
the pilot corrected "five hundred years" to "five centuries" and restored
"And the best part is: this is all open source!". A new single request made
the current 1,712-character, 136.40-second take, retaining the earlier audio.
See [README.md](README.md)
for the listening copy and reproduction. The assessment below is retained as
the decision's original evidence; its "no new speech" statement describes
that assessment, not the subsequent production step. The pilot subsequently
ratified the corrected performance and requested the video build. The film
reuses those exact cached bytes; the unmastered listening copy is now at
[narration.html](narration.html). No dependency was changed.

## What produced the discontinuity

The pilot reports disconnected moods. The generation records establish a
plausible cause: six independent Jessica / `eleven_v3` requests, one per
chapter. They are not six portions of one generated performance.

| Take | Characters | Recorded audio duration | Gap before this file |
| --- | ---: | ---: | ---: |
| encounter | 1,138 | 92.88 s | — |
| film-source | 116 | 9.04 s | 1.4533 s |
| this-scene | 58 | 4.00 s | 0.4183 s |
| open-wheel | 146 | 11.04 s | 1.3750 s |
| intention | 80 | 5.84 s | 1.8350 s |
| invitation | 102 | 7.84 s | 1.9100 s |

Gaps are computed from the cached audio manifest's placement offsets and
file durations; they exclude any silence already inside the recordings.
They are additional editorial pauses, distinct from shifts in performance.
The first 92.88 seconds are already one take, so a mood change within that
span cannot be attributed to a request boundary.

Evidence: `../machinome-release-1/_build/audio-manifest.json`, the six
`audio/*.wav.json` request records, and `../machinome-release-1/speech.mjs`.
Videomaker's `src/speech.mjs:speechRequest` explicitly omits neighboring
text for v3. Every actual request contains text, model, voice settings,
seed and pronunciation dictionary; none contains prior audio context.
The editorial `audio.direction` ("Curious, intimate museum guide; a machine
speaking.") is not passed by that request builder. It is not an effective
performance instruction merely because it exists in the movie document.

## Recommended production approach

Generate the entire approved script as **one take**, then direct the visuals
against its measured speech. Keep the current voice/model and pronunciation
dictionary for the first comparison so the generation boundary is the main
variable. One take allows the model to condition delivery on the whole arc;
it does not guarantee a successful performance, so listen before filming.

1. Assemble the reviewed narration in order, preserving the pilot's lines.
   Do not add connective explanation outside the granted mechanism lesson.
2. Make one `/v1/text-to-speech/{voice}/with-timestamps` request. Save the
   lossless PCM/WAV, exact request, pronunciation dictionary/version, provider
   alignment and checksum. Preserve the approved bytes instead of expecting
   regeneration with the same seed to produce the identical performance.
3. Listen to the whole take before the expensive visual render. Check the
   entrance, the meta surprise, the open-source excitement, the return to the
   wheel and the final invitation as one speaker's developing thought.
   Natural breaths and changes of energy should remain; continuity does not
   mean monotone or uninterrupted speech.
4. Anchor shots, camera moves, images, single-part highlights, source words
   and the technology arrivals to that take's alignment. There is no need
   for an independently synthesized segment at a visual scene boundary.
5. Keep the approved audio continuous through those boundaries. Generate
   subtitles from the same alignment. Start the film's stationary/accelerating
   wheel before the first word with one deliberate lead-in; do not create
   padding between every scene. Do not stretch speech to fit the old edit.

The first cut's narration totals 1,650 characters when joined with two
newlines between chapters. The reviewed screenplay must be counted again,
but there is substantial room under v3's documented **5,000-character
per-request limit**. This film does not presently need a long-form stitching
architecture. [ElevenLabs model limits](https://elevenlabs.io/docs/overview/models)

The timestamp endpoint returns character alignment alongside the audio;
these measured times can continue to drive the existing phrase and word
cues. A fixed seed is best-effort, not a reproducibility guarantee.
[ElevenLabs timestamp endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)

## Fit with the current tool

Videomaker already owns narration at the chapter level and supports many
shots in that chapter. For this film, use one `Chapter`, one `Narration`,
and all of its visual shots. Split the script into named source strings if
that improves readability, then assemble them once for the one narration;
separate Python classes are not required for every screen composition.
The meta scene must still show literal film source, including its actual
narration text, not a fabricated chapter that is no longer used.

All cues then refer to that one narration's clock. The full opening and
closing sentences are unique anchors; the repeated phrase "The wheel makes
revolutions" alone is ambiguous and the resolver correctly refuses it.
Use the longer unique phrases without changing the supplied wording.

The movie document supports `speechOffset` for the silent opening. The
current Python declaration compiler does not expose it: it emits only a
chapter's narration, elements and shots. A project-side evaluation step can
set the documented field explicitly before resolution, without altering
speech or pretending an unsupported Python keyword exists. If the pilot
wants a public Python declaration for it, that is a separate Videomaker
change, not necessary for deciding the narration strategy.

Local references: Videomaker `docs/declaring-a-movie.md` ("A chapter"),
`docs/movie-document.md` ("Chapters", "Anchors", "Resolution"),
`python/machinome_movie/movie.py`, `python/machinome_movie/evaluate.py`,
and `src/speech.mjs`. A shared performance spanning separately authored
chapters could be a future tool capability, but is not required here.

## Why not stitch or crossfade the existing takes?

The current ElevenLabs request-stitching guide explicitly excludes
`eleven_v3`. Adding `previous_text` or request IDs to this v3 pipeline is
not a documented continuity solution. A different compatible model could
use that route for longer films, but changing voices/models is unnecessary
for this experiment. [ElevenLabs request stitching](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching)

Joining the old files, matching their loudness, or crossfading a pause cannot
give the model the missing performance context. More scene-specific emotion
tags also do not establish continuation. First test a coherent full-script
take; use any delivery controls sparingly and verify what is actually sent.

Trade-off: a narration edit now invalidates the whole take and its alignment.
Finish the wording before synthesis, retain the selected take, and regenerate
the affected timing/captions if a new take is chosen. Visual-only changes
can reuse the approved audio. No new speech, rendering or dependency changes
were performed for this assessment.
