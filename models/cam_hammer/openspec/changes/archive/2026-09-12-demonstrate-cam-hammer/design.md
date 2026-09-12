# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Context

This is commissioned original CAD under queue 010, following two completed
gallery exhibits. Museum of Science describes a cam depressing the lever's
tail; Venice describes crank-driven intermittent hammering. Those sources
establish the principle, not historical dimensions, construction details,
a particular folio or invention priority. No museum CAD or images are copied.

## Goals / Non-Goals

Goals: an open, readable hand-cranked assembly; measurable cam engagement,
captured pivots, supported frame and anvil; inspectable rise, release and
strike; a self-contained real solid-node export with a companion page.

Non-goals: impact, gravity integration, strength, wear, forging capacity,
materials calibration, fabrication certification or a dimensioned replica.

## Decisions

Use XZ for the mechanism and Y for both journal axes. Place the lever pivot
at (0,0,110) mm, its rounded tail at local (-60,0,0), and its hammer at
local (100,0,0). Place the cam centre at (-60,0,170). The cam presses the
tail down and the long arm rises. A timber base and paired journal posts
support the moving shafts. Axial collars capture each shaft. Timber and
metal are visual material cues; joined decorative components are one
connected solid where appropriate.

The input is phase plus 360*run*time, reduced periodically using symbolic
degree atan2/sin/cos. Expose phase 0..360 and run 0..1. The single build
parameter is lift_angle, 18 degrees by default, bounded to 16..20.
For cam angle theta, the lever rises with a half-cosine from 0..240 degrees,
then returns by a half-cosine over 240..320, and rests through 360. The
physical cam retreats over 240..285, leaving the follower released during
the slower prescribed drop. These timings are illustrative, not a dynamics
prediction. Angle reduction is continuous in geometry at the cycle seam;
fractional run changes speed, not the tested pose envelope.

Generate the cam from the rounded follower's pitch curve in the cam frame:
rotate the moving tail centre minus the cam centre through -theta, then
offset inward by nose radius plus a stated 0.3 mm running gap. Use the
same designed rise envelope for the geometry and relation, but independent
test arithmetic and actual surfaces for expectations. Sampling and offset
accuracy must be measured; refine the outline if needed. The rounded shoe
is integral with the lever, not a falsely animated free roller. A simple
eccentric was considered but cannot show a released drop; an arbitrary
decorative snail cam would not prove the follower law.

Instructions hold Lift (120 degrees), Release (250), Strike (320), and Run
(phase 0/run 1). Ramps remain in the periodic safe envelope. The anvil face
is horizontal at the hammer's lowest strike surface. Its small assembly
seating gap and all journal running gaps are explicit in source and tests.
The page embeds the actual exported viewer; no duplicate machine logic.

## Risks / Trade-offs

- Cam offset may undercut or collide with the arm near release: verify
  dense contact neighborhoods and whole-root sweeps, refine original CAD.
- Floating parts can pass interference: measure bearing capture and
  ground support, including axial and radial perturbations. The frame is
  grounded; driven poses are kinematic, not dynamic equilibrium claims.
- A contact law can pass its own algebra: test mesh distance and one-sided
  blockage, deliberately mutate cam phase and require contact failure.
- Zero-clearance strike can expose numeric booleans: measure landing on
  the face and retain zero-penetration root checks; never add a volume epsilon.
- Browser expression or export defects: run the real export in Chromium
  at desktop and narrow sizes, exercise controls and return to an earlier pose.

## Migration Plan

Commit this plan, build and verify the machine, then add it to the shared
registry and archive its spec. Leave the existing exhibits intact and run
their regressions. Only mark done after evidence passes. All work remains
local; publication is a later pilot action.

## Open Questions

No pilot decision is outstanding within the commission. Geometric gaps
and profile sampling are engineering choices to settle with evidence and
record in the final validation report.

## Implementation findings

The straight tail arm collided with the cam's retreating flank at
225–270 degrees. Its top is now recessed to z=-2 mm between local
x=-48 and -16, with an 8 mm deep connected section below it. The shoe
and the lift/return envelope are unchanged. Whole-root interference,
contact and integrity remain active; the change fixes the colliding CAD.

Side-view inspection found the initial cam column hid the shoe. Move each
cam column to x=-108 and carry its journal on a 78 mm top bearing beam;
the journal location stays (-60,0,170). The contact is visible in the final
side and isometric snapshots and journal capture remains measured.

Tests use distinct build directories from publication. A simultaneous
export prunes fusion-ingredient files still needed by measurements, even
though each build obtains the framework's lock. The overlapping attempt
was discarded and rerun with independent directories; no dependency changed.
