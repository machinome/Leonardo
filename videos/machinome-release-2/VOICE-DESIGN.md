# An original Machinome voice

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Round 5 — correction: same line, C3 tone, Jessica benchmark

The pilot clarified that “pick from the video script” meant understand its
mood, not change the audition words. Round 4 changed the line and prevented
direct comparison. It remains as historical evidence, not an accepted
comparison or a new audition-text requirement. C3's androgynous tone is still
the selected reference. Jessica has a delivery quality the pilot prefers;
the exact reason is not established by these technical checks.

**Keep the comparison text fixed in future voice rounds unless the pilot
explicitly changes it.** Use the script to inform delivery, not to substitute
new words. The line, including punctuation, is:

> I'm Machinome, and my purpose is to enable all machines to be open source.
> What do you want to build next?

[Listen to design 5](voice-design-5.html). It presents the unchanged selected
C3 recording from design 3 first, a fresh Jessica reading of the same words,
then five new C3 readings. These return to a small performance space: an
untagged natural baseline, easy confidence, a warm invitation, genuine
interest, and a little more energy. The interpretation of the film's mood is
a capable, engaged collaborator enjoying the possibilities and inviting the
listener to make something. This is an artistic hypothesis, not an assertion
that the assistant has heard or diagnosed Jessica's advantage.

The five C3 readings retain saved identity `JoOLJ0OHRwCg8Ydjc4IF` and all
design-3 synthesis settings. Each has zero or one short direction cue for
the entire line, with no mood switches, profoundness or solemnity. Same
model, seed, speed, stability and similarity; no redesign or remix. The
pronunciation alias remains exactly as it was in the selected reference.

Jessica uses the film's existing voice ID `cgSgspJ2msm6clMCkdW9`. Her fresh
reading and C3's untagged baseline use identical request bodies, differing
only in the voice endpoint. It is clearly labelled as a fresh same-line
control, not a crop of the film or a recreation of its continuous delivery.
No Jessica traits are represented as transferred into C3. Naturalness,
cadence, warmth and perceived tone remain the pilot's listening judgment.

Six short TTS requests total: five C3 readings and one Jessica control.
No new voice-library entries, effects, cuts, pitch processing or
post-production time changes. The original selected C3 is reused byte for
byte. The film, approved narration and previous rounds remain untouched.

[Generation](voice-design-5.mjs) and [verification](check-voice-design-5.mjs)
retain source and safeguards in this repository; ignored
`_build/voice-design-5/` holds raw receipts, audio, character alignments,
voice IDs, hashes and the comparison manifest. No automatic paid retries.

```sh
node videos/machinome-release-2/voice-design-5.mjs /home/asa/devel/machinome/videomaker --check
# Initial creation: five C3 readings and one matched Jessica reference.
node videos/machinome-release-2/voice-design-5.mjs /home/asa/devel/machinome/videomaker --generate
# Cache-only and browser verification, review server on port 8782:
node videos/machinome-release-2/voice-design-5.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-2/check-voice-design-5.mjs /home/asa/devel/machinome/videomaker
```

The Videomaker skill supplies preservation and listening-review discipline;
Context7 supplied current TTS guidance. API semantics remain those recorded
in round 3; the comparison changes neither model nor provider.

Verified on 3 October 2026: C3 variations 1–5 run 10.37, 9.87, 10.11,
10.53 and 10.03 seconds; the fresh Jessica control runs 8.36 seconds.
All six new files fully decode and their returned alignments retain the
same closing words. Exact-string checks preserve the design-3 text and
pronunciation; request checks pin C3's identity/settings and match Jessica's
request to the untagged C3 baseline. All seven players pass playback,
seeking, byte-range delivery, mutual pause, download/navigation links and
390-pixel layout without browser errors. Cache verification makes no
provider calls. The film, script, approved narration and prior samples keep
their hashes. These measurements do not establish which delivery feels best.

## Round 4 — C3 chosen, five performance directions

Subsequent pilot review rejected the change of audition line. The script
was intended as mood input. Round 5 restores the original comparison text.

The pilot likes C3 in design 3 (proposal 2, saved voice
`JoOLJ0OHRwCg8Ydjc4IF`). The voice tone is good; emotion still needs work.
The brief asks for five variations, including more excitement but not only
excitement, using the video script. This selects C3 for continued refinement,
not a final emotional treatment or permission to replace the film narration.

[Listen to design 4](voice-design-4.html). The five directions are:

1. A spark of excitement: engaged explanation, delighted reveal.
2. Discovering it together: curiosity and shared discovery.
3. Warm conviction: approachable, confident and inviting.
4. A knowing smile: gentle playfulness in the self-reference.
5. Understated confidence: plainspoken, with a little dry amusement.

The 271-character excerpt is a contiguous, verbatim passage from the approved
video narration input, beginning “With Machinome, machines can have a source
code.” and ending “And the best part is: this is all open source!” It includes
the Python scene/camera/voice explanation, the self-referential code reveal
and “How cool is that?” No new spoken copy is authored for this audition.
The existing `mah-SHEEN-ohm` speech alias is the sole spelling substitution.
The page displays the exact written script. Source file hashes and extraction
offsets are recorded with the results.

Vocal identity and performance direction are separated: all five use the
same saved C3 ID, Eleven v3, Natural stability 0.5, similarity 0.75, style 0,
speed 1.05 and seed 20261003 from design 3. Only three short delivery tags
change, placed at the explanation, reveal and open-source payoff. The intent
is a natural emotional progression, without returning to solemnity or
profoundness. Tags are instructions, not additional spoken lines. The model
can still vary perceived timbre with emotion; fixed voice identity is the
technical constraint, and the pilot judges the result by listening.

Exactly five short TTS requests, one complete reading each; no new voice is
created, redesigned or remixed. The samples receive no pitch processing,
effects, edits or post-production time changes. The prior C3 closing sample
is retained on the comparison page as a reference on its original words.

[Generation source](voice-design-4.mjs) and
[verification source](check-voice-design-4.mjs) keep this project-owned.
Ignored `_build/voice-design-4/` retains raw responses, request hashes,
voice IDs, audio hashes and character alignments. Cache-only reuse contacts
no provider; unresolved request markers prevent duplicate paid attempts.

```sh
node videos/machinome-release-2/voice-design-4.mjs /home/asa/devel/machinome/videomaker --check
# Initial creation: five short readings of the existing selected voice.
node videos/machinome-release-2/voice-design-4.mjs /home/asa/devel/machinome/videomaker --generate
# Cache-only and browser verification (review server on port 8782):
node videos/machinome-release-2/voice-design-4.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-2/check-voice-design-4.mjs /home/asa/devel/machinome/videomaker
```

The Videomaker skill keeps the existing film and narration untouched and
separates technical validation from listening judgment. Current audio-tag
guidance was checked through Context7 against the
[official TTS guide](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech).

Verified on 3 October 2026: the five readings run 25.97, 25.08, 25.73,
25.73 and 27.17 seconds. Each fully decodes and its returned alignment
retains the script words. Request checks confirm one voice ID, identical
model/settings/seed and identical words after removing direction tags.
The six players (five new readings plus the selected reference) pass
playback, seeking, byte ranges, mutual pause, download/navigation links and
390-pixel layout with no browser errors. The page transcript equals the
selected script passage exactly. Cache-only verification made no requests;
hashes preserve source files, the film, full narration and design-3 samples.
Emotional effectiveness and perceived voice continuity await pilot listening.

## Round 3 — existing voices, natural and confident readings

The pilot could not assess the voices because the cadence and emotion were
wrong. The new instruction removes profoundness from the emotion, asks for
natural confidence, preserves the voices and requests three proposals.

[Listen to design 3](voice-design-3.html). C1, C3 and C5 were carried forward
as a spread across round 2, not as an unperformed quality ranking. Proposal 1
is C1, proposal 2 is C3, proposal 3 is C5. Their former readings are available
under each new sample for direct comparison.

This pass changes the method: it saves each existing `generated_voice_id`
as a private, reusable audition voice in ElevenLabs, then synthesizes a new
closing performance through that same voice's TTS endpoint. There is no
voice design/remix request and no reference-audio reconditioning. Saving
three candidates preserves their identities for this comparison; it does
not ratify any candidate as the final Machinome voice. They occupy three
voice-library slots and have not been shared or published.

All three get the identical performance request: Eleven v3, stability 0.5
(Natural), similarity 0.75, style 0, speed 1.05, and one seed. The opening
direction is `[conversational, confident]`; the final question is
`[friendly, direct]`. There are no profound, solemn, slow, whispered or
theatrical cues, and no ellipses. The same closing words and approved
pronunciation alias remain. The 1.05 speed is a synthesis setting, not
post-production acceleration. MP3s are retained exactly as received, with
no edits, pitch changes or effects.

Sources: [generation](voice-design-3.mjs) and [verification](check-voice-design-3.mjs).
Each candidate's saved-voice receipt, speech receipt, voice binding, audio
hash and character alignment live in ignored `_build/voice-design-3/`.
Request markers prevent duplicate voice creation or ambiguous paid retries;
cache-only reuse does not contact the provider.

```sh
node videos/machinome-release-2/voice-design-3.mjs /home/asa/devel/machinome/videomaker --check
# Initial creation: save three existing audition voices and buy three short readings.
node videos/machinome-release-2/voice-design-3.mjs /home/asa/devel/machinome/videomaker --generate
# Cache-only verification, with the existing review server on port 8782:
node videos/machinome-release-2/voice-design-3.mjs /home/asa/devel/machinome/videomaker
node videos/machinome-release-2/check-voice-design-3.mjs /home/asa/devel/machinome/videomaker
```

Current contracts were checked through Context7 and the official
[save-voice endpoint](https://elevenlabs.io/docs/api-reference/text-to-voice/create/),
[TTS with timing](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)
and [performance guidance](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).
The Videomaker skill governs private credentials, preserved audio and
technical versus listening review. Short samples can still vary in delivery;
the pilot's listening judgment remains the selection gate.

Saved candidate bindings (private account resources, not public voice links):

| Proposal | Existing voice | Saved voice ID | New duration |
| --- | --- | --- | --- |
| 1 | C1 | `jtlpSHajhD6dVHux60yP` | 8.36 s |
| 2 | C3 | `JoOLJ0OHRwCg8Ydjc4IF` | 10.19 s |
| 3 | C5 | `isdFxhGsw3B4F21g7smQ` | 8.75 s |

Verified on 3 October 2026: the returned saved IDs match the requested
preview identities and the IDs used for TTS. All three audio files fully
decode, their returned character alignments retain the closing words, and
all three requests use identical performance controls. The six-player
browser comparison passes playback, seeking, byte ranges, mutual pause,
links and 390-pixel layout with no browser errors. Cache-only replay makes
no provider requests. Hashes confirm the film, full narration, original C
and all five design-2 samples remain unchanged. Duration and alignment are
technical evidence, not a claim to have listened to the result.

## Round 2 — five variations around C

The pilot chose C as the starting point, rejected the heavy profoundness,
and requested five variations that feel like Machinome. The creative
interpretation is a curious collaborator: the source, the mechanism and the
making speaking together, with everyday presence and pleasure in discovery.
Gender neutrality remains part of the brief; solemnity does not.

[Listen to C1–C5](voice-design-2.html), with the original C available for
comparison. The five directions are conversational, bright and curious,
precise, gently playful, and warmly collaborative. These labels describe
the instructions, not a claim that listening quality has been assessed.

Each request is conditioned on the actual original C MP3, verified by
SHA-256, through the documented `reference_audio_base64` field of
`eleven_ttv_v3`. Prompt strength stays between 0.30 and 0.40 to retain a
recognizable reference while exploring lighter delivery. No real person's
voice is uploaded. The same 110-character spoken closing and pronunciation
alias are retained; no full narration is generated or replaced.

One short design request per direction. The provider returns extra previews;
all are retained, and the listening page presents the first preview for each
direction, selected by stable order rather than unperformed auditory curation.
No permanent voice is created. The pilot chooses by listening.

Prompt and generation source: [voice-design-2.mjs](voice-design-2.mjs).
Receipts, all returned audio, request hashes, selected preview IDs and measured
durations are in ignored `_build/voice-design-2/`. Cache and interrupted-request
safeguards are the same as round 1, independently for each direction.

Generated and technically verified on 3 October 2026. C1–C5 run 11.15,
11.31, 11.81, 11.31 and 11.55 seconds respectively. Every delivered sample
fully decodes; all five have distinct audio hashes and preview IDs. The
browser check passed all six players (including original C): playback,
seeking, one-at-a-time playback, byte-range delivery, links and narrow layout.
Original C, the film and the approved full narration retain their hashes.
Cache-only verification made no provider calls. Listening selection remains
with the pilot.

```sh
node videos/machinome-release-2/voice-design-2.mjs /home/asa/devel/machinome/videomaker --check
# Initial creation only: five paid short design requests, with no retry.
node videos/machinome-release-2/voice-design-2.mjs /home/asa/devel/machinome/videomaker --generate
# Cache-only verification:
node videos/machinome-release-2/voice-design-2.mjs /home/asa/devel/machinome/videomaker
# With the existing review server on port 8782:
node videos/machinome-release-2/check-voice-design-2.mjs /home/asa/devel/machinome/videomaker
```

Reference-audio conditioning was checked through Context7 against the
[official design contract](https://elevenlabs.io/docs/api-reference/text-to-voice/design).

## Round 1 — original A, B and C

The pilot asked for an original, gender-neutral voice: profound, something
that comes from the source. Then narrowed the audition to simple samples of
the closing narration. No recording is cloned and no existing person is the
reference. The current film and approved narration remain untouched.

Direction: grounded presence, rounded resonance, a centered middle-to-low
register with upper overtones that preserve gender ambiguity. Close and
quietly alive, not a booming narrator. The last question opens into genuine
curiosity. English with general American pronunciation is an audition
starting point, not a ratified accent choice.

All three candidates read the same short passage, using the pilot's
connected phrasing rather than changing the film source:

> I'm Machinome, and my purpose is to enable all machines to be open source.
> What do you want to build next?

The request uses `mah-SHEEN-ohm` as the pronunciation alias, consistent with
the approved brand pronunciation. The listening page preserves the spelling.

[Listen to A, B and C](voice-design-1.html). Selection is pending. These are
unmodified provider previews from one Voice Design request; no pitch shift,
effects, narration rebuild or permanent-voice creation is part of this pass.
Technical decoding checks do not establish perceived gender or vocal quality:
those need the pilot's listening review.

Generated on 3 October 2026. A is 11.15 seconds, B is 10.76 seconds and C is
11.15 seconds. All three decode fully. Browser checks passed playback,
seeking, HTTP range delivery, one-at-a-time playback, download links and a
390-pixel layout with no browser errors. Cache reuse made no further request.
The film and continuous narration hashes still match CODE-REVISION.md.

## Reproduction and provenance

The complete prompt and request are in [voice-design-1.mjs](voice-design-1.mjs).
The exact response, generated voice IDs, audio hashes and measured durations
are retained in ignored `_build/voice-design-1/`. Keep this directory for
selection; re-running the script reuses the response without another purchase.
An ambiguous interrupted request is blocked by `attempt.json`, not retried.
Credentials are loaded privately through the existing Videomaker key paths.

```sh
node videos/machinome-release-2/voice-design-1.mjs /home/asa/devel/machinome/videomaker --check
# Only the first generation needs --generate (one paid preview request).
node videos/machinome-release-2/voice-design-1.mjs /home/asa/devel/machinome/videomaker --generate
# Reuse and verify, without permission to make a new provider request:
node videos/machinome-release-2/voice-design-1.mjs /home/asa/devel/machinome/videomaker
```

API contract checked through Context7 on 3 October 2026 against the official
[Voice Design endpoint](https://elevenlabs.io/docs/api-reference/text-to-voice/design).
The Videomaker skill supplies project ownership, private credentials,
cache preservation and the distinction between technical and listening review.
