# Revolutions — production verification

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Inputs and scope

The film is a new release essay commissioned by the pilot, not a revision
of the earlier mechanism rehearsal. Its subject is human purpose and
AI-assisted making, demonstrated through the sawmill and Machinome.

The model is the unchanged export of Leonardo
`a01fb865426de9967f690b4a7a1230684eb1e523`: corrected two-rope drive, fitted
timber frame, 1460-second complete course. The film follows model seconds
400–528 with edits and deliberate holds. No CAD, simulation, viewer or
Videomaker source was changed. The mechanical source diff against that
revision is empty; existing mechanical certificates are cited, not claimed
to have been rerun for a content-only film.

Final narration and camera cues were committed at `9ec5428`; subsequent
production records and finishing code have their own commits. The generated
capture and release manifests hold exact input, tool, audio and output hashes.

## Completed checks before final encoding

- The episode parser validates all 16 shots, contiguous 177-second edit,
  camera keys, assembly paths, evidence files, actual model duration and
  pinned export revision.
- Browser preview produced 48 samples at 1280×720 using Viewer API 27.
  Pixel replay is identical; invalid camera requests preserve the prior
  view; no console, asset or request failures were reported.
- Storyboard and individual frames were visually inspected. Changes
  brought the opening wheel closer, clarified the stroke view, kept the
  timber visible in the two-rope sequence and adjusted the whole-machine
  composition. Framing includes deliberate close views of selected parts.
- All 16 final speech segments fit without truncation or stretching.
  Their total measured file duration is 143.934695 seconds. Fifty-four
  subtitle cues are ordered without overlap; alignment lies within each
  audio file, and the written captions restore “Machinome” from its speech
  alias. Last caption ends at 172.987 seconds.
- Pawl recovery, the two rope-sequence half-strokes and the “Pause it”
  freeze use measured character timestamps recorded in the README.
- The closing shot and empty series label were read; a scan of rendered
  narration, titles and overlays found no copyright, licence, creator,
  sponsor or appended attribution lines. Leonardo is the historical subject.
- A 30-second opening MP4 was encoded at 1920×1080 / 30 fps with H.264 and
  AAC, then inspected through frames decoded from that file.
- Original score and narration were mixed with speech-controlled ducking
  and two-pass loudness mastering. The measured PCM master is -16.01 LUFS,
  -1.81 dBTP, LRA 6.70; 48 kHz stereo. Audio levels and timing were checked,
  but the production was not listened to in this environment. Pronunciation,
  vocal performance and musical balance still need an auditory review.

## Final delivery

Rendered on 27 September 2026; final frame inspection completed on
28 September. `_build/machinome-revolutions.mp4` is
177.000 seconds, 1920×1080, 30 fps, 5,310 H.264 frames with 48 kHz stereo
AAC. The delivery is 24,789,691 bytes. Its SHA-256 is
`cdf4a154b125c7f336123ef918c6b66a29ac455a1c7cbfd811be26e38241f6f8`.

The final MP4 passes a full audio/video decode. Sixteen review images were
decoded from the delivery, one inside each narration segment, and the
resulting contact sheet was visually inspected. Additional inspection
covers individual frames, the encoded opening, source text, the closing
frame and the title thumbnail. These are frame inspections; continuous
playback and a listening pass were not performed in this environment.
Final AAC measures -16.03 LUFS, -1.88 dBTP, LRA 6.70. Timing, levels and
container checks do not replace the auditory review named above.

`release-manifest.json` records the final hash, codec/frame/duration checks,
decoded review frames, original score and mastered audio hashes. Its linked
`rehearsal-manifest.json` records model assets, viewer, browser, source
hashes and capture settings at project head
`e0bc00f6f84cb501c54c93a4733ec6e83f62747f`.
The later documentation commit does not change the film or its inputs.

The delivery folder also contains `captions.srt`, `thumbnail.png`,
`release-contact-sheet.jpg` and a resolved upload-description draft.
`rehearsal.mp4` preserves the narration-only rendition; the finished MP4
adds the original score while copying the captured video stream unchanged.

## Publication record

Nothing was pushed, uploaded or published. A public repository exists at
`https://github.com/machinome/Leonardo`, but its checked main revision
`cec7cf1a9e284887efa89477d136111f0679f428` predates this reconstruction and
the filmed model commit's public page returns 404. A current-source link
and an interactive-simulation link therefore remain unresolved.

This differs from older local records saying that no remote is configured:
there is an origin, but its existence does not publish the model in this film.
The upload draft states the current reconstruction's provenance and physical
limits. Its URL placeholders must be replaced by verified destinations at
publication. `releaseReady` in the media manifest measures those URLs only.
