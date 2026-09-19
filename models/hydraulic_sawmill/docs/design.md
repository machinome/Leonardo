# Milan hydraulic saw reconstruction: implemented design

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Authority and evidence

The pilot’s 12 September 2026 request replaces the former simplified exhibit
with a reconstruction of the mechanisms visible on Milan museum object IGB-37.
The explicit correction is an undershot wheel. The museum photographs and
Atlanticus 1078r, with confidence levels and inferred dimensions, are recorded
in [reconstruction.md](reconstruction.md). The earlier model and certificate
remain in Git history at `0936085` and in the original archived OpenSpec.

## Mechanical architecture

```text
undershot wheel → keyed crankshaft → connecting rod → guided saw sash
                                                        │
                                          pinned tie → long rocker
                                                        │ short arm
                                              driving pawl → ratchet
                                                              │
                                              holding pawl ───┤
                                                              ↓
                                          drum → rope → return pulley
                                                              ↓
                                                  carriage on rollers
```

The timber foundation, stand and channel are grounded display fixtures.
The two-post tower guides the sash. Bearings support the input and feed
shafts; fixed brackets locate the rocker, holding-pawl and return-pulley pins.
Blade forks and the upper stem/nut retain the blade at a displayed set tension.
A molejo insert fills the uncut part of the rigid halves' kerf. It recedes at
the teeth to show progressive cutting, without a cutting-force solver.

All rigid leaves are original exact CadQuery components. The assembled stand
is a fused stationary fixture, not disconnected parts hidden in a compound.
The rope has three molejo flexible leaves: the upper run and semicircular
pulley return, the lower fleet-angle span, and a helical drum winding. Distinct solids keep real running
clearances; the water surface sits just below the lower paddles.

## Kinematic closure

`layout.py` owns reconstruction dimensions; `parts.py` owns solids.
`kinematics.py` uses machinome’s symbolic degree math so Python and the
exported browser use the same closed mechanism.

The crank/rod equation closes the slider-crank. Intersection of the rocker-tip
and saw-journal circles closes a 235 mm rocker and 50 mm tie. Its short arm
is solved at construction time so a 75 mm driving pawl advances exactly one
32-tooth pitch during the return stroke. Feed therefore comes from the
linkage’s actual contact-circle displacement, not an unrelated eased index.

The driving and holding profiles share `contact.py` with CAD. A planar
polygon-clearance construction samples each recovery at 181 positions and
finds the first outward position clearing the actual teeth by 0.25 mm.
The exported law interpolates that cam table while preserving exact pin
spacing at every pose. This is prescribed quasi-static seating, not a
gravity/contact-force solver; the independent whole-solid tests check the
result, including intermediate positions.

The drum's rope pitch radius is 23.4 mm, with 3.2 mm axial winding pitch.
An initial 15° wrap grows to 847.5° over 74 turns; adjacent coils do not overlap.
The drum is widened locally, with a narrow bored cleat at Y=93 mm.
Carriage feed conserves the total rope length, including helix length and
the changing fleet angle of the lower free span. Feed varies very slightly
from turn to turn (approximately 4.60 mm). The fixed return pulley only
reverses the pull. The free span and winding meet at the lower drum tangent.

Flexible leaf ports exactly match their shape parameters. The free rope's
moving origin is placed in simulate(), driven by the same carriage law.
The winding leaf sits in a translating wrapper so its axial placement
remains distinct from its rest orientation. No extra machine input or
dependency change is needed. Orderly winding is prescribed, not physically
solved; the splice approximates the very small tangent/fleet-angle change.

## Control and explanation

The pilot's 19 September 2026 requests replace the four-turn inspection with
a full timber pass and remove every instruction and driver. A declared 296-second
loop is the only motion control: four seconds per wheel turn, 74 turns total.
Only kerf remains a build parameter, tested from 2 to 5 mm.

The 320 mm timber begins at X=-171 mm. Its slotted support cradles stand
120 mm each side of its centre. The carriage is 420 mm long, with axles
at +/-185 mm; neither axle crosses the blade during the course.
The leading bark face starts just 1 mm before the teeth. After 340.062622 mm
of travel the trailing face is 4.062622 mm beyond the blade's back.
End-grain veneers also clear both ends. Table and rails grow modestly to
720 and 760 mm, with the foundation length 875 mm; tower, wheel and log
cross-section are unchanged. These replace the rejected 100 mm trial.

The uncut molejo insert spans the kerf and a conservative 56 mm timber height.
Its leading boundary stops at X=-10.2 mm (0.2 mm ahead of the teeth). Its
length decreases with the carriage's measured feed, clamped from 320 to 0 mm.
A polygon swept across the fixed kerf width avoids a zero-length path, which
molejo refuses. In its final 0.1 mm the polygon also loses height; at completion
it is a finite, zero-area display mesh. That collapsed mesh is intentionally
not an exact OCCT solid. Tests measure its endpoints, volume and disappearance.

The physical tree has five root groups: Frame and guides, Water drive,
Saw mechanism, Timber carriage, Feed mechanism. Timber and running gear are
separate carriage subgroups. Both viewers expose the bundle's navigator.

The exhibit embeds the actual machinome widget, with whole, drive, saw and
rear-feed views and a reversible frame reveal. The UI’s numeric labels and
stroke trace interpolate a table measured from the Python meshes at 0.5°
intervals, with measured endpoints for all 74 turns to account for the
small fleet-angle contribution to feed; they never place CAD or implement another mechanism. The finite
readout script checks that table. Browser replay explicitly announces the
carriage reset and explains the historical manual release/reload sequence.

## Evidence and limits

Whole-root connectedness and non-interference are mandatory. Geometric tests
cover crank/key engagement, guide capture, both tie ends, fixed pawl journals,
active tooth engagement, blade forks, wheel retention, rope routing and
attachments, stroke, dwell, travel, repeatability and full-course support/clearance. The timeline endpoint tests measure both
timber ends independently of the motion law. No instruction scenario remains
because the machine declares no instructions.

The [validation record](full-pass-validation.md) separates exact rigid comparisons from
the flexible mesh fallback, sampled motion from continuous proof, and
historical observation from inferred fits. Load capacity, equilibrium,
fluid forces, cutting, friction, rope tension and threaded fastener strength
are not certified.
