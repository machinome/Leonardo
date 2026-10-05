# Hydraulic saw reconstruction: validation certificate

Historical certificate for the 12 September four-turn exhibit. For the current
full timber course, timeline-only controls and progressive kerf insert, see
[19 September validation](full-pass-validation.md).

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Validated 12 September 2026 in the Machinome Studio workspace. This replaces
the simplified exhibit’s certificate, preserved at gallery commit `0936085`.
The new cycle’s planning commit is `3ff37ba`. The implementation source
commit is `d5f92fbc7542c4e234a84c7150a40ab8bd34c829`. Its CAD and test
sources were verified byte-identical to the staged tree used during the
exact certificate (`daba7a0a15bdc119374d24bb35746607df9e2832`). A post-commit
faceted run also passed all 19 tests in 10.25 seconds with zero volume epsilon.
This provenance update changes documentation only.

## Environment

- machinome checkout `6e41f2d`, metadata version 0.6.0, with the
  post-release declarative node/motion API.
- machinome-viewer checkout `6fb082b`, metadata 0.1.0, viewer API 7.
  This local package is founded, not claimed to be publicly released.
- CadQuery 2.7.0; molejo 0.2.0; Playwright 1.62.0; Python 3.12; Linux.
- Exact OCCT comparisons for rigid pairs; rope comparisons use the flexible
  leaf’s mesh representation. “Exact run” does not turn the rope into an
  exact rigid solid.
- Browser: headless Chromium with SwiftShader WebGL. No dependency was edited.

## Red-first and fault detection

The existing model’s 10 tests passed. Three new omission contracts then failed
on the absent tie, end pulley/holding pawl and blade attachments:
**13 tests, 10 passed, 3 failed**. That red run preceded implementation.

Deliberate node-code mutation: changed the saw-to-tie angular relation from
`tie_pose(height)` to `tie_pose(height) + 5`, leaving the physical dimensions
and tests unchanged. The faceted run returned **19 tests, 15 passed, 4 failed**.
The timed whole-machine scenario reported a rocker/tie intersection of
27.8379358 mm³. This demonstrates detection of a broken closed linkage, not
merely validation that the saw still reciprocates. The mutation was removed;
the unchanged tests passed again, including the final exact runs below.

Development also exposed and corrected disconnected pulley flanges, filled
bores, journal/rod collisions, wheel retention fits and pawl-tooth interference.
The whole-root contracts were kept active; no volume epsilon was introduced.

## Mechanical certificate

| Contract | Coverage and independent observation |
| --- | --- |
| Connected rigid pieces | Every rigid leaf, exactly one body; fused stationary fixture included |
| Whole-root non-interference | 33 poses over four cycles; every 2° through one full cycle; dead-center and wrap neighborhoods; combined phase/time/playback states |
| Real-time instruction | Start instruction followed by a 16-second four-cycle ramp; assertions every 0.2 s, simulation step 0.05 s; measured final carriage position |
| Saw stroke | Mesh bounds at dead centers differ by 48 mm |
| Indexed feed | Measured downstroke dwell, return advance, 4.594579 mm per revolution and 18.378317 mm at the bounded endpoint |
| Crank pin and guides | Nine poses each; rod free within 0.3 mm and blocked at 1.5 mm; sash free within 0.3 mm and blocked at 1.3 mm |
| Closed rocker linkage | Every 15°; both tie eyes, rocker/pawl joints and fixed holding journal free within 0.2 mm and blocked at 1.5 mm |
| Keyed waterwheel | 1° free angular play and blockage by 10°; axial clearance 0.3 mm and retention at 2 mm |
| Working pawl | Eleven working/endpoint poses, 0.3° free play and reverse relative blockage by 5° |
| Holding pawl | Reverse ratchet motion blocked by 5° at the seated start; tooth-transition and pivot-closure checks through the cycle |
| Blade forks | Both clamps permit 0.2 mm axial play and block by 2 mm |
| Carriage and end pulley | Roller flange running clearance, pulley journal clearance and radial capture, retained axle geometry |
| Undershot water path | Actual water vertices remain below the axle and below the lower paddle tips at the wheel; the lowest wheel vertex moves downstream; tower height measures 645 mm |
| Rope route and length | 12 poses over four cycles; 289 sampled cross-section centers; endpoint, tangent, semicircle and winding-circle coordinates measured independently |
| Rope take-up and attachment | 23.4 mm pitch radius; winding increase equals carriage displacement; complete length 844.783170 mm remains constant; frame/drum/pulley/sash clearance and both bored terminations checked |
| Reproducible posing | Phase 73° is recovered after visiting 1100°, with identical mesh bounds |
| Explanatory labels | 721 CAD-derived saw/carriage measurements at 0.5° intervals match the checked-in readout table |

These are sampled geometric checks, not a continuous swept-volume proof.
A seated pawl’s limited reverse blockage is not a proof of zero backlash,
holding torque or stable contact under load.

Commands from the gallery root, using the workspace environment:

```sh
machinome test hydraulic_sawmill --mesh
machinome test hydraulic_sawmill --brep
machinome test hydraulic_sawmill --set kerf=2 --brep
machinome test hydraulic_sawmill --set kerf=5 --brep
python models/hydraulic_sawmill/scripts/readouts.py --check
python scripts/gallery.py check
```

| Configuration | Result |
| --- | --- |
| Default, faceted, zero volume epsilon | 19 passed, 0 failed; 12.78 s |
| Default kerf 3.2 mm, exact | 19 passed, 0 failed; 168.09 s |
| Minimum kerf 2 mm, exact | 19 passed, 0 failed; 170.53 s |
| Maximum kerf 5 mm, exact | 19 passed, 0 failed; 168.71 s |
| Readout measurement table | 721 samples match actual CAD |
| Gallery inventory | Six models, coherent queue, separate OpenSpec roots, one repository |

The other five machines and shared gallery code were unchanged. The complete
`python scripts/check_browsers.py` run passed for all six registered exhibits:
sawmill, loom, cam hammer, rack/pinion, pulley block and swivel crane. Their
existing browser checks form gallery regression; they do not acquire a
fabricated red-first history from this sawmill change.

## Pixels and browser

The selected [OpenSCAD evidence images](evidence/README.md) were rendered with
the default renderer and inspected: whole machine at 270°, rear linkage at
210°, lower drive at 90°. The isometric shows the under-wheel channel and
two-post table; the rear view resolves the closed tie/rocker, driving hook,
opposing pawl and ratchet. These are original CAD screenshots, not edited
museum photographs. The source photographs are privately cached and not
redistributed.

```sh
machinome export hydraulic_sawmill -o export/hydraulic_sawmill --fps 30 --frames 480
python models/hydraulic_sawmill/scripts/check-browser.py
python scripts/check_browsers.py
```

The finite sawmill browser smoke passed on the real version-4 manifest:
all referenced mesh assets, mechanism inventory, six native instructions,
exact numeric entry and sliders, changed CAD pixels under playback/scrubbing,
pixel-identical pose return, all four views, frame reveal, reset notice,
source ZIP contents, 1440 px desktop and 390 px narrow layout.
No JavaScript errors, console errors, failed requests or HTTP errors occurred.
Screenshots are saved under ignored `_evidence/hydraulic_sawmill/browser/`.

Before the source commit, the source-download smoke used an explicitly staged
Git tree archive, not a claim of publication. The final gallery export is
regenerated from the committed revision and records that revision alongside
the source ZIP. A second sawmill browser run also passed after the final
whole-view camera adjustment; that final desktop image was inspected with
the entire plinth inside the viewport.

The change is archived at
`openspec/changes/archive/2026-09-12-reconstruct-museum-hydraulic-saw/`.
All tasks are complete, all three baseline capability specifications match
their deltas, and strict OpenSpec validation passes with no active changes.
The committed-source export is reproduced with
`python scripts/gallery.py export hydraulic_sawmill`; its
`source-revision.txt` identifies the exact downloadable gallery revision.

## What is not certified

The visible functional systems are modeled and mapped to sources in
[reconstruction.md](reconstruction.md). Hidden dimensions, tie seating and
fittings are engineering interpretations of a twentieth-century museum model,
not a certified measured replica of the manuscript or museum artifact.

No fluid power, material removal, structural loading, wear, friction,
gravity equilibrium, pawl impact or torque is solved. Grounded fixtures are
the plinth, stationary stand and water channel. Bearing and rolling gaps
depict working fits, not elastic settlement under weight. Log securing and
rope tension are assumptions. Blade tension is represented by fixed forks,
a stem envelope and a nut, not a solved thread or blade strain.

The pawls’ contact tables are geometric approximations with running clearance;
they do not demonstrate force transmission efficiency. Rope length and
termination capture do not prove knot strength, tension or loaded winding.
Four cycles remain below one wrap; multilayer winding is not advertised.
The historical reload is manual and explained, not animated as an invented
automatic mechanism. Chromium software rendering is not a cross-browser
compatibility or performance certification.
