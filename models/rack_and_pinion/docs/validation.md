# Rack-and-pinion validation — 12 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Scope and environment

Queue 020 commissions this machine; planning commit `6160f9d` records the
brief and exact continuation prompt. Tested implementation source:
`e0edd8092cf588517c967a30eb6b5463d5a38f94`. The tests and inspections ran
on these same source bytes before that commit; committing did not change
them. The completion commit changes only evidence, queue/task status and
archive placement, not the tested model, tests, exhibit or browser script.
Only the new exhibit and shared registry/documentation entries are changed.
The pre-existing untracked `screenshots/` directory is preserved.

| Dependency | Tested content |
| --- | --- |
| machinome | `6e41f2da132a8604f9b68895967247fb8876fc4d`, package metadata 0.6.0 |
| machinome-viewer | `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`, local 0.1.0 |
| molejo | `e76c9039cf906cfc0005324d78ccee7116e0ff4a`, 0.2.0 for existing exhibits |
| CadQuery | 2.7.0 |
| trimesh | 4.4.9 |
| Playwright | 1.62.0, installed Chromium |

All three dependency repositories were clean. Linux, Python 3.12, workspace
environment `../../.venv`. This uses the post-0.6 declarative motion API;
published machinome 0.6 alone is insufficient. The viewer is locally
founded, not described as published. No dependency was modified.

The complete shared machinome API and machining manuals informed the
joint, relation and geometric-contract design. Context7 supplied current
CadQuery polygon/extrusion and Playwright iframe documentation. Historical
research reached the museum's object page via HTTP after the web reader
timed out; the object page verified the same mechanism and folio recorded
in the queue. Sources and historical limits are in the machine README.

## Red, iteration and deliberate mutation

The companion tests were written before model.py. The first faceted
command exited 1 because the mapped node file did not exist. The initial
complete model then ran 11 methods: 4 passed, 7 failed. The root detected
6412.5 mm³ of stand/weight interference. The guide-free test detected
21.6 mm³ when the rack moved 0.15 mm sideways, and the eye was too close
to the hook to allow its specified free play.

The weight was narrowed in Y, the backing rib brought fully within the
rack's width, and the eye given a larger bore-side gap while preserving
overlap with the weight block. All 11 methods then passed. Isometric
inspection led to one further change: the right posts moved outward,
with their guide supports extended, revealing the hook/load. The final
geometry passed the same unchanged contracts.

The deliberate mutation changed the actual pinion-to-slide relation's
pitch radius from `10*module` to `9*module`. This is a 10% transmission
error, not a change to a shared input knob. It produced 4 passing and
7 failing methods. The intended tooth-pitch free-play test failed with
0.84189265 mm³ interference under a -0.18 mm displacement; the whole-root
sweep detected 8.01845480 mm³ pinion/rack intersection. The independent
travel measurement was wrong by 0.48230855 mm already at phase 30°.
The top stop, static support, control combinations and instruction scenario
also failed. Restoring the relation returned the full suite to green.

Connectedness, pinion size, guides and journals stayed green during that
mutation: they are structurally blind to the transmission ratio. The
transmission and engagement contracts carry that responsibility.

## Measured geometric contracts

Four top-level rigid solids are checked: frame, pinion with shaft/crank,
rack with hook/stops, and weight with eye. Whole-root connectedness and
zero-positive-volume interference remain active. No volume epsilon,
excluded collision pair, removed part or narrowed root is used.

- The whole cycle has 37 root-interference poses. Nine additional poses
  cover the endpoints, 0.01° reversal neighborhoods and intermediate
  positions. Eighty phase/run/time combinations test all advertised
  control corners and intermediate run values; sixteen loop returns
  compare actual load vertices at t=0 and t=1.
- Eleven phases independently measure rack endpoints, weight bottom and
  the actual crank-grip centre. Expectations use the root module and
  independent radian arithmetic, never the model's generated motion law
  or joint values. The default rack rises 72 mm, its bottom from 96 to
  168 mm; the weight bottom rises from 27 to 99 mm. Mid-lift gives
  36 mm travel and a 68.754935° crank turn. Dimensional tolerance is 0.01 mm.
- Nineteen evenly spaced pinion angles cover a complete 18° tooth pitch.
  At each, the full root clears and the rack is free at ±0.06*m but
  blocked at ±0.18*m along Z against the pinion. These independently
  bracket the designed ±0.1*m centred tangential play. At m=3 the
  perturbations are ±0.18 and ±0.54 mm respectively.
- At seven lift poses, the rack is free at ±0.05*m and blocked at ±0.3*m
  laterally and axially against the guide frame. The nominal guide gap
  is 0.1*m. Five pinion poses similarly prove both radial directions and
  collar capture along the shaft, using the complete pinion.
- At Bottom and Top, the rack is free 0.5*m farther toward its stop and
  blocked by 1.5*m. The demonstration endpoints remain m short of the
  shoulders' physical contact; the animation does not collide with them.
- At four lift poses, the load clears the hook, is free within ±0.05*m
  vertically and blocked after 0.8*m downward. A whole-root support check
  at each pose grounds the timber frame and the held pinion explicitly.
  It finds the rack/load support chain with max_drop=0.8*m and no
  glue/press-fit exemptions. This models an operator holding the crank,
  not a self-locking gear or a brake.
- Root size measurements verify the base width and pinion addendum radius;
  out-of-range module values 2.49 and 3.51 refuse construction. Default
  and both advertised size boundaries run the same whole suite.
- The scenario runs all four instructions, dt=0.05 s, checking root
  non-interference every 0.1 s through their ramps and the final driver
  values. It also runs at each advertised size boundary.

| Rack run, final geometry | Result |
| --- | --- |
| Faceted, module 3 | 11 passed, 0 failed; 9.62 s |
| Faceted, module 2.5 | 11 passed, 0 failed; 12.52 s |
| Faceted, module 3.5 | 11 passed, 0 failed; 11.87 s |
| Exact, module 3 | 11 passed, 0 failed; 62.09 s |
| Exact, module 2.5 | 11 passed, 0 failed; 71.03 s |
| Exact, module 3.5 | 11 passed, 0 failed; 69.27 s |

Counts are runner methods, not individual sampled poses or pair tests.
Faceted checks were the development loop; exact results certify the
authored solids. All comparisons use zero volume epsilon.

## Reproduce

Activate the documented environment and run from the gallery root:

```sh
SOLID_BUILD_DIR=_build/rack_tests machinome test rack_and_pinion --faceted
SOLID_BUILD_DIR=_build/rack_tests machinome test rack_and_pinion --exact
SOLID_BUILD_DIR=_build/rack_25 machinome test rack_and_pinion --exact --set module=2.5
SOLID_BUILD_DIR=_build/rack_35 machinome test rack_and_pinion --exact --set module=3.5
python scripts/gallery.py check
python scripts/gallery.py build
python scripts/gallery.py export
python scripts/check_browsers.py
```

For regression during another exhibit's active session, each existing
model was tested on both kernels with its own `SOLID_BUILD_DIR` set to
`_build/rack_regression_<model>` and `PYTHONPATH` set to this gallery root.
This avoids publication sweeping the fusion-ingredient artifacts a test
is still reading. Initial rack tests used the direct module reference;
after registration the name `rack_and_pinion` selects that same root.

## Viewer and images

The export contains document version 4, four pieces and 361 frames at
30 fps. Phase/run, four named instructions and symbolic degree cosine
bindings are preserved. The pinion rotates about -Y at z=240 mm and
drives the carriage by 0.5235987755982988 mm per degree. Every manifest
STL exists; the finite builds emit no new FutureWarning.

The [selected OpenSCAD images](evidence/README.md) were opened and
inspected at mid-lift and top. Actual browser captures were also inspected
at 1440×1100 and 390×844. The finite script interacts with the exported
viewer's native instruction ramps, exact entry, phase slider, run slider,
timeline play/pause and scrubber. It compares the CAD region between the
control overlays, so changing a readout cannot masquerade as movement.
Returning manually to phase 90 gives identical CAD pixels. The timeline
end also returns identical pixels at run=0.5. Console errors, page errors,
failed requests, HTTP errors, missing assets and document overflow fail
the check. It checks the downloadable archive endpoint as well.

## Limits

Finite samples are not a continuous collision proof. The involute and
hook are intentionally chordal educational solids. Exact-kernel tests
certify those solids; vertex measurements and browser images remain
mesh-based observations. There is no elastic contact, physical backlash
take-up, friction, dynamics, brake or capacity calculation. Grounding the
held pinion represents an external torque source. Fixture joinery and
the open hook's safety are not manufacturing recommendations.

## Completion record

| Existing exhibit regression | Faceted | Exact |
| --- | --- | --- |
| Hydraulic sawmill | 10 passed, 0 failed; 6.79 s | 10 passed, 0 failed; 13.55 s |
| Automatic weaving loom | 12 passed, 0 failed; 16.79 s | 12 passed, 0 failed; 24.38 s |
| Cam hammer | 11 passed, 0 failed; 23.40 s | 11 passed, 0 failed; 46.08 s |

These untouched model/test files retain their existing evidence. No new
red-first history is claimed for them. All four roots built successfully;
the registry check reports four models, distinct machine OpenSpec roots
and a coherent queue. `python scripts/check_browsers.py` exited 0 after
all four registered exhibit checks. The rack's browser check also passed
on its own; the inspected viewport captures are recorded above.

The four behavioral requirements are synchronized to the machine's
baseline spec; direct comparison confirms every requirement and scenario
matches the delta, and strict OpenSpec validation passes. The completed
cycle is archived as `2026-09-12-demonstrate-rack-and-pinion`. Queue 020
is done; queue 030, the compound pulley, is next.

All four exhibits were re-exported from the tested implementation commit.
Each source-revision.txt matched that revision, and each source.zip was
opened to verify byte-for-byte inclusion of this machine's model, tooth
profiles and tests. This supersedes the preliminary browser download
smoke, whose ZIP came from the then-current planning commit. The completion
export refreshes the archives again to include this final record.
Generated exports remain ignored. Nothing was pushed or published.
