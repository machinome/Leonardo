<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Cut and Advance — validation film specification

Status: specification written 30 September 2026, before any of the code it
validates exists. It is the empirical validation of Videomaker's declarative
Python API: the film is produced from the Python source below, on the
existing renderer, and inspected by the pilot. Names of the API are
provisional; the shot list and what each shot validates are the contract.

## The lesson

Leonardo's hydraulic sawmill does two jobs with one waterwheel: it drives
the saw's stroke, and it feeds the timber forward one ratchet tooth per
stroke. The film shows the drive train, reads the one line of source that
couples wheel to crankshaft while the picture highlights the same parts,
watches the two pawls take turns in slow motion, follows the two ropes to
the carriage, and closes on the rhythm of cut and advance. About 100
seconds, 1920×1080, 30 fps, landscape. Honest about simplifications: posed
kinematics, no forces, no cutting simulated; a reconstruction, not an
artifact.

## What the film must prove

| capability | shot |
|---|---|
| Movie declared in `pyproject.toml` under `[tool.machinome.movies]`, evaluated to a `machinome-movie/0.1` document | whole film |
| Chapter narration as one continuous take; shots cut on spoken phrases | every chapter |
| Spoken anchors (`spoken`, `spokenEnd`, `plus`) on shot ends, camera keys, cue starts and ends | `question`, `coupling`, `pawls`, `shaft` |
| Marks on the loop take resolved to model seconds, with easing into a hold | `pawls` |
| The `paper` set (model stage) and the `paper-split` set (source beside model) | `wheel`, `coupling` |
| Synchronized cue: one anchor fires an action on the source element and on the model view | `coupling` |
| Typed, export-pinned source with spoken emphasis | `coupling` |
| Highlight with ghosted and dimmed others | `coupling`, `pawls`, `carriage` |
| Ring, arrow and label annotations following parts, with draw and fade entrances and exits | `stroke`, `pawls`, `shaft` |
| Camera move that changes field of view and up (Viewer API 28) | `shaft` |
| Camera moves with named easing | `hook`, `shaft` |
| Title with subtitle fading over the moving model | `question` |
| Spoken word reveal | `rhythm` |
| Picture: a still with keyed pan and zoom, project media with credit and rights | `still` |
| Transitions: dissolve, wipe, fade in, fade out | `coupling`, `stroke`, `hook`, `rhythm` |
| Part references written as declaration paths of the model class, resolved to export names | every `View` cue |
| No credit in the frames or the audio; attribution in the description | whole film |

## Shot list

Times are indicative. Spoken anchors are resolved from the cached take; only
literal durations and model seconds are authored.

### Chapter 1 — `question` (about 11 s)

Narration: *"A waterwheel can move a saw. But how does it feed the log
forward at just the right moment?"*

1. `hook` — set `paper`, camera `title-wide` moving to `title-near` with
   `out` easing over the shot; model runs 428 → 436; fades in from the paper
   colour over 1 s. Until spoken "But".
2. `question` — camera `title-near` held; model continues to 440; a title
   "CUT AND ADVANCE" with the subtitle "One wheel, two jobs" fades in at the
   cut and out before the shot ends. Until the narration ends plus 0.8 s.

### Chapter 2 — `drive` (about 24 s)

Narration: *"Water passes beneath the wheel and turns a shaft. In the model,
the waterwheel drives the crankshaft. A crank and a connecting rod turn that
rotation into the saw's stroke."*

3. `wheel` — set `paper`, camera `drive`, hiding structure, foundation and
   carriage; model 440 → 444. Until spoken "In the model".
4. `coupling` — set `paper-split`: left, the source lines 413–415 of
   `models/hydraulic_sawmill/model.py` typed through line 415 in the first
   0.6 s; right, the same view. Dissolve in over 0.6 s. One cue at spoken
   "waterwheel" highlights the undershot waterwheel with others ghosted and
   lights `waterwheel` in the source; at spoken "drives" lights `drives`; at
   spoken "crankshaft" the highlight moves to the keyed crankshaft and
   `crankshaft` lights; the marks clear 0.9 s after the phrase ends. Until
   the phrase "drives the crankshaft" ends plus 0.9 s.
5. `stroke` — set `paper`, camera `drive` moving to `whole-near` with
   `smooth` easing; wipe in from the right over 0.6 s; an arrow "Connecting
   rod" draws on at spoken "connecting rod" and fades out 0.4 s before the
   shot ends. Until the narration ends plus 0.6 s.

### Chapter 3 — `feed` (about 26 s)

Narration: *"Watch the timber. On the cutting stroke the rocker pulls a hook,
the driving pawl, and the ratchet turns one tooth. On the return, a holding
pawl keeps that progress."*

6. `pawls` — set `paper`, camera `pawls`, hiding structure, foundation, water
   and carriage. Model keyframes: at the cut, mark `pull_start` (436); at
   spoken "On the return", mark `return_start` (438) with `out` easing, so the
   pull plays slowly and settles; at the end, mark `cycle_end` (440). A ring
   draws on around the driving pawl at spoken "the driving pawl" and fades at
   spoken "On the return", with a label "Driving pawl" beside it; from spoken
   "a holding pawl" a ring draws on around the holding pawl until the end,
   with a label "Holding pawl". A highlight ghosts everything but the driving
   pawl and the ratchet during the pull, and dims everything but the holding
   pawl during the return. Top overlays "Pull · one tooth" and "Return ·
   hold" follow the same anchors. Until the narration ends plus 0.8 s.

### Chapter 4 — `ropes` (about 19 s)

Narration: *"Two ropes share one winding shaft. Rope one unwinds from the
large drum while rope two winds onto the thin section, and the carriage
moves the timber into the blade."*

7. `shaft` — set `paper`, camera `rope-wide` moving to `reduction-rolled`,
   which changes field of view and up, with `smooth` easing until spoken
   "and the carriage"; hiding structure, foundation and water; model 440 →
   448. A label "Rope 1" fades in on the large-radius rope reserve at spoken
   "Rope one" and a label "Rope 2" on the central take-up at spoken "rope
   two"; both fade out at the shot's end. Until spoken "and the carriage".
8. `carriage` — camera `whole-near`, hiding structure and water; the timber
   carriage highlighted with others dimmed for the whole shot; dissolve in
   over 0.6 s. Until the narration ends plus 0.6 s.

### Chapter 5 — `closing` (about 16 s)

Narration: *"Cut. Advance. Cut. Advance. The linkage sets the rhythm.
Explore the interactive model, linked in the description."*

9. `rhythm` — set `paper`, camera `whole-near`; model 448 → 456; a top
   overlay "Cut. Advance. Cut. Advance." whose words appear as they are
   spoken. Until spoken "The linkage".
10. `still` — the project still `sawmill-isometric.png` over the whole frame,
    fading in over 0.5 s, its view pushing from the whole image to a 1.4×
    zoom on the mechanism with `in-out` easing, fading out 0.5 s before the
    end; the model continues beneath. Until spoken "Explore".
11. `invitation` — camera `whole-near` to `whole` with `in-out` easing;
    model to 462; fade out to the paper colour over 1.2 s. Until the
    narration ends plus 1.2 s.

## The Python source

The target `videos/cut_and_advance/movie.py`, as far as this specification
can write it before the API exists. The `declarative-movie` change must make
a source of this shape evaluate; where it changes a spelling, this file is
updated with it and the change says why.

```python
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome_movie import (Movie, Chapter, Shot, Narration, Cue, Camera,
    Layer, Loop, View, Source, Still, Title, Label, Arrow, Ring, Reveal,
    Paper, PaperSplit, Dissolve, Wipe, FadeIn, FadeOut, Format, Narrator,
    Credits, Release, Evidence)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill

# The mill before the camera: the posed loop with its marks, cameras, layers,
# source excerpts and pictures. Reusable by any movie of this project.
class Sawmill(Loop):
    model = Mill
    export = "../../export/hydraulic_sawmill"
    marks = {"pull_start": 436, "return_start": 438, "cycle_end": 440}
    readiness = "Posed sawmill export; forces and material removal are not simulated."
    whole = Camera(position=(900, -1400, 1000), target=(0, 0, 250), fov=37)
    whole_near = Camera(position=(740, -1170, 870), target=(0, 0, 250), fov=37)
    title_wide = Camera(position=(1450, -2250, 1460), target=(0, 0, 650), fov=37)
    title_near = Camera(position=(1350, -2100, 1375), target=(0, 0, 650), fov=37)
    pawls = Camera(position=(145, 410, 400), target=(135, 0, 332), fov=37)
    rope_wide = Camera(position=(-540, 830, 610), target=(-80, 0, 300), fov=35)
    reduction_rolled = Camera(position=(-590, 350, 425), target=(-305, 0, 315), up=(0.15, 0, 1), fov=42)
    drive = Camera(position=(660, -1125, 455), target=(0, -135, 145), fov=37)
    structure = Layer(Mill.frame.timber_structure)
    foundation = Layer(Mill.frame.foundation)
    water = Layer(Mill.water_drive.channel, Mill.water_drive.water)
    carriage = Layer(Mill.carriage)
    coupling = Source("../../models/hydraulic_sawmill/model.py", lines=(413, 415))
    isometric = Still("media/sawmill-isometric.png",
                      credit="Leonardo project render of the reconstructed sawmill",
                      rights="Project-owned reconstruction render, AGPL-3.0-only", upscale=1.85)

jessica = Narrator(provider="elevenlabs", model="eleven_v3", voice="cgSgspJ2msm6clMCkdW9",
                   label="Jessica", output="pcm_24000",
                   settings={"stability": 0.5, "similarity_boost": 0.75},
                   direction="Curious, clear, unhurried. Leave room to watch the mechanism.")

class Question(Chapter):
    lines = Narration("A waterwheel can move a saw. But how does it feed the log forward at just the right moment?")
    mill = View(Sawmill, camera=Sawmill.title_wide)
    hook = Shot(Paper, {Paper.stage: mill}, until=lines.spoken("But"), fade_in=FadeIn(1.0),
                model=Sawmill.run(428, 436),
                cues=[Cue(0, mill.move(Sawmill.title_near, ease="out", until=lines.spoken("But")))])
    question = Shot(Paper, {Paper.stage: mill}, until=lines.end(plus=0.8),
                    model=Sawmill.run(436, 440),
                    cues=[Cue(0, Title("CUT AND ADVANCE", subtitle="One wheel, two jobs",
                                       enter=0.6, leave=0.6), until=lines.end())])

class Drive(Chapter):
    lines = Narration("Water passes beneath the wheel and turns a shaft. In the model, the waterwheel "
                      "drives the crankshaft. A crank and a connecting rod turn that rotation into the saw's stroke.")
    mill = View(Sawmill, camera=Sawmill.drive, hide=[Sawmill.structure, Sawmill.foundation, Sawmill.carriage])
    code = Source.panel(Sawmill.coupling)
    wheel = Shot(Paper, {Paper.stage: mill}, until=lines.spoken("In the model"), model=Sawmill.run(440, 444))
    coupling_shot = Shot(PaperSplit, {PaperSplit.left: code, PaperSplit.right: mill},
                         until=lines.spoken_end("drives the crankshaft", plus=0.9), transition=Dissolve(0.6), model=Sawmill.run(444, 450),
                         cues=[Cue(0, code.type(through_line=415, over=0.6)),
                               Cue(lines.spoken("waterwheel"), mill.highlight(Mill.water_drive.waterwheel, others="ghost"),
                                   until=lines.spoken("crankshaft")),
                               Cue(lines.spoken("crankshaft"), mill.highlight(Mill.water_drive.crankshaft, others="ghost"),
                                   until=lines.spoken_end("drives the crankshaft", plus=0.9)),
                               Cue(lines.spoken("the waterwheel drives the crankshaft"),
                                   code.emphasize("waterwheel", "drives", "crankshaft", hold=0.9))])
    stroke = Shot(Paper, {Paper.stage: mill}, until=lines.end(plus=0.6), transition=Wipe(0.6, direction="right"),
                  model=Sawmill.run(450, 456),
                  cues=[Cue(0, mill.move(Sawmill.whole_near, ease="smooth", until=lines.end())),
                        Cue(lines.spoken("connecting rod"), Arrow(Mill.saw.connecting_rod, "Connecting rod",
                            place=(0.2, 0.25), enter=("draw", 0.8), leave=("fade", 0.4)), until=lines.end(plus=0.6))])

class Feed(Chapter):
    lines = Narration("Watch the timber. On the cutting stroke the rocker pulls a hook, the driving pawl, "
                      "and the ratchet turns one tooth. On the return, a holding pawl keeps that progress.")
    mill = View(Sawmill, camera=Sawmill.pawls, hide=[Sawmill.structure, Sawmill.foundation, Sawmill.water, Sawmill.carriage])
    pawls_shot = Shot(Paper, {Paper.stage: mill}, until=lines.end(plus=0.8),
                      model=Sawmill.keys({0: "pull_start", lines.spoken("On the return"): ("return_start", "out"),
                                          lines.end(plus=0.8): "cycle_end"}),
                      cues=[Cue(0, Title("Pull · one tooth", position="top"), until=lines.spoken("On the return")),
                            Cue(lines.spoken("the driving pawl"),
                                Ring(Mill.feed.pawl, enter=("draw", 0.8), leave=("fade", 0.4)),
                                Label(Mill.feed.pawl, "Driving pawl", offset=(-0.16, -0.12), enter=("fade", 0.4)),
                                mill.highlight(Mill.feed.pawl, Mill.feed.feed_drum, others="ghost"),
                                until=lines.spoken("On the return")),
                            Cue(lines.spoken("On the return"), Title("Return · hold", position="top"), until=lines.end(plus=0.8)),
                            Cue(lines.spoken("a holding pawl"),
                                Ring(Mill.feed.holding_pawl, enter=("draw", 0.8)),
                                Label(Mill.feed.holding_pawl, "Holding pawl", offset=(0.12, 0.08), enter=("fade", 0.4)),
                                mill.highlight(Mill.feed.holding_pawl, others="dim"),
                                until=lines.end(plus=0.8))])

class Ropes(Chapter):
    lines = Narration("Two ropes share one winding shaft. Rope one unwinds from the large drum while rope two "
                      "winds onto the thin section, and the carriage moves the timber into the blade.")
    mill = View(Sawmill, camera=Sawmill.rope_wide, hide=[Sawmill.structure, Sawmill.foundation, Sawmill.water])
    shaft = Shot(Paper, {Paper.stage: mill}, until=lines.spoken("and the carriage"), model=Sawmill.run(440, 448),
                 cues=[Cue(0, mill.move(Sawmill.reduction_rolled, ease="smooth", until=lines.spoken("and the carriage"))),
                       Cue(lines.spoken("Rope one"), Label(Mill.feed.reserve, "Rope 1", offset=(0, -0.15),
                           enter=("fade", 0.4), leave=("fade", 0.4)), until=lines.spoken("and the carriage")),
                       Cue(lines.spoken("rope two"), Label(Mill.feed.takeup, "Rope 2", offset=(0.12, -0.12),
                           enter=("fade", 0.4), leave=("fade", 0.4)), until=lines.spoken("and the carriage"))])
    wide = View(Sawmill, camera=Sawmill.whole_near, hide=[Sawmill.structure, Sawmill.water])
    carriage_shot = Shot(Paper, {Paper.stage: wide},
                         until=lines.end(plus=0.6), transition=Dissolve(0.6), model=Sawmill.run(448, 454),
                         cues=[Cue(0, wide.highlight(Mill.carriage, others="dim"), until=lines.end(plus=0.6))])

class Closing(Chapter):
    lines = Narration("Cut. Advance. Cut. Advance. The linkage sets the rhythm. "
                      "Explore the interactive model, linked in the description.")
    mill = View(Sawmill, camera=Sawmill.whole_near)
    rhythm = Shot(Paper, {Paper.stage: mill}, until=lines.spoken("The linkage"), model=Sawmill.run(448, 456),
                  cues=[Cue(0, Title("Cut. Advance. Cut. Advance.", position="top", reveal=Reveal.spoken()),
                            until=lines.spoken("The linkage"))])
    still = Shot(Paper, {Paper.stage: mill}, until=lines.spoken("Explore"), model=Sawmill.run(456, 460),
                 cues=[Cue(0, Sawmill.isometric.show(area="frame", fit="contain", enter=0.5, leave=0.5,
                                             view=[(0, (0.5, 0.5), 1.0), (lines.spoken("Explore", plus=-0.5), (0.5, 0.42), 1.4, "in-out")]),
                           until=lines.spoken("Explore"))])
    invitation = Shot(Paper, {Paper.stage: mill}, until=lines.end(plus=1.2), fade_out=FadeOut(1.2),
                      model=Sawmill.run(460, 462),
                      cues=[Cue(0, mill.move(Sawmill.whole, ease="in-out", until=lines.end()))])

class CutAndAdvance(Movie):
    title = "Cut and Advance"
    series = "LEONARDO · HOW IT WORKS"
    status = "rehearsal"
    learning_goal = "Explain how one waterwheel coordinates the saw stroke and the intermittent timber feed."
    format = Format(1920, 1080, fps=30)
    narrator = jessica
    style = Paper.style(background="#faf7ef", foreground="#222222", accent="#237c86",
                        font="DejaVu Sans, sans-serif", safe_inset=0.08)
    evidence = Evidence(model="../../models/hydraulic_sawmill/model.py",
                        kinematics="../../models/hydraulic_sawmill/kinematics.py")
    credits = Credits(project="Leonardo da Vinci Gallery", creator="Vibecoded by Astra",
                      copyright="Copyright (C) 2026 Luis Henrique Cassis Fagundes",
                      license="AGPL-3.0-only", license_file="../../LICENSE")
    release = Release(simulation_url=None, source_url=None, description="description.md")
    question = Question()
    drive = Drive()
    feed = Feed()
    ropes = Ropes()
    closing = Closing()
```

Declared in `pyproject.toml`:

```toml
[tool.machinome.movies]
cut_and_advance = "videos.cut_and_advance.movie:CutAndAdvance"
```

The movie directory therefore needs an `__init__.py`, and `videos/` one
too, since the movie is imported as a module of the project like a model.

## How it is produced

From the videomaker repository's campaign worktree, with the workspace venv:

```sh
.venv/bin/python -m machinome_movie evaluate projects/Leonardo cut_and_advance
node bin/videomaker.mjs speech  projects/Leonardo/videos/cut_and_advance/_build/movie.json
node bin/videomaker.mjs check   projects/Leonardo/videos/cut_and_advance/_build/movie.json --viewer machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node bin/videomaker.mjs preview …/_build/movie.json --viewer …
node bin/videomaker.mjs render  …/_build/movie.json --viewer …
```

## Acceptance

- The only authored inputs are `movie.py`, `description.md`, the two media
  files and the `pyproject.toml` entry. No YAML.
- Evaluation is deterministic: two evaluations write byte-identical
  documents. Evaluation refuses, by name, a misspelled part path, an unknown
  camera, a phrase absent from its chapter's narration, and a project set
  that the film page cannot draw.
- `speech` generates five takes, one per chapter, with Jessica; `check`
  resolves every anchor and writes `_build/movie-resolved.json`; `preview`
  passes every proof it runs, its `report.json` retained; `render` produces
  `rehearsal.mp4` at 1920×1080 and 30 fps with `rehearsal.srt` beside it and
  the manifest recording the document's hash.
- The film's frames, thumbnail and audio carry no author, licence or
  product credit; `description.md` carries the record.
- The pilot inspects the storyboard and the MP4. Whether the film reads well
  is the pilot's judgment; every finding goes to the videomaker's
  `workflow/warts.md`.

## Out of scope, on purpose

The React stage and project-defined sets or elements; takes from running or
clocked scenarios; a browser page element; the studio's live preview; a
vertical cut; music. Each is a later step of the recorded direction.
