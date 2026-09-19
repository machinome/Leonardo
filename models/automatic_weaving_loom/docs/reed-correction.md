# Reed passage and beat-up correction — 13 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot requested a functional reed/carrier crossing before continuing
the loom. The checkpoint at `bb2a1ea` placed the reed's whole 37 mm stroke
in front of the carrier. Planning refinement `73508fa` records the correction
in the existing, machine-owned reconstruction change.

## Pilot-requested checkpoint — 10:09 UTC

The pilot requested: “this is taking too long, I'd like a wrap up. log the
state of this and commit.” Verification was stopped and the implementation
is committed as a checkpoint, not a completed reconstruction certificate.
All verification processes started for this correction are stopped. Nothing
was pushed, no OpenSpec baseline was synced or change archived, and the
unrelated untracked `screenshots/` directory is preserved.

The mechanical fix is implemented. All 26 faceted root tests pass at 16,
18 and 20 mm shed lift; the short-stroke mutation fails the intended test,
and three corrected OpenSCAD views plus desktop/narrow browser views were
inspected. The complete standalone browser check passed once before the
last readiness-wait adjustment. That adjustment still needs its final rerun.

| Final exact run | State at stop |
| --- | --- |
| Root, 16 / 18 / 20 mm | Nine methods passed in each; stopped during `test_assembly_integrity`, no complete verdict |
| Timing fixture | 7 passed, 0 failed; 69.94 s |
| Winding fixture | 8 passed, 0 failed; 1852.96 s including browser-isolation pauses |
| Head fixture | Stopped during `test_all_followers_match_their_cam_tracks`, no complete verdict |
| Grip / cord fixtures | Not reached by the final exact fixture sequence; require reruns |
| Other gallery models | Sawmill 19/19, hammer 11/11, rack 11/11, pulley 10/10, crane 12/12 passed |

The three exact root processes had run about 49 minutes wall time, including
temporary browser-isolation pauses; the head fixture about 17 minutes.
They were actively computing, not reporting a geometry failure. No stopped
or timed-out run is counted as a pass. The latest all-gallery browser run
(`reed-gallery-browsers-readiness.log`) was stopped during the sawmill check,
before it reached the loom's new `DOMContentLoaded` wait.

### Resume order

1. Verify the frozen source manifest below and preserve the existing logs.
2. Rerun final exact head, grip and cord fixtures, then the three complete
   root configurations, using distinct build directories and fresh log names.
   Root cam-flank capture, later support checks and instruction scenarios
   remain uncompleted on exact geometry; the faceted results do cover them.
3. Run `python scripts/check_browsers.py` with the committed per-loom
   600-second budget and readiness correction. Do not widen any assertion or
   infer a gallery-wide pass from the successful standalone run.
4. If all gates pass, update the certificate and README, finish tasks 4.2–4.5,
   sync baseline specs and archive the existing machine-owned change.
   Do not start the public-site queue item as part of this correction.

## Construction

The reed now travels 100 mm from Y=148, behind the carrier at Y=115, to
Y=48 beside the fell at Y=45. It dwells behind the hands during insertion,
crosses only after their withdrawal, beats, and returns before the next
insertion. The two directions occupy 26° either side of each beat.

The U-shaped guide bed and its timber supports span the complete stroke
under the carrier. Selector ties move behind the parked reed to Y=158 and
rise 22 mm to Z=466, clearing both the guide legs and cam rims. Their rear
bridges remain below the lowered heddles. Local timber bridges carry the
side rails over their vertical clearance slots.

A larger reed cam at X=−365 remains part of the same input shaft. The
shaft is extended and supported; a guide at Z=590 captures the longer
follower. The groove offsets a periodic spline normally, with 0.15 mm
nominal roller clearance. Its 70 mm base radius preserves capture through
the tight beat turn. The haul sheaves rise to Z=730, and the reed's haul bar
passes above the selectors at Z=570. Separate haul and return attachments
at X=−357 and −331 keep the return clear of the follower and support post.
Both cords retain their lengths, and the return weight moves oppositely.

The displayed red weft bends ahead of the reed while its free end remains
on the spool. This is prescribed contact in the existing schematic yarn
display. It does not solve weft length, yarn forces or new woven topology.
All concealed dimensions are original reconstruction choices.

## Failure evidence and regression coverage

- The new crossing regression failed on the checkpoint: at 45°, measured
  reed Y=66.5 instead of the required rear dwell at Y=148 (2 passed, 1 failed,
  faceted, fail-fast). The old test's Y=48/85 expectations were the blind spot.
- The red-weft regression failed independently: the displayed yarn remained
  at Y=76.5 within the ribbon at beat-up, instead of reaching Y≤46.55.
- Integration exposed a return cord crossing the shaft/follower, a support
  beam touching an arm cam, an unsupported guide bed, and selector ties
  crossing the tracks and reed legs. Those were corrected in geometry,
  without removing any whole-root check or adding volume tolerance.
- A small-radius reed cam did not retain its roller at beat; a polygonal
  normal offset produced a non-watertight mesh. The larger-base periodic
  curve replaces both unsuccessful constructions.
- The root now measures all four carrier-plane crossings over a 1° sweep,
  both end positions and rear dwells, rail capture throughout the stroke,
  red-weft approach and attachment, and roller capture every 2° through both
  beat sectors. The prior 45° capture samples saw only the reed cam's dwells.
- The actual warp-clearance sweep now includes the reed as well as the
  hands, spool and springs. Existing complete-root connectedness, 289-pose
  interference sweep, transition checks, support, cord routing and length,
  drive capture, handoff and instruction scenarios remain active.

## Validation record

Tested mechanical source: checkpoint `f50446d`. Its Python files match the
frozen source manifest; this provenance note changes no model or test code.

Implementation verification is paused at the pilot's request; no final exact
certificate is claimed. Raw logs and development renders are under
ignored `_evidence/automatic_weaving_loom/reed-*`. The frozen mechanical-source
manifest is `reed-final-sources.sha256` in that directory; validate it before
associating these results with a later commit.

The five fixture regressions passed on the faceted kernel: timing 7/7,
winding 8/8, head 3/3, grip 4/4 and cords 5/5. The head was rerun after the
final selector routing change; the isolated grip result predates that last
selector reroute and needs a final rerun. All 26 whole-root tests pass at each advertised
shed lift: 16 mm in 221.56 s, default 18 mm in 218.45 s, and 20 mm in
222.05 s, with zero interference volume epsilon.

Reducing the reed drive ratio to 0.37 deliberately restored the short
stroke. The new crossing test failed at the rear dwell: measured Y=85
instead of 148 mm (2 passed, 1 failed). Restoring the ratio preceded all
final exact runs. The three final OpenSCAD views have been inspected:
rear dwell at 90°, carrier-plane crossing at 15.84°, and beat at 180°.
The finite build and real export succeed. Both documents publish the reed's
Y=148 rear location and `animation.loop=60`. The native Studio browser check
also passes speed selection, the one-minute endpoint, changed CAD pixels
and playback; its inspected screenshot shows the corrected outboard drive.
The session closed during this check, after its browser had loaded; the
subsequent catalogue reports it closed. No project was reopened or message
sent. The remaining exact and all-gallery browser checks are paused.

The first all-gallery browser attempt ran alongside four heavy exact jobs.
The sawmill passed, and the loom passed its desktop stages, controls, pose
return, layout and measured 60.99-second playback period. The 180-second
per-exhibit deadline expired before completing the narrow viewport. That is
an incomplete run, not a browser pass. An isolated rerun, with the four exact
processes suspended, also reached the 180-second deadline after desktop
acceptance (60.41-second playback) and the first narrow-stage interaction.
The gallery runner therefore accepts a per-exhibit process budget: the dense
loom gets 600 seconds, while every other exhibit retains 180. This changes
no stage, geometry, layout, pixel-return, playback-period, console, network
or individual control deadline. A complete rerun is required, not an inferred
pass. Exact-test wall times include these browser-isolation pauses; their
model sources and build directories remain unchanged.

The intermediate 360-second run passed both viewports but expired before its
final wrap-up. A separately timed, unchanged browser script completed in
484.6 seconds under concurrent geometry work: desktop playback 59.83 seconds,
narrow playback 60.01 seconds, all stage/manual controls, repeat and moving
CAD pixels, layout, manifest assets, source ZIP inventory, and no console or
network errors. Pixel captures accounted for most of the time; the final ZIP
request and checks took 0.1 seconds and browser shutdown took 29.8 seconds.
The 600-second budget follows that complete measurement, not an assertion
relaxation. Timing instrumentation was external. Raw trace:
`reed-browser-timed.log`.

A subsequent gallery run passed desktop but hit the independent 30-second
`networkidle` navigation deadline on narrow reload. Following
[Playwright's navigation guidance](https://github.com/microsoft/playwright/blob/main/docs/src/api/params.md#navigation-wait-until),
the browser script now waits for `DOMContentLoaded`; existing visible-canvas,
native-control, CAD-pixel, asset and error assertions establish readiness.
Every acceptance assertion is retained. The network-silence timeout is
recorded in `reed-gallery-browsers-accepted.log`, not counted as a pass.

All six registered models build successfully. The first additional-gallery
test attempt was stopped when its build directory overlapped the concurrent
build; no result from that attempt is used. The final other-model regressions
use their own `_build/loom-gallery-regression-<model>` directories.

Reproduction commands, from the gallery root with the workspace environment:

```sh
SOLID_BUILD_DIR=_build/loom-reed-fix machinome test automatic_weaving_loom --faceted
SOLID_BUILD_DIR=_build/loom-reed-16 machinome test automatic_weaving_loom --set shed_lift=16 --faceted
SOLID_BUILD_DIR=_build/loom-reed-20 machinome test automatic_weaving_loom --set shed_lift=20 --faceted
SOLID_BUILD_DIR=_build/loom-reed-fix machinome test automatic_weaving_loom --exact
SOLID_BUILD_DIR=_build/loom-reed-16 machinome test automatic_weaving_loom --set shed_lift=16 --exact
SOLID_BUILD_DIR=_build/loom-reed-20 machinome test automatic_weaving_loom --set shed_lift=20 --exact
SOLID_BUILD_DIR=_build/loom-reed-delivery machinome build automatic_weaving_loom
python scripts/gallery.py export automatic_weaving_loom
python scripts/gallery.py check
python scripts/check_browsers.py
python models/automatic_weaving_loom/scripts/check_studio_time.py --base-url http://127.0.0.1:9000
```

Each fixture is checked with `machinome test models/automatic_weaving_loom/<fixture>.py
--exact` (and `--faceted` during development), where `<fixture>` is `timing`,
`winding`, `head_bench`, `grip_bench` or `cord_bench`.

Every configuration has a separate build directory. Do not publish a build
or export into a directory while a test is reading its artifacts. Source
edits must wait until those test processes finish.

Dependencies observed during this correction:

| Dependency | Content revision / installed version |
| --- | --- |
| machinome | `6e41f2da132a8604f9b68895967247fb8876fc4d`, reports 0.6.0 with post-release APIs |
| machinome-viewer | `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`, local 0.1.0 |
| molejo | `e76c9039cf906cfc0005324d78ccee7116e0ff4a`, 0.2.0 |
| CadQuery | 2.7.0 |

The project uses the enclosing workspace's `.venv/bin/machinome` and Python.
`machinome snapshot --time` takes a normalized fraction of the 60-second loop;
the root tests' `set_state(time=...)` takes machine seconds. Thus a snapshot
at `0.0625` is the 90° handoff, while `set_state(time=3.75, run=1, phase=0)`
is the same pose in the tests.
