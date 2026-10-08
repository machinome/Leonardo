"""Portrait study of the sawmill, through 'one wheel, two jobs'."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

from pathlib import Path

from machinome_movie import (
    Camera,
    Chapter,
    Credits,
    Cue,
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
    Title,
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
    ghost = Slot()
    stage = Slot()
    heading = Slot()
    note = Slot()


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
        Mill.water_drive.channel,
        Mill.water_drive.water,
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
    hook_title = Title("Uma roda. Duas funções.")
    identity = Title("A serraria de Leonardo", subtitle="HÁ CINCO SÉCULOS")
    limits = Title(
        "Reconstrução do movimento", subtitle="Forças e corte não simulados"
    )
    ending = Title("Cortar e avançar.")

    revolution = Shot(
        Portrait,
        {Portrait.stage: wheel, Portrait.heading: hook_title},
        until=lines.spoken("Há cinco séculos"),
        fade_in=FadeIn(0.25),
        model=Sawmill.run(400, 404),
        cues=[
            Cue(
                0,
                hook_title.show(enter=0.3, leave=0.25),
                until=lines.spoken("Há cinco séculos"),
            )
        ],
    )
    ancestor = Shot(
        Portrait,
        {
            Portrait.backdrop: wheel,
            Portrait.stage: mill,
            Portrait.heading: identity,
        },
        until=lines.spoken("A água gira"),
        transition=Reframe(0.8),
        model=Sawmill.run(404, 420),
        cues=[
            Cue(
                0,
                identity.show(enter=0.5, leave=0.4),
                until=lines.spoken("A água gira"),
            ),
            Cue(
                lines.spoken("Leonardo da Vinci"),
                mill.move(Sawmill.rear, until=lines.spoken("A água gira")),
            ),
        ],
    )
    water = Shot(
        Portrait,
        {Portrait.ghost: ghost, Portrait.stage: detail, Portrait.note: limits},
        until=lines.spoken("Uma manivela"),
        model=Sawmill.run(420, 424),
        cues=[
            Cue(
                0,
                detail.move(
                    Sawmill.crank, until=lines.spoken("movimenta este eixo")
                ),
            ),
            Cue(
                0,
                detail.highlight(Mill.water_drive.waterwheel, others="keep"),
                until=lines.spoken("que movimenta"),
            ),
            Cue(
                lines.spoken("que movimenta"),
                detail.highlight(Mill.water_drive.crankshaft, others="keep"),
                until=lines.spoken("Uma manivela"),
            ),
            Cue(0, limits.show(), until=lines.spoken("Uma manivela")),
        ],
    )
    stroke = Shot(
        Portrait,
        {Portrait.ghost: ghost, Portrait.stage: detail, Portrait.note: limits},
        until=lines.spoken("Mas a tora"),
        model=Sawmill.run(424, 432),
        cues=[
            Cue(
                0, detail.move(Sawmill.saw, until=lines.spoken("sobe e desce"))
            ),
            Cue(
                0,
                detail.highlight(Mill.water_drive.crank, others="keep"),
                until=lines.spoken("uma biela"),
            ),
            Cue(
                lines.spoken("uma biela"),
                detail.highlight(Mill.saw.connecting_rod, others="keep"),
                until=lines.spoken("sobe e desce"),
            ),
            Cue(
                lines.spoken("sobe e desce"),
                detail.highlight(Mill.saw.sash, others="keep"),
                until=lines.spoken("Mas a tora"),
            ),
            Cue(0, limits.show(), until=lines.spoken("Mas a tora")),
        ],
    )
    feed = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: feed_view,
            Portrait.note: limits,
        },
        until=lines.spoken("Cada passo"),
        model=Sawmill.keys(
            {
                0: 432,
                lines.spoken("Durante o corte"): 436,
                lines.spoken("Uma segunda lingueta"): 438,
                lines.spoken("Cada passo"): 440,
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
                0,
                feed_view.highlight(Mill.feed, others="keep"),
                until=lines.spoken("esta alavanca"),
            ),
            Cue(
                lines.spoken("esta alavanca"),
                feed_view.highlight(Mill.feed.rocker, others="keep"),
                until=lines.spoken("puxa uma lingueta"),
            ),
            Cue(
                lines.spoken("puxa uma lingueta"),
                feed_view.highlight(Mill.feed.pawl, others="keep"),
                until=lines.spoken("um dente"),
            ),
            Cue(
                lines.spoken("um dente"),
                feed_view.highlight(Mill.feed.feed_drum, others="keep"),
                until=lines.spoken("Uma segunda lingueta"),
            ),
            Cue(
                lines.spoken("Uma segunda lingueta"),
                feed_view.highlight(Mill.feed.holding_pawl, others="keep"),
                until=lines.spoken("enquanto a primeira volta"),
            ),
            Cue(
                lines.spoken("enquanto a primeira volta"),
                feed_view.highlight(Mill.feed.pawl, others="keep"),
                until=lines.spoken("Cada passo"),
            ),
            Cue(0, limits.show(), until=lines.spoken("Cada passo")),
        ],
    )
    transmission = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: ropes_view,
            Portrait.note: limits,
        },
        until=lines.spoken("A segunda corda"),
        model=Sawmill.run(440, 452),
        cues=[
            Cue(
                0,
                ropes_view.highlight(Mill.feed.winding, others="keep"),
                until=lines.spoken("Siga a corda"),
            ),
            Cue(
                lines.spoken("Siga a corda"),
                ropes_view.move(Sawmill.ropes, until=lines.spoken("Ela gira")),
            ),
            Cue(
                lines.spoken("Siga a corda"),
                ropes_view.highlight(Mill.feed.drive_line, others="keep"),
                until=lines.spoken("Ela gira"),
            ),
            Cue(
                lines.spoken("Ela gira"),
                ropes_view.move(
                    Sawmill.drum, until=lines.spoken("O tambor largo")
                ),
            ),
            Cue(
                lines.spoken("Ela gira"),
                ropes_view.highlight(Mill.feed.reduction_shaft, others="keep"),
                until=lines.spoken("O tambor largo"),
            ),
            Cue(
                lines.spoken("O tambor largo"),
                ropes_view.highlight(Mill.feed.reserve, others="keep"),
                until=lines.spoken("enquanto a parte mais fina"),
            ),
            Cue(
                lines.spoken("enquanto a parte mais fina"),
                ropes_view.highlight(Mill.feed.takeup, others="keep"),
                until=lines.spoken("A segunda corda"),
            ),
            Cue(0, limits.show(), until=lines.spoken("A segunda corda")),
        ],
    )
    consequence = Shot(
        Portrait,
        {
            Portrait.ghost: ghost,
            Portrait.stage: ropes_view,
            Portrait.note: limits,
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
                0,
                ropes_view.highlight(
                    Mill.feed.takeup,
                    Mill.feed.haul_span,
                    Mill.feed.haul,
                    others="keep",
                ),
                until=lines.spoken("puxa a tora"),
            ),
            Cue(
                lines.spoken("puxa a tora"),
                ropes_view.highlight(Mill.carriage.timber, others="keep"),
                until=lines.spoken("Uma roda,"),
            ),
            Cue(0, limits.show(), until=lines.spoken("Uma roda,")),
        ],
    )
    two_jobs = Shot(
        Portrait,
        {Portrait.stage: whole, Portrait.heading: ending},
        until=lines.end(plus=1.25),
        model=Sawmill.run(460, 464),
        fade_out=FadeOut(0.6),
        cues=[
            Cue(
                0,
                whole.move(
                    Sawmill.wide, until=lines.spoken("cortar e avançar")
                ),
            ),
            Cue(
                lines.spoken("cortar e avançar"),
                ending.show(enter=0.2),
                until=lines.end(plus=1.25),
            ),
        ],
    )


class Study(Movie):
    title = "Uma roda, duas funções"
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
        license="AGPL-3.0-only",
        license_file="../../LICENSE",
    )
    release = Release(description="description.md")
    continuous = Continuous()


if __name__ == "__main__":
    output = HERE / "_build/movie.json"
    doc = evaluate(Study, name="study-1-pt-br", out=output)
    doc["chapters"][0]["speechOffset"] = 0.35
    write(doc, output)
    print(output)
