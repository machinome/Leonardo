<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Cut and Advance

The first film of this project declared in Python: `movie.py` is the whole
screenplay, `spec.md` says what each shot was written to prove, and
`description.md` is the draft of the upload description that carries the
attribution the film's frames do not. It is the validation film of
Videomaker's declarative-python campaign, produced on 30 September 2026.

The movie is declared in the project's `pyproject.toml` under
`[tool.machinome.movies]` as `cut_and_advance`. It films the posed sawmill
export at revision `28b43bce1b88446995f0ff231dd9075d1a839ab3` (1460 s
loop), through the machinome-viewer API 28 bundle built from source.

## Produce it

From the Videomaker checkout that carries the declarative-python campaign,
with the workspace venv's Python and the speech key available to the
`speech` command:

```sh
python -m machinome_movie evaluate <this project> cut_and_advance
node bin/videomaker.mjs speech   <this project>/videos/cut_and_advance/_build/movie.json
node bin/videomaker.mjs check    <this project>/videos/cut_and_advance/_build/movie.json --viewer <bundle>
node bin/videomaker.mjs preview  <this project>/videos/cut_and_advance/_build/movie.json --viewer <bundle>
node bin/videomaker.mjs render   <this project>/videos/cut_and_advance/_build/movie.json --viewer <bundle>
```

`evaluate` writes `_build/movie.json`, the data document the tool reads;
`check` writes `_build/movie-resolved.json`, the same document with every
spoken anchor resolved against the cached takes to seconds on the frame
grid. Both are build products, ignored by Git; `movie.py` is the source.
Render at the movie's own frame rate: a quick render at another rate may
be refused, since the film is a whole number of frames on its own grid.

## What came out

Five chapters, eleven shots, 58.97 s at 1920×1080 and 30 fps; the narrator
sets the pace and every cut follows her. The takes measured 5.68, 12.64,
11.76, 11.76 and 10.32 s. `_build/rehearsal.mp4` with `rehearsal.srt` beside
it, `storyboard.jpg`, `preview/report.json` and `rehearsal-manifest.json`
are the evidence; findings went to Videomaker's `workflow/warts.md`.
