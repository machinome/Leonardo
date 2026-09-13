# Automatic loom reconstruction: verification record

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

**Checkpoint on 13 September 2026 — not a completion certificate.** This replaces the former
illustrative model's report, preserved at the planning commit `cec7cf1`.
The reconstruction was commissioned on 12 September 2026; mechanical
validation continued on 13 September. The pilot explicitly authorized
documented inference for concealed mechanisms.

The project-owned simulation workflow supplies the red-first checks,
physical engagement contracts, whole-root integrity, fault challenges,
visual inspection and final exact-kernel gates. No framework, viewer or
sibling machine has been changed.

## Environment and evidence precision

- solid-node checkout `6e41f2da132a8604f9b68895967247fb8876fc4d`,
  metadata 0.6.0 with the post-release declarative API.
- solid-node-viewer checkout `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`,
  local 0.1.0, founded but not publicly released, viewer API 7.
- molejo checkout `e76c9039cf906cfc0005324d78ccee7116e0ff4a`, version 0.2.0.
- CadQuery 2.7, Python 3.12, Linux; workspace virtual environment.
- Exact runs compare rigid pairs on OCCT solids. Flexible leaves retain their
  mesh representation; an exact run does not make a rope an exact rigid part.
- No interference volume epsilon is used. The fixed timber frame is declared
  ground; this does not prove freestanding stability. Only the three hanging
  weights use declared rigid-support exceptions, because their independently
  measured flexible cords provide a tension that the rigid static checker
  cannot supply.

## Red-first findings and challenges

The absent upper train, descending drive and head actuators first failed
omission contracts. Detailed grip checks then failed on incomplete retention,
missing capture and collisions during exchange. Implementation did not omit
those parts or weaken the whole-root integrity gate.

| Finding | Resolution / evidence |
| --- | --- |
| Missing one/six/twelve train | Explicit indexing pin, dwell lands, cycloidal gears, retained shafts |
| Upper wheel centre-distance fault | Deliberate offset failed engagement, interference and shaft measurements; restored |
| Lower winding feed absent | Captured scroll follower, descending rack, four gears and perforated belt |
| Arm output slot too short | Real circular pin path exceeded the slot end; widened/recentred the actual slot |
| Buried pulley journal | A frame union closed the bore, creating an internal void and shaft interference; rerouted the bearer |
| Open arm bearings | Truncating the old frame removed upper guide caps; restored closed guides and measured their capture |
| Bearing feet overlapped their seats | Corrected seat height and added the intermediate-post mortise |
| Empty hand in closing shed | Full withdrawal replaces the unsuccessful four-millimetre-only retreat |
| Warp contact on entry / release | Early-opening heddle dwell, opening along the shed, outboard grip actuators |
| Counterweight crossed a cam | Arm returns now hang behind the shaft at Y=260 mm |
| Counterweight moved with its driven end | Corrected the reed return sign; full rope length and equal-and-opposite endpoint motion are measured |

The pilot's counterweight observation has a deliberate regression challenge:
changing both the reed weight and its cord endpoint to the same-direction
motion produced **3 passed, 2 failed**. At 5° the actual rope was already
0.56217 mm shorter than its required length; the vertical endpoint sum
changed by 0.56211 mm. Restoring opposite motion returned **5 passed, 0 failed**.
Endpoint attachment alone still passed the fault: it cannot prove fixed
rope length, which is why these are independent checks.

## Results at the resumed checkpoint

| Fixture / gate | Observed result |
| --- | --- |
| Upper timing, exact | 7 passed, 0 failed, 91.98 s |
| Lower winding and belt, exact | 8 passed, 0 failed, 1238.56 s |
| Flexible cords / winding, exact | 5 passed, 0 failed, 13.33 s |
| Opposed-opening grips, exact | 4 passed, 0 failed, 6.99 s |
| Whole head, faceted, final cam geometry | 3 passed, 0 failed, 37.38 s |
| Integrated root, before seconds migration, 16 / 18 / 20 mm | 21/21 each, 215.88 / 229.23 / 247.01 s |
| Python-declared clock | 60 s loop; 0 / 15 / 30 / 45 / 60 s produce 0 / 360 / 720 / 1080 / 1440° |
| Root after seconds migration, 16 / 18 / 20 mm | 22/22 each, 399.61 / 408.29 / 406.96 s, faceted, zero volume epsilon |
| Whole-head and root final exact certification | Outstanding; no complete verdict |
| OpenSCAD snapshots | Isometric, side-alignment and head views rendered and inspected |
| Standalone desktop/narrow browser before declared clock | All six stages, exact/slider controls, repeat CAD pixels, playback, assets and source inventory passed |
| Live Studio clock | PASS: actual served `loop=60`, native ×0.1/×0.25/×0.5, 1:00.0 endpoint, changed CAD and playback; screenshot inspected |
| All registered gallery browser checks | Outstanding |

Whole-head and default-root exact runs were deliberately stopped at the pilot's
new pause request. They had no completed verdict. Boundary exact runs also
cannot be counted: rebuilding a shared artifact directory removed the other
parameter variants' STL files while those runs were reading them. The resulting
`FileNotFoundError` is an orchestration failure, not a geometric verdict. Future
root runs must each use a separate build directory; do not build/export into a
running test's directory. The clock migration also requires new root runs.

Every final fixture run above uses `checks.sampled_poses`: each sample explicitly sets
`phase=0`, `run=1` and its time, then restores an explicit neutral state.
Earlier sweeps could inherit `run=0` from a preceding held-pose check and
therefore fail to exercise motion. `clear_state()` is not a reset to driver
defaults; an initial helper using it also produced failures and was corrected.
The fixture results in the table are reruns on the corrected sampler, not the
superseded first-pause results. Root sweeps now cover explicit seconds: 289
samples over 0–60 s and one-turn contact checks over 0–15 s.

The resumed run reproduced the 36 mm³ left-jaw/frame collision on exact solids
and corrected the bar route without weakening the closed guide. Expanded tests
then failed on spring/yarn contact (0.15312 mm³) and a reed haul routed 72.5 mm
inside its follower stem. Moving springs outboard and the attachment to the
stem top resolved those failures. Minimum-lift yarn contact (including 305°)
and maximum-lift selector-rim/heddle contact required handed bar routes and
42 mm selector base radii. The table's three complete faceted root runs include
these final boundary corrections. A +10° selector-phase mutation failed real
cam contact at 90° (1.6412692 mm³); its relation was restored. This challenge
preceded the later radius correction and may be repeated on the final source.

The pilot corrected an export-only interpretation of the duration request.
The model now declares `Time(loop=60)` in Python and drives its shaft at 24°/s.
The new declaration test failed first (`None != 60`) and then passed, including
the independently expected quarter-loop shaft angles. The normal Studio build
and standalone export both publish `animation.loop=60`; frame count is restored
to 360 and is only timeline resolution. Direct pytest invocation of a plain
solid-node `TestCase` did not prepare `self.node` and was an invalid harness
attempt, not a model failure; the normal `solid test` runner prepares it.

The [first pause](pause-2026-09-13.md) remains historical. The
[latest checkpoint](checkpoint-2026-09-13.md) is the current resume record.

## Coverage to retain in the final certificate

- All rigid pieces connected, with whole-root interference active.
- 289 samples over four input revolutions, transition neighborhoods,
  combined phase/run/time controls, held endpoint and instruction trajectories.
- Physical one-tooth indexing, dwell retention, six/twelve engagement,
  scroll/rack capture, all lower gear mates, bearings and axial retention.
- Every perforated-belt bridge joins both bands; actual belt material clears
  both sprockets and blocks an independently displaced sprocket.
- Seven captured head followers, both slots of each 5:1 rocker, real arm and
  jaw guides, all-direction spool retention and selector-ramp contact.
- Actual warp surfaces clear both hands and the spool at 73 phases, including
  entry and exit, not merely an open centre pose.
- Six operating cord lengths, their terminations, spring endpoints, opposite
  counterweight travel, and actual equal warp let-off / cloth take-up.
- Desktop and narrow browser controls, CAD pixels, playback, source ZIP,
  manifest asset inventory and gallery regression.

## Limits

These are sampled geometric and kinematic contracts, not a continuous
swept-volume, torque, friction, tension, impact or wear solution. The input
is imposed. Rope tension, installed belt tension, spring closing and textile
tension are assumptions. No manufacturing safety or museum-measured dimensions
are certified.

The cloth web and eight pre-existing picks advance 2.22 mm over the finite
four-turn envelope. No new interlaced textile topology is generated. The
current weft span is schematic, and replay resets winding rather than
simulating an invented historical automatic reset.

Current checkpoint logs and source hashes are retained under the project's
ignored `_evidence/automatic_weaving_loom/checkpoint-2026-09-13/`. The latest
checkpoint names their commands, outcomes and resume order. These are working
evidence, not a complete exact certificate.

Earlier working logs are retained under the project's ignored
`_evidence/automatic_weaving_loom/pause-2026-09-13/`: `grip.log`,
`cords-restored.log`, `counterweight-mutation.log` and
`root-before-opposed-jaws.log`. These are checkpoint evidence, not final
certificates. Reproducible grip commands and remaining gates are recorded in
the pause checkpoint. Research photographs remain private under `_reference/`.
