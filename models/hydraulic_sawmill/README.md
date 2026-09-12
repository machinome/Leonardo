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

Play/pause, speed, the four-cycle scrubber, four camera views and mechanism
reveal let you follow each transmission. The feed view looks at the rear
linkage; restore the frame to understand the fixed pivots. Reduced-motion
preferences start paused. The standard viewer at
`/export/hydraulic_sawmill/` also exposes all six named instructions and exact
driver entry.

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
ratchet tooth: **4.594579 mm of carriage travel**, or 18.378317 mm over the
four-turn demonstration. The carriage dwells during the cutting downstroke.

`phase` spans 0–1440°; `playback` spans 0–1. Set playback to zero for manual
phase inspection. Their combined motion clamps at the four-cycle endpoint.
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
The rope assumes maintained tension. Water is illustrative, the kerf is
already open and the timber is assumed secured. The tension screw is shown
set, without helical thread or blade-strain simulation. Stopping water,
releasing pawls and reloading remain manual operations, explained in the
exhibit; no hidden automatic return is invented.

See the [source-by-source reconstruction record](docs/reconstruction.md),
[design](docs/design.md) and [validation](docs/validation.md).

## Reproduce the evidence

Use the workspace’s **post-0.6 development API**, including declarative joints
and relations, and viewer API 7. Published solid-node 0.6.0 alone is
insufficient. Viewer 0.1.0 is locally founded, not claimed to be released.
Exact dependency revisions are recorded in the validation certificate.

```sh
solid build hydraulic_sawmill
solid test hydraulic_sawmill --faceted
solid test hydraulic_sawmill --exact
solid test hydraulic_sawmill --set kerf=2 --exact
solid test hydraulic_sawmill --set kerf=5 --exact
python models/hydraulic_sawmill/scripts/readouts.py --check
solid snapshot hydraulic_sawmill -o models/hydraulic_sawmill/docs/evidence/museum-isometric.png --autocenter --viewall --time 0.1875 --imgsize 1400x1000
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
