# Swivel crane evidence

<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->

Completed 12 September 2026 under queue item 040 and planning commit `cbed3e9`.
Tested model, companion tests, exhibit and browser-check source:
`b144465116d2302c6e4fc293f2b2d0728bdd8d34`. The later completion commit only
records that revision, archives the cycle and updates queue status; it does not
change the tested mechanism or UI. Exact session prompt:
“See the projects/Leonardo. Build next project.”

## Final mechanical regression

`python scripts/gallery.py check` passed: six models, separate machine-owned
OpenSpec roots, one repository, coherent queue. `python scripts/gallery.py build`
and `python scripts/gallery.py export` built and exported all six roots.
The final crane was rebuilt, re-exported and re-rendered after refining its thread.

Exact runs used `python scripts/gallery.py test --kernel exact`, followed by
`SOLID_BUILD_DIR=_build/swivel_crane solid test swivel_crane --exact` after the
crane-only thread correction. None of the five other models changed.

| Model | Exact result | Reported test time |
| --- | --- | --- |
| Hydraulic sawmill | 10 passed, 0 failed | 11.36 s |
| Automatic weaving loom | 12 passed, 0 failed | 21.29 s |
| Cam hammer | 11 passed, 0 failed | 35.50 s |
| Rack and pinion | 11 passed, 0 failed | 71.47 s |
| Compound pulley | 10 passed, 0 failed | 49.76 s |
| Swivel crane, final ruled thread | 12 passed, 0 failed | 333.07 s |

Total: 66 passing exact tests, with no remaining failures. The final crane's
separate faceted run passed all 12 tests in 24.44 s, volume epsilon 0 mm³.
There are no advertised crane build parameters; its physical driver boundaries,
intermediates and combinations are covered below. Geometric tolerances in the
motion measurements are not collision allowances.

## Measurements

The companion tests measure world-space vertices, independently transform the
stone about world Z, and check fixed-footing invariance. They cover 36 physical
control combinations, endpoints, intermediate values and returning to a prior
pose. Screw vertices rotate by the independent lead formula; measured trolley
travel, 0.12 mm free axial play and blockage at 0.85 mm cover eleven stations
including nine positions within the first turn.

Rope tests recover the actual centreline from the public ring-major mesh.
They measure segment endpoints, circular radii and swept angles, compare total
length with 230+27π mm and verify drum take-up against the stone's measured
rise. Eight heights include both boundaries. Separate checks cover rope/rigid
interference at 27 combinations, tube connectedness and watertightness,
nonadjacent route separation, socket attachment and groove capture.

Whole-root rigid connectedness and non-interference are active. The latter
sweeps 17 full-cycle poses, the Cartesian input combinations, and a denser
trajectory with neighborhoods around each transition. Additional checks cover
mast, screw, guide rods, sheaves and load capture, declared support fixtures,
actual drum/sheave rotation, fractional demonstration blending and named
instruction ramps.

## Development findings

- Initial red run: the intentionally empty footing scaffold failed the screw
  test because slew/traverse/hoist/run were undeclared. The single-solid
  non-interference pass at that stage was vacuous, not assembly evidence.
- Early full geometry exposed footing reinforcement intruding into its bore,
  overlong trolley axles touching the jib, and a lifting eye with no upward
  clearance. Geometry was corrected; no collision epsilon or narrowed root.
- CAD kernel cutting-order defect: cutting the nut bore before the helical
  pocket silently left the thread pocket uncut. A direct 24×50×18 mm blank
  stayed at 20173.277 mm³ after that attempted cut, while thread-first then
  bore gave 19647.108 mm³. The exact Boolean incorrectly reported zero
  overlap for the failed construction; mesh engagement exposed about 322 mm³
  interference. The final nut cuts its thread before its bore. Both kernels
  must pass on this final construction. No dependencies were edited.
- Deliberate central-mechanism mutation: changed the screw relation from
  `ratio=-360/12` to `ratio=360/12`. Faceted run: 7 passed, 5 failed, 19.94 s.
  The intended screw-vertex expectation failed at 1 mm traverse (up to 17 mm
  vertex error); whole-root interference, mixed coordinates, trajectory and
  scenario checks also failed. Reverted the sign: 12 passed, 0 failed, 25.01 s,
  faceted kernel with zero volume epsilon. Rope-only tests are structurally
  blind to screw handedness and correctly stayed green during that mutation.
- The first final exact run passed 11 tests but failed the screw blockage
  test: the periodic helical BREP returned no intersection at ±0.85 mm,
  despite the mesh's visible engagement. Replaced the periodic surface with
  original ruled thread sections at 20° intervals, retaining the 12 mm lead,
  clearances and independent fit contracts. The short threaded region is now
  x=60–168 mm. A direct exact probe then measured 0 volume at 0 and 0.12 mm,
  and 43.493 mm³ at both ±0.85 mm. This is a modeling workaround inside the
  project; no external kernel or framework changes were made.
- Coarse thread tessellation (0.06 mm / 0.4 rad) introduced a measured
  0.015 mm³ mesh interference despite the exact running gap. Retained the
  strict zero-epsilon checks and refined both mating parts to 0.025 mm /
  0.2 rad: all 12 faceted tests passed in 24.44 s on the final ruled geometry.

## Rendering and export

Inspected default-OpenSCAD snapshots, all 1400×1100:

- [Isometric](isometric.png), time 0.28, `--autocenter --viewall`: complete
  footing, supported mast/jib, trolley, rope path and suspended stone are visible.
- [Screw detail](screw.png), time 0.29,
  `--camera 330,-75,335,115,-15,250`: a deliberate close view along the screw,
  showing its entry into the threaded trolley and the adjacent rope grooves.
- [Down the mast](mast.png), time 0.58,
  `--camera 110,0,850,110,0,180 --viewall`: rotated jib and offset hoist lane.

Example command, from the gallery root with the workspace environment active:

```sh
SOLID_BUILD_DIR=_build/swivel_crane solid snapshot swivel_crane \
  -o models/swivel_crane/docs/evidence/isometric.png \
  --autocenter --viewall --time 0.28 --imgsize 1400x1100
```

`gallery.py build` passed for all six roots. Inspected the crane's
`_build/swivel_crane/swivel_crane/viewer.json`: version 4, four drivers, five
instructions, all nine rigid instances' assets present, inherited Z slew,
local-X screw/traverse and local-Y drum/sheave expressions preserved.
`gallery.py export swivel_crane` produced the actual standalone viewer.

The finite `models/swivel_crane/scripts/check_browser.py` exercised the actual
export in headless Chromium at 1440×1200 and 390×1000. It checked all named
placement stages, independent edits of all three physical inputs while holding
the other values, the traverse slider and an identical pixel return to pickup
at both widths. Desktop checks additionally exercised playback, timeline
scrubbing and pixel-identical loop closure. Pixel comparisons exclude the
controls, so changing labels alone cannot satisfy motion checks.

Initial export auto-framing cropped the slewed jib on a narrow viewport.
The exhibit now mounts the shipped widget with an envelope-sized camera, with
the narrow model lowered below the taller controls. All geometry, simulation,
drivers and playback still belong to the real export. The selected browser
images show the complete crane, native controls and explanatory page without
horizontal overflow. Local links and source archive returned successfully;
there were no console, failed-request or asset errors.

`python scripts/check_browsers.py` then passed all six registered browser
checks, including the crane's final camera layout, within the runner's unchanged
180-second per-exhibit limit. Inspected selected final captures:
[desktop](browser-desktop.png) and [narrow](browser-narrow.png).
After committing `b144465`, regenerated the crane export and verified its
ZIP integrity, revision marker, and byte-for-byte source equality for the model,
tests, exhibit, viewer host and finite browser check. Generated exports and
archives remain ignored and contain committed source, not private working files.

## Environment

Checked 12 September 2026 on Linux with Python 3.12.3, CadQuery 2.7.0,
molejo 0.2.0 and Playwright 1.62.0 / its installed headless Chromium.
The editable solid-node package reports 0.6.0 but includes post-release
declarative API changes. The local viewer reports 0.1.0; it is founded, not
published. These are checkout-specific results, not evidence that published
0.6.0 alone supplies every API used here.

Dependency content revisions (all three worktrees clean and unmodified):

- solid-node: `6e41f2da132a8604f9b68895967247fb8876fc4d`
- solid-node-viewer: `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`
- molejo: `e76c9039cf906cfc0005324d78ccee7116e0ff4a`

## Evidence limits

The initial-pose-relative rotation tests alone cannot detect a common offset
of all components; the absolute carrier and rope endpoints supply the layout
anchors. Rigid integrity excludes flexible rope, hence its separate checks.
Samples establish a tested envelope, not a continuous formal collision proof.
Ideal grounding, held mast/trolley and taut-rope suspension are explicit test
fixtures; geometric tests do not certify material strength or structural loads.
