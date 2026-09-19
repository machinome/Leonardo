# Leonardo video sources

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Each `videos/<episode-id>/` directory owns the source for one educational video:
an `episode.mjs` entry point, narration, shot directions, evidence and release
copy. Generated media belongs in the episode's ignored `_build/` directory.
No generated audio or video is committed here.

The independent `videomaker` project will consume these sources. Its renderer
is not implemented yet. The dependency-free source modules can already be
imported with Node; they describe a video and have no production side effects.

First episode: [Leonardo's sawmill: one wheel, two jobs](hydraulic-sawmill/README.md).
