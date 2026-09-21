# Leonardo da Vinci Gallery

Leonardo's machines, made inspectable: turn a drive, follow the movement,
and see how the parts work together. **Vibecoded by Astra**, from one user
prompt per design, as a demonstration of
[machinome](https://machinome.readthedocs.io/).

Copyright (C) 2026 Luis Henrique Cassis Fagundes.
All original gallery code, CAD and documentation are **AGPL-3.0-only**;
see [LICENSE](LICENSE) and [NOTICE](NOTICE).

This is one repository with several named models. Six exhibits are
implemented; the final static Sphinx site remains in the
[build queue](QUEUE.md). The complete public site is not built yet.
Intended source home: [LibreSolid/Leonardo on GitHub](https://github.com/LibreSolid/Leonardo)
(publication is pending; this URL is a recorded working assumption).

| Model | What you can follow | Record |
| --- | --- | --- |
| `hydraulic_sawmill` | Milan undershot saw: pulling pawl, radially wound axle, two-rope reduction and carriage | [Machine](models/hydraulic_sawmill/README.md) · [OpenSpec](models/hydraulic_sawmill/openspec/) |
| `automatic_weaving_loom` | Vinci accompanied-spool loom: one/six/twelve indexing, four lower gears, belt, captured head and weighted cords | [Machine](models/automatic_weaving_loom/README.md) · [OpenSpec](models/automatic_weaving_loom/openspec/) |
| `cam_hammer` | Cam contact, lever lift, released drop and anvil strike | [Machine](models/cam_hammer/README.md) · [OpenSpec](models/cam_hammer/openspec/) |
| `rack_and_pinion` | Crank rotation, engaged teeth, guided lift and a hooked weight | [Machine](models/rack_and_pinion/README.md) · [OpenSpec](models/rack_and_pinion/openspec/) |
| `pulley_block` | Three supporting rope spans, captured sheaves and 3:1 effort/load travel | [Machine](models/pulley_block/README.md) · [OpenSpec](models/pulley_block/openspec/) |
| `swivel_crane` | Independent slew, engaged screw traverse and continuous 2:1 drum hoisting | [Machine](models/swivel_crane/README.md) · [OpenSpec](models/swivel_crane/openspec/) |

These began as educational interpretations, not dimensioned replicas.
Each machine identifies its historical sources, reconstruction choices and
limits. The sawmill was subsequently researched and rebuilt at the pilot’s
request against the Milan museum photographs, with the undershot water path
and complete visible feed train; its [research record](models/hydraulic_sawmill/docs/reconstruction.md)
distinguishes observations from inferred fittings. The loom has likewise
been rebuilt around Vinci's accompanied-spool interpretation, with its
[concealed mechanisms documented as inferences](models/automatic_weaving_loom/docs/reconstruction.md).
Its four-turn demonstration now spans one minute for slow-motion inspection.
Prescribed motion is labelled as such. The saw now traverses a complete
320 mm timber in a 1460-second timeline (365 wheel turns), with a shrinking molejo insert showing
the kerf opening; it does not simulate physical material removal.
The loom advances a pre-existing cloth sample by 2.22 mm but does not solve
yarn tension or form new interlaced textile topology.
The hammer's return is prescribed; gravity and impact are not simulated.
The rack lift demonstrates travel and engagement; holding torque, a brake
and lifting capacity are outside its scope.
The pulley preserves rope length and measures displacement; tension,
efficiency, termination strength and load rating are not solved.
The crane holds its coordinates and prescribes winding and upright suspension;
worksite stability, structural strength and lifting capacity are outside its scope.

## Build and inspect

Use Python 3.12 and an environment containing machinome's **post-0.6
declarative motion API**, CadQuery, molejo and machinome-viewer API 7 or
later. Published machinome 0.6.0 alone is insufficient. The viewer's local
0.1.0 package is founded, not asserted to be released. See the tested
[environment and consolidation record](docs/consolidation.md).

In the development workspace, from this repository root:

```sh
source ../../.venv/bin/activate
python scripts/gallery.py check
python scripts/gallery.py list
machinome build hydraulic_sawmill
machinome build automatic_weaving_loom
machinome build cam_hammer
machinome build rack_and_pinion
machinome build pulley_block
machinome build swivel_crane
python scripts/gallery.py test
python scripts/gallery.py export
python scripts/check_browsers.py
python -m http.server 8769 --bind 127.0.0.1
```

Open the [sawmill](http://127.0.0.1:8769/models/hydraulic_sawmill/) or
[loom](http://127.0.0.1:8769/models/automatic_weaving_loom/demo.html) or
[cam hammer](http://127.0.0.1:8769/models/cam_hammer/) or
[rack lift](http://127.0.0.1:8769/models/rack_and_pinion/) or
[compound pulley](http://127.0.0.1:8769/models/pulley_block/) or
[swivel crane](http://127.0.0.1:8769/models/swivel_crane/).
Their plain viewers are at `export/<model>/index.html`.
`gallery.py build|test|export` handles all registered models, or accepts
model names to select a subset. Tests default to the exact kernel;
`test --kernel faceted` is the development loop.
The browser check requires Playwright with Chromium installed.

Exports include their local viewer assets and a source archive of the
committed gallery. Commit source changes before creating publication
archives. Generated geometry, exports and inspection images are ignored.
Serve exports over HTTP; opening them as `file://` is not supported.

The version floors in `pyproject.toml` do not promise that a fresh PyPI-only
install has the required API. Establishing a public, reproducible dependency
set is an explicit gate on the last queue item. No unpublished framework
commit is silently presented as installable from its public remote.

## Continue Astra's demo

The pilot's next-session prompt is:

> See the Leonardo project, build next work on the queue.

Read [AGENTS.md](AGENTS.md), run `python scripts/gallery.py next`, and carry
that one item through design, implementation, verification and commit.
[QUEUE.md](QUEUE.md) contains complete briefs and acceptance gates;
[gallery.toml](gallery.toml) owns order and status. No new prompt is needed
for ordinary implementation decisions within those briefs.

Every machine owns `models/<name>/openspec/`. Gallery-wide work owns the
root `openspec/`. Run OpenSpec in the relevant directory and check its
reported planning root before writing. Do not initialize nested Git repos
or machine manifests. The root registry selects the models just as in the
3DPrintedClocks gallery.

## History and authorship

The original sawmill commit `9f4cc67` and loom commits `39e5d98`, `fd00458`
remain unchanged ancestors of this repository. The tags
`history/hydraulic-sawmill` and `history/automatic-weaving-loom` preserve
their original tips. [The consolidation record](docs/consolidation.md)
explains the import and path moves. No original prompt transcript was
present in those repositories; the single-prompt attribution comes from
the pilot's statement, recorded in [the gallery brief](docs/brief.md).

The final site must visibly credit machinome and link to this gallery's
GitHub source. Building the site does not publish it: publication remains
the pilot's action after the queue is complete.
