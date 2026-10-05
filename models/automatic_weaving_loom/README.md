# Leonardo's automatic weaving loom

Historical reconstruction of the narrow-ribbon, **accompanied-spool** loom
represented by Luigi Boldetti's 1954 model at the
[Museo Leonardiano in Vinci](https://museoleonardiano.it/en/opera/automatic-weaving-loom/).
The former illustrative drive is replaced by an upper timing train, descending
feed, four lower gears, perforated belt and mechanically actuated weaving head.

Concealed mechanisms are explicitly inferred, as authorized by the pilot.
This is original reconstruction CAD, not a measured replica or a claim that
Leonardo specified every completed cam, grip and fitting. See the
[source-and-inference record](docs/reconstruction.md).

The pilot's reed/carrier correction is implemented and **paused at the pilot's
requested checkpoint**, before final certification. See the [current correction record](docs/reed-correction.md)
for the longer stroke, relocated tracks and drive, red-first evidence and
completed checks. The [Studio-time checkpoint](docs/checkpoint-2026-09-13.md)
is historical; the former educational certificate does not certify this
reconstruction.

Vibecoded by Astra as part of the single [Leonardo gallery](../../README.md).
Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only;
see [LICENSE](../../LICENSE).

## Open the reconstruction

From the Leonardo repository root, with the workspace environment on PATH:

```sh
machinome build automatic_weaving_loom
python scripts/gallery.py export automatic_weaving_loom
python -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/models/automatic_weaving_loom/demo.html`.
Orbit the actual CAD, select a named stage, or scrub `phase`. The plain viewer
is at `/export/automatic_weaving_loom/index.html`. Serve over HTTP, not
`file://`. The source download contains the committed gallery revision,
not an uncommitted working tree.

In **Studio**, open `Leonardo/automatic_weaving_loom`, expand **Timeline**, and
choose **Playback speed** ×0.1, ×0.25 or ×0.5. The Python declaration supplies
the one-minute clock; no companion HTML page is needed. With the project
already open, `python models/automatic_weaving_loom/scripts/check_studio_time.py`
checks that live UI (default Studio address `http://127.0.0.1:9000`).

In this workspace, `solid` and Python are under
`/home/asa/devel/machinome-studio/.venv/bin/`. This model needs the installed
post-0.6.0 declarative machinome API, CadQuery 2.7 and molejo 0.2. The separate
viewer is the local 0.1.0 package, founded but not publicly released.

## Follow the mechanism

The common shaft carries a single engaging pin and the completed head cams.
It indexes the six-position wheel by 60° per revolution; the six/twelve gear
mesh advances the scroll by 30°. A captured pin lowers the descending rack
1.8 mm. The rack drives the rear lower wheel, rear upper wheel, perforated
leather belt, and front upper/lower pair. Every wheel is mounted and retained.

Two arm cams drive captured followers and 5:1 slotted rockers. Constant-length
haul cords translate the hands, with weighted return cords. Two other tracks
alternate the heddles; a double-lobed track drives the reed. Two selectors
open the spring-closed retaining jaws at the receiving region. The receiving
jaw closes before the donor releases; both hands withdraw before shed closure.

| Stage | Phase | Observation |
| --- | ---: | --- |
| Beat left | 0° | Spool outside the left selvedge, shed closed, reed forward |
| Open shed | 60° | First shed open, accompanied spool reaches the receiving hand |
| Handoff | 90° | Both jaws closed during the exchange dwell |
| Beat right | 180° | Spool outside the right selvedge, reed forward |
| Return pick | 270° | Opposite shed and opposite gripping exchange |
| Run | — | Resume the finite four-turn demonstration |

Instructions settle in 0.6 seconds. Stage buttons set `run=0`, holding their
phase while the viewer timeline continues. `run=1` adds four input turns over
the 60-second machine timeline; intermediate values scale it.
The Python root declares `time = Time(loop=60)` and advances at 24°/s.
This publishes `animation.loop=60` to Studio as well as exports, enabling
the native speed selector and machine-time readout. Export frame count is
only timeline resolution, not the simulation's duration. The viewer's play/pause
button controls the timeline. Motion clamps at 1440°, the end of the modeled
scroll segment. Replay resets the winding state; no automatic unwinding or
historical reset mechanism is asserted.

One turn makes two picks. Four turns represent eight picks and 2.22 mm of
equal warp let-off and cloth take-up. The eight displayed picks are a
pre-existing woven sample moving with the cloth web, not new textile topology
formed by a contact solver. The free weft span is schematic.

## Construction and dimensions

X is across the ribbon, Y toward the warp supply, Z upward. Every dimension
is a reconstruction choice, not a measurement of the museum object.

| Interface | Geometry |
| --- | --- |
| Main shaft / weaving plane | Z=400 / 520 mm; shaft Y=180 mm |
| Upper gears | Six and twelve teeth, module 6, 54 mm centre distance |
| Lower gears | Four 24-tooth wheels, module 4, 48 mm pitch radius |
| Belt | 64 perforations at 4π mm pitch; two pegged sprockets |
| Warp / heddles | 24 ends, 6 mm spacing; Y=170 and 190 mm; opposite ±18 mm lift |
| Spool / hands | 24 × 12 × 6 mm boat; 260 mm total spool travel |
| Retaining jaws | 14 mm selector lift; interleaving fingers and side cheeks |
| Reed | 100 mm stroke, Y=48…148 mm; crosses the carrier at Y=115; fell Y=45 mm |
| Textile winding | 14.8 mm pitch radius, 0.555 mm per input turn |
| Timber head tower / reed-drive support | Z=615 / 736 mm |

The guarded parameter `shed_lift` ranges from 16 to 20 mm. It changes the
physical cam profiles, heddle motion and yarn motion together:
`machinome build automatic_weaving_loom --set shed_lift=20`.

The reed parks behind the carrier through each insertion and exchange. It
crosses between the withdrawn hands, approaches the fell and returns during
the 26° on either side of each beat. Its extended guide bed sits beneath the
carrier. The selector crossbars move behind the reed and rise 22 mm to clear
the bed and cam rims; the larger reed cam sits outboard on the common shaft
with a raised guide and sheaves.
The red weft's displayed bend follows the working face while its free end
stays attached to the spool. This remains a kinematic illustration of yarn
contact, not textile formation or a force simulation.

The construction is divided into [timing.py](timing.py),
[winding.py](winding.py), [head.py](head.py), [cords.py](cords.py),
[textile.py](textile.py), shared geometry in [parts.py](parts.py), and the
registered [model.py](model.py). Independent fixtures exercise timing,
winding, head closure, gripping and flexible routing. They are test fixtures,
not additional gallery models.

## Verification and limits

```sh
machinome test automatic_weaving_loom --mesh
machinome test automatic_weaving_loom --brep
machinome test automatic_weaving_loom --brep --set shed_lift=16
machinome test automatic_weaving_loom --brep --set shed_lift=20
machinome test models/automatic_weaving_loom/timing.py --brep
machinome test models/automatic_weaving_loom/winding.py --brep
machinome test models/automatic_weaving_loom/head_bench.py --brep
machinome test models/automatic_weaving_loom/grip_bench.py --brep
machinome test models/automatic_weaving_loom/cord_bench.py --brep
python models/automatic_weaving_loom/scripts/inspect_demo.py
```

The browser check uses the generated export and Playwright/Chromium, serves it
on an ephemeral local port, and checks controls, changing/returning CAD pixels,
playback and desktop/narrow layout. Results belong to this reconstruction's
[verification record](docs/verification.md), not its former educational
certificate preserved in Git history.

This is a connected **kinematic** simulation. Input torque, rope and belt
tension, spring closing and textile tension are assumptions. No force,
friction, impact, wear, wood strength, multilayer winding or manufacturing
safety is solved. Sampled interference and capture checks do not constitute a
continuous swept-volume proof. Flexible materials require separate checks;
the rigid-only integrity gate cannot certify them.

The original `demonstrate-leonardos-loom` cycle remains historical evidence.
The new machine-owned OpenSpec cycle is `reconstruct-museum-automatic-loom`;
no framework or sibling machine is part of this change. Museum photographs
are private research references and are not redistributed.
