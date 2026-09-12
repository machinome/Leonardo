# Leonardo's automatic weaving loom

A working **kinematic demonstration** in solid-node: turn one drive and watch alternate warp threads separate, two arms exchange the weft spool, the reed advance, and the cloth beams turn. The model follows the narrow-ribbon interpretation of Leonardo's Codex Atlanticus f.985r–v described by the Museo Leonardiano di Vinci.

This is original educational CAD based on online historical material, not a dimensionally faithful replica or a manufacturing design. The captured eccentric drive and supported carrier handoff are checked geometrically. The other transmission laws are prescribed; intermediate gearing, grip latches, yarn tension, cloth accumulation and impact dynamics are not reconstructed.

## Open the demonstration

Vibecoded by Astra as part of the single [Leonardo gallery](../../README.md).
Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only;
see [LICENSE](../../LICENSE). The gallery's root registry names this model
`automatic_weaving_loom`; this folder is no longer a separate repository.

For the standalone presentation, from the **Leonardo repository root**, with the workspace virtual environment on PATH:

```sh
solid build automatic_weaving_loom
python scripts/gallery.py export automatic_weaving_loom
python -m http.server 8765 --bind 127.0.0.1
```

Open **http://127.0.0.1:8765/models/automatic_weaving_loom/demo.html**. The model animates automatically, and the page explains the four stages beside the 3D viewer. Orbit, pan and zoom to inspect the mechanism. A plain viewer is also available at `/export/automatic_weaving_loom/index.html`. Generate the export before opening it; serve it over HTTP, not `file://`.

In this workspace the exact executable is `/home/asa/devel/libresolid-studio/.venv/bin/solid`; Python is in the same `bin/` directory. The code requires the installed declarative motion API, which follows the published solid-node 0.6.0 release. Installed distribution labels alone do not distinguish these local additions. The independently installed viewer is 0.1.0 (founded, not published), CadQuery 2.7.0 and molejo 0.2.0.

## Follow the cycle

One 360° cycle represents **two picks**, one in each direction. The 360-frame export takes 12 seconds at 30 fps. That is an illustrative presentation speed, not a historical production rate.

| Button | Phase | What to observe |
| --- | ---: | --- |
| Beat left | 0° | Spool outside the left selvedge; shed closed; reed forward. |
| Open shed | 60° | Cream warp rises, blue warp falls; left arm accompanies the spool. |
| Handoff | 90° | Both sets of fingers meet beneath the spool in the open shed. |
| Beat right | 180° | Spool outside the right selvedge; reed reaches its forward limit. |
| Return pick | 270° | Blue warp is uppermost; the spool returns through the opposite shed. |
| Run | — | Restore automatic motion. |

Stage instructions land in 0.6 seconds and set `run=0`, holding their phase even while the viewer's timeline continues. `phase` then lets you scrub the mechanism manually. `run=1` adds a full cycle over the viewer timeline; intermediate values scale the motion. The viewer's play/pause button controls the timeline itself.

The cream and blue strands are alternate warp ends. The red spool carries the orange illustrative weft span. Eight red picks in the short cloth sample alternate over and under the warp; this sample stays in place. The free weft span exchanges its anchored edge near the closed shed, without a contact or yarn-length solve. The beams turn 10° per two-pick cycle to illustrate forward feed, then reset with the repeating presentation; they do not accumulate cloth.

## What is built

The primary source is [model.py](model.py). Its 118-node tree contains 11 rigid occurrences (10 distinct pieces), 81 flexible leaves, and the assemblies that connect them.

Read the construction from the ground up:

1. `TimberFrame`: a connected timber structure, journals and slide guides.
2. `Crank`: shaft, handwheel, opposed eccentric discs and captured pins.
3. `Heddle`: a connected frame of alternate needle eyes, pushrod and slotted yoke.
4. `Carrier`: two translating arms with interleaved support fingers and a boat-shaped weft spool.
5. `Reed`, `ReedTracks`, `Roller`: beat-up and material-feed illustration.
6. `WarpEnd`, cloth strands and `WeftTail`: flexible yarn geometry.
7. `AutomaticWeavingLoom`: phase relations, controls and complete assembly.

For an isolated foundation view, use `solid build models/automatic_weaving_loom/model.py:TimberFrame`. For the crank, use `solid build models/automatic_weaving_loom/model.py:Crank --set eccentricity=18`. Rebuild `automatic_weaving_loom` afterward. Driven subassemblies receive their coordinates from the complete machine.

## Dimensions and mechanical assumptions

X runs across the cloth, Y from the front cloth beam toward the rear warp beam, and Z upward. Ground is Z=0; the weaving plane is Z=180 mm. All dimensions below are demonstrator choices, not measurements of Leonardo's drawing.

| Interface | Chosen geometry |
| --- | --- |
| Frame | 360 × 332 × 255 mm; moving arms extend beyond its sides. |
| Warp | 24 ends at 6 mm spacing, X=-69…69 mm; radius 0.48 mm. |
| Heddles | Y=20 and 40 mm; opposite ±18 mm lifts at the default. |
| Spool | 24 × 12 × 6 mm; 260 mm crosswise travel. |
| Eccentric / yoke | Ø6 mm pin, 6.6 × 46.6 mm slot; 0.3 mm vertical play per side. |
| Sliding arms | 8 × 5 mm bodies in 8.6 × 5.6 mm guide apertures. |
| Reed | 37 mm stroke, Y=-65…-102 mm; cloth fell at Y=-105 mm. |
| Reed feet / bed | 0.3 mm lateral and vertical running gaps; bed seats 0.2 mm above its bearer. |
| Spool / fingers | 0.3 mm vertical seating gap; fingers occupy alternating lateral lanes. |
| Roller journals | Ø10 mm shafts in Ø10.8 mm bores. |

`shed_lift` is the one build parameter: `solid build automatic_weaving_loom --set shed_lift=20`. The supported range is 16–20 mm. It changes the eccentric throw, heddle travel and yarn geometry together. The upper limit keeps the pin inside the slot; the lower limit preserves the illustrative shed clearance. Other dimensions are fixed for this reconstruction.

The support test **grounds the timber frame as a fixture** and checks the moving rigid pieces against it. It does not certify freestanding stability, dynamics, friction, wear, wood strength or manufacturing tolerances. No geometry or machine safety claim should be inferred from the educational scale.

## Verification

```sh
solid test automatic_weaving_loom --faceted
solid test automatic_weaving_loom --exact
solid test automatic_weaving_loom --exact --set shed_lift=16
solid test automatic_weaving_loom --exact --set shed_lift=20
solid snapshot automatic_weaving_loom -o models/automatic_weaving_loom/snapshot.png --autocenter --viewall --time 0.25
python models/automatic_weaving_loom/scripts/inspect_demo.py
```

The last command requires Playwright with Chromium and the generated export. It creates an ephemeral localhost server, checks actual browser controls and playback, records `_evidence/browser-demo.png`, and shuts the server down.

The companion tests cover whole-model connectivity, rigid non-interference at 17 cycle samples, support on the grounded frame at nine samples, eccentric capture and bounded play, opposite heddle positions, spool travel and handoff, reed timing, actual flexible-yarn clearance, eye alignment, parameter guards and all six instruction targets. The instruction scenario also checks rigid interference every 0.5 simulated seconds. These are sampled geometric contracts, not continuous collision proofs.

See [docs/verification.md](docs/verification.md) for results, fault injection, inspection and known blind spots. Generated geometry, screenshots, browser assets and raw logs remain ignored; the source, records and reproducible checks are committed.

## Historical sources and interpretation

- [Museo Leonardiano: Leonardo and the art of weaving](https://artsandculture.google.com/story/leonardo-and-the-art-of-weaving-leonardo-da-vinci-museum/2wVxLwuL6F11KQ?hl=en): principal explanation of the two alternating arms and narrow ribbon limitation.
- [Museo Leonardiano: automatic loom reconstruction video record](https://museoleonardiano.it/opera/telaio-automatico-md/): identifies Codex Atlanticus f.985r–v.
- [Museum object page](https://museoleonardiano.it/en/opera/automatic-weaving-loom/) and its [reference photograph](https://museoleonardiano.it/wp-content/uploads/2024/09/formato-immagine-sito-50.png): timber-frame architecture, rollers and visible drive components. The image was inspected locally and is not redistributed.
- [Brix and Reesing, Creating Present-Day Solutions from Historical Knowledge](https://www.dmg-lib.org/thinkMOTION/wp-content/uploads/2011_Mexico-BrixReessing.pdf): secondary engineering context for common-shaft coordination.

Accessed 12 September 2026. No upstream CAD geometry or code was copied. The exact arm trajectories, supports and phase laws are this model's explanatory implementation, not a claim about the historical drawing's complete transmission.

## Project record

Originally created with `solid new Automatic-weaving-loom`, retaining both integrity contracts. The original independent repository and planning commit `39e5d98` were subsequently merged into the Leonardo gallery without rewriting history. Its OpenSpec change `demonstrate-leonardos-loom` still records the original research, design, behavioral specifications, implementation and verification. The source now lives directly in this machine folder. See the [consolidation record](../../docs/consolidation.md).
