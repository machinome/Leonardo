# The cam hammer — a circle becomes a beat

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

An original educational model by **Astra**, made from one continuation
prompt as a [machinome demonstration](https://machinome.readthedocs.io/).
The hand crank turns a shaped cam above the lever's short tail. Pressing
the tail down lifts the hammer; the cam retreats and the hammer returns
to the anvil. [Open the exhibit](index.html) after building the export and
serving the gallery root over HTTP.

## Controls

| Control | What it does |
| --- | --- |
| phase, 0–360° | Turn the crank manually with run at 0 |
| run, 0–1 | Add timeline rotation, from stopped to one revolution per loop |
| Lift | Hold halfway through the lift at 120° |
| Release | Hold the newly opened contact at 250° |
| Strike | Hold the hammer on the anvil at 320° |
| Run | Reset phase to 0 and couple the machine to the viewer timeline |

The viewer starts with playback active. Its own Pause/Play button controls
the timeline. A full-speed cycle returns to the same pose. Looping with
fractional run restarts at the selected phase; that timeline reset is not
a physical jump proposed for a real machine. Instructions can also ramp
the crank backwards to inspect earlier stages.

The build parameter `lift_angle` is 18° by default and accepts 16–20°.
The whole mechanism is tested across this small advertised envelope.
The 290 × 130 mm base and 60/100 mm lever arms are chosen teaching
dimensions, not measurements from Leonardo's drawings.

## Mechanism and limits

The lever rises with a half-cosine over the first 240° of crank travel.
Its return occupies 240–320°, followed by rest. The cam's return envelope
retreats over 240–285°, opening a real gap before the hammer lands. A
6 mm rounded fixed shoe follows the designed pitch envelope with a nominal
0.3 mm running gap. The cam outline is sampled every 0.5° and offset along
the pitch-curve normal; contact is checked on the resulting geometry.
The recessed tail clears the retreating flank.

Both 10 mm shafts run in 10.7 mm journal bores. Collars leave 0.3 mm axial
play per side. The frame's columns and bearing beams leave the contact
visible from the side. The anvil foot sits 0.2 mm above its base seat; the
hammer's flat striking face lands at z=91 mm. The four complete rigid
solids are frame, cam/crank/shaft, hammer lever/shaft, and anvil. Their
joined ingredients represent permanently joined components; this is not
a manufacturing or assembly instruction set. Timber and metal colours
are visual cues, not a material or load-capacity model.

Motion is prescribed kinematics. No gravity or impact solver, rebound,
wear, friction, elastic deformation, forging operation, strength or
fabrication certification is claimed. The shaft capture and geometric
support checks do not predict dynamic loads. Nothing is cut or forged.

## Historical basis

- [Museum of Science, Gadget Anatomy](https://www.mos.org/leonardo/activities/gadget-anatomy.html)
  describes the cam pushing down a lever tail in a gravity trip hammer.
- [The Venice Leonardo exhibition, Hammer Cam](https://leonardoavenezia.com/en/)
  describes a crank-driven cam producing intermittent hammer strokes.

Both were checked on 12 September 2026. They establish the mechanism and
its educational context. Our cam profile, rounded shoe, proportions,
joinery and timing are reconstruction choices. No folio number or claim
that Leonardo invented the mechanism is inferred. No museum images,
historical CAD, or third-party model assets are copied.

The exact continuation prompt was: “See the projects/Leonardo. Build next
project.” [Queue item 010](../../QUEUE.md#010-cam-hammer) and the
[gallery commission](../../docs/brief.md) supplied its scope and delegated
the complete local cycle. The plan is commit `1c0be60`; the
[OpenSpec record](openspec/) belongs to this machine.

## Reproduce

From the gallery root, activate the workspace environment as described in
the [gallery README](../../README.md). It requires the local post-0.6
motion API and separate viewer, not solely published machinome 0.6.0.

```sh
machinome build cam_hammer
SOLID_BUILD_DIR=_build/cam_hammer_tests machinome test cam_hammer --faceted
SOLID_BUILD_DIR=_build/cam_hammer_tests machinome test cam_hammer --exact
SOLID_BUILD_DIR=_build/cam_hammer_16 machinome test cam_hammer --exact --set lift_angle=16
SOLID_BUILD_DIR=_build/cam_hammer_20 machinome test cam_hammer --exact --set lift_angle=20
python scripts/gallery.py export cam_hammer
python models/cam_hammer/scripts/check_browser.py
python -m http.server 8769 --bind 127.0.0.1
```

Open `http://127.0.0.1:8769/models/cam_hammer/`. The browser check starts
and shuts down its own temporary server. Keep test build directories
separate from simultaneous builds/exports: publication removes unused
fusion-ingredient artifacts that geometric tests still need.

Read the [validation record](docs/validation.md) and
[selected inspected images](docs/evidence/README.md) for measured results,
tested content and limits. Exports and raw logs are intentionally ignored.
The intended source home is [LibreSolid/Leonardo](https://github.com/LibreSolid/Leonardo);
publication remains the pilot's action.
