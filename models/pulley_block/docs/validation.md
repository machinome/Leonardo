# Compound-pulley validation — 12 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Scope and environment

Queue 030 authorizes this complete model. Planning commit `5a05aa0` records
the historical basis, ordinary reconstruction choices and exact continuation
prompt. The completion record below identifies the tested source commit;
the completion commit only finalizes evidence, queue status and archival.
The project was clean except for pre-existing untracked `screenshots/`.
Those files and the other machine sources are preserved. A live floor
session was assigned cam_hammer, not this model; no agent was dispatched.

| Dependency | Tested content revision |
| --- | --- |
| solid-node | `6e41f2da132a8604f9b68895967247fb8876fc4d`, metadata 0.6.0 |
| solid-node-viewer | `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`, local 0.1.0, API 7 |
| molejo | `e76c9039cf906cfc0005324d78ccee7116e0ff4a`, 0.2.0 |
| CadQuery / trimesh / Playwright | 2.7.0 / 4.4.9 / 1.62.0 |

Linux, Python 3.12, workspace `../../.venv`, installed Chromium. The three
dependency repositories were clean on inspection; none was modified.
The post-0.6 declarative API is required; PyPI solid-node 0.6 alone is
insufficient and the local viewer is not described as released.

The complete shared solid-node API and machining skills informed the motion
and geometric contracts. Context7 supplied current CadQuery, molejo and
Playwright documentation. Molejo's public Python, concepts and B-rep manuals
supplied the line/arc vocabulary, declared ring ordering and exactness contract.
The viewer's public mount/handle types informed its thin camera shell.
OpenSpec proposal/apply/sync/archive skills structure the machine-owned cycle.
Historical evidence and source access limits are in the machine README.

## Red-first and deliberate mutation

The tests preceded model.py. The first faceted command exited 1 because the
node file did not exist. The first complete model then ran ten methods:
six passed and four failed. The whole-root check found 18.5661522465 mm³
of carrier/load interference. The load-eye bore had been partly refilled
by the joining neck. Cutting the bore through the joined eye, neck and
weight fixed the geometry without changing the acceptance tests.

The resulting ten methods passed. Inspection then led to narrower, open
anchor cheeks so the small return wrap is visible. The same contracts
passed for the final carrier geometry.

The intentional mutation changed **node code**, the rope's effort-end
formula from `88-4*height` to `88-3*height`. The rigid grip retained its
correct -3h travel. Seven methods passed and three failed:

- Constant-length measurement found 619.532881984 mm instead of
  622.212373908 mm at phase 30°, a 2.679491924 mm error.
- The control-combination test found a 1.464466094 mm length error.
- The attachment test found the rope tip 20 mm above the grip socket at Mid.

The wrong coefficient shortens the actual rope by h and detaches its effort
end. Restoring it returned ten methods to green. Rigid connectedness,
interference, journal capture, sheave rotation and rigid support stayed
green during this mutation: they are structurally blind to flexible length.
Even rope clearance alone stayed green. The separate length and endpoint
contracts carry that responsibility; no new red history is claimed for
the untouched older exhibits.

## Measured contracts

The root has seven rigid solids (frame, three wheels, carrier, load, grip),
five distinct rigid artifacts and one non-rigid rope. Whole-root connectedness
and zero-positive-volume interference remain active with no excluded pair,
epsilon or narrowed root. The flexible rope has its own collision tests
against **every** rigid solid, so the root's rigid-only selection cannot
silently omit it.

- Twenty-five timeline poses check rigid clearance. Fifteen phase poses
  cover the full cycle, endpoints, 0.01° reversal neighborhoods and
  intermediate lift. Eighty phase/run/time combinations cover all slider
  corners and fractional run; sixteen endpoint comparisons prove loop return
  on the rope's actual vertices.
- Actual load bottom rises from 24 to 64 mm; actual effort-grip top falls
  from 208 to 88 mm. Their independently measured displacement ratio is
  3:1. No joint or derived-coordinate value is an expected measurement.
- The rope's world mesh has 433 rings of 16 vertices, plus two cap centres.
  Averaging each ring recovers its centreline. All ten element endpoints
  are measured against independently stated positions. Straight lengths,
  arc radii and accumulated angles recover **622.212373908 mm** through
  the entire range. The tail and all four half-wraps are counted. A second
  check relates mesh volume to the independently calculated 16-gon profile
  area; its 0.16 mm equivalent-length tolerance bounds chordal arc sampling,
  not collision volume.
- Nine phase poses check rope/rigid intersections, one watertight rope body
  and nonlocal centreline separation. Pairs separated by over 6 mm along
  the centreline must stay over 3 mm apart in space (rope diameter 2.5 mm).
  This complements the explicit noncrossing vertical lanes and measured
  circular wraps; it is a sampled self-intersection check, not a universal
  self-contact solver.
- Five poses test each sheave against its actual carrier in all three
  local directions: free at ±0.12 mm and blocked at ±0.65 mm, independently
  bracketing 0.25 mm radial and 0.3 mm axial play. The wheels' actual
  vertices also follow +h/R, -2h/R and +3h/R rotations about the three
  stated Y axles, including moving-block translation.
- At four poses the rope is axially free at ±0.12 mm and caught at ±2.1 mm
  by each sheave flange. Dead-tail and effort endpoints remain at measured
  insertion depths. The effort socket gives ±0.10 mm free and ±0.65 mm
  blocked transverse motion; the dead-end wrap/socket is free at ±0.10 mm
  vertically and blocked after +0.65 mm.
- At four poses the load eye is vertically free within ±0.1 mm and caught
  0.7 mm downward by its support pin. The support solver explicitly grounds
  the frame, suspended carrier and held effort grip, and proves the remaining
  rigid supports with max_drop=0.7 mm and no glue exemptions.
- The instruction scenario runs Low, Mid, High and Run at dt=0.05 s,
  checks whole-root clearance every 0.2 s through the ramps, and verifies
  each final input. Flexible controls are covered by the separate full-range
  route and combination sweeps.

No build-size knob is advertised. The only public parameters are the two
drivers; their endpoints and intermediate combinations are covered. Ranges
are metadata, not protection against arbitrary out-of-envelope input.

| Final pulley suite | Result |
| --- | --- |
| Faceted development | 10 passed, 0 failed; 9.69 s |
| Exact certification | 10 passed, 0 failed; 42.23 s |

Counts are runner methods, not sampled poses or individual pair assertions.
Exact certification includes actual line/arc flexible B-reps in intersection
and perturbation tests. Mesh-derived measurements remain explicitly sampled.

An additional exact measurement divides the rope solid's volume by its
analytic circular area `pi*1.25**2`. It gives 622.2123739082077 mm at Low,
622.2123739082077 mm at Mid and 622.2123739082080 mm at High, each within
1e-6 mm of the independent length formula. `rope.shape_tolerance` is 0.0
at all three poses. This also checks the unsampled analytic tube itself.

Reproduce that additional measurement after setting `SOLID_BUILD_DIR` and
`PYTHONPATH` as above, using the public node API:

```python
import math
from models.pulley_block.model import PulleyBlock
n = PulleyBlock()
n.set_state(phase=0, run=0, time=0)
n.assemble()
n.build_stls()
for phase in (0, 90, 180):
    n.set_state(phase=phase)
    length = n.rope.shape().Volume() / (math.pi * 1.25**2)
    assert abs(length - (440 + 58*math.pi)) < 1e-6
    assert n.rope.shape_tolerance == 0.0
    print(phase, length)
```

## Reproduce

Activate the documented environment and run from the gallery root:

```sh
SOLID_BUILD_DIR=_build/pulley_tests solid test pulley_block --faceted
SOLID_BUILD_DIR=_build/pulley_exact solid test pulley_block --exact
python scripts/gallery.py check
python scripts/gallery.py build
python scripts/gallery.py export
python models/pulley_block/scripts/check_browser.py
python scripts/check_browsers.py
```

During development the direct reference
`models/pulley_block/model.py:PulleyBlock` selected the same root before its
registration. Existing exhibits use isolated build directories
`_build/pulley_regression_<name>` for regression, with both kernels and
PYTHONPATH set to this gallery. This avoids concurrent publication sweeping
artifacts that another test still needs. Raw logs live in ignored
`_evidence/pulley_block/`; summaries are retained here.

## Presentation and browser evidence

The final export has document version 4, 361 frames at 30 fps, phase/run,
four native instructions, symbolic degree-cosine bindings, five deduplicated
rigid assets and a single analytic flexible shape. Every named asset exists.
The thin exhibit shell uses the shipped widget with a modest front camera
angle; the standalone exported viewer also remains available.

[Selected OpenSCAD images](evidence/README.md) were opened and inspected at
Mid and High. The first image command failed because the output directory
did not yet exist; creating the evidence directory and repeating succeeded.
Browser captures were inspected at 1440×1100 and 390×844.

The finite browser script uses the real widget's instruction ramps, exact
entry, sliders, play/pause and timeline. CAD-region screenshots exclude the
control overlays, so text changes cannot satisfy a geometry-motion check.
Returning to phase 90 produces identical CAD pixels; fractional run returns
identical pixels at the timeline endpoints. Page/console errors, failed
requests, HTTP errors, missing assets and horizontal overflow fail the smoke.
Live labels are compared against independent measurements of the built
Python meshes at Low/Mid/High, manual phase 60 and fractional-run samples.
Labels are read-only explanatory arithmetic, not a second CAD or motion
renderer; playback values are rounded to the visible timeline frame.

The preliminary source ZIP came from the then-current planning commit;
the completed exports must replace it with committed implementation source.
The completion record pins and verifies that replacement.

## Limits

Finite samples are not a continuous collision proof. The simple planar path
also has an analytic length derivation, but tests do not solve dynamics.
The stand's joinery and integral pins are simplified. The block is prescribed
upright; the support check's suspended fixtures are explicit assumptions,
not certification of flexible tension or static equilibrium. The effort
socket represents a secured end without modeling a knot or crimp strength.
No friction, efficiency, elasticity, sway or capacity claim is made.

## Completion record

| Existing exhibit regression | Faceted | Exact |
| --- | --- | --- |
| Hydraulic sawmill | 10 passed, 0 failed; 11.41 s | 10 passed, 0 failed; 16.13 s |
| Automatic weaving loom | 12 passed, 0 failed; 28.33 s | 12 passed, 0 failed; 29.11 s |
| Cam hammer | 11 passed, 0 failed; 31.08 s | 11 passed, 0 failed; 46.25 s |
| Rack and pinion | 11 passed, 0 failed; 22.25 s | 11 passed, 0 failed; 73.46 s |

All five models built and exported successfully; the catalogue check
reports five models, separate OpenSpec roots and a coherent queue. Existing
source/test files remain byte-for-byte unchanged from `92a1253`.
`python scripts/check_browsers.py` exited 0 after all five registered
exhibits passed. The final pulley run used the front camera and public
driver-handle readouts, verified labels against measured meshes on both
viewports, and reported no browser console, page or network failures.
The final commit records the tested source revision, all-exhibit browser
check, OpenSpec archive and source ZIP audit.
