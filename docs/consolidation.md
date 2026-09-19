# Consolidation record — 12 September 2026

The repository root is now `projects/Leonardo` in the development workspace.
The original folders became `models/hydraulic_sawmill` and
`models/automatic_weaving_loom`; their Python sources were flattened into
`model.py`, `test_model.py` and supporting modules. Relative imports were
updated, and the root manifest now owns both named models. Machine-local
manifests were removed. Existing mechanical geometry and contracts were
retained.

## Preserved history

| Original repository | Original tip | Durable tag |
| --- | --- | --- |
| Hydraulic-sawmill | `9f4cc67a4a30194bbe580112e349d1a3b36d8c37` | `history/hydraulic-sawmill` |
| Automatic-weaving-loom | `fd0045883e77fa035131b088934452af62c5dfb3` | `history/automatic-weaving-loom` |

The loom's planning commit `39e5d98` is also retained. The sawmill was
relocated in a descendant commit; the loom tip was joined as a second
parent in a merge whose tree includes the loom under its new prefix. No
commit was squashed, rewritten, or substituted by an archive. Check with:

```sh
git log --all --graph --oneline
git merge-base --is-ancestor history/hydraulic-sawmill HEAD
git merge-base --is-ancestor history/automatic-weaving-loom HEAD
git log --follow -- models/hydraulic_sawmill/model.py
```

All ignored builds, reference material, evidence and both screenshots were
moved with their machine directories. The sawmill's previously untracked
`screenshot.png` remains local and ignored. The original Git administrative
directories are retained locally under `.git/legacy-repositories/` as a
recovery aid, not as active nested working repositories. Neither original
repo had another branch, tag, worktree or remote. The imported commits and
tags travel with this repository; the administrative backups do not need to.

## Evidence environment

Consolidation uses the existing workspace environment:

- Python 3.12; CadQuery 2.7.0; molejo 0.2.0.
- machinome checkout `685188a6be5e7a68502bb3723e5a1185d1bdf671`,
  post-0.6 development API (metadata alone still says 0.6.0).
- machinome-viewer `6fb082ba9823fb0839631bd4a3ecbf4a41b33b64`,
  local 0.1.0 / viewer API 7.
- Original per-machine evidence remains in each machine's `docs/` and
  is historical evidence, not a claim to have repeated those runs today.

The sawmill's new OpenSpec is an explicitly retrospective baseline of the
existing exhibit, not invented advance planning or a new mechanical design.

## Consolidation verification

The refactored source and registry passed on 12 September 2026:

| Check | Result |
| --- | --- |
| Named sawmill, exact default | 10 passed, 0 failed; 14.83 s |
| Named loom, exact default | 12 passed, 0 failed; 23.76 s |
| Sawmill, exact `kerf=2`, `paddles=24` | 10 passed, 0 failed; 12.42 s |
| Both named browser exports | Succeeded, retaining real model assets and controls |
| Sawmill browser | Geometry changes with scrub; feed, views, reveal, reset, play/pause, source download and 390 px layout passed; no page/HTTP errors |
| Loom browser | Handoff and Return pick land on 90° and 270°; Run resumes a changing timeline; no page errors |
| Both machine OpenSpec roots | Strict validation passed |
| Queue and registry check | Two built models, separate machine baselines, site last, next item cam hammer |
| Git integrity and ancestry | `git fsck --full` and both original-tip ancestor checks passed |

Commands: `python scripts/gallery.py test`, `python scripts/gallery.py
export`, `python scripts/check_browsers.py`, and `machinome test
hydraulic_sawmill --exact --set kerf=2 --set paddles=24`, from the root with
the workspace environment activated. Raw logs are local under `_evidence/`.

Fresh OpenSCAD images were inspected at sawmill times 0.065 (isometric) and
0.125 (shaft axis), and loom time 0.25 (isometric). The full frames fit;
the sawmill's drive/rod and the loom's separated shed are visible. The
desktop browser screenshots show both real exports with working controls.
A selected, unchanged copy of each CAD image is retained in
[evidence/](evidence/). These are evidence of this layout migration, not
continuous-motion or new manufacturing certificates.

No mechanism or geometric contract was changed: the source-module moves,
two relative test imports and copyright comments are the Python model
diff. Existing red-first and fault-injection evidence remains attributed
to its original implementation. New runs certify the relocated defaults
and the named sawmill boundary; the loom's original additional parameter
boundary runs remain historical evidence. Final-site acceptance includes
a broader all-exhibit browser and reproducibility check.

This record is committed with the tested consolidation. The later source
archive refresh only regenerates ignored exports so their source.zip and
source-revision.txt identify that committed gallery, including its queue
and instructions. The public Sphinx site remains pending item 050.
