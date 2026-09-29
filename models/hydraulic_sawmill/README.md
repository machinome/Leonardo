# Leonardo’s hydraulic sawmill

The fixed frame is now **24 individually cut oak timbers and 34 wooden pins**,
with matching mortises, tenons, housings and bored joints. A reversible
carpentry study uses the same parts as the working machine; its cutting book
supplies stock sizes, grain directions, machining coordinates, four views and
exact STEP solids. See [construction and provenance](docs/carpentry.md) and
the [current validation](docs/carpentry-validation.md).

A connected historical reconstruction of the hydraulic saw in Milan’s Museo
Nazionale Scienza e Tecnologia, IGB-37, researched against its photographs and
Leonardo’s Codex Atlanticus 1078r. Water passes **under** the paddlewheel.
The actual CAD assembly animates in the browser.

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
Vibecoded by Astra for the [Leonardo gallery](../../README.md).
The pilot commissioned this more complete reconstruction on 12 September 2026;
it supersedes the earlier simplified sawmill’s scope, not its preserved history.
The 20 September correction follows the three supplied museum photographs:
teeth face +X, the gear sits across the timber from the waterwheel, and an
extended iron axle runs through two wooden bearings to its square-fitted crank.

## Open and explore

From the Leonardo repository root, in the workspace environment:

```sh
source ../../.venv/bin/activate
python models/hydraulic_sawmill/scripts/demo.py
```

Open **http://127.0.0.1:8769/models/hydraulic_sawmill/**.
Use `--build-only` for a finite export, `--no-build` to serve an existing
export, or `--port 8770`. Stop the local server with Ctrl+C.

Play/pause, speed, the full-pass timeline, five camera views and mechanism
reveal let you follow each transmission. The feed view looks at the rear
linkage; restore the frame to understand the fixed pivots. Reduced-motion
preferences start paused. The standard viewer at
`/export/hydraulic_sawmill/` exposes the same timeline and an assembly sidebar.
There are no machine input drivers or instruction buttons. Open “Explore the
assembly” to navigate frame, water drive, saw, timber carriage and feed;
the timber and rollers have their own subgroups. The fixed saw tower and
horizontal bed frame expand into individual timbers, with separate pins.

Select **Open the carpentry study** for the frame-only assembly at
`/export/hydraulic_sawmill-frame/`. Its 0–11 slider and numbered stage buttons
withdraw pins and separate the fitted members in erection order; reverse the
sequence to assemble. The adjacent **Cutting book** link opens
`/export/hydraulic_sawmill-frame/carpentry/`. These are frame study controls,
not extra inputs to the operating saw.

## What is reconstructed

- Individually joined table legs, upper rails, low stretchers, end crossmembers,
  running rails, feed bearers, grooved tower, crosshead, shoulder ties and shaft
  seats. Staggered corner tenons retain wood between mortises; running-surface
  pin heads are recessed below the rollers.
- Low descending channel and undershot wheel with eight paddle stations,
  rims, spokes, keyed shaft, bearing journals and retaining collars.
- Crank, captured connecting rod, two-post grooved guide, moving saw sash,
  toothed blade, pinned attachment forks and a set tension nut.
- A closed saw-journal tie and long rocking lever with its short drive arm,
  pivoted driving hook, opposing holding pawl and 32-tooth ratchet.
- Rope winding over itself in a fixed plane beside the ratchet on its bare axle, lower pulley inside the opposite
  saw upright, and compound winding shaft inside the bed. Its large winding
  section drives a thin central take-up, with a second rope over the upper
  roller to the carriage's top centre.
- Continuous bed rails and a closed rectangular carriage with both end
  crossmembers, bored rope ties, flanged rollers, retained axles and log cradles.

A 24 mm crank throw gives a **48 mm stroke**. One downward pulling stroke advances one
ratchet tooth: **0.334454 mm of carriage travel on the first turn**. Feed derives
from the winding radii, growing input coil, helical output lengths and changing free spans; it is not
constant per turn. The full pass takes **365 turns / 1460 seconds (24m 20s)**,
advancing **341.017588 mm**. The carriage dwells
during the recovery upstroke. The hook pulls rather than pushes; rollback
reaction seats the opposing holding pawl against the locking tooth face.

The **320 mm timber** starts wholly before the teeth and finishes beyond the
blade. Slotted cradles support it throughout; all four rollers stay on the
modestly extended rails. The timber is 30 mm shorter than the original,
while the table grows from 610 to 720 mm. Blade entry clearance is 1 mm;
exit clearance is about 5.02 mm. A shrinking molejo insert fills the uncut kerf ahead of the
teeth and reveals the split behind them, disappearing at completion.
The sole geometric parameter is `kerf`, 2–5 mm (default 3.2 mm). Paddle count
is fixed to the reconstruction, not exposed as an arbitrary variant.
A loop restart is visibly labelled as a replay reset, not automatic reversal.

## Historical and physical limits

The Milan object is a **1952–1953 interpretative model**, not a surviving
Renaissance machine. Its photographs establish the mechanism arrangement;
hidden joints, fasteners and internal dimensions remain documented choices.
This is not a dimensionally certified replica or a claim that Leonardo
invented hydraulic sawing.

The linkage closes geometrically. Pawl seating is constructed from the tooth
profiles, with running clearance; gravity, friction and torque are not solved.
The input rope builds radially in a fixed plane just inside the ratchet;
it does not traverse the axle into the rocker. The ropes assume maintained
tension and orderly stacking/winding; slip, slack and winding stability are
not solved. No unphotographed guiding hardware is added. Water and material removal are
illustrative, and the timber is assumed secured. The rigid halves have an
open kerf; the flexible insert supplies the cutting impression. Its last
0.1 mm collapses to zero area, not a remaining solid or sawdust simulation.
The tension screw is shown
set, without helical thread or blade-strain simulation. Stopping water,
releasing pawls and reloading remain manual operations, explained in the
exhibit; no hidden automatic return is invented.

See the [source-by-source reconstruction record](docs/reconstruction.md),
[design](docs/design.md) and [photographed-drive validation](docs/transmission-validation.md).
The [full-pass validation](docs/full-pass-validation.md) predates the transmission correction.
The [previous validation](docs/validation.md) records the superseded four-turn exhibit.

## Reproduce the evidence

Use the workspace's current development checkouts, including support for
mates that reference an existing child joint. Package version labels alone
do not identify that capability. Exact tested revisions are recorded in the
[placement-refactor evidence](docs/mates-validation.md). Install the
gallery's `dev` extra for the PEP 8 test.

```sh
machinome build hydraulic_sawmill
python -m unittest test_style
machinome test hydraulic_sawmill --faceted
machinome test hydraulic_sawmill --exact
machinome test hydraulic_sawmill --set kerf=2 --exact
machinome test hydraulic_sawmill --set kerf=5 --exact
machinome test models/hydraulic_sawmill/frame.py --exact
python models/hydraulic_sawmill/scripts/readouts.py --check
machinome snapshot hydraulic_sawmill -o models/hydraulic_sawmill/docs/evidence/transmission-isometric.png --autocenter --viewall --time 0 --imgsize 1400x1000
python scripts/gallery.py check
python models/hydraulic_sawmill/scripts/demo.py --build-only
python models/hydraulic_sawmill/scripts/check-browser.py
python scripts/check_browsers.py
```

The finite browser script serves its own temporary localhost server unless
`--url` supplies one. Exports contain committed source: regenerate after
committing source changes. Generated meshes, research downloads and browser
batches are ignored; a small selected [evidence set](docs/evidence/) is tracked.

## Reading the assembly code

`MillStructure` names the stationary timberwork, leaving `Frame` for a
Machinome attachment coordinate system. Its saw station, carriage entry and
feed station place the major assemblies with `.on()` mates. Parts declare
their own bores, pivots and journals; for example:

```python
rocker_mount = rocker.pivot.on(rocker_pin.journal, rocker.turn)
roller_mount = upper_roller.bore.on(upper_pin.journal, upper_roller.spin)
```

These mates preserve the existing joints and motion laws. Fixed axle
placements and repeated wheels still use short placement loops where the
current interface needs them. Rope profiles retain the coordinates that
describe their changing shape.

The normal sawmill test run includes PEP 8 checks for its Python sources.
`python -m unittest test_style` checks every gallery Python source, including
new files, using the repository's 79-column code and 72-column prose limits.

Primary reference: [Milan museum hydraulic saw](https://www.museoscienza.org/en/collections/objects/hydraulic-saw).
The [detailed catalogue](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica)
and [Atlanticus 1078r](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/1078-r/)
are linked and assessed in the research record. Museum photos and manuscript
scans are not redistributed.

The [machine-owned OpenSpec](openspec/) preserves both the original
retrospective record and this commissioned reconstruction cycle.
