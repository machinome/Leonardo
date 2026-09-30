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
                                Label(Mill.feed.pawl, "Driving pawl", offset=(0.12, -0.08), enter=("fade", 0.4)),
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
