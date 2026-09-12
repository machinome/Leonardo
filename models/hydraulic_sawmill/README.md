# Leonardo’s hydraulic sawmill

An original animated mechanical exhibit inspired by Leonardo da Vinci’s
hydraulic saw, Codex Atlanticus f. 1078r. Built with `solid new`, solid-node,
CadQuery and molejo. The browser displays the actual exported model.

Copyright (C) 2026 Luis Henrique Cassis Fagundes.
Vibecoded by Astra as part of the [Leonardo gallery](../../README.md).
Licensed under the GNU Affero General Public License, version 3 only
(`AGPL-3.0-only`). See [LICENSE](../../LICENSE).

## Open the exhibit

From the **Leonardo repository root**, with the workspace environment activated:

```sh
source ../../.venv/bin/activate
python models/hydraulic_sawmill/scripts/demo.py
```

Open **http://127.0.0.1:8769/models/hydraulic_sawmill/**. The command exports
the machine and viewer, packages committed gallery source, and serves locally.
Use `--port 8770` for a different port, `--build-only` for finite export, or
`--no-build` to serve an existing export. Stop with Ctrl+C.

Play/pause, speed selection, a four-cycle scrubber, four camera views and a
mechanism reveal are available. Drag to orbit and scroll to zoom. Space toggles
playback when the page background has focus. Reduced-motion preferences start
the exhibit paused. The standard viewer is also at `/export/hydraulic_sawmill/`.

## Model

- A 200 mm, sixteen-paddle waterwheel with a keyed shaft.
- A 24 mm crank throw and 146 mm connecting rod producing a 48 mm saw stroke.
- A toothed blade in a guided wooden sash.
- A wheeled timber carriage with a pre-cut blade slot and engraved end grain.
- A sixteen-tooth ratchet, indexed pawl carrier, drum and flexible haul rope.
- An 8 mm carriage index on each return stroke; 32 mm over the four-cycle pass.
- Open timber framing, an inlet flume, a tailrace and an exhibit plinth.

This is a **kinematic reconstruction**, not a cutting or fluid simulation.
The ratchet actuation is prescribed; the indexed pawl carrier is an exhibit
interpretation, and a complete historical linkage from saw to feed is not
reconstructed. Water is illustrative, and the log is already slotted. No
claims are made about required torque, friction, structural loading or
manufacturability. Each repeated pass resets the carriage.

The root’s `phase` driver spans 0–1440 degrees. `playback=1` adds four turns
across the normalized timeline; set it to zero for manual phase inspection.
Geometry parameters: `kerf` (2–5 mm) and `paddles` (12–24).

## Environment and verification

This project uses the workspace’s **post-0.6 development API**, including
declarative joints and relations. PyPI solid-node 0.6.0 alone is insufficient;
use a checkout matching the workspace API reference and viewer API 7 or later.
The viewer’s 0.1.0 package is locally founded, not claimed to be published.

```sh
solid build hydraulic_sawmill
solid test hydraulic_sawmill --faceted
solid test hydraulic_sawmill --exact
solid snapshot hydraulic_sawmill -o models/hydraulic_sawmill/evidence/isometric.png --autocenter --viewall --time 0.065
python scripts/gallery.py export hydraulic_sawmill
python models/hydraulic_sawmill/scripts/check-browser.py
```

Commands use the gallery's named model. All part classes live in `parts.py` and
are tested through the assembled root, where their joints are connected.
See [design](docs/design.md) and [validation](docs/validation.md) for the
reconstruction decisions and measured limits. Generated meshes, exports and
inspection images are ignored by Git.

Historical reference: [Museo Leonardiano hydraulic saw](https://museoleonardiano.it/en/opera/hydraulic-saw/).
The source and dimensions here are original; museum photographs and geometry
are not redistributed.

The [machine's OpenSpec](openspec/) was added retrospectively during gallery
consolidation; its evidence does not claim to be the original planning cycle.
