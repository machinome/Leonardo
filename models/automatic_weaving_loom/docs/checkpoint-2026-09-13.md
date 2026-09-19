# Loom reconstruction: Studio-time checkpoint, 13 September 2026

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot requested: “reach the next checkpoint and leave things in good state
for next agent to resume the work, commit what you have done so far.” This is
a **partial implementation checkpoint**, not completed reconstruction
certification. It supersedes the earlier [grip-only pause](pause-2026-09-13.md)
as the resume entry point. Do not archive the active OpenSpec change yet.

## Authority and repository

- Work only in `/home/asa/devel/machinome-studio/projects/Leonardo`, its own Git
  repository on `main`. Verify that root before writing or committing.
- Planning commit: `cec7cf1`. This checkpoint's source and records are committed
  together; obtain its id from `git log -1` or the history of this document.
- Active machine-owned change: `reconstruct-museum-automatic-loom` under
  `models/automatic_weaving_loom/openspec/changes/`.
- The pilot authorized documented mechanical completions of concealed museum
  mechanisms. They are not measured historical facts. See [reconstruction.md](reconstruction.md).
- The pilot uses **Studio**, not the companion HTML exhibit. The duration must
  be declared in Python, not merely supplied to `machinome export`.
- Preserve the pre-existing untracked `screenshots/`. No shop, dependency,
  sibling-model or remote changes belong to this checkpoint. Nothing is pushed.

## Latest advancement

`AutomaticWeavingLoom` now declares `time = Time(loop=60)` from
`machinome.motion.ports`. Its shaft advances at 24° per machine second, so the
same four turns/eight picks span one minute. `phase`, `run`, winding travel,
all gear ratios and fixed-length opposite counterweight motion are unchanged.
Root tests now use seconds, including 289 samples across 0–60 s. Isolated
fixtures retain their own documented fractional timelines.

`machinome build automatic_weaving_loom` rebuilt the normal Studio artifact at
`_build/automatic_weaving_loom/viewer.json`. Both this artifact and the live
Studio session's served document report `animation.loop: 60`. Studio's native
Timeline control exposes ×0.1, ×0.25 and ×0.5, as well as faster options.
The export has also been regenerated with the same declaration. The attempted
export-only 1800-frame change was reversed: frame count remains 360.

The new Python time contract failed before the declaration and then passed:
0, 15, 30, 45 and 60 seconds map to 0, 360, 720, 1080 and 1440 shaft degrees.
The actual live Studio interaction check passed: native ×0.1/×0.25/×0.5,
the 1:00.0 endpoint, changed CAD pixels on reset, and playback at ×0.5. Its
screenshot was inspected. All **22/22 whole-root faceted contracts passed**
at 16 mm (399.61 s), 18 mm (408.29 s) and 20 mm (406.96 s), zero volume epsilon,
after the seconds migration. The full exact head/root certificate remains
outstanding. All runs started by this conversation are stopped or finished;
Studio itself remains open and was not stopped.

## Mechanical advancement since the previous pause

- Reproduced and corrected the 36 mm³ left jaw/frame overlap with an outboard
  bar dogleg, preserving its closed guide and keeping its inner span in the shed.
- Moved both closing springs outboard. Added real spring/yarn and all operating
  cords/springs versus all rigid components clearance checks. Only bounded
  3 mm termination zones allow actual attachment contact; no whole mate is exempt.
- Moved the reed haul tie to the follower's actual top. The former route ran
  72.5 mm inside the stem. Its fixed length is now 365.99336 mm; the attachment
  and counterweight top sum to 832.5 mm throughout motion.
- Corrected minimum-16 mm-lift yarn interference with handed jaw bars and a
  shortened right bridge. Corrected maximum-20 mm-lift cam/heddle interference
  with 42 mm selector cam base radii and correspondingly lowered follower pins.
- Final geometry passed all 21 faceted root contracts at 16, 18 and 20 mm
  before the time-unit migration. All 22 pass after it, at all three lifts.
- Final independent exact suites: timing 7/7, winding 8/8, gripping 4/4,
  cords 5/5. Head faceted 3/3. These use the corrected explicit-state sampler.
- Same-direction reed counterweight fault failed both actual rope length and
  opposed endpoint travel (3 passed/2 failed); restored exact cord suite 5/5.
  A selector phase +10° fault also failed cam capture; relation restored.
- Inspected original CAD snapshots are committed in [evidence/](evidence/README.md).
  Actual standalone desktop/narrow controls and changing/repeated CAD pixels
  passed before the Python clock migration. The final all-gallery browser gate
  has not run. The exhibit is not the pilot's primary interface.

## Validation status and artifact discipline

See [verification.md](verification.md) for counts, times and dependency commits.
Logs are copied to ignored `_evidence/automatic_weaving_loom/checkpoint-2026-09-13/`.
The current checkpoint must never be advertised as full exact certification.

The current faceted logs are `leonardo-loom-seconds-{16,18,20}-faceted.log`;
Studio evidence is `leonardo-loom-studio-time-browser-v2.log`. Older completed
fixture logs, stopped exact runs, mutations and source hashes are retained
beside them. `scripts/gallery.py check`, Python compile checks, `git diff --check`
and strict OpenSpec validation also pass at this checkpoint.

The previous boundary exact runs shared `_build/loom-final-lift16/` with an
export/build. A subsequent build pruned other parameter variants' STL files,
causing `FileNotFoundError`. Those runs were interrupted and are invalid.
Whole-head/default-root exact runs were also interrupted at this requested
checkpoint, without completed verdicts. Do not count partially printed passes.
Use a different build directory for each concurrently running configuration;
never build or export into one while a test reads it.

The project-owned `sampled_poses` helper sets **all** phase/run/time values and
restores an explicit neutral state. Do not replace this with time-only updates
or `clear_state()`: the former can inherit a held `run=0`, the latter unbinds
drivers instead of restoring defaults. Do not run these plain `TestCase`s
directly under pytest: use `machinome test`, which instantiates their node.

## Resume commands and remaining work

From the Leonardo root, with `../../.venv/bin` on PATH:

```sh
SOLID_BUILD_DIR=_build/loom-seconds-18 PYTHONUNBUFFERED=1 machinome test automatic_weaving_loom --exact
SOLID_BUILD_DIR=_build/loom-seconds-16 PYTHONUNBUFFERED=1 machinome test automatic_weaving_loom --set shed_lift=16 --exact
SOLID_BUILD_DIR=_build/loom-seconds-20 PYTHONUNBUFFERED=1 machinome test automatic_weaving_loom --set shed_lift=20 --exact
SOLID_BUILD_DIR=_build/loom-final-fixtures PYTHONUNBUFFERED=1 machinome test models/automatic_weaving_loom/head_bench.py --exact
```

Each root path above is distinct. The head's exact cam-contact check can take
more than 30 minutes; active CPU alone is not a hang. Preserve complete output
and check the final exit status. Repeat the final head-phase challenge if
needed; consider an independent lower-drive mutation to strengthen the record.
Restore faults and rerun their green contracts before final certification.

For the pilot's already-open Studio project:

```sh
machinome build automatic_weaving_loom
python models/automatic_weaving_loom/scripts/check_studio_time.py --base-url http://127.0.0.1:9000
```

This check refuses a closed project and sends no agent messages. It inspects
the actual Studio document and UI. Studio normally hides playback behind the
**Timeline** button; its **Playback speed** selector supplies slow motion.

After the mechanical gates, finish the companion exhibit regression and
delivery record:

```sh
python scripts/gallery.py check
python scripts/gallery.py export automatic_weaving_loom
python models/automatic_weaving_loom/scripts/inspect_demo.py
python scripts/check_browsers.py
```

The all-gallery runner has a 180-second per-exhibit timeout; measure the loom
check without simultaneous heavy exact jobs before diagnosing a failure.
Record real browser errors rather than weakening controls/pixel checks.
Finish the verification record and task checkboxes, strictly validate the
OpenSpec change, sync accepted baseline specs, archive, and make the final
implementation commit. A checkpoint commit does not satisfy that final gate.
Regenerate the source archive from the final committed revision; do not push.

This remains a connected kinematic reconstruction: imposed input and assumed
rope/belt tension and spring closing. Forces, wear, yarn contact dynamics,
newly woven topology and manufacturing safety are not solved.
