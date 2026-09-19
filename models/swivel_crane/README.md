# The swivel crane

<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->

Three independent coordinates place one suspended stone: slew the mast,
traverse the screw-driven trolley, then hoist through two supporting rope spans.
Original CAD by Astra, commissioned by queue item 040 as a machinome demo.

Open [the exhibit](index.html) through the local HTTP server described below.
It embeds the real exported model, including its native controls and playback.

## Controls

| Control | Range | Meaning |
| --- | --- | --- |
| `slew` | −60 to +60° | Rotation about the mast's vertical axis |
| `traverse` | 0 to 60 mm | Trolley travel; nominal radius 80 to 140 mm |
| `hoist` | 0 to 25 mm | Rise of the lower sheave, lifting eye and stone |
| `run` | 0 to 1 | Manual settings at zero; complete demonstration at one; bounded blend between |

**Pick up**, **Lift clear**, **Swing** and **Place** set all three physical
coordinates and set `run=0`. Select Pick up before using the manual controls.
**Demonstrate** sets `run=1`; the viewer's Play/Pause and timeline control time.
The stone stays suspended at the named pickup and placement positions.

The 12-second loop lifts, traverses and slews, lowers, lifts again, retraces
its path, and lowers back to its starting pose. There is no discontinuous
reset. The entire Cartesian control envelope, including intermediate blends,
is the intended demonstration range. Driver ranges are presentation metadata.

## Mechanism and original dimensions

The 124 mm diameter footing is an explicitly bolted support fixture. Its
journal and thrust flange capture the rotating mast. A timber jib carries
two 6 mm guide rods and a single-start lead screw, centred at z=260 mm.
The screw has a 12 mm lead, 8 mm core and 12 mm crest diameter, with an original
square helical rib, built from ruled sections at 20° intervals. Its explicitly
polygonal geometry avoids periodic-surface Boolean failures. The trolley has a
mating pocket enlarged by 0.4 mm axially
per flank and radially at the crest; bores have 0.35 mm radial clearance.
The positive mating clearance also accommodates the small chord approximation.
Screw rotation is −360° per 12 mm of positive trolley travel for this hand.

The trolley carries the complete hoist in a plane 34 mm in front of the
screw. Two 24 mm pitch-diameter sheaves lead to a 36 mm pitch-diameter drum:

    trolley socket → lower sheave → upper guide → drum wrap → drum socket

Two free spans shorten by the stone's rise. The drum wraps an additional
twice that length: 50 mm take-up for 25 mm rise. Its winding angle increases
from 90° to 249.15°, preserving a total rope centreline length of
`230 + 27π = 314.823 mm`, including both sheave arcs and the stored wrap.
Less than one turn keeps the rope in a single visible lane. The attached
endpoint follows a tangent blind socket that rotates with the drum.
The orange rope has a 2 mm diameter and a nominal 0.4 mm gap above each groove
floor. Journal and cheek clearances permit rotation and block escape.

The stone includes an integral lifting eye on a separate yoke pin; this
closed captured connection is the demonstrator's hook connection. The model
does not prescribe a rated rigging attachment, removable knot or brake.

## Historical source and limits

[Museo Leonardiano: swivel crane](https://museoleonardiano.it/en/opera/swivel-crane/),
accessed 12 September 2026, identifies **Codex Atlanticus f.105v**. It describes
the fixed base, rotating mast, lifting pulleys and transverse screw, crediting
machinery probably designed by **Brunelleschi** and recorded by **Leonardo**.
The museum reconstruction is Luigi Boldetti's work from 1966; our model does
not copy its geometry or dimensions.

Scale, thread form, rails, bolted pedestal, compact trolley-mounted winch and
rope terminations are Astra's educational choices. Winding, held coordinates
and upright taut-rope suspension are prescribed. The geometric support checks
declare the footing grounded, the mast and trolley held, and the moving yoke
supported by the ideal rope. They do not solve cantilever reactions, wind,
sway, tension, friction, brake torque, structural stability or lifting capacity.
The model makes no construction or load-rating claim.

## Build and verify

From the gallery repository root, using its documented development environment:

```sh
source ../../.venv/bin/activate
machinome build swivel_crane
machinome test swivel_crane --faceted
machinome test swivel_crane --exact
python scripts/gallery.py export swivel_crane
python models/swivel_crane/scripts/check_browser.py
python -m http.server 8769 --bind 127.0.0.1
```

Open `http://127.0.0.1:8769/models/swivel_crane/`. The browser smoke starts an
ephemeral local server itself and closes it when finished. It requires
Playwright and Chromium. Generated exports are ignored; the source download
is a Git archive of the committed gallery. Source changes must be committed
before producing a publication archive.

See [evidence](docs/evidence/README.md) for checked poses, commands, independent
measurements, failure injection, inspected images and dependency revisions.
This machine owns its [OpenSpec records](openspec/); the parent gallery's
final public Sphinx site is a separate queue item.
