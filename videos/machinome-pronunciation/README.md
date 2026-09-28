<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Pronunciation audition

Approved by the pilot on 28 September 2026. A 9.68-second Jessica / Eleven v3 sample,
with two occurrences of Machinome and a nearby “genome” for comparison.
This is an isolated audition, not a supported Videomaker format or a change
to the release film.

The desired pronunciation is /məˈʃiːnoʊm/. At generation, the speech key could not
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
loading are verified; the pilot listened and approved the pronunciation.

## Explicit phoneme audition

The later full-paragraph spelling take was not approved: the pilot heard
an unwanted final “me.” After the pilot enabled dictionary permission,
`phoneme.yaml` generated a separate take of the exact syntax-study
narration, using Jessica / Eleven v3 and an IPA dictionary rule. No spelling
substitution is sent. This remains an isolated production experiment, not a
new stable Videomaker feature.

```sh
node generate.mjs /home/asa/devel/machinome/videomaker phoneme
```

The dictionary locator and rule hash are cached in `_build/phoneme/`, along
with the request, alignment, complete WAV and separate SRT. An unchanged rerun
reuses both dictionary and audio. Changed inputs are refused rather than
silently reusing a stale take. One dictionary and one paid 300-character
speech request were made on 28 September 2026; no permissions were changed
by the script. The original approved standalone sample remains untouched.

The pilot approved the full-context take and requested the 28-second rebuild.
The approved take is 23.6 seconds, mono 24 kHz PCM16. WAV SHA-256:
`b61dc2bab1c168dfffb4644fac4d6407fff31d7a5ff081adfd2df444af511750`.
It was auditioned on the existing syntax-study review page with separate
audio subtitles. Browser playback, subtitle delivery, exact narration and
cache reuse were checked. The pilot's listening approval, not API success,
authorizes its use. That same <http://127.0.0.1:8769/> now serves the rebuilt
video; the WAV remains available as `pronunciation-phoneme.wav`.
