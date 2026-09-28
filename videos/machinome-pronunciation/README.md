<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Pronunciation audition

Awaiting the pilot's approval. A 9.68-second Jessica / Eleven v3 sample,
with two occurrences of Machinome and a nearby “genome” for comparison.
This is an isolated audition, not a supported Videomaker format or a change
to the release film.

The desired pronunciation is /məˈʃiːnoʊm/. The current speech key cannot
create pronunciation dictionaries, so this sample uses the continuous
spelling `Masheenome`, without a hyphen. The IPA remains an editorial
target, not an applied phoneme rule. Captions retain `Machinome`.

From this directory:

```sh
node generate.mjs /home/asa/devel/machinome/videomaker
python -m http.server 8769 --bind 127.0.0.1 --directory _build
```

Open <http://127.0.0.1:8769/>. Instructions, transcript, playback and downloads
are on the page. Generation reuses the checked cache; a missing cache makes
one paid synthesis request. Credentials are read only from Videomaker's
ignored `.env`. Generated WAV, separate SRT and provenance stay in `_build/`.

The WAV is the provider's complete 24 kHz mono PCM, without trimming,
stretching, background sound or mastering. File properties and browser
loading are verified; pronunciation remains for the pilot to hear and ratify.
