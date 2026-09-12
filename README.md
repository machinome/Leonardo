# Leonardo da Vinci Gallery

Leonardo's machines, made inspectable: turn a drive, follow the movement,
and see how the parts work together. **Vibecoded by Astra**, from one user
prompt per design, as a demonstration of
[solid-node](https://solid-node.readthedocs.io/).

Copyright (C) 2026 Luis Henrique Cassis Fagundes.
All original gallery code, CAD and documentation are **AGPL-3.0-only**;
see [LICENSE](LICENSE) and [NOTICE](NOTICE).

This is one repository with several named models. The first two exhibits
are implemented; four more machines and the final static Sphinx site are
in the [build queue](QUEUE.md). The complete public site is not built yet.
Intended source home: [LibreSolid/Leonardo on GitHub](https://github.com/LibreSolid/Leonardo)
(publication is pending; this URL is a recorded working assumption).

| Model | What you can follow | Record |
| --- | --- | --- |
| `hydraulic_sawmill` | Waterwheel, crank, reciprocating blade and indexed timber feed | [Machine](models/hydraulic_sawmill/README.md) · [OpenSpec](models/hydraulic_sawmill/openspec/) |
| `automatic_weaving_loom` | Alternating sheds, a supported weft handoff and beat-up | [Machine](models/automatic_weaving_loom/README.md) · [OpenSpec](models/automatic_weaving_loom/openspec/) |

These are original educational interpretations, not dimensioned replicas.
Each machine identifies its historical sources, reconstruction choices and
limits. Prescribed motion is labelled as such. The saw does not cut material;
the loom does not solve yarn tension or accumulate cloth.

## Build and inspect

Use Python 3.12 and an environment containing solid-node's **post-0.6
declarative motion API**, CadQuery, molejo and solid-node-viewer API 7 or
later. Published solid-node 0.6.0 alone is insufficient. The viewer's local
0.1.0 package is founded, not asserted to be released. See the tested
[environment and consolidation record](docs/consolidation.md).

In the development workspace, from this repository root:

```sh
source ../../.venv/bin/activate
python scripts/gallery.py check
python scripts/gallery.py list
solid build hydraulic_sawmill
solid build automatic_weaving_loom
python scripts/gallery.py test
python scripts/gallery.py export
python scripts/check_browsers.py
python -m http.server 8769 --bind 127.0.0.1
```

Open the [sawmill](http://127.0.0.1:8769/models/hydraulic_sawmill/) or
[loom](http://127.0.0.1:8769/models/automatic_weaving_loom/demo.html).
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

The final site must visibly credit solid-node and link to this gallery's
GitHub source. Building the site does not publish it: publication remains
the pilot's action after the queue is complete.
