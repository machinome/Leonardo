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

## Open Questions

Resolve the vertical feed transmission's contact surfaces, the exact carrier
actuation/return path, and belt tooth seating from evidence and geometric
construction. These are implementation research tasks, not claims already
settled by the photographs. Record their disposition in the reconstruction
and validation documents before completion.
