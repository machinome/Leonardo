"""Portrait study of the sawmill, through 'one wheel, two jobs'."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.

from pathlib import Path

from machinome.movie import (
    Camera,
    Chapter,
    Credits,
    Cue,
    Element,
    Evidence,
    FadeIn,
    FadeOut,
    Format,
    Layer,
    Loop,
    Movie,
    Narrator,
    Reframe,
    Release,
    Set,
    Shot,
    Slot,
    Style,
    View,
    evaluate,
    write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill
from narration import AUDIO, lines

HERE = Path(__file__).resolve().parent
TRANSMISSION = "../../models/hydraulic_sawmill/docs/transmission-validation.md"


class Portrait(Set):
    module = "stage.jsx"
    backdrop = Slot()
    plate = Slot()
    ghost = Slot()
    stage = Slot()


class Shade(Element):
    module = "stage.jsx"


class Sawmill(Loop):
    model = Mill
    export = "../machinome-release-3/_build/model"
    readiness = (
        "Posed reconstruction of the Milan museum interpretation; "
        "no fluid, force or cutting physics."
    )
    wheel = Camera(position=(0, -710, 120), target=(0, -151, 120), fov=37)
    wide = Camera(position=(1350, -1810, 1120), target=(0, -20, 230), fov=37)
    rear = Camera(position=(1320, 1320, 970), target=(0, 0, 285), fov=37)
    crank = Camera(position=(470, 850, 480), target=(0, 0, 215), fov=37)
    saw = Camera(position=(470, 890, 575), target=(0, 0, 335), fov=37)
    pawls = Camera(position=(145, 540, 425), target=(135, 30, 332), fov=37)
    ropes = Camera(position=(-660, 1040, 690), target=(-80, 0, 300), fov=37)
    drum = Camera(position=(-640, 425, 450), target=(-305, 0, 300), fov=37)
    carriage = Camera(position=(-1030, 920, 810), target=(-40, 0, 330), fov=37)
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

    drive_context = Layer(
        Mill.frame,
        Mill.carriage,
        Mill.feed,
    )
    feed_context = Layer(Mill.frame, Mill.water_drive, Mill.carriage)
    rope_context = Layer(
        Mill.frame, Mill.water_drive, Mill.saw, Mill.feed.feed_drum
    )


class Continuous(Chapter):
    performance = lines
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    detail = View(Sawmill, camera=Sawmill.rear, hide=[Sawmill.drive_context])
    feed_view = View(Sawmill, camera=Sawmill.saw, hide=[Sawmill.feed_context])
    ropes_view = View(
        Sawmill, camera=Sawmill.pawls, hide=[Sawmill.rope_context]
    )
    whole = View(Sawmill, camera=Sawmill.carriage)
    ghost = View(Sawmill, camera=Sawmill.rear)
    shade = Shade()

    revolution = Shot(
        Portrait,
        {Portrait.stage: wheel},
        until=lines.spoken("Há cinco séculos"),
        fade_in=FadeIn(0.5),
        model=Sawmill.run(400, 404),
    )
    ancestor = Shot(
        Portrait,
        {
            Portrait.backdrop: wheel,
            Portrait.stage: mill,
        },
        until=lines.spoken("A água sob a roda"),
        transition=Reframe(1.2),
        model=Sawmill.run(404, 420),
        cues=[
            Cue(
                lines.spoken("projetou"),
                mill.move(
                    Sawmill.rear, until=lines.spoken("A água sob a roda")
                ),
            ),
        ],
    )
    water = Shot(
        Portrait,
        {
            Portrait.backdrop: mill,
            Portrait.plate: shade,
            Portrait.ghost: ghost,
            Portrait.stage: detail,
        },
        until=lines.spoken("Uma manivela"),
        transition=Reframe(1.2),
        model=Sawmill.run(420, 424),
        cues=[
            Cue(
                0,
                detail.move(
                    Sawmill.crank, until=lines.spoken("gira este eixo")
                ),
                mill.move(Sawmill.crank, until=lines.spoken("gira este eixo")),
            ),
            Cue(
                lines.spoken("roda gira"),
                detail.highlight(Mill.water_drive.waterwheel, others="keep"),
                until=lines.spoken("este eixo", plus=-0.12),
            ),
            Cue(
                lines.spoken("este eixo"),
                detail.highlight(Mill.water_drive.crankshaft, others="keep"),
                until=lines.spoken("Uma manivela", plus=-0.2),
            ),
        ],
    )
    stroke = Shot(
        Portrait,
        {Portrait.ghost: ghost, Portrait.stage: detail},
        until=lines.spoken("Mas a tora"),
        model=Sawmill.run(424, 432),
        cues=[
            Cue(
                0,
                detail.move(
                    Sawmill.saw,
                    until=lines.spoken(
                        "no movimento de subida e descida da serra"
                    ),
                ),
            ),
            Cue(
                lines.spoken("Uma manivela"),
                detail.highlight(Mill.water_drive.crank, others="keep"),
                until=lines.spoken("uma biela", plus=-0.12),
            ),
            Cue(
                lines.spoken("uma biela"),
                detail.highlight(Mill.saw.connecting_rod, others="keep"),
                until=lines.spoken("transformam esse giro", plus=-0.1),
            ),
            Cue(
                lines.spoken("no movimento de subida e descida da serra"),
                detail.highlight(Mill.saw.sash, others="keep"),
                until=lines.spoken("Mas a tora", plus=-0.2),
            ),
        ],
    )
    feed = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: feed_view,
        },
        until=lines.spoken("Esse pequeno passo"),
        model=Sawmill.keys(
            {
                0: 432,
                lines.spoken("Durante o corte"): 436,
                lines.spoken("Uma segunda lingueta"): 438,
                lines.spoken("Esse pequeno passo"): 440,
            }
        ),
        cues=[
            Cue(
                0,
                feed_view.move(
                    Sawmill.pawls, until=lines.spoken("Durante o corte")
                ),
            ),
            Cue(
                lines.spoken("esta alavanca"),
                feed_view.highlight(Mill.feed.rocker, others="keep"),
                until=lines.spoken("puxa uma lingueta", plus=-0.12),
            ),
            Cue(
                lines.spoken("puxa uma lingueta"),
                feed_view.highlight(Mill.feed.pawl, others="keep"),
                until=lines.spoken("um dente", plus=-0.12),
            ),
            Cue(
                lines.spoken("um dente"),
                feed_view.highlight(Mill.feed.feed_drum, others="keep"),
                until=lines.spoken("Uma segunda lingueta", plus=-0.25),
            ),
            Cue(
                lines.spoken("Uma segunda lingueta"),
                feed_view.highlight(Mill.feed.holding_pawl, others="keep"),
                until=lines.spoken("enquanto a primeira retorna"),
            ),
            Cue(
                lines.spoken("enquanto a primeira retorna"),
                feed_view.highlight(Mill.feed.pawl, others="keep"),
                until=lines.spoken_end("enquanto a primeira retorna"),
            ),
        ],
    )
    transmission = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: ropes_view,
        },
        until=lines.spoken("A segunda corda"),
        model=Sawmill.run(440, 452),
        cues=[
            Cue(
                lines.spoken("enrola uma corda nesse eixo"),
                ropes_view.highlight(Mill.feed.winding, others="keep"),
                until=lines.spoken("Siga a corda", plus=-0.25),
            ),
            Cue(
                lines.spoken("Siga a corda"),
                ropes_view.move(Sawmill.ropes, until=lines.spoken("Ela gira")),
            ),
            Cue(
                lines.spoken("para baixo e para o outro lado"),
                ropes_view.highlight(Mill.feed.drive_line, others="keep"),
                until=lines.spoken("Ela gira", plus=-0.1),
            ),
            Cue(
                lines.spoken("Ela gira"),
                ropes_view.move(
                    Sawmill.drum, until=lines.spoken("um tambor largo")
                ),
            ),
            Cue(
                lines.spoken("um eixo composto"),
                ropes_view.highlight(Mill.feed.reduction_shaft, others="keep"),
                until=lines.spoken("um tambor largo", plus=-0.1),
            ),
            Cue(
                lines.spoken("um tambor largo"),
                ropes_view.highlight(Mill.feed.reserve, others="keep"),
                until=lines.spoken("enquanto uma seção mais fina", plus=-0.12),
            ),
            Cue(
                lines.spoken("enquanto uma seção mais fina"),
                ropes_view.highlight(Mill.feed.takeup, others="keep"),
                until=lines.spoken("A segunda corda", plus=-0.25),
            ),
        ],
    )
    consequence = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: ropes_view,
        },
        until=lines.spoken("Uma roda,"),
        model=Sawmill.run(452, 460),
        cues=[
            Cue(
                0,
                ropes_view.move(
                    Sawmill.carriage, until=lines.spoken("em direção à lâmina")
                ),
            ),
            Cue(
                lines.spoken("A segunda corda"),
                ropes_view.highlight(
                    Mill.feed.takeup,
                    Mill.feed.haul_span,
                    Mill.feed.haul,
                    others="keep",
                ),
                until=lines.spoken("puxa a tora", plus=-0.1),
            ),
            Cue(
                lines.spoken("puxa a tora"),
                ropes_view.highlight(Mill.carriage.timber, others="keep"),
                until=lines.spoken("em direção à lâmina"),
            ),
        ],
    )
    two_jobs = Shot(
        Portrait,
        {Portrait.stage: whole},
        until=lines.end(plus=2.2),
        model=Sawmill.run(460, 464),
        fade_out=FadeOut(1.0),
        cues=[
            Cue(
                0,
                whole.move(Sawmill.wide, until=lines.end(plus=2.2)),
            ),
        ],
    )


class Study(Movie):
    title = "Revoluções"
    status = "study-1-pt-br"
    learning_goal = "Ver como uma roda aciona a serra e o avanço da tora."
    format = Format(1080, 1920, fps=24)
    narrator = Narrator(
        provider=AUDIO["provider"],
        model=AUDIO["model"],
        voice=AUDIO["voice"],
        label=AUDIO["voiceLabel"],
        output=AUDIO["outputFormat"],
        settings=AUDIO["voiceSettings"],
    )
    style = Style(
        background="#101419",
        foreground="#eeeae3",
        accent="#e9b778",
        font="Space Grotesk, sans-serif",
        safe_inset=0.08,
    )
    evidence = Evidence(
        direction="README.md",
        reconstruction="../../models/hydraulic_sawmill/docs/reconstruction.md",
        transmission=TRANSMISSION,
    )
    credits = Credits(
        project="Leonardo da Vinci Gallery",
        creator="Astra",
        copyright="Copyright (C) 2026 Luis Henrique Cassis Fagundes",
        license="CERN-OHL-S-2.0+",
        license_file="../../LICENSE",
    )
    release = Release(description="description.md")
    continuous = Continuous()


if __name__ == "__main__":
    output = HERE / "_build/movie.json"
    doc = evaluate(Study, name="study-1-pt-br", out=output)
    doc["audio"]["replacements"] = AUDIO["replacements"]
    doc["chapters"][0]["speechOffset"] = 0.6
    write(doc, output)
    print(output)
