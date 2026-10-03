# An original Machinome voice

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

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
