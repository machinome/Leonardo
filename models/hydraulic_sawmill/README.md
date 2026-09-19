# Leonardo’s hydraulic sawmill

A connected historical reconstruction of the hydraulic saw in Milan’s Museo
Nazionale Scienza e Tecnologia, IGB-37, researched against its photographs and
Leonardo’s Codex Atlanticus 1078r. Water passes **under** the paddlewheel.
The actual CAD assembly animates in the browser.

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
Vibecoded by Astra for the [Leonardo gallery](../../README.md).
The pilot commissioned this more complete reconstruction on 12 September 2026;
it supersedes the earlier simplified sawmill’s scope, not its preserved history.

## Open and explore

From the Leonardo repository root, in the workspace environment:

```sh
source ../../.venv/bin/activate
python models/hydraulic_sawmill/scripts/demo.py
```

Open **http://127.0.0.1:8769/models/hydraulic_sawmill/**.
Use `--build-only` for a finite export, `--no-build` to serve an existing
export, or `--port 8770`. Stop the local server with Ctrl+C.

Play/pause, speed, the full-pass timeline, four camera views and mechanism
reveal let you follow each transmission. The feed view looks at the rear
linkage; restore the frame to understand the fixed pivots. Reduced-motion
preferences start paused. The standard viewer at
`/export/hydraulic_sawmill/` exposes the same timeline and an assembly sidebar.
There are no machine input drivers or instruction buttons. Open “Explore the
assembly” to navigate frame, water drive, saw, timber carriage and feed;
the timber and rollers have their own subgroups.

## What is reconstructed

- Low descending channel and undershot wheel with eight paddle stations,
  rims, spokes, keyed shaft, bearing journals and retaining collars.
- Crank, captured connecting rod, two-post grooved guide, moving saw sash,
  toothed blade, pinned attachment forks and a set tension nut.
- A closed saw-journal tie and long rocking lever with its short drive arm,
  pivoted driving hook, opposing holding pawl and 32-tooth ratchet.
- Winding drum, continuous length-conserving rope, fixed end return pulley,
  bored carriage tie-off, flanged rollers, retained axles and log cradles.

A 24 mm crank throw gives a **48 mm stroke**. One return stroke advances one
ratchet tooth: **approximately 4.60 mm of carriage travel**. The full pass takes
**74 turns / 296 seconds**, advancing **340.062622 mm**. The carriage dwells
during the cutting downstroke.

The **320 mm timber** starts wholly before the teeth and finishes beyond the
blade. Slotted cradles support it throughout; all four rollers stay on the
modestly extended rails. The timber is 30 mm shorter than the original,
while the table grows from 610 to 720 mm. Blade entry clearance is 1 mm;
exit clearance is about 4.06 mm. A shrinking molejo insert fills the uncut kerf ahead of the
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
The rope assumes maintained tension and orderly helical winding on the drum. Water and material removal are
illustrative, and the timber is assumed secured. The rigid halves have an
open kerf; the flexible insert supplies the cutting impression. Its last
0.1 mm collapses to zero area, not a remaining solid or sawdust simulation.
The tension screw is shown
set, without helical thread or blade-strain simulation. Stopping water,
releasing pawls and reloading remain manual operations, explained in the
exhibit; no hidden automatic return is invented.

See the [source-by-source reconstruction record](docs/reconstruction.md),
[design](docs/design.md) and [full-pass validation](docs/full-pass-validation.md).
The [previous validation](docs/validation.md) records the superseded four-turn exhibit.

## Reproduce the evidence

Use the workspace’s **post-0.6 development API**, including declarative joints
and relations, and viewer API 20 (Machinome browser names and assembly navigator).
Published machinome 0.6.0 alone is insufficient. The tested viewer 0.2.0 is
a local development package, not claimed to be released.
Exact dependency revisions are recorded in the validation certificate.

```sh
machinome build hydraulic_sawmill
machinome test hydraulic_sawmill --faceted
machinome test hydraulic_sawmill --exact
machinome test hydraulic_sawmill --set kerf=2 --exact
machinome test hydraulic_sawmill --set kerf=5 --exact
python models/hydraulic_sawmill/scripts/readouts.py --check
machinome snapshot hydraulic_sawmill -o models/hydraulic_sawmill/docs/evidence/full-pass-start.png --autocenter --viewall --time 0 --imgsize 1400x1000
python scripts/gallery.py check
python scripts/gallery.py export hydraulic_sawmill
python models/hydraulic_sawmill/scripts/check-browser.py
python scripts/check_browsers.py
```

The finite browser script serves its own temporary localhost server unless
`--url` supplies one. Exports contain committed source: regenerate after
committing source changes. Generated meshes, research downloads and browser
batches are ignored; a small selected [evidence set](docs/evidence/) is tracked.

Primary reference: [Milan museum hydraulic saw](https://www.museoscienza.org/en/collections/objects/hydraulic-saw).
The [detailed catalogue](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica)
and [Atlanticus 1078r](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/1078-r/)
are linked and assessed in the research record. Museum photos and manuscript
scans are not redistributed.

The [machine-owned OpenSpec](openspec/) preserves both the original
retrospective record and this commissioned reconstruction cycle.
