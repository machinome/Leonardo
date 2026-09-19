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
The pre-open kerf avoids claiming material removal.

All rigid leaves are original exact CadQuery components. The assembled stand
is a fused stationary fixture, not disconnected parts hidden in a compound.
The rope is a molejo flexible leaf with two straight runs, a semicircular
pulley return and a varying drum wrap. Distinct solids keep real running
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

The drum’s rope pitch radius is 23.4 mm. Its 11.25° index takes up
4.594579 mm, which is both carriage travel and loss of free upper rope.
An initial 270° wrap grows to 315° over four cycles. The fixed return
pulley reverses the pull without multiplying force or travel. The complete
centerline is 844.783170 mm long throughout.

The flexible leaf’s ports must exactly match its shape parameters. Its
moving origin is therefore placed explicitly in `simulate()`, driven by
the same drum take-up as the carriage. The three shape parameters describe
the two remaining free spans and wrap; no alternate free-running rope input
is exposed. This uses the public framework contract and changes no dependency.

## Control and explanation

There are two drivers: phase 0–1440° and playback 0–1. Their sum clamps at
four turns even when both are nonzero. Six instructions expose the start,
half stroke, bottom, active feed, complete pass and timeline operation.
Only kerf is a build parameter, tested from 2 to 5 mm.

The exhibit embeds the actual machinome widget, with whole, drive, saw and
rear-feed views and a reversible frame reveal. The UI’s numeric labels and
stroke trace interpolate a table measured from the Python meshes at 0.5°
intervals; they never place CAD or implement another mechanism. The finite
readout script checks that table. Browser replay explicitly announces the
carriage reset and explains the historical manual release/reload sequence.

## Evidence and limits

Whole-root connectedness and non-interference are mandatory. Geometric tests
cover crank/key engagement, guide capture, both tie ends, fixed pawl journals,
active tooth engagement, blade forks, wheel retention, rope routing and
attachments, stroke, dwell, travel, repeatability and combined control limits.
A timed instruction scenario checks the assembled pass.

The [validation record](validation.md) separates exact rigid comparisons from
the flexible mesh fallback, sampled motion from continuous proof, and
historical observation from inferred fits. Load capacity, equilibrium,
fluid forces, cutting, friction, rope tension and threaded fastener strength
are not certified.
