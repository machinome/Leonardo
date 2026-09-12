# Validation record

Validated 12 September 2026 in the LibreSolid Studio workspace.

## Environment

- solid-node development checkout `518bed1` (package metadata 0.6.0; this
  checkout includes post-release declarative joints and relations).
- solid-node-viewer checkout `6fb082b`, package 0.1.0, viewer API 7.
- CadQuery 2.7.0, molejo 0.2.0, Playwright 1.62.0, Python 3.12.
- Linux; browser acceptance in headless Chromium with SwiftShader WebGL.

## Mechanical evidence

The scaffold was created with `solid new Leonardo-hydraulic-sawmill`. The CLI
normalized the name to underscores; its generated directory was moved to the
pilot's requested hyphenated path and initialized as an independent Git repo.

Before implementing the machine, four behavior tests failed against the starter
solid. The default scaffold's connectivity and interference checks were kept;
the interference check was expanded to 33 poses across the four-turn pass.

The final root suite exercises every part in its assembled context:

| Contract | Coverage |
| --- | --- |
| Connected rigid pieces | Every rigid piece, exact solid count |
| No solid interference | Whole model, 33 poses across four cycles |
| Blade clearance | Both timber halves, 13 poses in one cycle |
| Crank engagement | Rod free within 0.3 mm and blocked at 1.5 mm lateral displacement; 9 poses |
| Sash guides | Free within 0.3 mm and blocked at 1.3 mm lateral displacement; 9 poses |
| Saw stroke | Measured 48 mm between dead centres |
| Timber feed | Downstroke dwell, return advance, 8 mm per turn |
| Repeatability | Return to phase 73° after phase 1100° reproduces mesh bounds |
| Keyed drive | Wheel free at 1° play and blocked at 10° relative rotation |
| Seated ratchet pawl | Free at 0.3° play, blocked at 5° in the driving direction |

Default (`kerf=3.2`, `paddles=16`): **10 passed, 0 failed**, exact kernel,
13.07 seconds reported by the test runner. Boundary configuration (`kerf=2`,
`paddles=24`): **10 passed, 0 failed**, exact kernel, 9.66 seconds.
Both configurations also passed the faceted development checks.

Mutation evidence: changed the connecting rod's orbit binding from `angle` to
`angle + 12` in model code. The whole-model interference and crank pin
engagement tests failed (8 passed, 2 failed). Restored the code and confirmed
green. The stroke and feed checks remained green under this mutation: they do
not prove crank-pin alignment; the geometric engagement checks do.

## Visual and browser evidence

Inspected OpenSCAD snapshots of the final model:

- `evidence/isometric.png`: oblique view at timeline 0.065.
- `evidence/shaft-axis.png`: along the waterwheel shaft at timeline 0.125.

`scripts/check-browser.py` opens the actual exported assembly and checks:
WebGL canvas presence; a changed rendered image after scrubbing; the 450° pose
and 8 mm feed readout; mechanism reveal; camera selection; reset; advancing and
pausing playback; source archive availability; and a 390 px mobile viewport
without horizontal overflow. There were no page errors or HTTP failures.
Desktop, drive-detail and mobile screenshots were saved under `evidence/` and
visually inspected. The exhibit wraps the installed viewer through its public
mount, visibility and time APIs; it carries no alternate CAD renderer.

Generated logs and images are retained locally under `evidence/`, ignored by
Git. Build/export artifacts are reproducible and likewise ignored.

## Limits

This is a geometric and kinematic exhibit. Forces, friction, water flow,
material removal, structural loading and manufacturing validation are outside
the evidence. Bearings and the log are depicted with small assembly clearances;
gravity/support equilibrium and retention hardware are not certified.

The indexed pawl carrier is independently prescribed from the common phase.
Its tooth engagement is checked, but it is not a complete reconstruction of a
physical linkage transmitting work from the saw to the feed mechanism. Its
reset lift is prescribed rather than resolved from spring/contact forces.
The flexible haul rope is checked visually; the rigid-piece interference net
does not certify its drum winding or attachment under tension.

The suite samples motion; it is not a continuous swept-volume proof. Browser
testing used Chromium software rendering, not a performance benchmark or a
cross-browser compatibility claim. No framework or viewer code was changed.
