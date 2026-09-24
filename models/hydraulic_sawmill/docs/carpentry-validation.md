# Buildable frame: verification record

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

24 September 2026. The fixed-frame increment is complete: 11/11 frame checks
and all 42 mechanism checks pass on exact solids, including both boundary
kerfs. Sawmill and carpentry browser acceptance passes. Unrelated existing
gallery browser failures are explicitly recorded below.

## Scope and identity

The pilot commissioned a buildable fixed frame, preserving the working
sawmill. Baseline: Leonardo `9729d2e`; planning commit: `8ae3cd5`.
The implementation is the source tree committed with this record. Its exact
CAD/test fingerprints below identify the tested content without claiming
a self-referential commit ID. Exports are regenerated from the completed
commit; their `source-revision.txt` records that committed source.

The model has 24 named oak timbers, 34 named wooden pins and one display
plinth. It retains the museum-model scale, original guide/journal datums,
full 365-turn timber pass and 2–5 mm kerf envelope. Moving machinery and
channel carpentry remain outside this fixed-frame increment. Historical
sources, observed/inferred details, hand tools, members, joints and assembly
order are in [carpentry.md](carpentry.md).

## Red, mutation and restored geometry

The first frame contract was run against the actual old frame through a
temporary adapter. Of two initial checks, the separate-timber check failed:
“The bed must be individual fitted timbers.” The old root really was fused;
an earlier import/setup error is not counted as the red geometric contract.

The completed frame checks measure all 58 identities, single connected
solids, zero shared volume, the two staggered tenon necks and intervening
leg material, transverse free play and blockage, every pin's engagement
with **each** mating timber, recessed running-rail heads and support to the
plinth. The frame-only root additionally checks 109 assembly stages
(89 uniformly spaced samples plus both sides of ten integer transitions)
and exact restoration of part bounds after 0 → 11 → 0.

A deliberate mutation skipped L2's rectangular mortise cuts. It produced
**3 failures out of 11**, including L2/S1 interference of 725.543251 mm³
at assembly stage 0 and the independent mortise material probe. Restoring
the cuts restored **11/11 faceted** (20.68 s). The final frame suite also
passes **11/11 exact** (50.82 s). No volume epsilon was used.

The existing 42 mechanism checks are retained. They now recurse through
real fixture parts where the former tests consumed a fused bed/tower mesh:
free motion clears every part; blocked motion meets at least one actual
member in each tested direction. Ray/containment probes concatenate those
real meshes. Rope clearance includes every new timber and pin. The complete
faceted mechanism regression passes **42/42** (65.64 s).

Development caught protruding pin ends, vertical pins lacking gravity
retention, head clearance at running surfaces, a missing underside ratchet
relief, extraction into F2 and the outer bearing obstructing side-frame
withdrawal. The geometry/order was corrected. Positive 0.1 mm shoulder
seating allowances address coplanar tessellation ambiguity in the actual
geometry, not through an interference tolerance.

## Exact mechanism regression

| Root / setting | Result | Elapsed |
| --- | --- | --- |
| Frame and frame study | 11/11 exact | 50.82 s |
| Working saw, kerf=3.2 mm | 42/42 exact | 1351.44 s |
| Working saw, kerf=2 mm | 42/42 exact | 1337.80 s |
| Working saw, kerf=5 mm | 42/42 exact | 1339.62 s |

Whole-root integrity, complete-course and tooth-transition samples, guide
and journal play, retained pivots, pawl recovery, carriage support and both
ropes remain active. No tests were skipped or interference epsilon added.
Geometry stayed fixed during these runs. The subsequent numbering of the
separate study's instruction labels did not change the working root; the
final frame exact suite includes those numbered declarations.

## Browser and cutting book

The real export—not a second JavaScript mechanism—passes desktop and narrow
browser checks: actual CAD movement, pixel-identical reassembly, the timed
crosshead instruction reaching stage 3, camera reset, assembly navigator,
all 24 illustrated cutting-book entries and 96 unclipped SVGs, 24 stock rows, 34 pin
rows, 58 STEP files, opened machining tables, and no horizontal overflow,
console errors or failed assets. The sawmill's registered browser command
also runs the frame check.

The cutting-book generator reimports every delivered STEP file and verifies
one valid solid, preserved volume and bounding coordinates. All 58 round
trips pass. The browser also isolates the real L2 leg through the navigator
and returns pixel-identically to the full frame.

Visual inspection rejected the standard viewer's narrow-screen overlap.
The project-owned study now lays controls outside the CAD viewport and uses
a responsive camera through the public viewer API. Its stage buttons call
the exported instructions; its slider sets the exported driver. A native
page remains available at `export/hydraulic_sawmill-frame/native.html`.
Visual inspection also caught CadQuery's default left margin clipping small
SVG viewports. Explicit 20-pixel margins correct the drawings; the browser
check now verifies transformed geometry bounds inside all 96 SVG canvases.
An initial pixel-test mismatch was the native slider's focus ring, not
geometry drift; the separate-panel study permits unmasked CAD comparison.

The readout comparison passes: 721 stroke/feed samples and 2921 full-pass
feed samples match the actual CAD meshes. The sawmill browser regression
passes all five views, reveal, desktop/narrow, complete course and isolated
holding-pawl recovery. The gallery-wide run passes sawmill, loom, hammer and
rack. The unchanged pulley and a separate crane retry fail at their initial
canvas check with `MachinomeWidget is not defined`, both with default and
software-WebGL flags. This is the same unrelated issue already recorded in
[the preceding certificate](transmission-validation.md); neither is claimed
green, and no other exhibit or dependency was changed to address it.

## Inspected CAD evidence

These are OpenSCAD-rendered snapshots, not generated illustrations:

- [Assembled timbers](evidence/carpentry-assembled.png): continuous rails,
  two grooved uprights, seated crosshead and separate bearing blocks.
- [Separated frame](evidence/carpentry-separated.png): all member families,
  open bridle slots, pins and the staged subassemblies.
- [Corner joint close-up](evidence/carpentry-corner.png): shouldered stretcher
  tenon, pin bore and matching leg mortise after withdrawal.
- [End-on alignment at stage 7](evidence/carpentry-alignment.png): paired
  uprights, opened side frames, rail housings and lifted crosshead.
- [Working machine at quarter pass](evidence/carpentry-machine.png): the
  complete mechanism retained inside the joined frame.

Raw browser captures remain under ignored
`_evidence/hydraulic_sawmill/carpentry-browser/`; reference photographs remain
private. The book's SVGs are not print-to-scale templates. Tables specify
local blank coordinates; STEP solids retain exact cuts.

## Reproduction

From the repository root, with the workspace environment activated and
`PYTHONPATH` set to this project:

```sh
machinome build hydraulic_sawmill
machinome test models/hydraulic_sawmill/frame.py --faceted
machinome test models/hydraulic_sawmill/frame.py --exact
machinome test hydraulic_sawmill --faceted
machinome test hydraulic_sawmill --exact
machinome test hydraulic_sawmill --set kerf=2 --exact
machinome test hydraulic_sawmill --set kerf=5 --exact
python models/hydraulic_sawmill/scripts/readouts.py --check
python models/hydraulic_sawmill/scripts/demo.py --build-only
python models/hydraulic_sawmill/scripts/check-frame-browser.py
python scripts/gallery.py check
python scripts/check_browsers.py
```

Separate exact runs used independent `SOLID_BUILD_DIR` directories. The
gallery check passes: six models, separate OpenSpec roots, one repository,
coherent queue. No shared model/registry code or other machine was changed.

## Dependencies and source fingerprints

Local packages: Machinome 0.7.0, machinome-viewer 0.7.0 (API 27), molejo
0.2.0, CadQuery 2.7.0, cadquery-ocp 7.8.1.1.post1, Playwright 1.62.0.
Framework/viewer release-state checkouts are not claimed to be published.
Their clean content revisions, inspected read-only:

- machinome: `6df14c292f3e26025913dcd090148a503cdc84da`
- machinome-viewer: `2c965fb2ec9621cfda37dae3c183c089f7243e12`
- molejo checkout: `9500616a345d5ebd5a9be297fe3fc7acbc4945ff`

SHA-256, paths relative to `models/hydraulic_sawmill/`:

```text
e3db14ce0d41916db938c4a920d2f11a03255206b7ccec2089e455f3e8a3ef07  carpentry.py
3b8ad6ff433f737e5031155f4ae6cac4da3e5885e5b67d2e6d2645107450d48a  frame.py
73842faf573495907ec61ceadb148f3da3e1a45f4bc394a4c9fe45e167e7df74  erection.py
02317da4e6a8571b46522aa4805f285d8b879532340d0e7f63ccd922dd309b1f  model.py
831db64250854308047ba46d7b6679cc26e4f24be816ad7554cba2a2f449a688  parts.py
5a73a2df69c70505c2014c5a2d5dfa12b348cb38aed81dd73995b6dc67adc01c  test_frame.py
ca8c043a4bea2f24d8a5e0ea43f4e5c86f289cbc02e7cbec103c91fe13c072cd  test_model.py
```

## Limits

This certifies cuttable geometry, fitted joints and a collision-checked
sampled erection sequence at the established model scale. It does not
certify full-size mill loads, wood movement, splitting, fatigue or foundations.
The display plinth is ground; A1 rests on it. F1/B2 and F2/B2 use explicit
cantilever holds in the vertical-support solver, backed by real peg capture
and ±2° tipping-interference checks. Horizontal pins assume fitted-wood
retention; no insertion-force or drawbore-deformation simulation is claimed.
Loose members are supported during erection, not simulated in free fall.
The existing force, water and rope-winding assumptions remain unchanged.
