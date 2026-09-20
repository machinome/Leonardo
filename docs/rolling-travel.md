# Rolling-travel helper migration

The rack lift and the loom's two travelling-pick feeds now express pitch-circle
arc travel through `machinome_mechanics.rolling_travel`. The rack keeps its
30 mm default pitch radius (`10 * module`); both loom feeds keep the 14.8 mm
beam pitch radius. The loom's separate cloth-wrap radians conversion remains
plain degree-to-radian arithmetic because it is angular conversion, not rolling
linear travel.

The original formulas on `b361190ad76763a3d703a85c6583e23e95ee8096` were
`angle * radius * pi / 180`. Independent samples included -90 degrees at
10 mm (-15.707963267948966 mm), 7.5 degrees at 75 mm
(9.817477042468104 mm), and the rack's 137.50987083139756 degrees at 30 mm
(71.99999999999999 mm). The helper returned the same physical values (the
last rack sample rounded to 72.0 through the helper's multiplication order).
The rack passes `module.value`, the framework's supported unchecked symbolic
face, so parameter dependence is retained without asking the mechanics helper
to support declared quantity tokens.

Validation used explicit `PYTHONPATH` entries for this repository and the
independent `mechanics-rolling-travel` mechanics worktree; no shared install
was repointed. The command was
`PATH=/home/asa/devel/machinome-studio/.venv/bin:$PATH PYTHONPATH=$PWD:/home/asa/devel/machinome-studio/WTs/mechanics-rolling-travel python scripts/gallery.py test rack_and_pinion automatic_weaving_loom --kernel exact`.
Exact `rack_and_pinion` validation passed all 11 tests at the default 3 mm
module in 68.64 seconds and all 11 at the nondefault 2.5 mm module in 72.34
seconds, including travel, reversal, tooth engagement, backlash, guides and
stops. The nondefault command added
`SOLID_BUILD_DIR=_build/rolling-travel-rack-25 --set module=2.5`.
The loom's established complete root gate is faceted rather than exact: its
existing verification record says the exact certificate is still outstanding.
With `SOLID_BUILD_DIR=_build/rolling-travel-loom-faceted`, the full faceted
root suite passed 27/27 in 295.25 seconds at zero volume epsilon, including
the new direct coefficient contract. An exploratory exact run passed the
nine tests before `test_assembly_integrity`, then remained inside that
289-sample full-machine contract for about 23 minutes without a failure; it
was interrupted rather than misreported as a certificate. This migration
does not claim to close the gallery's existing exact-certification gap.

A direct no-mesh pose check also swept static phases 0, 60 and
270 degrees plus running times 15, 45 and 60 seconds. At each pose, all eight
travelling picks matched the independent expectation
`front_lower.turn * BEAM_PITCH * pi / 180` to 12 decimal places. Representative
turn/travel pairs were -2.1485917317405896°/-0.5550000000000007 mm,
-6.44577519522176°/-1.665 mm and
-8.594366926962351°/-2.2200000000000006 mm. The same check is retained as
`test_00_travelling_picks_follow_beam_pitch_circle`.

OpenSCAD inspection images are generated, ignored artifacts at
`_build/rolling-travel-rack.png` (top pose) and
`_build/rolling-travel-loom.png` (mid-cycle). Visual inspection found the rack,
pinion, guides and suspended load coherent at top travel, and the loom's lower
train, textile, warp and head coherently assembled at mid-cycle. This narrow
refactor does not advance or change the gallery queue.
