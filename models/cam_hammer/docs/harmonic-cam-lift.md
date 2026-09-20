# Harmonic cam-lift migration

This behavior-preserving refactor delegates the local follower envelope to
`machinome_mechanics.harmonic_cam_lift`. The local adapter explicitly retains
the 240-degree rise and its `return_span=80` default. The physical cam profile
continues to request `return_span=45`, so it retreats by 285 degrees while the
prescribed hammer return continues to 320 degrees. The independent piecewise
test oracle remains project-owned and unchanged.

## Source identity

- Project base: `87b76494fe9509b82b72468e9448a2949c908d42`
- Project branch: `mechanics-harmonic-cam-lift`
- Mechanics planning commit: `8d40d0a6b23490a715187f81e4e9b2f3bfc4ad43`
- Tested uncommitted mechanics `machinome_mechanics/cams.py` SHA-256:
  `ee7e70d16cad6e6403743d58d86af78d2b97a58d5fc3028d1fd75f64518293c5`
- Framework before validation:
  `8d2bd71171be81f13ba5dd492851ed8b3a9ababb` (clean, locally ahead of its
  remote)
- Viewer before validation:
  `4355da1a7f64dacd7d86eb27dbdfdf7ced94598f` (clean)

The file digest identifies the tested helper implementation beyond its
planning commit. Leonardo already declares `machinome-mechanics`; version
0.1.0 is founded but unpublished, so these checks use the named source
worktree without changing the shared environment.

## Validation discipline

Every command that imports this CAD model runs alone through a user-systemd
unit with `MemoryMax=768M`, `MemorySwapMax=0`, `RuntimeMaxSec=300`, and one
OpenBLAS/OMP thread. `/usr/bin/time -v` records process RSS. Build artifacts
use ignored `_build/harmonic-cam-lift-*` paths; logs and selected generated
images are retained outside those recreated trees under the ignored
`_evidence/harmonic-cam-lift/` directory.

The common command envelope was:

```sh
systemd-run --user --wait --pipe --collect --unit=<unique-name> \
  -p MemoryMax=768M -p MemorySwapMax=0 -p RuntimeMaxSec=300 \
  --property=WorkingDirectory=/mnt/data/machinome-projects/Leonardo \
  --setenv=PYTHONPATH=/mnt/data/machinome-projects/Leonardo:/home/asa/devel/machinome-studio/WTs/mechanics-harmonic-cam-lift \
  --setenv=OPENBLAS_NUM_THREADS=1 --setenv=OMP_NUM_THREADS=1 \
  /usr/bin/time -v <command>
```

## Independent parity probe

Command:

```sh
python models/cam_hammer/docs/probes/harmonic_cam_lift.py
```

Result: PASS for 168 numeric adapter values across signed turns, seam
neighborhoods, lifts 16/18/20/-18 and both return spans; 21 evaluations of
the actual production follower relation with a deferred animation-time value;
and all 2,160 physical-cam profile points at lifts 16/18/20. The legacy oracle
retains the exact former square-root clip algebra rather than using the new
helper's clamp. The bound-law check identifies the relation's driven node and
`swing` coordinate instead of assuming position alone. Elapsed 3.55 seconds,
maximum process RSS 524,956 KiB, no swap. Log:
`_evidence/harmonic-cam-lift/probe4.log`.

Two earlier probe attempts are retained as probe-development evidence. The
first evaluator omitted degree `cos`; the second exposed a mistakenly removed
`sin` import still needed by `pitch_point`. Both failed before completing the
profile comparison and were corrected without changing the helper. Logs:
`_evidence/harmonic-cam-lift/probe.log` and `probe2.log`. `probe3.log` records the first complete pass
before the oracle was strengthened to use the exact former clip algebra.

## CAD contracts and build

Commands:

```sh
SOLID_TEST_KERNEL=faceted machinome test cam_hammer --faceted
SOLID_TEST_KERNEL=exact machinome test cam_hammer --exact
machinome build cam_hammer
```

The build passed in 10.05 seconds with maximum process RSS 515,880 KiB and no
swap (`_evidence/harmonic-cam-lift/build.log`).

The full test commands did not fit the mandatory 768 MiB process-tree cap and
are incomplete, not suite passes. Faceted testing passed the 37-sample assembly
integrity method plus cam contact, ground/anvil seating, intermediate
lift/return, nine-sample shaft capture and parameter guards before the cgroup
killed it on the release-gap method after 15.19 seconds. Exact testing passed
the 37-sample assembly and cam-contact methods before reaching the ground check
and being killed after 25.86 seconds. Both reached exactly 768 MiB charged
memory with zero swap. Logs: `_evidence/harmonic-cam-lift/faceted.log` and
`exact.log`.

The project record's historical uncapped certification reports 11/11 at
default, 16 and 20 degrees on both kernels; it is context, not a current
baseline run. It was not relabelled as capped evidence or rerun after the cap
failures. The independent probe's exact 2,160-point profile
comparison and actual bound-law evaluation directly cover this refactor; the
partial CAD runs retain unchanged contact and assembly evidence without
weakening assertions or tolerances.

## Fresh visual evidence

Commands:

```sh
machinome snapshot cam_hammer \
  -o _build/harmonic-cam-lift-lift.png --autocenter --viewall \
  --time 0.333333333 --imgsize 1400x1000
machinome snapshot cam_hammer \
  -o _build/harmonic-cam-lift-release.png --autocenter --viewall \
  --camera 0,0,0,90,0,0,600 --time 0.694444444 --imgsize 1400x1000
```

Both OpenSCAD snapshots passed: lift in 5.97 seconds at 668,904 KiB maximum
RSS, release in 6.04 seconds at 669,352 KiB, with no swap. Logs are
`_evidence/harmonic-cam-lift/lift-image.log` and `release-image.log`.
After successful inspection, the generated images were moved from those exact
command output paths to retained
`_evidence/harmonic-cam-lift/harmonic-cam-lift-lift.png` and
`harmonic-cam-lift-release.png`; their bytes were not regenerated.
Inspection found the lift pose assembled with the shoe at the cam and hammer
head raised. The shaft-axis release pose shows the intended open cam/shoe gap,
returning lever, seated pivots and intact frame. Pixels do not certify hidden
contact or clearance; the geometric contracts and parity probe provide that
evidence.
