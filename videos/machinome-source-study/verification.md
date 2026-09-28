<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Source-study verification — 28 September 2026

## Delivered scene

- `_build/rehearsal.mp4`: 28.000 seconds, 1920×1080, 30 fps, 840 frames,
  H.264 High/yuv420p and stereo AAC at 48 kHz; 2,593,156 bytes.
- Video SHA-256:
  `9f93e8f9183dcb442a88d3faba103115f24a8cfef1a23bdeb696260c6ac65057`.
- `_build/rehearsal.srt`: 10 UTF-8 cues from 0.800 to 23.840 seconds;
  SHA-256 `02d3c74ff2e39bcbc3d657ad874d8f61ee567bdcef4ca0a192621bbed7ed4763`.
  The MP4 contains only video/audio streams, and inspected film frames contain
  no narration subtitles. Explanatory title/source/closing label are deliberate.
- `_build/rehearsal-manifest.json`: complete source, model, font, viewer, audio,
  browser, encoder and subtitle provenance.

Rendered using Videomaker `1f7b27809e26c3230b9aca7d32a535441bb8a928` and
consumer source `e61dcbb491f850d6d6813058bbf2e31f8e2cdbc7`. Later documentation
commits do not change that rendered source. The real Python file matches the
export revision `a01fb865426de9967f690b4a7a1230684eb1e523`; the excerpt is lines
200–206, with only four common leading spaces removed. Full-file SHA-256 is
`02317da4e6a8571b46522aa4805f285d8b879532340d0e7f63ccd922dd309b1f`.

## Picture

Nine 1920×1080 preview frames cover the six typing beats, initial state, complete
source and closing. Real Viewer API 27 checks pass camera readback, canvas
coverage, source panel bounds/text equality, invalid-camera preservation and
exact pixel replay. The capture rendered all 840 frames without browser errors.

Decoded the actual final MP4 at 1.4, 11.8 and 25 seconds into
`_build/review-{opening,typing,closing}.png` and inspected them. The first shows
the first declaration in progress; the middle shows the connection typing;
the last shows all seven actual lines, syntax colors, the moving sawmill and
the human-purpose closing label. No model or code is clipped by the panel.
This is sampled frame inspection, not a claim of continuous human viewing.

## Narration and reported clipped starts

Jessica (`cgSgspJ2msm6clMCkdW9`), Eleven v3, stability 0.5. A single 23.04-second
take was acquired as PCM 24 kHz and wrapped in WAV without trimming; the same
cached take was reused throughout iteration. Raw audio SHA-256:
`206d3c34dd8d4622643a298b001522f18bdccbf85471efd48a38cb7ca1d7e797`.
There is 0.8 seconds of authored preroll and no music, voice gate or onset fade.

The provider clip crosses amplitude 0.005 at 38.125 ms. Its next 350 ms correlates
0.999534 with the positioned narration mix and 0.998907 with the decoded final
AAC audio. Checking the first 350 ms at each of the ten caption starts against
the corresponding raw segment gives mix correlations at least 0.999956.
The final encoded soundtrack measures -15.81 LUFS integrated, -1.42 dBTP.
These checks show onset preservation and headroom, not intelligibility or emotion.

The original V1 mix and encoded master also retain their cached clip onsets.
No dropped-splice bug was demonstrated. Some original raw clips begin almost
immediately; the new take changes both synthesis model and acquisition while
avoiding a separate synthesis restart per shot. **No listening audition was
possible in this environment.** The pilot should judge whether this resolves
the perceived missing syllables before regenerating the whole release film.

Reproduce onset comparison from Videomaker:

```sh
node scripts/review-onsets.mjs \
  ../projects/Leonardo/videos/machinome-source-study/_build/audio-manifest.json \
  ../projects/Leonardo/videos/machinome-source-study/_build/narration.wav \
  ../projects/Leonardo/videos/machinome-source-study/_build/rehearsal.mp4
```

## Tool and scope checks

Videomaker's 14 tests pass, including source authenticity/escaping/typing,
PCM sample preservation, legacy MP3 cache guards and a short mixed-layout browser
and encode test proving SRT is external. Its OpenSpec change validates.
No mechanical source changed and no CAD re-certification is claimed.

The original 177-second release master remains unchanged at SHA-256
`cdf4a154b125c7f336123ef918c6b66a29ac455a1c7cbfd811be26e38241f6f8`.
Nothing was pushed, uploaded or published. Description links remain unresolved.
