<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Cut and Advance — validation film specification

Status: version 2, written 30 September 2026 before the code it validates
exists, for Videomaker's react-stage campaign. Version 1 (the same day)
validated the declarative Python API on the old fixed film page and was
rendered and inspected; the pilot found the source code left out and the
page's hard-coded chrome unacceptable, and commissioned the stage. Version 2
keeps the lesson, the five chapters and the narration (the cached takes are
reused; no speech is bought) and changes what the film must prove: the
project's own template owns the whole screen, source is shown beside the
model in three chapters with spoken concepts lighting the tokens that name
them, and one element of the film is the project's own. Names of the API are
provisional; the shot list and what each shot validates are the contract.

## The lesson

Leonardo's hydraulic sawmill does two jobs with one waterwheel: it drives
the saw's stroke, and it feeds the timber forward one ratchet tooth per
stroke. The film shows the drive train, reads the lines of source that
couple wheel to crankshaft while the picture highlights the same parts,
watches the two pawls take turns beside the laws that pose them, follows the
two ropes from the winding shaft beside the lines that wind them, and closes
on the rhythm of cut and advance. About a minute, 1920×1080, 30 fps,
landscape. Honest about simplifications: posed kinematics, no forces, no
cutting simulated; a reconstruction, not an artifact.

## What the film must prove

| capability | shot |
|---|---|
| Movie declared in `pyproject.toml`, evaluated to a `machinome-movie/0.2` document that carries sets, slots, elements, cues and actions | whole film |
| **The project's template owns the screen**: a root set `Leonardo` written in the project's `stage.tsx`, drawing its own masthead and nothing the film did not ask for; no progress rule anywhere | whole film |
| **A derived set inherits the chrome, not the layout**: `LeonardoSplit` keeps the masthead and lays out two containers | `coupling`, `pawls`, `holding`, `shaft` |
| **Source beside the model in two containers**, typed on cue, spoken words lighting tokens while the same parts highlight in the model beside it | `coupling`, `pawls`, `holding`, `shaft` |
| Emphasis pairs a spoken concept with a source token that spells it differently, on any line of the excerpt; a word inside a dotted path is a token, and a repeated token is chosen by line | `pawls` (*the driving pawl* → `feed.pawl.turn`), `shaft` (*Rope one* → `feed.reserve.shift`), `coupling` (`waterwheel`, `drives`, `crankshaft` on line 415) |
| **A project element**: `Jobs`, the two-jobs card, declared in Python with a typed action and drawn by the project's component, lit on cue in step with the model | `hook`, `question` |
| A title element placed in a slot of the template, shown with fades and a subtitle | `question` |
| A title revealed word by word as spoken | `rhythm` |
| A picture element in the template's plate slot with keyed pan and zoom, fading over the model | `still` |
| Chapter narration as one take; shots cut on spoken phrases; spoken anchors on shot ends, cue starts and ends, moves and model keys | every chapter |
| Marks on the loop take resolved to model seconds, with easing into a hold | `pawls`, `holding` |
| A view keeps its state across a cut inside its chapter (camera, typed source) | `pawls` → `holding` |
| Highlight with ghosted and dimmed others; ring, label and arrow marks bound to a view, placed in the view's own box | `coupling`, `pawls`, `holding`, `shaft`, `stroke`, `carriage` |
| Camera moves with named easing; a move that changes field of view and up | `hook`, `shaft` |
| Transitions: dissolve, wipe, fade in, fade out | `coupling`, `stroke`, `carriage`, `hook`, `invitation` |
| Every proof of the old page kept on the stage: readback checked, pixel replay, blends within tolerance, marks on screen, shot cache, provenance recording the stage bundle | whole film |
| No credit in the frames or the audio; attribution in the description | whole film |

## The template

`videos/cut_and_advance/stage.tsx` (with `stage.css` beside it) is the
film's look, written by the project:

- **`Leonardo`**, the root set: paper background from the movie's style; a
  masthead of the series label at the top left, in the accent colour, and
  the brand at the top right, muted, both props of the set (`series`,
  `brand`), drawn inside `Chrome` so it stays
  above pictures and transitions; no rule, no bar, no progress. Slots:
  `stage` (the whole picture below the masthead), `plate` (over the stage,
  for a picture), `headline` (a band at the top of the stage, for a title),
  `aside` (a column at the right, for a card).
- **`LeonardoSplit`**, derived: the same masthead; slots `left` (a source
  container, about half the width), `right` (the model), `headline`.
- **`Jobs`**, the project element: a card listing the two jobs, "Move the
  saw" and "Feed the log", each a `{key, text}` of its `jobs` prop; its action
  `light(job)` names a key and fills that line with the accent colour while
  the cue lasts.

## Shot list

Times are indicative. Spoken anchors are resolved from the cached takes;
only literal durations and model seconds are authored. Marks: `pull_start`
436, `return_start` 438, `cycle_end` 440 model seconds.

### Chapter 1 — `question`

Narration: *"A waterwheel can move a saw. But how does it feed the log
forward at just the right moment?"*

1. `hook` — set `Leonardo`; `stage` the mill from `title_wide` moving to
   `title_near` with `out` easing over the shot; `aside` the `Jobs` card,
   whose first line lights at spoken "move a saw"; model 428 → 436; fades in
   from the paper colour over 1 s. Until spoken "But".
2. `question` — same set and elements; the card's second line lights at
   spoken "feed the log"; `headline` the title "CUT AND ADVANCE" with the
   subtitle "One wheel, two jobs" fading in at the cut and out before the
   end; model to 440. Until the narration ends plus 1.2 s.

### Chapter 2 — `drive`

Narration: *"Water passes beneath the wheel and turns a shaft. In the model,
the waterwheel drives the crankshaft. A crank and a connecting rod turn that
rotation into the saw's stroke."*

3. `wheel` — set `Leonardo`; the mill from camera `drive`, hiding
   structure, foundation and carriage; model 440 → 444. Until spoken "In the
   model".
4. `coupling` — set `LeonardoSplit`: `left` the source `model.py`
   413–415 typed through line 415 in the first 0.6 s; `right` the same view.
   Dissolve in over 0.6 s. At spoken "waterwheel" the undershot waterwheel
   highlights with others ghosted and `waterwheel` lights in the source; at
   "drives", `drives`; at "crankshaft" the highlight moves to the keyed
   crankshaft and `crankshaft` lights; the marks clear 0.6 s after the phrase
   ends. Until the phrase "drives the crankshaft" ends plus 0.9 s.
5. `stroke` — set `Leonardo`; the view moves from `drive` to `whole_near`
   with `smooth` easing; wipe in from the right over 0.6 s; an arrow
   "Connecting rod" draws on at spoken "connecting rod" and fades before the
   end. Until the narration ends plus 1.2 s.

### Chapter 3 — `feed`

Narration: *"Watch the timber. On the cutting stroke the rocker pulls a hook,
the driving pawl, and the ratchet turns one tooth. On the return, a holding
pawl keeps that progress."*

6. `pawls` — set `LeonardoSplit`: `left` the source `model.py` 425–435
   (the rocker, tie, pawl and ratchet laws) typed over 1 s; `right` the mill
   from camera `pawls`, hiding structure, foundation, water and carriage;
   `headline` the title "Pull · one tooth" for the shot. Model keys: at the
   cut, mark `pull_start`; at the end, mark `return_start` with `out` easing,
   so the pull plays slowly and settles. At spoken "the rocker pulls a hook,
   the driving pawl, and the ratchet": `feed.rocker.turn` lights at "rocker",
   `feed.pawl.turn` at "the driving pawl", `ratchet_angle` at "ratchet",
   holding 0.6 s past the phrase. At spoken "the driving pawl" a ring draws
   on around the driving pawl with the label "Driving pawl", and the view
   ghosts everything but the driving pawl and the ratchet drum, until the
   end. Until spoken "On the return".
7. `holding` — same set; the source panel keeps its completed excerpt and
   the view its camera; `headline` "Return · hold". Model keys: at the cut,
   `return_start`; at the end, `cycle_end`. At spoken "a holding pawl keeps",
   `feed.holding_pawl.turn` lights at "holding pawl". At spoken "a holding
   pawl" a ring draws on around the holding pawl with the label "Holding
   pawl", and the view dims everything but the holding pawl, until the end.
   Until the narration ends plus 1.5 s.

### Chapter 4 — `ropes`

Narration: *"Two ropes share one winding shaft. Rope one unwinds from the
large drum while rope two winds onto the thin section, and the carriage
moves the timber into the blade."*

8. `shaft` — set `LeonardoSplit`: `left` the source `model.py` 472–486 (the
   reserve and take-up windings) typed over 1 s; `right` the mill from
   `rope_wide` moving to `reduction_rolled`, which changes field of view and
   up, with `smooth` easing until spoken "and the carriage"; hiding
   structure, foundation and water; model 440 → 448. At spoken "Rope one
   unwinds from the large drum while rope two winds": `feed.reserve.shift`
   lights at "Rope one" and `feed.takeup.shift` at "rope two", holding 0.6 s.
   A label "Rope 1" fades in on the reserve at spoken "Rope one" and a label
   "Rope 2" on the take-up at spoken "rope two"; both fade at the end. Until
   spoken "and the carriage".
9. `carriage` — set `Leonardo`; a second view from `whole_near`, hiding
   structure and water; the timber carriage highlighted with others dimmed
   for the whole shot; dissolve in over 0.6 s. Until the narration ends plus
   1.2 s.

### Chapter 5 — `closing`

Narration: *"Cut. Advance. Cut. Advance. The linkage sets the rhythm.
Explore the interactive model, linked in the description."*

10. `rhythm` — set `Leonardo`; the mill from `whole_near`; model 448 →
    456; `headline` the title "Cut. Advance. Cut. Advance." whose words
    appear as they are spoken. Until spoken "The linkage".
11. `still` — `plate` the project still `sawmill-isometric.png`, fit
    contain, fading in over 0.5 s, its view pushing from the whole image to
    a 1.4× zoom on the mechanism with `in-out` easing, fading out 0.5 s
    before the end; the model continues beneath. Until spoken "Explore".
12. `invitation` — the view moves from `whole_near` to `whole` with
    `in-out` easing; model to 462; fade out to the paper colour over 1.2 s.
    Until the narration ends plus 1.6 s.

## The Python source

The target `videos/cut_and_advance/movie.py`, as far as this specification
can write it before the API exists. The `declarative-stage` change must make
a source of this shape evaluate; where it changes a spelling, this file is
updated with it and the change says why.

```python
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome_movie import (Movie, Chapter, Shot, Narration, Cue, Camera, Layer, Loop,
    Set, Slot, Element, Action, View, Source, Still, Title, Picture, Reveal,
    Dissolve, Wipe, FadeIn, FadeOut, Format, Narrator, Style, Credits, Release, Evidence)
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
    feed_laws = Source("../../models/hydraulic_sawmill/model.py", lines=(425, 435))
    winding = Source("../../models/hydraulic_sawmill/model.py", lines=(472, 486))
    isometric = Still("media/sawmill-isometric.png",
                      credit="Leonardo project render of the reconstructed sawmill",
                      rights="Project-owned reconstruction render, AGPL-3.0-only", upscale=1.85)

# The film's template, drawn by stage.tsx beside this file.
class Leonardo(Set):
    module = "stage.tsx"
    series = "LEONARDO · HOW IT WORKS"      # props the template's masthead reads
    brand = "MACHINOME"
    stage = Slot()
    plate = Slot()
    headline = Slot()
    aside = Slot()

class LeonardoSplit(Leonardo):
    left = Slot()
    right = Slot()
    headline = Slot()

class Jobs(Element):
    module = "stage.tsx"
    light = Action(job=str)

jessica = Narrator(provider="elevenlabs", model="eleven_v3", voice="cgSgspJ2msm6clMCkdW9",
                   label="Jessica", output="pcm_24000",
                   settings={"stability": 0.5, "similarity_boost": 0.75},
                   direction="Curious, clear, unhurried. Leave room to watch the mechanism.")

class Question(Chapter):
    lines = Narration("A waterwheel can move a saw. But how does it feed the log forward at just the right moment?")
    mill = View(Sawmill, camera=Sawmill.title_wide)
    jobs = Jobs(jobs=[{"key": "saw", "text": "Move the saw"}, {"key": "log", "text": "Feed the log"}])
    title = Title("CUT AND ADVANCE", subtitle="One wheel, two jobs")
    hook = Shot(Leonardo, {Leonardo.stage: mill, Leonardo.aside: jobs}, until=lines.spoken("But"),
                fade_in=FadeIn(1.0), model=Sawmill.run(428, 436),
                cues=[Cue(0, mill.move(Sawmill.title_near, ease="out", until=lines.spoken("But"))),
                      Cue(lines.spoken("move a saw"), jobs.light(job="saw"), until=lines.spoken("But"))])
    question = Shot(Leonardo, {Leonardo.stage: mill, Leonardo.aside: jobs, Leonardo.headline: title},
                    until=lines.end(plus=1.2), model=Sawmill.run(436, 440),
                    cues=[Cue(lines.spoken("feed the log"), jobs.light(job="log"), until=lines.end(plus=1.2)),
                          Cue(0, title.show(enter=0.6, leave=0.6), until=lines.end())])

class Drive(Chapter):
    lines = Narration("Water passes beneath the wheel and turns a shaft. In the model, the waterwheel "
                      "drives the crankshaft. A crank and a connecting rod turn that rotation into the saw's stroke.")
    mill = View(Sawmill, camera=Sawmill.drive, hide=[Sawmill.structure, Sawmill.foundation, Sawmill.carriage])
    code = Source.panel(Sawmill.coupling)
    wheel = Shot(Leonardo, {Leonardo.stage: mill}, until=lines.spoken("In the model"), model=Sawmill.run(440, 444))
    coupling = Shot(LeonardoSplit, {LeonardoSplit.left: code, LeonardoSplit.right: mill},
                    until=lines.spoken_end("drives the crankshaft", plus=0.9), transition=Dissolve(0.6),
                    model=Sawmill.run(444, 450),
                    cues=[Cue(0, code.type(through_line=415, over=0.6)),
                          Cue(lines.spoken("waterwheel"), mill.highlight(Mill.water_drive.waterwheel, others="ghost"),
                              until=lines.spoken("crankshaft")),
                          Cue(lines.spoken("crankshaft"), mill.highlight(Mill.water_drive.crankshaft, others="ghost"),
                              until=lines.spoken_end("drives the crankshaft", plus=0.6)),
                          Cue(lines.spoken("the waterwheel drives the crankshaft"),
                              code.emphasize("waterwheel", "drives", "crankshaft", line=415, hold=0.6))])
    stroke = Shot(Leonardo, {Leonardo.stage: mill}, until=lines.end(plus=1.2), transition=Wipe(0.6, direction="right"),
                  model=Sawmill.run(450, 456),
                  cues=[Cue(0, mill.move(Sawmill.whole_near, ease="smooth", until=lines.end())),
                        Cue(lines.spoken("connecting rod"),
                            mill.arrow(Mill.saw.connecting_rod, "Connecting rod", place=(0.2, 0.25),
                                       enter=("draw", 0.8), leave=("fade", 0.4)),
                            until=lines.end(plus=1.2))])

class Feed(Chapter):
    lines = Narration("Watch the timber. On the cutting stroke the rocker pulls a hook, the driving pawl, "
                      "and the ratchet turns one tooth. On the return, a holding pawl keeps that progress.")
    mill = View(Sawmill, camera=Sawmill.pawls,
                hide=[Sawmill.structure, Sawmill.foundation, Sawmill.water, Sawmill.carriage])
    code = Source.panel(Sawmill.feed_laws)
    pull = Title("Pull · one tooth")
    hold = Title("Return · hold")
    pawls = Shot(LeonardoSplit, {LeonardoSplit.left: code, LeonardoSplit.right: mill, LeonardoSplit.headline: pull},
                 until=lines.spoken("On the return"),
                 model=Sawmill.keys({0: "pull_start", lines.spoken("On the return"): ("return_start", "out")}),
                 cues=[Cue(0, code.type(through_line=435, over=1.0)),
                       Cue(0, pull.show(), until=lines.spoken("On the return")),
                       Cue(lines.spoken("the rocker pulls a hook, the driving pawl, and the ratchet"),
                           code.emphasize(("rocker", "feed.rocker.turn"), ("the driving pawl", "feed.pawl.turn"),
                                          ("ratchet", "ratchet_angle"), hold=0.6)),
                       Cue(lines.spoken("the driving pawl"),
                           mill.ring(Mill.feed.pawl, enter=("draw", 0.8), leave=("fade", 0.4)),
                           mill.label(Mill.feed.pawl, "Driving pawl", offset=(-0.2, -0.15), enter=("fade", 0.4)),
                           mill.highlight(Mill.feed.pawl, Mill.feed.feed_drum, others="ghost"),
                           until=lines.spoken("On the return"))])
    holding = Shot(LeonardoSplit, {LeonardoSplit.left: code, LeonardoSplit.right: mill, LeonardoSplit.headline: hold},
                   until=lines.end(plus=1.5),
                   model=Sawmill.keys({0: "return_start", lines.end(plus=1.5): "cycle_end"}),
                   cues=[Cue(0, hold.show(), until=lines.end(plus=1.5)),
                         Cue(lines.spoken("a holding pawl keeps"),
                             code.emphasize(("holding pawl", "feed.holding_pawl.turn"), hold=0.6)),
                         Cue(lines.spoken("a holding pawl"),
                             mill.ring(Mill.feed.holding_pawl, enter=("draw", 0.8)),
                             mill.label(Mill.feed.holding_pawl, "Holding pawl", offset=(0.15, 0.1), enter=("fade", 0.4)),
                             mill.highlight(Mill.feed.holding_pawl, others="dim"),
                             until=lines.end(plus=1.5))])

class Ropes(Chapter):
    lines = Narration("Two ropes share one winding shaft. Rope one unwinds from the large drum while rope two "
                      "winds onto the thin section, and the carriage moves the timber into the blade.")
    mill = View(Sawmill, camera=Sawmill.rope_wide, hide=[Sawmill.structure, Sawmill.foundation, Sawmill.water])
    code = Source.panel(Sawmill.winding)
    shaft = Shot(LeonardoSplit, {LeonardoSplit.left: code, LeonardoSplit.right: mill},
                 until=lines.spoken("and the carriage"), model=Sawmill.run(440, 448),
                 cues=[Cue(0, code.type(through_line=486, over=1.0)),
                       Cue(0, mill.move(Sawmill.reduction_rolled, ease="smooth", until=lines.spoken("and the carriage"))),
                       Cue(lines.spoken("Rope one unwinds from the large drum while rope two winds"),
                           code.emphasize(("Rope one", "feed.reserve.shift"), ("rope two", "feed.takeup.shift"), hold=0.6)),
                       Cue(lines.spoken("Rope one"),
                           mill.label(Mill.feed.reserve, "Rope 1", offset=(0, -0.18), enter=("fade", 0.4), leave=("fade", 0.4)),
                           until=lines.spoken("and the carriage")),
                       Cue(lines.spoken("rope two"),
                           mill.label(Mill.feed.takeup, "Rope 2", offset=(0.15, -0.15), enter=("fade", 0.4), leave=("fade", 0.4)),
                           until=lines.spoken("and the carriage"))])
    wide = View(Sawmill, camera=Sawmill.whole_near, hide=[Sawmill.structure, Sawmill.water])
    carriage = Shot(Leonardo, {Leonardo.stage: wide}, until=lines.end(plus=1.2), transition=Dissolve(0.6),
                    model=Sawmill.run(448, 454),
                    cues=[Cue(0, wide.highlight(Mill.carriage, others="dim"), until=lines.end(plus=1.2))])

class Closing(Chapter):
    lines = Narration("Cut. Advance. Cut. Advance. The linkage sets the rhythm. "
                      "Explore the interactive model, linked in the description.")
    mill = View(Sawmill, camera=Sawmill.whole_near)
    beat = Title("Cut. Advance. Cut. Advance.")
    iso = Picture(Sawmill.isometric, fit="contain")
    rhythm = Shot(Leonardo, {Leonardo.stage: mill, Leonardo.headline: beat}, until=lines.spoken("The linkage"),
                  model=Sawmill.run(448, 456),
                  cues=[Cue(0, beat.show(reveal=Reveal.spoken()), until=lines.spoken("The linkage"))])
    still = Shot(Leonardo, {Leonardo.stage: mill, Leonardo.plate: iso}, until=lines.spoken("Explore"),
                 model=Sawmill.run(456, 460),
                 cues=[Cue(0, iso.show(enter=0.5, leave=0.5,
                                       view=[(0, (0.5, 0.5), 1.0),
                                             (lines.spoken("Explore", plus=-0.5), (0.5, 0.42), 1.4, "in-out")]),
                           until=lines.spoken("Explore"))])
    invitation = Shot(Leonardo, {Leonardo.stage: mill}, until=lines.end(plus=1.6), fade_out=FadeOut(1.2),
                      model=Sawmill.run(460, 462),
                      cues=[Cue(0, mill.move(Sawmill.whole, ease="in-out", until=lines.end()))])

class CutAndAdvance(Movie):
    title = "Cut and Advance"
    series = "LEONARDO · HOW IT WORKS"
    status = "rehearsal"
    learning_goal = "Explain how one waterwheel coordinates the saw stroke and the intermittent timber feed."
    format = Format(1920, 1080, fps=30)
    narrator = jessica
    style = Style(background="#faf7ef", foreground="#222222", accent="#237c86",
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

What this source asks of the declarations, beyond version 1: `Set` and
`Element` subclasses in the project with a `module`, `Slot()`s, plain
class attributes as props and `Action(...)` declarations with typed
parameters; an `Element` instance's keyword arguments as its props and its
declared actions as methods; `Title` and `Picture` as elements placed in
slots, with `show`; marks (`ring`, `label`, `arrow`) as methods of the view
they point into; `emphasize` taking a word or a `(spoken, token)` pair, on
any line, a dot being a token boundary, with `line=` when a token repeats in
the excerpt; `Style` on the movie; empty slots allowed; a source panel and a
view keeping their state across a cut in their chapter.

## How it is produced

From the videomaker checkout that carries the react-stage campaign, with
the workspace venv:

```sh
.venv/bin/python -m machinome_movie evaluate projects/Leonardo cut_and_advance
node bin/videomaker.mjs speech  projects/Leonardo/videos/cut_and_advance/_build/movie.json   # cached takes; nothing bought
node bin/videomaker.mjs check   projects/Leonardo/videos/cut_and_advance/_build/movie.json --viewer machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node bin/videomaker.mjs preview …/_build/movie.json --viewer …
node bin/videomaker.mjs render  …/_build/movie.json --viewer …
```

`check` bundles `stage.tsx` with the tool's stage runtime into
`_build/stage/`, type-checks it against the generated `movie.d.ts`, and
refuses by name a set or element the bundle does not register or a set
whose slots differ from the declaration.

## Acceptance

- The only authored inputs are `movie.py`, `stage.tsx`, `stage.css`,
  `description.md`, the two media files and the `pyproject.toml` entry. No
  YAML; nothing hard-coded in the tool's page decides a pixel of this film.
- Evaluation is deterministic: two evaluations write byte-identical
  documents. Evaluation refuses, by name, a misspelled part path, an unknown
  camera, a phrase absent from its chapter's narration, an element placed in
  a slot the set lacks, an action on an element the shot does not place, a
  token absent from or repeated in its excerpt.
- `speech` finds the five cached takes and buys nothing; `check` resolves
  every anchor and writes `_build/movie-resolved.json`; `preview` passes
  every proof it runs, its `report.json` retained; `render` produces
  `rehearsal.mp4` at 1920×1080 and 30 fps with `rehearsal.srt` beside it and
  the manifest recording the document's and the stage bundle's hashes.
- No frame carries a progress rule, the brand or a series label the
  template did not draw, or any credit; `description.md` carries the record.
- The pilot inspects the storyboard and the MP4 with `movie.py` and
  `stage.tsx` open. Whether the film reads well is the pilot's judgment;
  every finding goes to the videomaker's `workflow/warts.md`.

## Out of scope, on purpose

Takes from running or clocked scenarios; the browser page element (the
museum shot); the studio's live preview; a vertical cut; music. Each is a
later step of the recorded direction, cut by the orchestrator and not
decided by the pilot.
