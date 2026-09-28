<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Revolutions, second script direction

Script commissioned on 28 September 2026. The opening through the early
invitation now has a rehearsal; the rest remains an unrendered editorial draft.
`episode.yaml` is the narration authority, with visual directions beside each
passage. `production.yaml` selects real source, model, voice and evidence.
The previous films and approved 28-second syntax study remain unchanged.

The pilot's new order is the spine: revolution and ancestor; Machinome and
Python; the waterwheel class and whole mill class; observe a physical drive
relationship and read the same relationship in code; follow the complete
mechanism including the ratchet axle's winding, both ropes and reduction;
explain tests using a real test; explain the necessary human piloting; show
the museum reference and invite the viewer to judge, explore and give feedback.
A self-aware invitation and the single like request now follow the first
two Python classes. The pilot rejected both the spoken explanation of the
name and the teaching preamble "Start small"; neither remains in narration.

The opening line is retained from the release film, not from the earlier
mechanism rehearsal. The human-direction passage is no longer an early
detour: it answers the limit just established by the tests. The first-person
machine voice stays a tool, and improvement remains human-directed. Do not
invent historical authorship, hidden dimensions or a physical force solver.

## Presentation

- Dark 16:9 frame throughout; Jessica / Eleven v3 and the approved IPA rule.
- Real PEP 8 Python with imports and actual class names. Never silently
  rename `Wheel` or replace source with pseudo-instructions.
- Full-screen code alternates with full-screen machine, never competes
  with moving geometry beside it. Code mostly holds still; measured word
  emphasis carries the instructional motion.
- Follow cause and effect slowly. Rope 1 unwinds from the large compound
  drum while rope 2 winds onto the thin section of that same shaft.
- The input rope builds radially on the ratchet's bare axle, not along it
  and not on an invented large drum. Changing radius changes the feed.
- The photo is a real, already-inspected reference, not generated imagery.
  Hold it for the reliability question, then match-cut to the model.
- Optional SRT is a separate asset, never burned into the film. Brief part
  labels and a time-acceleration/physical-limit label are not subtitles.
- Keep creator, licence and photo attribution in the upload description.

## Draft versus renderable behavior

The full script's 369-second timeline is a provisional reading board, not
measured speech. The seven-scene opening rehearsal has its own measured edit,
described below. Later model poses and camera presets remain starting points,
not inspected final framing for every new scene.

The current normal renderer does not interpret directions as editing commands:
it would show a model where this draft calls for source or the photograph.
Do **not** render this draft through it and call it the intended film.
The source-only/word-emphasis experiment proves those individual devices;
the full multi-scene edit, macro rope view, museum still and interactive
viewer capture remain production work beyond the opening. The pilot next
commissioned an empirical opening rehearsal, not a stable tool interface.
No new Videomaker interface or spec is proposed here.

Before production:

1. Review narration and scene sequence with the pilot.
2. Build the missing shot composition empirically in the same production lane.
   Implement explicit reveals/cuts, early/late winding views and the completed
   pass shot described in prose; the draft's model ranges do not yet encode
   all those sub-shots. Validate framing and assembly visibility in pixels.
3. Generate with the approved dictionary, measure complete takes and adjust
   slots rather than truncate. Use actual alignment for all code highlights
   and model-phase keys for downstroke/feed and upstroke/dwell.
4. If showing test output, run and capture the actual test. This draft selects
   genuine code and existing evidence; it does not claim a fresh test run.
5. Clear museum-image use for the release and settle any required attribution.
   The research download is not a licence. Verify public simulation/source
   destinations before claiming working links in a published description.

Draft checks can be reproduced from Videomaker with:

```sh
node bin/videomaker.mjs check \
  ../projects/Leonardo/videos/machinome-revolutions-v2/episode.yaml
```

This checks source pins, ranges, evidence, timing coverage and named model
paths. A passing source check does not mean the new edit has been rendered.

Initial draft validation passed: 19 contiguous scenes, 360 provisional seconds,
621 spoken words before the subsequent editorial adjustment. Seven literal
source selections matched the pinned export revision, existing evidence files
and valid named assembly paths. The revised full draft passes the same checks
with 19 contiguous scenes and 369 provisional seconds.
The narration, overlays and empty series label contain no credit markers.
No geometry, tests or stable tool behavior changed.

## Opening rehearsal

`rehearsal.yaml` selects the first seven passages from `episode.yaml`, through
`early-invitation`. It does not duplicate the narration. `rehearse.mjs` is a
project-owned empirical adapter: it reuses Videomaker's source pinning,
timeline/camera mapping, speech mixing, subtitles and dark code stage, with
the real viewer. Nothing about the mechanical simulation is reimplemented.
It is not a supported new Videomaker format or an executable screenplay.

```sh
node rehearse.mjs /home/asa/devel/machinome/videomaker speech
node rehearse.mjs /home/asa/devel/machinome/videomaker preview \
  /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node rehearse.mjs /home/asa/devel/machinome/videomaker render \
  /home/asa/devel/machinome/machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
```

One continuous 1,024-character Jessica / Eleven v3 take was generated with
the already-approved IPA dictionary version attached. The dictionary was
reused, not recreated. The unchanged request is cached; preview/render have
no synthesis path. The speech command also reuses a matching cached take.
No trimming, time stretching or per-sentence splicing is applied.

The measured edit is 76.2 seconds, 1920×1080 at 30 fps. The wheel class enters
at 43.200 s, the mill class at 53.368 s and the invitation at 63.968 s.
The final spoken line ends at 74.568 s. Code holds still and is shown alone;
the whole machine returns for the invitation. Both code compositions, the
opening wheel and the whole-machine framing have been visually inspected.
The wide camera includes the entire foundation, with margins throughout its
small oblique shift. Browser checks verify literal source, layout bounds,
still code, moving machinery and pixel-identical seek replay. The 17 existing
Videomaker tests pass. Audio validation covers the cached waveform, provider
alignment and complete timing; it is not a listening review of the new take.

Generated media, raw speech/alignment, separate SRT, previews and provenance
are under `_build/rehearsal/`. The existing port 8769 review server receives
the new MP4, SRT and `watch.html`; the previous 28-second video stays available.
Its local `simulation/` link points to the pinned export and its source ZIP.
Those local rehearsal links do not settle the public release destinations.
No museum image appears in this opening, so its publication-rights gate
does not affect this rehearsal. This is not a final release or a claim that
all of the full script has been filmed.

Encoded validation passed: 2,286 video frames at 30 fps; matching 76.2-second
video and audio streams, both starting at zero; no embedded subtitle stream.
Decoded frames at 2, 10, 28, 46, 58 and 72 seconds were visually inspected.
The real review page passed playback and all three replay-button checks;
MP4, SRT, previous segment, simulation and source links returned HTTP 200.
The linked simulation mounted its canvas without browser or asset errors.

The original generic static server could not seek into the larger film:
replay requests returned to time zero. `serve-review.py` adds single byte-range
responses while keeping the same directory, loopback address and port 8769.
Prefix, middle, suffix and open-ended ranges matched the original bytes;
out-of-bounds ranges returned 416. Browser replay then reached 0, 43.2 and
63.968 seconds correctly. This changes local asset delivery only, not media
or the viewer. To reopen the review after the server has stopped:

```sh
python serve-review.py --port 8769 \
  --directory ../machinome-syntax-study/_build
```

The review files are copies of this episode's MP4, same-basename SRT,
`revolution.png` as `rehearsal-opening.png`, and `watch.html` as `index.html`.
The served `simulation` symlink points to `../../export/hydraulic_sawmill`
from this episode directory. Do not publish these local links as release URLs.

Artifact SHA-256:

- MP4: `60288831d6040f533d3f162c14c73d99856ff7069290963f72aabe3ae0f54d1b`
- SRT: `77c9328d7afef239dd1352592d63eb2f11e19f7ff9e9edae48a61053d6b9456b`
