"""The release film: a machine introduces its ancestor and itself."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path
import ast
import hashlib
import textwrap

from machinome_movie import (
    Action,
    Camera,
    Chapter,
    Credits,
    Cue,
    Dissolve,
    Element,
    Evidence,
    FadeIn,
    FadeOut,
    Format,
    Layer,
    Loop,
    Movie,
    Narration,
    Narrator,
    Reframe,
    Release,
    Set,
    Shot,
    Slot,
    Source,
    Style,
    Title,
    View,
    evaluate,
    write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill

HERE = Path(__file__).resolve().parent


class Exhibition(Set):
    module = "stage.jsx"
    stage = Slot()
    heading = Slot()
    note = Slot()
    graphic = Slot()


class Workbench(Set):
    module = "stage.jsx"
    right = Slot()
    imports = Slot()
    code = Slot()
    heading = Slot()
    note = Slot()


class SourceRoom(Set):
    module = "stage.jsx"
    code = Slot()
    heading = Slot()
    note = Slot()


class Card(Element):
    module = "stage.jsx"
    enter = Action()


class Listing(Element):
    module = "stage.jsx"
    focus = Action(token=str)


class Constellation(Element):
    module = "stage.jsx"
    unfold = Action()


class Signature(Element):
    module = "stage.jsx"
    enter = Action()


class Sawmill(Loop):
    model = Mill
    export = "../../export/hydraulic_sawmill"
    readiness = (
        "Existing 1460-second posed reconstruction. No fluid, force, "
        "stress or cutting physics. Museum interpretation, not a replica."
    )
    # Exactly on the wheel's Y axis. Return to this lens for the match.
    wheel = Camera(position=(0, -575, 120), target=(0, -151, 120), fov=37)
    wide = Camera(position=(948, -1273, 856), target=(0, -20, 205), fov=37)
    side = Camera(position=(980, -450, 780), target=(0, 0, 260), fov=37)
    rear = Camera(position=(850, 850, 710), target=(0, 0, 285), fov=37)
    crank = Camera(position=(410, 720, 460), target=(0, 0, 215), fov=37)
    saw = Camera(position=(380, 720, 510), target=(0, 0, 335), fov=37)
    pawls = Camera(position=(145, 410, 405), target=(135, 30, 332), fov=37)
    ropes = Camera(position=(-540, 830, 610), target=(-80, 0, 300), fov=37)
    drum = Camera(position=(-590, 350, 425), target=(-305, 0, 300), fov=37)
    carriage = Camera(position=(-740, 680, 690), target=(-40, 0, 330), fov=37)
    source = Camera(position=(1200, -1540, 960), target=(0, -20, 205), fov=37)
    not_wheel = Layer(
        Mill.frame,
        Mill.saw,
        Mill.carriage,
        Mill.feed,
        Mill.water_drive.channel,
        Mill.water_drive.water,
        Mill.water_drive.crankshaft,
        Mill.water_drive.crank,
        Mill.water_drive.crank_retainer,
    )
    imports = Source("../../models/hydraulic_sawmill/model.py", lines=(7, 7))
    coupling = Source(
        "../../models/hydraulic_sawmill/model.py", lines=(415, 415)
    )


def scene_excerpt(name, maximum=None):
    """Extract the actual film source for its appearance on screen."""
    source = Path(__file__).read_text()
    node = next(
        n
        for n in ast.parse(source).body
        if isinstance(n, ast.ClassDef) and n.name == name
    )
    lines = source.splitlines()[node.lineno - 1 : node.end_lineno]
    if maximum is not None:
        lines = lines[:maximum]
    return dict(
        code=textwrap.dedent("\n".join(lines)),
        file=f"movie.py / {name}",
        digest=hashlib.sha256(source.encode()).hexdigest(),
    )


class Encounter(Chapter):
    lines = Narration(
        "A wheel makes revolutions. "
        "Five centuries ago, Leonardo da Vinci designed a water-powered "
        "sawmill. Machines like this were changing the relationship between "
        "people and work: a river could help turn a tree into timber. "
        "I am a machine, too. In the history of human tools, this sawmill "
        "is one of my ancestors. Let me show you how it works. "
        "Water beneath the wheel turns this shaft. A crank and connecting "
        "rod turn that rotation into the saw's up-and-down stroke. "
        "But the timber has to move, too. On the cutting stroke, this long "
        "lever pulls a pawl across one tooth of a ratchet. A second pawl "
        "holds that progress while the first returns. "
        "That small step winds a rope onto this axle. Follow it down, "
        "and across. It turns a compound shaft: a broad drum unwinds one "
        "rope while a thinner section takes up another. The second rope "
        "draws the timber towards the blade. One wheel, two jobs: cut, "
        "and advance. "
        "To reconstruct this machine, I relied on historical documents "
        "and museum pictures, and used the Python language. "
        "Here is one of its relationships. "
        "The waterwheel's spin drives the crankshaft. "
        "With Machinome, machines can have a source code."
    )
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    disclosure = Card(text="AI content", eyebrow="", small=True)
    reconstruction = Card(
        text="Hydraulic sawmill", eyebrow="LEONARDO DA VINCI", small=False
    )
    limit = Card(
        text="Reconstructed motion · forces and cutting not simulated",
        eyebrow="",
        small=True,
    )
    imports = Source.panel(Sawmill.imports)
    relationship = Source.panel(Sawmill.coupling)
    code_title = Card(
        text="Machines can have source code.", eyebrow="", small=False
    )

    revolution = Shot(
        Exhibition,
        {Exhibition.stage: wheel, Exhibition.note: disclosure},
        until=lines.spoken("Five centuries"),
        fade_in=FadeIn(0.8),
        model=Sawmill.run(400, 404),
    )
    ancestor = Shot(
        Exhibition,
        {Exhibition.stage: mill, Exhibition.heading: reconstruction},
        until=lines.spoken("Water beneath"),
        transition=Dissolve(1.5),
        model=Sawmill.run(404, 424),
        cues=[
            Cue(
                lines.spoken("designed"),
                mill.move(Sawmill.wide, until=lines.spoken("I am")),
            ),
            Cue(
                lines.spoken("I am"),
                mill.move(Sawmill.side, until=lines.spoken("Let me")),
            ),
            Cue(
                lines.spoken("Let me"),
                mill.move(Sawmill.rear, until=lines.spoken("Water beneath")),
            ),
        ],
    )
    rotation = Shot(
        Exhibition,
        {Exhibition.stage: mill, Exhibition.note: limit},
        until=lines.spoken("But the timber"),
        model=Sawmill.run(424, 432),
        cues=[
            Cue(0, mill.move(Sawmill.crank, until=lines.spoken("A crank"))),
            Cue(
                0,
                mill.highlight(Mill.water_drive, others="ghost"),
                until=lines.spoken("A crank"),
            ),
            Cue(
                lines.spoken("A crank"),
                mill.move(Sawmill.saw, until=lines.spoken("But the timber")),
            ),
            Cue(
                lines.spoken("A crank"),
                mill.highlight(
                    Mill.water_drive.crank,
                    Mill.saw.connecting_rod,
                    Mill.saw.sash,
                    others="ghost",
                ),
                until=lines.spoken("But the timber"),
            ),
        ],
    )
    feed = Shot(
        Exhibition,
        {Exhibition.stage: mill, Exhibition.note: limit},
        until=lines.spoken("That small step"),
        model=Sawmill.keys(
            {
                0: 432,
                lines.spoken("On the cutting stroke"): 436,
                lines.spoken("A second pawl"): 438,
                lines.spoken("That small step"): 440,
            }
        ),
        cues=[
            Cue(
                0,
                mill.move(
                    Sawmill.pawls, until=lines.spoken("On the cutting stroke")
                ),
            ),
            Cue(
                0,
                mill.highlight(
                    Mill.feed.rocker,
                    Mill.feed.pawl,
                    Mill.feed.feed_drum,
                    others="ghost",
                ),
                until=lines.spoken("A second pawl"),
            ),
            Cue(
                lines.spoken("On the cutting stroke"),
                mill.arrow(
                    Mill.feed.pawl,
                    "Pulls one tooth",
                    place=(0.72, 0.18),
                    enter=("draw", 0.7),
                ),
                until=lines.spoken("A second pawl"),
            ),
            Cue(
                lines.spoken("A second pawl"),
                mill.highlight(Mill.feed.holding_pawl, others="ghost"),
                mill.arrow(
                    Mill.feed.holding_pawl,
                    "Holds the step",
                    place=(0.73, 0.20),
                    enter=("draw", 0.7),
                ),
                until=lines.spoken("That small step"),
            ),
        ],
    )
    transmission = Shot(
        Exhibition,
        {Exhibition.stage: mill, Exhibition.note: limit},
        until=lines.spoken("The second rope"),
        model=Sawmill.run(440, 452),
        cues=[
            Cue(
                0,
                mill.highlight(
                    Mill.feed.winding,
                    Mill.feed.feed_drum,
                    Mill.feed.drive_line,
                    others="ghost",
                ),
                until=lines.spoken("It turns"),
            ),
            Cue(
                lines.spoken("Follow it"),
                mill.move(Sawmill.ropes, until=lines.spoken("It turns")),
            ),
            Cue(
                lines.spoken("It turns"),
                mill.move(Sawmill.drum, until=lines.spoken("while a thinner")),
            ),
            Cue(
                lines.spoken("It turns"),
                mill.highlight(
                    Mill.feed.reduction_shaft,
                    Mill.feed.reserve,
                    Mill.feed.takeup,
                    others="ghost",
                ),
                until=lines.spoken("The second rope"),
            ),
        ],
    )
    consequence = Shot(
        Exhibition,
        {Exhibition.stage: mill, Exhibition.note: limit},
        until=lines.spoken("To reconstruct"),
        model=Sawmill.run(452, 464),
        cues=[
            Cue(
                0, mill.move(Sawmill.carriage, until=lines.spoken("One wheel"))
            ),
            Cue(
                0,
                mill.highlight(
                    Mill.feed.haul,
                    Mill.feed.haul_span,
                    Mill.carriage,
                    others="ghost",
                ),
                until=lines.spoken("One wheel"),
            ),
            Cue(
                lines.spoken("One wheel"),
                mill.move(Sawmill.wide, until=lines.spoken("To reconstruct")),
            ),
        ],
    )
    reconstruction_source = Shot(
        Exhibition,
        {Exhibition.stage: mill},
        until=lines.spoken("Here is"),
        model=Sawmill.run(464, 472),
        cues=[
            Cue(0, mill.move(Sawmill.source, until=lines.spoken("Here is")))
        ],
    )
    relationship_source = Shot(
        Workbench,
        {
            Workbench.right: mill,
            Workbench.imports: imports,
            Workbench.code: relationship,
            Workbench.heading: code_title,
        },
        until=lines.end(plus=1.4),
        transition=Reframe(1.8),
        model=Sawmill.run(472, 480),
        cues=[
            Cue(
                0,
                imports.type(through_line=7, over=0.6),
                relationship.type(through_line=415, over=1.0),
            ),
            Cue(
                lines.spoken("The waterwheel's spin drives the crankshaft"),
                relationship.emphasize(
                    "waterwheel",
                    ("spin", "water_drive.waterwheel.spin"),
                    "drives",
                    "crankshaft",
                    hold=0.8,
                ),
            ),
            Cue(
                lines.spoken("The waterwheel's spin"),
                mill.highlight(
                    Mill.water_drive.waterwheel,
                    Mill.water_drive.crankshaft,
                    others="ghost",
                ),
                until=lines.spoken("With Machinome"),
            ),
        ],
    )


# This class appears literally during the self-reference scene.
class ThisScene(Chapter):
    lines = Narration(
        "And here's the code of this exact scene! How cool is that?"
    )
    code = Listing(**scene_excerpt("ThisScene"))
    mirror = Shot(
        SourceRoom,
        {SourceRoom.code: code},
        until=lines.end(plus=1.4),
        model=Sawmill.run(484, 488),
        cues=[
            Cue(
                lines.spoken("this exact scene"),
                code.focus(token=lines.text),
                until=lines.end(plus=1.4),
            )
        ],
    )


class FilmSource(Chapter):
    lines = Narration(
        "This video's source code is in Python too. "
        "A scene, a camera, a voice. The words I say tell the camera "
        "when to move."
    )
    code = Listing(**scene_excerpt("FilmSource", maximum=10))
    headline = Card(
        text="This film has source code, too.", eyebrow="", small=False
    )
    reveal = Shot(
        SourceRoom,
        {SourceRoom.code: code, SourceRoom.heading: headline},
        until=lines.end(plus=1.0),
        model=Sawmill.run(480, 484),
        transition=Dissolve(0.6),
        cues=[
            Cue(
                lines.spoken("source code"),
                code.focus(token="Narration"),
                until=lines.end(plus=1.0),
            )
        ],
    )


class OpenWheel(Chapter):
    lines = Narration(
        "And the best part: this is all open source! "
        "Different ways to describe a part, connected in one machine. "
        "Ideas you can inspect, change, and share."
    )
    wheel = Constellation(
        names=[
            "OpenSCAD",
            "SolidPython2",
            "CadQuery",
            "build123d",
            "molejo",
            "STEP",
            "STL",
            "JSCAD",
        ],
        notes=[
            "",
            "",
            "",
            "solids + sheets",
            "flexible parts",
            "import",
            "import",
            "",
        ],
        title="OPEN SOURCE",
        subtitle="Source code for machines.",
        mark=(HERE / "assets/mark-white.svg").read_text(),
    )
    ecosystem = Shot(
        Exhibition,
        {Exhibition.graphic: wheel},
        until=lines.end(plus=1.8),
        model=Sawmill.run(488, 492),
        transition=Dissolve(0.9),
        cues=[Cue(0, wheel.unfold(), until=lines.end(plus=1.8))],
    )


class Intention(Chapter):
    lines = Narration(
        "The wheel makes revolutions. "
        "What matters is the intention you humans put on it."
    )
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    return_to_wheel = Shot(
        Exhibition,
        {Exhibition.stage: wheel},
        until=lines.spoken("What matters"),
        transition=Dissolve(1.5),
        model=Sawmill.run(492, 496),
    )
    intention = Shot(
        Exhibition,
        {Exhibition.stage: mill},
        until=lines.end(plus=1.8),
        transition=Dissolve(1.5),
        model=Sawmill.run(496, 504),
        cues=[Cue(1.5, mill.move(Sawmill.wide, until=lines.end(plus=1.8)))],
    )


class Invitation(Chapter):
    lines = Narration(
        "I'm Machinome. My purpose is to enable all machines to be "
        "open source. What do you want to build next?"
    )
    logo = Signature(
        svg=(HERE / "assets/wordmark-white.svg").read_text(),
        tagline="Source code for machines.",
        question="What do you want to build next?",
    )
    invitation = Shot(
        Exhibition,
        {Exhibition.graphic: logo},
        until=lines.end(plus=3.0),
        transition=Dissolve(1.2),
        fade_out=FadeOut(0.8),
        model=Sawmill.run(504, 508),
        cues=[
            Cue(
                lines.spoken("What do you want"),
                logo.enter(),
                until=lines.end(plus=3.0),
            )
        ],
    )


class Revolutions(Movie):
    title = "Revolutions"
    series = "Revolutions"
    status = "first-visual-proposal"
    learning_goal = (
        "Meet Machinome through its mechanical ancestor, understand the "
        "sawmill's two jobs, and see real source for the machine and film."
    )
    format = Format(1920, 1080, fps=24)
    narrator = Narrator(
        provider="elevenlabs",
        model="eleven_v3",
        voice="cgSgspJ2msm6clMCkdW9",
        label="Jessica",
        output="pcm_24000",
        settings={"stability": 0.5, "similarity_boost": 0.75},
        direction="Curious, intimate museum guide; a machine speaking.",
    )
    style = Style(
        background="#101419",
        foreground="#eeeae3",
        accent="#e9b778",
        font="Space Grotesk, sans-serif",
        safe_inset=0.05,
    )
    evidence = Evidence(
        brief="brief.md",
        reconstruction="../../models/hydraulic_sawmill/docs/reconstruction.md",
        transmission=(
            "../../models/hydraulic_sawmill/docs/transmission-validation.md"
        ),
    )
    credits = Credits(
        project="Leonardo da Vinci Gallery",
        creator="AI-directed proposal",
        copyright="Copyright (C) 2026 Luis Henrique Cassis Fagundes",
        license="AGPL-3.0-only",
        license_file="../../LICENSE",
    )
    release = Release(description="description.md")
    encounter = Encounter()
    film_source = FilmSource()
    this_scene = ThisScene()
    open_wheel = OpenWheel()
    intention = Intention()
    invitation = Invitation()


if __name__ == "__main__":
    output = HERE / "_build/movie.json"
    write(
        evaluate(Revolutions, name="machinome-release-1", out=output), output
    )
    print(output)
