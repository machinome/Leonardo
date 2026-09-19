# Rack and pinion — turning becomes lifting

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

An original educational reconstruction by **Astra**, made from the gallery's
single continuation prompt as a **machinome demonstration**. A hand crank
turns a twenty-tooth pinion, raising a guided rack, its open hook and a
small weight. Turn it back and the load descends: the contact that converts
rotation into travel is visible and geometrically tested.

[Interactive exhibit](index.html) · [Validation record](docs/validation.md) ·
[Selected images](docs/evidence/README.md) · [Behavioral spec](openspec/specs/rack-lift-demonstration/spec.md)

## Controls

Choose Bottom (phase 0°), Mid-lift (90°), Top (180°), or Run. The phase
control describes one complete lift-and-return cycle; it is not the
pinion's rotation angle. For manual inspection, set run to 0 and move
phase. For animation, choose Run and play the native viewer timeline.

At the default size, Bottom → Mid-lift → Top raises the rack by
0 → 36 → 72 mm and turns the crank by 0 → 68.7549 → 137.5099 degrees.
The second half reverses smoothly. There is no tooth jump or loop reset.
Intermediate run values blend the moving cycle with the selected static
pose, reducing its excursion; they do not change playback speed.
Every advertised combination stays bounded and closes its loop.

The one build knob is `module`, the tooth module in mm. Default 3,
supported 2.5–3.5. The entire stand scales with it; corresponding strokes
are 60–84 mm. This is a CAD build parameter, not a runtime slider.

## Geometry and assumptions

- Modern 20° involute teeth, 20 on the pinion, pitch radius `10*module`.
  Each involute flank uses 20 radial intervals; the tip/root arcs are
  also chordal polygons. The rack's straight flanks are conjugate to
  the underlying analytic involute. The exact kernel certifies the
  authored polygon solids, not an ideal curve that was never built.
- Addendum `module`, dedendum `1.25*module`, and total tangential backlash
  `0.2*module` shared between the teeth of both members. The pose law
  centres that play; contact is demonstrated by perturbation, with no
  torque, elastic contact or backlash dynamics solver.
- Rigid timber stand with twin journal supports and two enclosed rack
  guides. Radial, axial and guide clearances are `0.1*module` nominal.
  Collars capture the crank shaft. Stop shoulders sit `module` beyond
  each demonstrated endpoint; they do not stop the motion by collision.
- The rack and open hook are one connected rigid piece. A separate
  weight's lifting eye crosses the hook in a perpendicular plane and
  seats under downward perturbation. The frame is grounded, and support
  checks hold the crank as an explicit fixture representing an operator.

Holding brake, holding torque, lifting capacity, friction, deformation,
material strength, dynamics and manufacturing joinery are outside this
demonstration. This is not a rated lifting tool. The open hook is not a
latched safety attachment. Geometry samples and static seating are evidence
for the stated poses, not a continuous dynamic safety proof.

## Historical source

The [Museo Leonardiano's Rack and pinion record](https://museoleonardiano.it/en/opera/rack-and-pinion/)
describes a crank, upright rack and hook, referring to Leonardo's
Codex Atlanticus f.998r. Its museum model is credited to Fausto Colombo,
Giovanni Sacchi and Giorgio Valentini (1983). The
[catalogue reference](https://museoleonardiano.it/en/opera/page/5/) is retained
from the commission. Both were retrieved on 12 September 2026; the object
page's canonical Italian path is `/opera/pignone-a-cremagliera/`.

The museum's record establishes the mechanism and manuscript attribution.
Our dimensions, involute teeth, guided frame, collars, hook and load are
original educational choices. No museum mesh, traced asset, historical
dimensions or invention-priority claim is used. The folio image itself
was not independently interpreted for this build.

## Build and verify

From the gallery root, with the environment in the root README activated:

```sh
machinome build rack_and_pinion
SOLID_BUILD_DIR=_build/rack_tests machinome test rack_and_pinion --faceted
SOLID_BUILD_DIR=_build/rack_tests machinome test rack_and_pinion --exact
SOLID_BUILD_DIR=_build/rack_25 machinome test rack_and_pinion --exact --set module=2.5
SOLID_BUILD_DIR=_build/rack_35 machinome test rack_and_pinion --exact --set module=3.5
python scripts/gallery.py export rack_and_pinion
python models/rack_and_pinion/scripts/check_browser.py
python scripts/check_browsers.py
python -m http.server 8769 --bind 127.0.0.1
```

Open `http://127.0.0.1:8769/models/rack_and_pinion/`. The browser check starts
and stops an ephemeral server by itself when no `--url` is passed. It uses
the actual exported viewer, tests native controls and CAD pixel changes,
checks an identical return to a prior pose, and covers desktop/narrow views.
Use independent test build directories to avoid another session's model
publication removing test ingredient artifacts. Generated exports stay
ignored. Re-export after committing so source.zip contains the final source.

The tested environment uses post-0.6 local machinome, local viewer 0.1.0
and CadQuery 2.7. Published machinome 0.6 alone does not supply this API.
See the [gallery environment record](../../docs/consolidation.md).

## Commission

Queue `020-rack-and-pinion` and the gallery's commission delegated this
design, implementation, evidence and local commits. The exact prompt was:

> See the projects/Leonardo. Build next project.

This machine's OpenSpec is local to this directory. The gallery's purpose,
licensing and publishing authority remain as recorded in the root brief.
