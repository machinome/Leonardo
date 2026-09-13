# Reconstructing the Vinci accompanied-spool loom

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Commission and evidence boundary

The pilot commissioned a historical, fully connected reconstruction on
12 September 2026, replacing the former illustrative transmission. During
implementation the pilot explicitly authorized the remaining concealed
mechanisms: “Complete the gaps and document the inferred mechanisms”.

This is a reconstruction of the **narrow-ribbon, accompanied-spool** reading
represented by Luigi Boldetti's 1954 Vinci model. It is not the different
flying-shuttle loom reconstructed at Milan in 2002. Nor is it a measured
replica, a newly discovered complete design by Leonardo, or a force solver.

Primary sources inspected in full-resolution images:

- [Vinci object and photograph](https://museoleonardiano.it/en/opera/automatic-weaving-loom/).
  The museum identifies Boldetti, 1954, wood, iron and leather. Its published
  dimensions repeat another object's record; no measured scale is inferred.
- [Atlanticus 985r](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/0985-r/)
  and [985v](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/0985-v/),
  including e-Leo's transcriptions. These establish the one/six/twelve tooth
  counts, alternate shedding and detailed receiving/releasing hands, including
  a short retreat. They do not dimension every concealed mating surface.
- [Milan's related Boldetti model, IGB-9910](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008265/modello-telaio-meccanico-tessitura).
  Both catalogue photographs provide opposite-side corroboration of the
  timber frame, upper drive, lower wheel pairs, cords and weights. Its scale
  is not transferred to the Vinci model.
- [Vinci's account of weaving](https://artsandculture.google.com/story/leonardo-and-the-art-of-weaving-leonardo-da-vinci-museum/2wVxLwuL6F11KQ?hl=en)
  corroborates the paired arms and narrow-ribbon limitation.

Museum photographs and folio scans are research references, not redistributed
assets. Downloads remain under ignored `_reference/automatic_weaving_loom/`.

## Inventory: observed structure versus inferred construction

| System | What the evidence establishes | Explicit digital completion |
| --- | --- | --- |
| Input and upper train | One engaging tooth, intermediate six, output twelve; L-shaped layout | Radial pin slots, complementary dwell lands and sampled cycloidal mating flanks |
| Scroll face and descending member | Scroll-like upper face and a descending guided member beside the lower wheel | Captured spiral groove and pin; rack teeth on the lower member; finite winding envelope |
| Lower wheels | Two lower winding/coupling stations and connected wheel pairs | Four equal 24-tooth wheels, module 4; exact concealed tooth counts are not established by these photographs |
| Connection between stations | A belt-like connection in the drawing and museum views | Perforated leather loop on pegged coaxial sprockets; 64 holes at a 4π mm pitch |
| Shedding | Alternating heddles and a common input | Two captured face tracks and guided stems, retaining the former model's tested needle spacing |
| Paired arms | Two hands accompany and exchange the spool | Guided arms, captured cam followers, 5:1 slotted rocking levers and taut haul cords; these lever dimensions and cam profiles are inferred |
| Short retreat | Described among the gripping details on 985v | Initial release retreat continues into full withdrawal outside the ribbon before shed closure; this subsequent parking route is inferred |
| Grips and release | Receiving, holding and releasing hands with spring action | Upper retaining jaws, lower support fingers and opposed cam-driven selector ramps; spring closing remains an explicit force assumption |
| Reed | Coordinated beat-up | Captured two-lobed face track, guided follower, routed haul cord and weighted return |
| Cords and weights | Visible returns and hanging weights | Three weighted return routes with geometrically fixed lengths; exact tie-off points and sheave grooves are inferred |
| Frame and textile route | Upper weaving head, lower winding apparatus and tall timber frame | Original supports, running clearances and guide locations; no hidden historical joinery is asserted |

The concealed head is deliberately exposed for inspection. Its seven face
tracks are **not** claimed to be seven discs observed on the museum object.
They are the pilot-authorized completion that turns the former disconnected
motion laws into testable physical constraints. Likewise the rack, dwell
retention and perforation dimensions are constructions, not copied dimensions.

## Kinematic construction

Coordinates are X across the ribbon, Y toward the warp end and Z up. The
weaving plane is Z=520 mm; the main shaft is at Y=180, Z=400 mm. The lower
wheels are at Z=106 and 202 mm. The heddle-support tower reaches Z=615 mm;
the main longitudinal rails are below the working head, at Z=510 mm.
Dimensions are reconstruction choices.

The input's pin indexes the six-position wheel by 60° per full input turn.
The continuously meshing six/twelve pair gives 30° at the output. The pin
engages from 120° to 240° of an input revolution; complementary lands retain
the indexed member during the other two-thirds. Shared generating-circle
geometry supplies the tooth flanks rather than an unsuitable unmodified
six-tooth involute.

The scroll groove increases its radius by 0.06 mm per output degree. Thus
each input revolution lowers the captured rack by 1.8 mm. At a 48 mm lower
wheel pitch radius this gives 2.148592° per turn. The rear upper wheel, belt,
front upper wheel and front lower wheel follow that actual transmission.
The belt has two side bands and the leather remaining between its holes;
these material bridges travel around both sprockets. A finite four-turn
envelope covers 120° of scroll rotation and 7.2 mm of rack travel.
At the pilot's request the Python root declares `Time(loop=60)`: this same
four-turn envelope spans 60 machine seconds at 24°/s. Studio receives the
declared duration and exposes its native slow-motion speed selector. Export
frame count is not used to define machine time. This changes the time base,
not gear ratios, travel or the bounded reset.

Each arm cam moves its follower through 26 mm. A rocker with pins 20 and
100 mm from its fixed pivot converts this into 130 mm of vertical output;
horizontal pin slots accommodate the real circular pin paths. Routed cords
convert output lift to arm translation at a 1:1 length relation. The opposite
cords and weights maintain return tension. Both hands withdraw to their outer
parking positions between picks. An earlier four-millimetre-only retreat
left the empty hand inside the closing warp and failed the yarn-contact test;
it is not the delivered mechanism. The reed has a separate 100 mm captured
stroke, described below. Opposed 14 mm selector motions open only a hand that has reached the
receiving region; the other hand remains closed on the spool. The receiving
hand closes before the donor opens: both are closed during 85–95° and
265–275°. Cosine-eased arm approaches stop at the centre during 60–120° and
240–300°, allowing this grip exchange without sliding the enclosed spool.
Each compound selector ramp converts vertical rise into equal opening along
the shed: +Y for the left jaw and −Y for the right. Its additional 1:2 X slope
reduces opening as the empty hand withdraws.
The actuator and guide sit outside the warp at X=±185 mm. They hold the
departing jaw open until its retaining hooks clear the spool. The jaws open
along the shed, not vertically through its upper warp layer. An earlier
vertical-opening construction and its inboard actuator failed actual
yarn-contact tests despite passing rigid-only interference checks.
The closing leaf springs are also outboard at X=±185 mm: an inboard bowed
leaf failed the expanded yarn-clearance contract. The left jaw's crossbar
doglegs 8.5 mm forward only outside the ribbon, at |X|≈100 mm in the hand's
frame, to clear its timber guide cap while opening. Its inboard span remains
in the wider shed. The right bar and its short inner bridge sit 5 mm farther
back than the earlier construction to clear the 16 mm minimum shed. Moving
both complete bars forward was unsuccessful; these routes are deliberately
handed and checked at the advertised lift boundaries.
The selector cam tracks use a 42 mm base radius and 14 mm rise. A 45 mm base
left their outer rims touching the lowered heddle crossbar at 20 mm lift;
the smaller rims and correspondingly lowered follower pins preserve capture
while clearing the full build-parameter envelope.
The gates retain the boat above, sideways and inward, while the arm supplies
the bottom and outer stop. Their fingers occupy opposite halves of the boat,
with a fixed cheek on each hand opposing its moving cheek. Ownership
changes only in the shared stationary dwell; elsewhere the spool follows the
hand whose actual body and jaw enclose it. The ownership relation is a
kinematic contact-mode declaration, not a separate spool motor.

Heddles open with cosine easing over 0–50°, hold the full shed through 130°,
and close by 180°. The opposite shed repeats over the second half-turn.
Their cam base radius is 42 mm. This early opening and dwell preserve room
for the supporting fingers at entry and exit, including the minimum shed
height. A simple sine lift was insufficient when checked against actual
yarn surfaces. The inferred cam geometry changes with the lift parameter.

The arm hauls use three quarter-turn sheaves each and their returns one.
Arm return weights hang at Y=260 mm, behind the shaft's cam envelope; a
Y=200 mm route collided with a cam during an instruction transition.
The reed has its own three-sheave haul and one-sheave return. When the reed
recedes toward its return pulley, its weight descends: reversing this sign
shortened the actual rope by twice the reed motion and failed the length
contract. Each rope is measured on its actual flexible sweep, not just the
coordinates from which that sweep was constructed.
The reed haul starts on the follower stem's actual top, Z=602.5 mm at rest,
not on the cam pin below it. The former checkpoint's 72.5 mm internal-cord
error remains documented in its historical evidence. The longer mechanism's
haul and return have nominal lengths 517.99336 and 298.99779 mm. The summed
heights of the haul attachment and weight top remain 1027.5 mm; the two arm
attachment/weight sums remain 848 mm each. The reed's return is attached
26 mm inboard of its haul, on the same rigid crossbar, so its horizontal span
clears the follower and supporting post. All six rope lengths are constant.

### Reed passage correction, 13 September

The pilot identified a functional gap in the checkpoint: Y=48–85 never
crossed the carrier at Y=115. A test that merely checked those former end
coordinates could not establish beat-up. The corrected stroke is Y=48–148.
The reed dwells behind the carrier during insertion and transfer, advances
between fully withdrawn hands, reaches the fell at each half-turn boundary,
then retreats before the hands enter again. Each advance/return occupies
26° either side of the beat; the remaining interval is a rear dwell.

Two 132 mm guide rails span Y=32–164 beneath the carrier, joined at the
existing front bearer. Timber supports carry the rails over their full
length. The open centre of this U-shaped bed clears the central cams. Each
selector's cross-shed tie moves back to Y=158 behind the parked reed and
rises 22 mm to Z=466, with risers at its ends; its rear
bridge keeps the original height to clear a fully lowered heddle. Small
timber bridges carry the side rails over slots that clear the raised ties
at maximum lift. The ties clear both the parked reed and the largest cam
rims; simply raising them above the tracks would still obstruct the reed's
legs or intersect a cam.

The reed cam is relocated to X=−365 on the extended, supported common shaft.
Its roller-centre radius spans 70–170 mm. A periodic spline and true normal
offsets form a groove with 1.65 mm half-width for the 1.5 mm roller. A smaller
base radius made the tight return unable to retain the roller; a segmented
offset produced an unusable mesh. The adopted curve must pass the dedicated
2° beat-flank capture sweep as well as the ordinary head tests. This is an
original concealed-mechanism completion, not a dimension measured from Vinci.

The follower guide is at Z=590, its haul sheaves at Z=730, and the reed's
rigid haul crossbar is above the grip selectors at Z=570. The unchanged six
other cam tracks and the weaving plane retain their original alignment.
The displayed red weft bends ahead of the reed during beat-up, returning to
the free straight span when the reed withdraws. That prescribed contact
display does not calculate forces, conserve newly delivered weft length,
or generate new interlaced cloth topology.

Cord tie-offs and leaf-spring clamps/bearing ends occupy named terminal zones
no more than 3 mm from the measured route ends. The routing contract checks
every operating cord and spring against every rigid component and confines
any attachment overlap to those zones; it does not exempt whole mating parts.
Detailed knot compression, clamp preload and termination strength are not
solved or certified.

At the 14.8 mm textile pitch radius, each input turn releases 0.555 mm of
warp and winds the same length of cloth. The four-turn envelope therefore
advances 2.22 mm of material. A continuous cloth web reaches the lower cloth
beam through its upper guide; the warp unwinds from the rear upper beam.
Eight pre-existing picks move with the cloth. They are a displayed woven
sample, not newly formed yarn topology. The current weft span shows the
carrying spool and prescribed reed contact, not a weft-length or force solve.

The imposed input, maintained rope tension, installed belt tension and
spring closing are force assumptions. There is no simulation of wood
deflection, impacts, friction, yarn constitutive behavior or manufacturing
safety. The test certificate must distinguish those assumptions from measured
solid engagement, guide capture, flexible routing and retained geometry.

## Current implementation status

The reed/carrier correction supersedes the short-stroke geometry described
at the earlier pause. Its implementation, mutation, snapshots and the latest
pilot-requested pause are recorded in [reed-correction.md](reed-correction.md).
Full exact certification and the final browser-harness rerun remain pending.

### Earlier Studio-time checkpoint

At the pilot's requested pause, this change was not yet
certified or archived. All 22 integrated contracts, including the declared
seconds clock, pass on the faceted kernel at 16, 18 and 20 mm shed lift. The final
upper timing, lower winding, grip and cord fixtures respectively pass seven,
eight, four and five exact tests using explicit-state sweeps. Whole-head and
whole-root exact certification remains pending. Deliberately restoring same-direction
counterweight motion failed both length and opposed-travel checks; shifting
a selector phase also failed physical cam contact.

The frame/jaw interference has been corrected without removing the closed
guide. Final isometric, transmission-alignment and head snapshots have been
inspected. The actual export has been regenerated, and desktop/narrow controls,
pose-changing and repeat-pose pixels pass. The subsequent Python-declared
one-minute clock passes its actual Studio metadata, native slow-speed options,
one-minute endpoint, changing CAD and playback check. Gallery-wide browser
regression remains pending.
See the [historical checkpoint](checkpoint-2026-09-13.md) and
[verification record](verification.md).
