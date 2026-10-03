# An original Machinome voice — audition 1

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

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
