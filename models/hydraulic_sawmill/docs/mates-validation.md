# Named attachment frames — 29 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot requested simpler, presentable sawmill source using frames and
mates, an unambiguous name for the stationary structure, and a PEP 8 test.
This is a behavior-preserving project refactor, not a new mechanism or an
OpenSpec interface change. The existing reconstruction and carpentry
contracts remain authoritative.

## Source and environment

The comparison baseline is gallery commit `35de674` (the September 28
evening history after the pilot's timestamp adjustment). No geometry,
kinematic law, control, historical claim or public exhibit label changed.
The implementation is the source tree committed with this record.

- Framework checkout: `bf24687da524264c43dcecad76527ce71431e343`.
- Viewer checkout: `40031a5297d034405b69cbaeec7f252877230e42`.
- Installed distribution metadata: machinome 0.7.0, viewer 0.7.0,
  molejo 0.2.1 and CadQuery 2.7.0. These editable distribution labels do
  not identify the available development API; use the content revisions.
- Style tools: pycodestyle 2.15.0 and Black 26.5.1.

## What changed

`MillStructure` replaces the mechanical class named `Frame`. Its named
stations carry the saw, carriage and feed. Each mating part declares its
own connector. Repeated shaft positions share one bearing frame; rocker
and holding-pawl positions come from their fixed pins' journals. Moving
mates reference the existing scalar joints, preserving their names and
laws. Rigid mates preserve the rod's and feed links' multiple freedoms.

The saw mechanism now uses its crank-axis origin locally; its single
root mate supplies the height. This removes the repeated global height
from the rod and sash placements. Shape coordinates inside individual
parts and changing rope profiles remain geometric data.

The current framework refuses a fixed mate end on a sibling placed by
another mate. Consequently the two fixed pulley axles retain explicit
rest placement, and the moving rollers mate to their journals. Repeated
wheel and end-grain placement retains its existing loops.

`test_style.py` checks all gallery Python source against `setup.cfg`,
including new untracked files and excluding ignored build output. The
sawmill's normal test suite invokes the same check on its own sources.
The checker was observed failing on a 77-column docstring and then
passing after it was shortened. No additional style exclusions were added.

## Verification

- Before editing, every leaf's world-space mesh vertices were recorded
  at 0, 0.5, 1, 2, 3, 730 and 1460 seconds. After the refactor, the same
  tree paths, vertex arrays and seven poses agreed with zero relative
  tolerance and an absolute tolerance of 1e-7 mm.
- Deliberately changing the main bearing placement to `AXLE_Z + 10`
  made the existing whole-machine integrity test fail: waterwheel versus
  crankshaft, 5123.0518 mm³ intersection on the faceted kernel. Restoring
  the placement restored the default 43/43 faceted result.
- Carpentry and disassembly: 11/11 faceted and 11/11 exact checks passed.
- Full sawmill regression: 43/43 exact checks passed in 1284.08 seconds,
  including whole-root integrity sweeps, rope clearance and attachment,
  tooth transitions, captured journals and the complete timber course.
- Whole-gallery PEP 8, sawmill Black check, gallery catalogue validation
  and whitespace checks passed.
- OpenSCAD isometric view at 0.5 seconds and shaft-axis view at 2 seconds
  were rendered and inspected. Local images are under
  `_evidence/hydraulic_sawmill/mates-{isometric,shaft}.png`.
- Readout verification passed: 721 stroke/feed samples and 2921 full-pass
  feed samples match the actual CAD meshes.
- At kerf=2 and kerf=5, the faceted suites each reported 42/43: the uncut
  insert's touching boundary against the left timber half produced
  1.364e-12 and 1.137e-12 mm³ of mesh intersection respectively. The
  unchanged seven-position contact test passes on exact solids at both
  values. No epsilon or geometric gap was added to conceal this mesh
  result; the exact verdict decides that contact.
- The export contains 126 nodes, 101 rigid asset references and seven
  flexible leaves. All referenced assets exist, and its version-4
  document retains the 1460-second loop and empty driver/instruction
  tables.
- The existing browser acceptance script passed for desktop and narrow
  viewports: all five views, playback, returning to a prior pose,
  mechanism reveal, assembly navigation, complete timber travel and
  measured holding-pawl pixels. The carpentry study also moves and
  reassembles, its stage instructions work, and its 24-member cutting
  book and assets load. No console or network failures were reported.

## Repeating the checks

From the gallery root, with its development environment active:

```sh
python -m unittest test_style
black --check test_style.py models/hydraulic_sawmill
machinome test hydraulic_sawmill --exact
machinome test models/hydraulic_sawmill/frame.py --exact
python models/hydraulic_sawmill/scripts/readouts.py --check
python scripts/gallery.py check
python scripts/gallery.py export hydraulic_sawmill
python models/hydraulic_sawmill/scripts/frame-study.py
python models/hydraulic_sawmill/scripts/check-browser.py
```

The full exact regression was run at the default 3.2 mm kerf. Boundary
values received full faceted regressions plus exact reruns of the
seven-position insert-contact test, as distinguished above. No claim of
new historical evidence, manufacturing validation or physical simulation
is added by this refactor. Other gallery mechanisms were not changed.
