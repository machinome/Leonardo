# Leonardo video sources

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The only active video on `main` is the Machinome release film,
[Revolutions](machinome-revolutions-v2/README.md). Its screenplay opens with
“A wheel makes a revolution,” followed by “More than five hundred years ago,
Leonardo da Vinci studied a machine.” Continue production in that directory;
the full film is still a draft, with an existing opening rehearsal.

`episode.yaml` owns narration and shot directions; `production.yaml` owns
settings and evidence. Generated media and cached speech stay in the episode's
ignored `_build/` directory, outside Git.

All earlier films, alternate versions, pronunciation trials and tool demos
are preserved on the local `video-experiments` branch, including sources
that were previously untracked. Keep those experiments on that branch;
do not merge its video collection back into `main`.
Its archive checkout is `/mnt/data/machinome-projects/Leonardo-video-experiments`,
where the existing generated experiment media is also preserved locally.

The independent `videomaker` project consumes the release sources. See the
film's README for its current production procedure and remaining work.
