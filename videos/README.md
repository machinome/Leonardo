# Leonardo video sources

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The current rendered release-film proposal is
[Revolutions — proposal 1](machinome-release-1/README.md), following the
pilot's [original brief](machinome-release.md): a dark, continuous camera encounter
with the sawmill, its real Python source, the film's own source and the
open-source technology wheel. It has a narrated first review cut.

[Proposal 2](machinome-release-2/README.md) has a revised, **single-take
narration** ready for listening (2:19.44), the original brief, the pilot's
[review of proposal 1](machinome-release-review-1.md), and the continuity
assessment. Its visual second cut has not been rendered. The review
supersedes the original brief where it changes it; both human-written records
are preserved verbatim.

The earlier [Revolutions study](machinome-revolutions-v2/README.md) remains
available. Its screenplay opens with
“A wheel makes a revolution,” followed by “More than five hundred years ago,
Leonardo da Vinci studied a machine.” It retains its earlier full-film
draft and opening rehearsal; new proposal work is in `machinome-release-1/`.

The current proposal uses `movie.py` for narration, shots and production
declarations, with its own stage and visual-direction document. The earlier
study uses `episode.yaml` and `production.yaml`. Generated media and cached
speech stay in each film's ignored `_build/` directory, outside Git.

All earlier films, alternate versions, pronunciation trials and tool demos
are preserved on the local `video-experiments` branch, including sources
that were previously untracked. Keep those experiments on that branch;
do not merge its video collection back into `main`.

The independent `videomaker` project consumes the release sources. See the
film's README for its current production procedure and remaining work.
