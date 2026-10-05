# Cam hammer validation — 12 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Scope and tested environment

Queue 010 commissions this complete exhibit. Planning commit: `1c0be60`.
Tested source: `9df5851ada1021e343d22973d6c93fd4831e7237`.
The recorded tests ran on the same source bytes immediately before that
commit; committing them did not change their content. The completion
commit changes only this record, task/queue status and archive placement.

| Dependency | Tested content |
| --- | --- |
| machinome | local post-0.6 source `6e41f2da132a8604f9b68895967247fb8876fc4d` (package metadata 0.6.0) |
| machinome-viewer | `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64` (local 0.1.0) |
| molejo | `e76c9039cf906cfc0005324d78ccee7116e0ff4a` (0.2.0; existing exhibits) |
| CadQuery | 2.7.0 |
| trimesh | 4.4.9 |
| Playwright | 1.62.0, installed Chromium |

All three dependency checkouts were clean when recorded. This is Linux,
Python 3.12, the workspace environment at `../../.venv`. The framework's
post-0.6 motion API and local viewer are not represented as published
releases. CadQuery polygon/extrusion documentation and Playwright iframe
documentation were fetched through Context7 from their official manuals.

## Red, repair and mutation evidence

The companion geometric tests were written before model.py. The initial
faceted command failed because the model did not exist. With the complete
geometry but the follower law deliberately held at zero, the root
non-interference test failed (cam/lever intersection 0.13028 mm³ in the
first failing pose). Wiring the designed law produced 7 passing and 4
failing methods: the straight tail was still clipped by the retreating cam.

Local mesh measurements isolated that interference to the arm core, not
the shoe: 6.59, 55.84, 268.78 and 250.97 mm³ at 225°, 240°, 255° and 270°.
The tail now has a continuous recessed section under the retreating
envelope. This CAD change cleared the root sweep without weakening it.
Side inspection then moved the cam columns away from the contact region;
the journal centres and motion remain as planned.

The deliberate mutation changed the actual relation from
`cycle.drives(cam.spin)` to `cycle.drives(cam.spin, offset=8)`.
The run reported **7 passed, 4 failed**. The specific contact test failed at
10°: measured gap **0.12045 mm**, below the required 0.20 mm. Root
interference, transition neighborhoods and the instruction scenario also
failed. The independent hammer-position check stayed green, as expected:
it measures lever motion and is structurally blind to a cam-only phase
error. Restoring the relation returned all 11 methods to green.

A concurrent publication once removed fusion-ingredient artifacts while
tests were reading them. That attempt was discarded. Cam test runs use
`_build/cam_hammer_tests`, `_build/cam_hammer_16` and `_build/cam_hammer_20`,
separate from the `_build/cam_hammer` publication directory. No dependency
was patched and no cache was deleted to hide the problem.

## Geometric coverage and results

Whole-root connectedness and zero-volume-interference contracts remain
active for all four rigid solids. The full-cycle sweep has 37 poses;
additional checks cover 0°, 240°, 285°, 320° and 360° with 0.1° neighborhoods,
and the drop at 245–310°. Forty-eight combinations of phase (0,120,250,360),
run (0,0.5,1) and time (0,0.25,0.7,1) test combined controls and independently
measure the head's world position. The periodic law covers the same bounded
pose envelope through additional revolutions.

Cam contact is checked every 10° through the 240° rise on actual cam
vertices against the round shoe surface: required separation 0.20–0.42 mm
around the designed 0.3 mm gap. One-sided lever perturbations prove it is
free at 0.12° toward the cam and blocked by 0.8°. This is a pushing contact;
no bilateral gear-mesh claim is made. During release, 260–300° samples
require more than 1 mm separation. Intermediate hammer position uses
independent half-cosine arithmetic and measured head bounds, with 0.01 mm
dimensional tolerance. Strike checks measure z=91 mm and the anvil footprint,
then prove upward freedom and downward blockage.

A separate measurement pass also checked between profile sample angles.
At 30.25°, 60.25°, 90.25°, 180.25°, 210.25° and 239.75°, measured gaps
were 0.30520–0.30853 mm. The 120° lift gave a 0.30011 mm gap and head
centre z=120.70500 mm. At maximum lift (240°) the head centre was
z=136.14642 mm and its lowest corner z=119.12342 mm. Release at 250°
opened 1.58566 mm; the 270° and 280° gaps were 7.26720 and 8.71014 mm.
Strike at 320° returned the lowest face to z=91.00000 mm. These were
measurements of the built geometry, not values returned by the motion law.

At nine cycle poses each shaft is free at ±0.2 mm and blocked at ±0.7 mm
in each radial direction, and free at ±0.15 mm and blocked at ±0.7 mm
axially. Frame ground and anvil seating are measured. A whole-root support
check at the resting pose grounds the timber frame and detects support at
0.8 mm drop. No glue/press-fit support exemptions are supplied. Driven
poses additionally prove capture; this is not a dynamic equilibrium proof.

The instruction scenario runs Lift, Release, Strike and Run with dt=0.05 s
and whole-root interference checked every 0.1 s during their ramps. Both
the geometric tests and scenario run at each lift parameter below. Out-of-
range construction is rejected at 15.9° and 20.1°.

| Run | Result |
| --- | --- |
| Cam, faceted, 18° | 11 passed / 0 failed, 23.09 s after mutation restoration |
| Cam, faceted, 16° | 11 passed / 0 failed, 27.32 s |
| Cam, faceted, 20° | 11 passed / 0 failed, 27.64 s |
| Cam, exact, 18° | 11 passed / 0 failed, 62.96 s |
| Cam, exact, 16° | 11 passed / 0 failed, 62.26 s |
| Cam, exact, 20° | 11 passed / 0 failed, 63.73 s |
| Existing sawmill, faceted / exact | 10 / 10 passed, 1.23 / 12.45 s |
| Existing loom, faceted / exact | 12 / 12 passed, 14.73 / 38.15 s |

All runs use zero volume epsilon. Exact results certify the geometry;
faceted results were the development loop. These are runner method counts,
not a count of every sampled pose or pair. Existing tests were preserved;
no new red-first history is claimed for those unchanged exhibits.

## Reproduction commands

From the gallery root in the installed environment:

```sh
SOLID_BUILD_DIR=_build/cam_hammer_tests machinome test cam_hammer --mesh
SOLID_BUILD_DIR=_build/cam_hammer_16 machinome test cam_hammer --mesh --set lift_angle=16
SOLID_BUILD_DIR=_build/cam_hammer_20 machinome test cam_hammer --mesh --set lift_angle=20
SOLID_BUILD_DIR=_build/cam_hammer_tests machinome test cam_hammer --brep
SOLID_BUILD_DIR=_build/cam_hammer_16 machinome test cam_hammer --brep --set lift_angle=16
SOLID_BUILD_DIR=_build/cam_hammer_20 machinome test cam_hammer --brep --set lift_angle=20
python scripts/gallery.py test hydraulic_sawmill automatic_weaving_loom --kernel faceted
python scripts/gallery.py test hydraulic_sawmill automatic_weaving_loom --kernel exact
python scripts/gallery.py build
python scripts/gallery.py export
python scripts/gallery.py check
python scripts/check_browsers.py
```

Run the build/export phase after any tests sharing its build directories.
Raw local logs are under `_evidence/` and intentionally ignored; the table
records their results. This machine's model.py contains all its node classes,
covered by its root companion and scenario; kinematics.py declares no nodes.

## Publication and browser evidence

The finite build publishes document version 4, four pieces, `phase`/`run`
drivers and Lift/Release/Strike/Run instructions. The cam rotation retains
the symbolic phase + 360*run*time expression, with rest translation
(-60,0,170); the lever retains the symbolic periodic rise/return with rest
translation (0,0,110). Every referenced rigid STL exists; no errors.json
remains. No class touched by this change emits FutureWarning.

The [selected OpenSCAD images](evidence/README.md) were rendered and read,
showing lift isometrically and release along the shaft. An early side image
exposed the obscured shoe and prompted the bearing-column revision.

The finite browser check uses the real `machinome export` manifest and widget,
not a second machine or viewer implementation. It tests the native
instruction ramps, exact editor, slider, run, playback, scrubbing, source
ZIP and document overflow at 1440×1100 and 390×844. CAD-region screenshots
exclude the UI overlays when comparing motion and require an identical
return to the prior manual pose. A moving timeline thumb initially made
whole-canvas equality fail; holding the timeline and comparing only the CAD
region resolved that test-observation issue. Browser console errors,
page errors, failed requests and HTTP errors are all checked.

The all-exhibit browser command completed successfully for sawmill, loom
and cam hammer. All registered models also built successfully, and the
gallery check reported three models with separate OpenSpec roots and a
coherent queue. The cam browser screenshots were inspected at both widths.

## Limits

Samples are not a mathematical continuous collision proof. Contact tests
measure the discretized outline (0.5° chords), not an imagined smooth
historical cam. The independent mesh contact check remains mesh-based even
inside an exact run; exact perturbations and whole-root intersections
provide complementary solid evidence. No elastic deformation, gravity
integration, impact, wear, friction or forging capacity is modeled. Support
is certified at rest; dynamic bearing reactions and manufacturing joinery
are outside this educational commission. Fractional-run timeline looping
restarts at phase and is explicitly described on the exhibit.

## Completion

The machine's four behavioral requirements are synchronized to
`openspec/specs/cam-hammer-demonstration/spec.md`. The completed local cycle
is archived as `2026-09-12-demonstrate-cam-hammer`; queue 010 is done and
queue 020 (rack and pinion) is next. The source archive is regenerated from
the committed gallery for every export, with its revision recorded beside
it. No remote repository was created, pushed or published.
