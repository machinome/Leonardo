# Full timber pass — 19 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot requested the complete timber course, useful assembly navigation,
timeline-only controls and a molejo cutting insert. After rejecting the short
100 mm trial, the pilot requested museum-like proportions and a tight fit.
The delivered reconstruction uses 320 mm timber, a 420 mm carriage, a 720 mm
table and 760 mm rails. Planning baseline: `fbf4cd6`; preceding source:
`80e01fc`. No dependency was edited and nothing was published.

## Tested source and environment

Git blob IDs identify the actual model/test content, without a self-referential
implementation commit:

| File | Git blob |
| --- | --- |
| `model.py` | `2fe2f71098458523e1f63eb3f51d68878f69c905` |
| `parts.py` | `03ceee098c8dcbfef51f910eede21c6a99b522fb` |
| `layout.py` | `af06cf7443142431f4d15a496f2fd898af55726e` |
| `kinematics.py` | `bee3183158b688f56e92924083fa877264739cca` |
| `test_model.py` | `ea68ca8172457e7bd94acdcb4726baa101faad94` |

- Framework content `df0bee4c7a5c727becf9ea33b7409ef796256a3d`, development
  metadata 0.7.0.
- Viewer content `8495d74be1329c2c3170a03c66aab5f02d5d7442`, development
  metadata 0.2.0, API 20. These are installed development versions, not release claims.
- Python 3.12, CadQuery 2.7.0, molejo 0.2.0, Playwright 1.62.0;
  headless Chromium/SwiftShader on Linux.

## Mechanical evidence

The endpoint test failed on the original timber's leading face at X=105 mm,
already past the teeth. The insert test failed before the node existed.
The pilot's proportion correction was proved red against the 100 mm trial:
measured length 100 mm, required 320 mm. Tight-clearance assertions now bound
both entry and exit gaps, as well as requiring positive clearance.

A deliberate mutation halved the uncut insert's remaining length. Its test
measured 160 mm instead of 320 mm and failed. The mutation was removed and
the unchanged test passed again.

The extended frame initially left the pulley bracket disconnected; its
support beam now reaches the moved leg. The first narrow rope cleat also
split around its bore; its width now preserves the surrounding iron. Root
connectedness caught both. No collision epsilon or omitted rigid part was used.

| Run | Result |
| --- | --- |
| Default, faceted after mutation restoration and final rope representation | 23 passed, 0 failed; 19.72 s |
| Default kerf 3.2 mm, exact | 23 passed, 0 failed; 261.26 s |
| Kerf 2 mm, exact | 23 passed, 0 failed; 261.33 s |
| Kerf 5 mm, exact | 23 passed, 0 failed; 262.66 s |

All runs use zero volume epsilon. Whole-root rigid integrity covers 149
instants over 296 seconds, plus a 2-degree sweep over one wheel turn and
transition neighborhoods. Linkage closure, tooth engagement, blade attachment,
keys, journals and guides remain checked.

Independent mesh measurements establish 320 mm timber length, 1 mm initial
bark-to-teeth clearance and 4.062622 mm trailing-face clearance at completion.
End-grain veneers also clear the blade. Seventy-four wheel turns give
340.062622 mm travel; the saw stroke remains 48 mm. The carriage dwells during
cutting, both halves stay supported by slotted cradles, and rollers remain on
the rails with downward perturbations blocked. Neither axle crosses the blade.

Thirteen rope poses include endpoints and the final-turn neighborhood.
Measured joins, pitch radius, helical pitch, constant centerline length
(961.663819 mm), take-up and both bored attachments are checked. Winding grows
from 15° to 847.5°, with 3.2 mm axial separation versus 1.8 mm rope diameter.
The carriage law includes the small fleet-angle change in the lower span.

Molejo's B-rep evaluator refused the original combined return curve with its
angled final span: it produced SurfaceOfExtrusion while claiming analytic
zero-tolerance surfaces. The project uses an equivalent separate straight
sweep for that span. Direct B-rep evaluation of all three rope leaves succeeds
at start, midpoint and endpoint. The library was not patched or its refusal
suppressed. Helical B-reps carry molejo's declared 1e-6 approximation tolerance;
line/arc sweeps are analytic.

The insert is separately checked against blade, cradles and both timber
halves while it has volume. Its front recedes at X=-10.2 mm. Length and volume
are independently derived from measured timber position. Completion has finite
vertices and exactly zero mesh area/volume.

## Presentation evidence

The real export has no drivers or instructions, a 296-second loop and five
functional root groups. Timber and running gear have separate subgroups.
All referenced rigid assets exist. The exhibit's 721 first-turn stroke/feed
samples and 75 measured turn endpoints are checked against actual CAD.
Readout interpolation does not drive the geometry.

The final browser run passed at 1440x1200 and 390x844, covering
full-pass seeks, readouts, pixel changes and exact pose return, play/pause,
replay reset, camera views, reveal, assembly disclosure, source archive,
overflow, console and asset failures. Native inspection checks one timeline,
no input controls, carriage disclosure and Timber focus using Enter.

The viewer's native per-row Focus button was observed to have its pointer
target intercepted by a neighboring row. The documented Enter navigation
works; no forced click or dependency patch hides that limitation.

The [start, mid-cut and end snapshots](evidence/README.md) show the revised
long timber, tight blade clearance and progressive cut. They use OpenSCAD,
not illustrative image generation. Browser captures are retained under ignored
`_evidence/hydraulic_sawmill/browser/`.

## Broader regression and limits

The shared gallery launcher resolves `machinome`, correcting its stale
`solid` lookup. The gallery inventory check passes for all six models.
All six existing faceted suites passed; the sawmill was rerun after its
proportion revision. The broader browser run passed the loom, hammer and
rack exhibits but stopped at the untouched pulley exhibit: its iframe canvas
did not appear within the check's timeout. This is not an all-gallery browser
certificate. Unrelated models were not edited to conceal that failure.
The untouched loom's exact run was stopped after more than 20 minutes in
its whole-root integrity check; it is incomplete, not a passing regression.
Other untouched exact regressions passed: cam hammer 11/11 (65.39 s),
rack and pinion 11/11 (97.49 s), compound pulley 10/10 (60.96 s).
The untouched crane's bounded exact regression reached its screw engagement
test but exceeded the 240-second limit; it is also incomplete. These broader
limits do not replace the completed default/boundary sawmill certificates.

Checks sample geometry; they do not prove continuous swept volumes or
force/fluid/cutting behavior. The insert is a 56 mm-high visual approximation
within the bark envelope. Its final 0.1 mm loses height to reach zero area;
that collapsed mesh is intentionally not an OCCT solid. Orderly helical rope
winding and maintained tension are prescribed; there is no level-wind device
or force solver. Small fleet-angle changes at segment joins are approximated.
Loop reset replays the exhibit, not an automatic historical machine return.

The former four-turn certificate remains in [validation.md](validation.md).
