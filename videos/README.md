# Leonardo video sources

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Each `videos/<episode-id>/` directory owns the source for one educational video:
an `episode.yaml` screenplay with narration and shot directions together,
`production.yaml` settings, evidence and release copy. Generated media belongs in the episode's ignored `_build/` directory.
No generated audio or video is committed here.

The independent `videomaker` project will consume these sources. Its renderer
is not implemented yet. Read and edit the YAML directly in a text editor;
the future tool will consume these same files. No code execution is needed
to inspect an episode.

First episode: [Leonardo's sawmill: one wheel, two jobs](hydraulic-sawmill/README.md).
