# Photographed transmission correction — 21 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

**Verified for this sawmill, including the holding-pawl chatter correction.**
The latest geometry uses the pilot's fixed-plane radial input winding, not
the rejected axial helix. No dependency has been modified. The supported
spline-bend representation and the pilot's subsequent holding-pawl correction
pass all 42 exact tests at default and boundary kerfs, and the browser checks.

This record supersedes intermediate single-rope, outboard-pulley, hanging-strap,
notched-frame and axial-winding results. In particular, the 74-, 259- and
967-turn arrangements are not the current reconstruction. Project baseline:
`5349757`; planning commit: `986ec1b50df6830ae2f04cf7358b5383ac17ff32`.
The implementation is recorded by the commit containing this certificate;
the tested mechanical blobs are identified below. Nothing has been published.

## Implemented arrangement

The teeth face +X; the carriage moves toward -X. The wheel remains at Y=-151.
The iron axle runs through timber seats at Y=-207 and -32 to the square-fitted
crank at Y=-13. The connecting rod is centred at Y=0, followed by the feed tie
and rocker at Y=12 and 22. The short arm reaches the adjacent pawl plane at
Y=58. There is no far-side crank returning through a long cantilever pin.

The hook pulls on the downstroke. The holding pawl's rollback reaction seats
it; its release envelope follows a connected clear path over the departing
tooth rather than jumping through it to a lower landing. The table is warmed
through a tooth and periodic at its seam. Tip reach is 41.425 mm, fitted so the
drop clears the tooth before dwell; the fixed pivot is unchanged. No damping
animation masks the contact geometry. Locking-face contact is measured within
the existing 5-degree play bound (about 4.5 degrees in the seated pose).

The first rope winds directly on the slender ratchet axle, at Y=52 just inside
the gear. It stays in that axial plane and builds radially over earlier turns.
It passes down around the pulley on the inward face of the opposite fixed
saw upright, then up to the large winding section of the compound shaft.
That shaft is inside the bed, supported in the existing end legs. Its thin
central section winds the separate hauling rope over the upper roller to the
top centre of the carriage. No guide hardware is invented to enforce stacking.

Both fixed running rails are continuous at the saw tower. Both moving-carriage
end members join the side timbers. The blade does not reach those members
during the working course. The horizontal bed and fixed saw tower are separate
named rigid groups in the assembly tree.

See [design.md](design.md) for dimensions and equations and
[reconstruction.md](reconstruction.md) for photographic evidence and limits.

## Measured transmission

- Saw stroke: 48 mm; ratchet: 32 teeth; waterwheel period: 4 seconds.
- First-turn travel: 0.334454 mm.
- Input coil radius grows from approximately 6.276 to 27.050 mm.
- First whole tooth completing the required course: turn 365.
- Complete pass: 1460 seconds (24 minutes 20 seconds), 341.017588 mm travel.
- The 320 mm timber starts 1 mm ahead of the teeth and ends 5.017588 mm beyond
  the blade's back. All four carriage rollers remain on continuous rails.
- Feed increases as the input coil grows; it is not a constant millimetres per
  turn. The final tooth advances about 3.136 mm, including the changing upper
  hauling angle. Playback acceleration does not change the declared duration.

The input spiral uses 1.82 mm radial pitch for 1.8 mm rope: nominal packed
diameter plus 0.02 mm geometric clearance. Tangency is solved against the
spiral, not a fictitious fixed-radius pulley. Its length is integrated with
12-point Gaussian quadrature; tests independently measure endpoints/radii
and use the analytic asinh antiderivative. Both ropes conserve length within
0.001 mm in the measured poses. The rendered spline's radial error is checked
within 0.002 mm. Output winding remains helical at the selected 3.2 mm lead.

## Red-first and deliberate defects

- Original handedness, remote iron layers and square-crank contracts failed
  before reconstruction. A later central-load-path test rejected the far-side
  crank and return pin.
- The top-haul/rectangular-frame run failed 3 of 33 tests: low attachment,
  missing upper roller and unmatched wooden end projection.
- The inward-pulley/bare-axle/tree checks failed 3 of 37 tests before their
  placement was corrected.
- The closed-frame checks failed before restoring the continuous running
  rails and missing rear carriage crossmember.
- The pilot's latest report exposed a real blind spot: earlier rope clearance
  checks omitted the moving rocker. The new test reproduced 27.319711 mm³ of
  rope/rocker intersection. The radial-winding placement test also failed.
  That red run was 39 passed, 2 failed out of 41 (34.14 s, faceted).
- With fixed-plane radial winding, all 41 tests passed (45.07 s, faceted,
  zero volume epsilon), including the moving-link rope-clearance contract.
- Deliberately multiplying compound-shaft rotation by 0.98 failed exactly the
  rope-conservation and complete-course tests: 39 passed, 2 failed (38.91 s).
  The timber ended at X=+1.681279 rather than beyond X=-7. The mutation was
  reverted. The clean rerun passed all 41 tests in 57.24 s, zero volume epsilon.
  The mutation is not present in the final source.
- An earlier holding-pivot mutation from Z=340 to Z=385 also failed the
  contact-reaction contract. The holding check is not just collision with a
  frozen pawl; it measures the contact normal and moment about its real pivot.
- The pilot's holding-pawl chatter report reproduced a 6.865590-degree
  oscillation during return stroke 10: 41 passed, 1 failed out of 42 (41.73 s,
  faceted). A separate real-browser pixel test reproduced the fault on return
  16 at crank phase 183 degrees, against the pre-fix export.
- The periodic contact table and revised tip reach pass all 42 faceted tests
  (92.09 s, zero volume epsilon), including numerical checks throughout all
  365 recoveries and actual-pawl meshes on five selected turns. A further
  401-pose clearance sweep over crank 145–165 degrees in 0.05-degree steps
  passes at the drop. The contact-normal test now finds the first surface
  contact, rather than assuming the earlier 2.5-degree rollback pose.

## Verification

Full-root connectedness and rigid non-interference remain active: 149
full-pass instants, a dense first revolution, tooth transitions and endpoint
neighbourhoods. Tests also exercise shaft/bearing support and retention,
square-drive fit, hook force direction, holding reaction, frame continuity,
rope joins, winding, complete travel and repeatability.

Input-rope clearance to the moving feed links is checked at 25 full-pass
poses. Rope length, attachments and clearance to the frame, shafts, sash and
carriage are checked at 13 poses. These are sampled geometry contracts, not
proofs of continuous contact dynamics.

The first radial-winding exact runs rejected the drive rope's non-coplanar
Line–Arc–Line sweep:

```text
molejo.brep.BrepError: the construction declared an exact solid but carries
SurfaceOfExtrusion, SurfaceOfRevolution; an approximated surface must declare
its tolerance
```

A public-API probe isolated this to the lower-pulley drive rope. Default, kerf=2
and kerf=5 full reruns each completed with **39 passed, 2 failed out of 41**:
333.28 s, 336.92 s and 341.52 s respectively. Both failed checks stop at the
same converter error, not an exact intersection verdict. This was corrected
within the project by representing the bend with a supported 16-segment
spline and exact endpoint tangents, not by patching dependencies or relaxing
the kernel. The bend's measured radius and arc length remain within 0.001 mm
of the intended circle. The spline declares 1e-6 mm conversion tolerance.
Those reruns passed **41/41 exact** at default, kerf=2 and kerf=5:
719.34 s, 709.11 s and 718.41 s. No test is skipped and no faceted verdict
is substituted inside an exact run. Final runs including the holding-pawl
correction passed **42/42 exact** at all three settings: default 899.45 s,
kerf=2 888.31 s, and kerf=5 913.84 s.

All five other gallery models passed their unchanged faceted regressions:
loom 27, hammer 11, rack 11, pulley 10 and crane 12 tests. The earlier combined
run's sawmill result described the now-superseded axial winding, so only the
new sawmill run above certifies the radial version.

The sawmill browser script passed desktop and 390 px narrow layouts, all
five views, playback, scrubbing, CAD pose return, real assets, readouts,
assembly navigation, frame reveal and the source ZIP, with no console or
network failures. Its isolated-part regression checks actual exported pawl
pixels at selected recovery poses on turns 0, 10, 16, 64, 182 and 364, then
verifies that the same part still moves during indexing. Readouts independently match 721 stroke samples and 2921
full-pass feed samples. Gallery inventory and strict OpenSpec validation pass.
A capture inspection also caught a blank view during a height-only remount;
responsive remounting is now limited to width changes, and the browser test
rejects a blank canvas. The gallery-wide rerun includes this final check.

The gallery-wide browser run passed sawmill, loom, hammer and rack. The
unchanged pulley exhibit failed to create its canvas; an independent crane
run failed at the same initial canvas check. A read-only browser diagnostic
identified `MachinomeWidget is not defined` in both existing custom viewer
pages; changing software-WebGL flags did not resolve it. These unrelated exhibit failures are not
claimed green and no other machine or dependency was changed to address them.

During verification, the preview source download was an explicitly labelled
working-tree snapshot produced through a temporary Git index. Final exports
are regenerated from the accepted implementation commit; their
`source-revision.txt` identifies it. Exports are not tracked in Git.

## Physical and historical limits

This is a kinematic reconstruction of Milan's 1952–1953 interpretative model,
not a measured Renaissance machine or a strength calculation. Internal
dimensions, hidden fastening and knot envelopes are stated reconstruction
choices. Rope tension, orderly stacking, absence of slip and secured timber
are assumptions. A bare shaft does not prove that turns will stay stacked:
lateral winding stability, compression, knot deformation, torque, friction,
water power, cutting loads and wood deflection are not solved.

The uncut-kerf insert is a visual cutting impression, not material-removal
physics. The viewer's end reset represents an operator stopping, releasing,
unwinding and reloading, not an invented automatic return.

## Tested working content

These Git blobs identify the tested mechanical source independently of the
certificate's own commit identifier:

| File | Git blob |
| --- | --- |
| `model.py` | `7fbb6a6b50d3277ebcbe3b7e0e01c372aaa43ea4` |
| `parts.py` | `e7d932c5ed19d753dcfe85fdcf748d5f9e9447e0` |
| `layout.py` | `7788dcf233602939a39cc450ba9c0f338e6ad0df` |
| `contact.py` | `959cbea6a34226aec1f4255b04621866a65ae136` |
| `kinematics.py` | `f1f95eed62c5abcea812bc59896d3cf14f0a165c` |
| `rope_drive.py` | `30222c30f23f7cd960a95c27149a7d11418b405e` |
| `test_model.py` | `7591a0c78fe8f9f6982ee05f6a23e03f4fec8c20` |

## Environment and reproduction

- machinome development content: `e63700e4fdb90e066d47f358e9de0ea935ac1be9`.
- molejo content: `e76c9039cf906cfc0005324d78ccee7116e0ff4a`.
- viewer development content: `e82b5214e4460e606cb86608f042e7a6fcefa49d`.
- Python 3.12, CadQuery 2.7.0, molejo 0.2.0, Playwright 1.62.0.
  Local machinome/viewer metadata is 0.7.0/0.2.0, not a publication claim.
- Linux Chromium with SwiftShader; default OpenSCAD for CAD evidence renders.

Use the commands in the machine [README](../README.md). Exact boundary runs
use distinct `SOLID_BUILD_DIR` directories. The sawmill's evidence gates are
complete; the unrelated gallery browser failures above remain separately
disclosed and are not a green gallery-wide publication certificate.

The focused drop-clearance probe uses the same public exact assertions:

```python
from machinome.test import TestCase
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill
machine = LeonardoHydraulicSawmill()
machine.set_keyframe(0)
machine.assemble()
machine.build_stls()
checks = TestCase()
for i in range(2900, 3301):
    machine.set_keyframe((i / 20) / 90)
    checks.assertNotIntersecting(machine.feed.holding_pawl, machine.feed.feed_drum)
```
