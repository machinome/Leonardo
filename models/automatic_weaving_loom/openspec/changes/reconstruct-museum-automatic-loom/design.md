## Context

This follows the pilot's historical reconstruction commission in proposal.md.
The source is the accompanied-spool ribbon loom, not the different flying
shuttle in the later full-size Milan reconstruction. The original gallery
model and its evidence remain available in history at ce141ab.

Primary research, inspected 12 September 2026:

- Vinci's [object record](https://museoleonardiano.it/en/opera/automatic-weaving-loom/)
  and its photograph `formato-immagine-sito-50.png`: Boldetti, 1954, wood,
  iron and leather; accompanied spool, narrow fabric. The repeated dimensions
  on this and the spinning-machine page are not a reliable measured scale.
- [Atlanticus 985r](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/0985-r/),
  complete image and e-Leo transcription: main wheel with two lifting teeth
  on one face, one tooth on the other, intermediate six and output twelve;
  lower coupled wheel pairs and numerous separate shuttle details.
- [Atlanticus 985v](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/0985-v/),
  image and transcription: spring/grip mechanisms, and a grip sequence that
  includes closing and a small retreat before opening to receive again.
- [Milan IGB-9910](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008265/modello-telaio-meccanico-tessitura),
  photographs `IGB-009910_20090417_001.jpg` and `_002.jpg`: another Boldetti
  model, useful opposite-side corroboration, not the requested object or a
  dimension source for it.
- [Vinci's weaving account](https://artsandculture.google.com/story/leonardo-and-the-art-of-weaving-leonardo-da-vinci-museum/2wVxLwuL6F11KQ?hl=en)
  corroborates the accompanied spool and restricted cloth width.

The newer Milan IGB-12593 record describes a perforated connecting belt and
weighted tensioning, but its flying-shuttle architecture must not be imported
as though it were the Vinci machine. Research downloads are private ignored
files under `_reference/automatic_weaving_loom/`.

## Goals / Non-Goals

**Goals:** retain the recognizable timber frame, upper loom and lower winding
layout; model every functional gear and its mate; provide physical drive paths
to shedding, grips, arms, reed and both beams; prove joints, phase and contact
on actual solids; show the real CAD in a usable browser exhibit.

**Non-Goals:** assert measured historical dimensions, copy third-party CAD,
simulate yarn constitutive forces or structural strength, or change the other
gallery exhibits. A kinematic reconstruction has imposed input motion, as the
completed sawmill does. It must not give an unconnected output a separate
animation and call that transmission.

## Decisions

### Pilot clarification during implementation

When asked whether concealed arm, grip and reed transmissions should await
additional museum drawings or receive documented mechanical completions,
the pilot explicitly chose: “Complete the gaps and document the inferred
mechanisms”. This authorizes original, tested constructions for those gaps;
it does not turn them into observed historical facts or authorize omission.

### Reconstruction and evidence

Coordinates remain X across the ribbon, Y from cloth to warp, Z up. Layout
dimensions are original CAD choices, documented beside their source confidence.
There is one input shaft. Every moving rigid member has a declared joint;
relations follow the transmitting components. Flexible cords and yarns use
molejo, with independent routing and length tests.

The upper single-tooth/six/twelve train is the first independently verified
subassembly. The six-tooth intermediate must index once per input revolution;
the twelve-tooth output advances by half that angle and dwells between indexes.
Original conjugate tooth profiles and positive running gaps are derived
geometrically. The precise tooth flanks and hidden dwell retention are
reconstruction choices, not measurements from the manuscript.

The upper output face and descending connection must be resolved against the
images before committing a feed implementation. The current working reading
is an indexed face cam, a guided descending member and a lower winding-wheel
drive. The outer view alone does not establish its hidden mating surfaces;
a mechanically convenient substitute must not be presented as an observation.

The lower apparatus contains front and rear pairs of winding/coupling wheels,
their supported shafts, a connecting belt and weighted return/tension paths.
Each visible wheel needs an inventory entry, a physical mate and a contact
contract. A material path runs from the lower warp supply to the upper shed,
through the reed and down to cloth take-up. Any finite winding reset is a
replay/manual-reset operation and must be labelled.

The prior independently prescribed carrier and reed motions are replaced by
actual cam/follower, link or cord transmissions. The museum establishes the
paired hands and the folio establishes the grip sequence; hidden cam profiles,
pins, guide bores and clearances require explicit reconstructed dimensions.
The spool is retained during travel and both transfers, with no teleporting
or interval of unsupported/free-driven motion.

### Control and verification

Retain phase and run, a small stage-button set and a finite winding envelope.
Clamp combined controls to the tested envelope. Derive the displayed output
positions from the same Python mechanism; never build a second JS mechanism.
Check desktop and narrow viewports, playback, stage controls and repeat poses.

The pilot subsequently requested a one-minute simulation for Studio's native
slow-motion controls, explicitly correcting an export-only interpretation.
Declare `time = Time(loop=60)` on the Python root and drive the same four turns
at 24 degrees per second. Root test timestamps are seconds, with the full
289-sample sweep covering 0–60 seconds. Build and export must both publish
`animation.loop = 60`; changing export frame count is not the implementation.
The native viewer receives the declared loop and exposes its speed selector.

Root connectedness and non-interference stay mandatory, across the cycle and
transition neighborhoods. Tooth-pitch sampling, bounded free/blocked tests,
shaft retention and independent geometry measurements establish engagement.
Contact tests must fail with wrong phase, missing teeth or a misplaced shaft.
Use faceted tests during development, exact tests for the final certificate,
then inspect OpenSCAD snapshots and real exported browser geometry.

## Risks / Trade-offs

- Obscured mechanisms → resolve with the primary and corroborating views,
  record remaining uncertainty by component, and keep any unresolved mechanism
  out of completion claims. Do not replace the requested reconstruction with
  the later flying-shuttle loom.
- Short historical tooth counts → use generated conjugate geometry and prove
  engagement over a tooth pitch; nominal ratios alone are insufficient.
- Belts, springs and grips → test actual routes, attachments and transfer
  overlap, and name assumed tension/contact forces separately from geometry.
- Dense geometry → isolate component contracts for development but retain the
  complete-root tests for every accepted increment and final evidence.

## Migration Plan

Commit the complete planning record, implement tested subassemblies, integrate
the reconstructed root under the existing registry name, and update the same
exhibit URL. Preserve the former archive. After all gates pass, sync baseline
specifications, archive this change and commit locally; do not push.

## Implementation findings and resolved constructions

### Pilot correction: reed must cross the carrier (13 September)

The pilot observed that the reed never crosses the carrier and requested
tracks beneath it, with the obstructing head drive raised as necessary.
The checkpoint stroke, Y=48–85, lies entirely ahead of the carrier at Y=115;
its timing test certified those coordinates without proving beat-up.
Correct this before resuming the remaining reconstruction delivery work.

The working construction is a 100 mm stroke from Y=148 behind the carrier
to Y=48 at the fell. Hold the reed behind the hands during insertion and
exchange; advance and return around each beat only after the hands withdraw.
Extend the two guide rails under the crossing, retaining a front cross-bearer
so the central cams have clearance. Move the larger reed cam outboard on the
same shaft, extend and support that shaft, and raise its follower guide and
haul sheaves to accommodate the full stroke. Keep the remaining six head
tracks, heddle eyes, arm transmissions and winding coordinates unchanged.
These dimensions are delegated reconstruction choices; the tests and pixels
must establish the completed layout. Re-route both reed cords to their actual
attachments, preserve their lengths and opposed weight motion, and make the
schematic red weft respond to the reed's working face during beat-up.

Independent regressions must measure reed geometry on both sides of the
carrier plane, its passage only while the hands clear the full reed width,
its capture in the extended rails, the fell approach, and its return to the
rear dwell. Retain every whole-root integrity and flexible-routing check.
The earlier 22-test checkpoint is historical evidence, not certification of
this correction.

The pilot-authorized completions are recorded in `docs/reconstruction.md`:
captured spiral groove and descending rack, four 24-tooth lower wheels and
a 64-perforation leather belt; seven head cam tracks, 5:1 slotted rockers,
opposed-opening retaining jaws, outboard closing springs and three weighted
cord returns. These resolve the original implementation questions, not the
historical uncertainty about concealed museum details.

Red-first integration checks found several conditions that isolated rigid
fixtures could not see. A four-millimetre-only empty-hand retreat left that
hand inside the closing shed, so both arms now fully withdraw before closure.
An early-opening, full-shed dwell replaces insufficient sinusoidal opening.
Vertical grip opening and inboard spring bows crossed actual warp yarns;
the jaws now open along opposite Y directions, with their springs outboard.
The left actuator bar overlapped the closed arm-guide cap by 36 mm³; its
outboard dogleg clears the cap without weakening the guide. Both bars retain
inboard routes in the wider shed. At the minimum 16 mm lift, the right bar's
short bridge also required shortening toward the back to clear the warp.
At maximum 20 mm lift, the selector-cam outer rims touched the lowered heddle
crossbar. Reducing the selector base radius from 45 to 42 mm and lowering
their follower pins by the same 3 mm preserves captured actuation while
clearing the heddle. These boundary failures are geometry corrections, not
reductions of the advertised range or changes to the clearance tests.

The pilot's counterweight observation became independent constant-length
and opposed-endpoint tests. A deliberate same-direction mutation fails both.
Expanded flexible/rigid route checks also found 72.5 mm of reed haul inside
the follower stem. Moving its attachment to the real stem top keeps the
sheaves unchanged and shortens the fixed rope by that amount. Cord and spring
termination contact is explicitly bounded to 3 mm terminal zones; no entire
rigid mate is excluded from the routing check.

A test sequencing finding matters to every final certificate: `set_state`
merges state, so a sweep changing time alone can inherit a held `run=0`.
The project-owned sampler explicitly sets phase, run and time at each sample
and restores a numeric neutral pose; it does not call `clear_state`, which
unbinds drivers. Final regression uses these explicit sweeps. No dependency
was changed to achieve this.
