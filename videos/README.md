# Leonardo video sources

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The selected release film on `main` is
[Revolutions — cut 5](machinome-release-5/README.md): the Studio sequence,
descending open-source technology stream and continuous Jessica narration,
without sound effects. Its current deliverable is the 203.625-second web
preview; the older saved MP4 does not contain the latest scenes.
The sound-effects experiment is preserved separately on the local
`release-video-sound-effects` branch, with its generated audio retained in
the original checkout's ignored build directory.

[Cut 5 in Brazilian Portuguese](machinome-release-5-pt-br/README.md) is a
separate copy with its first complete, directed Leo narration available
for listening. Its video has not yet been synchronized to that take.

The earlier rendered release-film proposal is
[Revolutions — proposal 1](machinome-release-1/README.md), following the
pilot's [original brief](machinome-release.md): a dark, continuous camera encounter
with the sawmill, its real Python source, the film's own source and the
open-source technology wheel. It has a narrated first review cut.

[Proposal 2](machinome-release-2/README.md) has a revised, **single-take
narration** ready for listening (2:16.40, including the two listening-review
amendments), the original brief, the pilot's
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
