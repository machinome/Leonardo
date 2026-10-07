"""Revoluções — versão brasileira do quarto corte."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path

from machinome_movie import (
    Action, Camera, Chapter, Credits, Cue, Dissolve, Element, Evidence,
    FadeIn, FadeOut, Format, Layer, Loop, Movie, Narrator, Picture,
    Release, Set, Shot, Slot, Source, Still, Style, Title, View, evaluate, write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill
from narration import AUDIO, lines
from scene_source import excerpt, model_excerpt

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent / 'machinome-release-3/assets'
RETURN = "A roda faz revoluções, e os humanos constroem"


class Exhibition(Set):
    module = 'stage.jsx'
    stage = Slot()
    ghost = Slot()
    heading = Slot()
    note = Slot()
    graphic = Slot()


class Mechanism(Set):
    module = 'stage.jsx'
    ghost = Slot()
    stage = Slot()
    note = Slot()


class Archive(Set):
    module = 'stage.jsx'
    picture = Slot()
    note = Slot()


class Workbench(Set):
    module = 'stage.jsx'
    stage = Slot()
    imports = Slot()
    code = Slot()


class SourceRoom(Set):
    module = 'stage.jsx'
    code = Slot()


class TestBench(Set):
    module = 'stage.jsx'
    stage = Slot()
    code = Slot()
    note = Slot()


class Listing(Element):
    module = 'stage.jsx'
    focus = Action(token=str)
    blink = Action(token=str, line=int, occurrence=int)
    write = Action()
    complete = Action()


class Constellation(Element):
    module = 'stage.jsx'
    hub = Action()
    reveal = Action(name=str)
    drive = Action()


class Signature(Element):
    module = 'stage.jsx'
    enter = Action()


class Sawmill(Loop):
    model = Mill
    export = '../machinome-release-3/_build/model'
    readiness = 'Posed reconstruction of a museum interpretation; no fluid, force or cutting physics.'
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
    test = Camera(position=(-560, -200, 600), target=(50, 0, 345), fov=37)
    not_wheel = Layer(Mill.frame, Mill.saw, Mill.carriage, Mill.feed,
                      Mill.water_drive.channel, Mill.water_drive.water,
                      Mill.water_drive.crankshaft, Mill.water_drive.crank,
                      Mill.water_drive.crank_retainer)
    drive_context = Layer(Mill.frame, Mill.carriage, Mill.feed)
    feed_context = Layer(Mill.frame, Mill.water_drive, Mill.carriage)
    rope_context = Layer(Mill.frame, Mill.water_drive, Mill.saw, Mill.feed.feed_drum)
    imports = Source('../../models/hydraulic_sawmill/model.py', lines=(7, 7))
    test_context = Layer(Mill.frame, Mill.water_drive, Mill.feed,
                         Mill.saw.connecting_rod, Mill.saw.sash.frame)
    drawing = Still('../machinome-release-3/assets/000R-1078.jpg',
                    credit='Leonardo da Vinci, Codex Atlanticus 1078r; codex-atlanticus.it via Wikimedia Commons, File:000R-1078.jpg.',
                    rights='Public domain, as recorded by Wikimedia Commons (PD-Art / PD-old); retrieved 2026-10-07.',
                    upscale=1.5)


class CrankStroke:
    narration = (
        "Uma manivela e uma biela transformam esse giro "
        "no movimento de subida e descida da serra."
    )
    view = View(Sawmill, camera=Sawmill.rear,
                hide=[Sawmill.drive_context])
    stroke = lines.spoken("no movimento de subida e descida da serra")
    end = lines.spoken("Mas a tora")
    shot = Shot(
        Mechanism, {Mechanism.stage: view},
        until=end, model=Sawmill.run(424, 432),
        cues=[
            Cue(0, view.move(Sawmill.saw, until=stroke)),
            Cue(lines.spoken("Uma manivela"),
                view.highlight(Mill.water_drive.crank, others="keep"),
                until=lines.spoken("uma biela", plus=-0.12)),
            Cue(lines.spoken("uma biela"),
                view.highlight(Mill.saw.connecting_rod, others="keep"),
                until=lines.spoken("transformam esse giro", plus=-0.1)),
            Cue(stroke, view.highlight(Mill.saw.sash, others="keep"),
                until=lines.spoken("Mas a tora", plus=-0.2)),
        ])


class ThisScene:
    narration = "E aqui está o código desta exata cena! Que legal!"
    code = Listing(**excerpt("ThisScene"))
    end = lines.spoken("E a melhor parte")

    shot = Shot(
        SourceRoom, {SourceRoom.code: code},
        until=end, model=Sawmill.run(484, 488),
        cues=[
            Cue(lines.spoken(narration),
                code.focus(token=narration), until=end),
        ],
    )


def technology_cues(element):
    return [Cue(lines.spoken(name), element.reveal(name=name), until=lines.spoken(RETURN))
            for name in ['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh']]


def relation_blinks(element):
    # Read the English relationship, then map its Portuguese meaning back
    # onto the same real source tokens. Never translate Python identifiers.
    pairs = [('waterwheel', 'waterwheel'), ('drives', 'drives'),
             ('crankshaft', 'crankshaft'), ('rotação', 'spin'),
             ("roda-d'água", 'waterwheel'), ('aciona', 'drives'),
             ('virabrequim', 'crankshaft')]
    return [Cue(lines.spoken(phrase), element.blink(token=token, line=416, occurrence=0),
                until=lines.spoken_end(phrase)) for phrase, token in pairs]


class Continuous(Chapter):
    performance = lines
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    ghost = View(Sawmill, camera=Sawmill.rear)
    drive = CrankStroke.view
    feed = View(Sawmill, camera=Sawmill.saw, hide=[Sawmill.feed_context])
    ropes = View(Sawmill, camera=Sawmill.pawls, hide=[Sawmill.rope_context])
    returned = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    identity = Title('Serraria hidráulica', subtitle='LEONARDO DA VINCI')
    limits = Title('Movimento reconstruído · forças e corte não simulados')
    drawing = Picture(Sawmill.drawing, fit='cover')
    drawing_source = Title('Codex Atlanticus · 1078r', subtitle='Fonte: Wikimedia Commons · codex-atlanticus.it')
    python = Signature(svg=(HERE.parent / 'machinome-release-2/assets/python-logo.svg').read_text(),
                       tagline='Python', url='', question='', compact=True)
    imports = Source.panel(Sawmill.imports)
    assembly = Listing(**model_excerpt('models/hydraulic_sawmill/model.py', [(401, 417)]))
    tests = Listing(**model_excerpt('models/hydraulic_sawmill/test_model.py',
                                   [(8, 8), (25, 27), (604, 612)]))
    test_view = View(Sawmill, camera=Sawmill.test, hide=[Sawmill.test_context])
    test_note = Title('13 posições amostradas · 0–4 segundos')
    film_code = Listing(**excerpt('CrankStroke'))
    mirror_code = ThisScene.code
    ecosystem = Constellation(
        names=['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh'],
        drivers=['Three.js', 'NumPy', 'SciPy', 'Manifold', 'FastAPI', 'React', 'OpenSpec'],
        spacing=310.0, mark=(BRAND / 'mark-orange.svg').read_text(),
        title='CÓDIGO ABERTO', arrival=3.0, angularAcceleration=12.0, entrySpeedFraction=0.12, timeOffset=0.0, fadeDuration=0.0,
    )
    signature = Signature(svg=(BRAND / 'wordmark-orange.svg').read_text(),
                          tagline='Código-fonte para máquinas.',
                          url='https://github.com/machinome/machinome/',
                          question='O que você quer construir agora?', compact=False)

    revolution = Shot(Exhibition, {Exhibition.stage: wheel},
        until=lines.spoken("Há cinco séculos"), fade_in=FadeIn(0.5),
        model=Sawmill.run(400, 404))
    ancestor = Shot(Exhibition, {Exhibition.stage: mill, Exhibition.heading: identity},
        until=lines.spoken("A água sob a roda"), transition=Dissolve(1.2),
        model=Sawmill.run(404, 424), cues=[
            Cue(0, identity.show(enter=0.6, leave=0.6), until=lines.spoken("Eu também sou uma máquina")),
            # finish.mjs samples one continuous orbit on the measured take.
            Cue(lines.spoken("projetou"), mill.move(Sawmill.rear, until=lines.spoken("A água sob a roda"))),
        ])
    water = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: drive, Mechanism.note: limits},
        until=lines.spoken("Uma manivela"), model=Sawmill.run(424, 428), cues=[
            Cue(0, drive.move(Sawmill.crank, until=lines.spoken("gira este eixo")),
                ghost.move(Sawmill.crank, until=lines.spoken("gira este eixo"))),
            Cue(lines.spoken("sob a roda"), drive.highlight(Mill.water_drive.waterwheel, others='keep'),
                until=lines.spoken("este eixo", plus=-0.12)),
            Cue(lines.spoken("este eixo"), drive.highlight(Mill.water_drive.crankshaft, others='keep'),
                until=lines.spoken("Uma manivela", plus=-0.2)),
            Cue(0, limits.show(), until=lines.spoken("Uma manivela")),
        ])
    # This real shot is the source revealed later. Add the synchronized context
    # plate in the document finishing pass; its camera duplicates this view.
    crank = CrankStroke.shot
    feed_motion = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: feed, Mechanism.note: limits},
        until=lines.spoken("Esse pequeno passo"), model=Sawmill.run(432, 440), cues=[
            Cue(0, feed.move(Sawmill.pawls, until=lines.spoken("Durante o corte")),
                ghost.move(Sawmill.pawls, until=lines.spoken("Durante o corte"))),
            Cue(lines.spoken("esta alavanca comprida"), feed.highlight(Mill.feed.rocker, others='keep'),
                until=lines.spoken("puxa uma lingueta", plus=-0.12)),
            Cue(lines.spoken("puxa uma lingueta"), feed.highlight(Mill.feed.pawl, others='keep'),
                until=lines.spoken("um dente", plus=-0.12)),
            Cue(lines.spoken("um dente"), feed.highlight(Mill.feed.feed_drum, others='keep'),
                until=lines.spoken("Uma segunda lingueta", plus=-0.25)),
            Cue(lines.spoken("Uma segunda lingueta"), feed.highlight(Mill.feed.holding_pawl, others='keep'),
                until=lines.spoken("enquanto a primeira retorna")),
            Cue(0, limits.show(), until=lines.spoken("Esse pequeno passo")),
        ])
    transmission = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken("A segunda corda"), model=Sawmill.run(440, 452), cues=[
            Cue(lines.spoken("enrola uma corda nesse eixo"), ropes.highlight(Mill.feed.winding, others='keep'),
                until=lines.spoken("Siga a corda", plus=-0.25)),
            Cue(lines.spoken("Siga a corda"), ropes.move(Sawmill.ropes, until=lines.spoken("Ela gira")),
                ghost.move(Sawmill.ropes, until=lines.spoken("Ela gira"))),
            Cue(lines.spoken("para baixo e para o outro lado"), ropes.highlight(Mill.feed.drive_line, others='keep'),
                until=lines.spoken("Ela gira", plus=-0.1)),
            Cue(lines.spoken("Ela gira"), ropes.move(Sawmill.drum, until=lines.spoken("um tambor largo")),
                ghost.move(Sawmill.drum, until=lines.spoken("um tambor largo"))),
            Cue(lines.spoken("um eixo composto"), ropes.highlight(Mill.feed.reduction_shaft, others='keep'),
                until=lines.spoken("um tambor largo", plus=-0.1)),
            Cue(lines.spoken("um tambor largo"), ropes.highlight(Mill.feed.reserve, others='keep'),
                until=lines.spoken("enquanto uma seção mais fina", plus=-0.12)),
            Cue(lines.spoken("enquanto uma seção mais fina"), ropes.highlight(Mill.feed.takeup, others='keep'),
                until=lines.spoken("A segunda corda", plus=-0.25)),
            Cue(0, limits.show(), until=lines.spoken("A segunda corda")),
        ])
    consequence = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken("Uma roda"), model=Sawmill.run(452, 460), cues=[
            Cue(0, ropes.move(Sawmill.carriage, until=lines.spoken("em direção à lâmina")),
                ghost.move(Sawmill.carriage, until=lines.spoken("em direção à lâmina"))),
            Cue(lines.spoken("A segunda corda"), ropes.highlight(Mill.feed.haul_span, others='keep'),
                until=lines.spoken("puxa a tora", plus=-0.1)),
            Cue(lines.spoken("puxa a tora"), ropes.highlight(Mill.carriage.timber, others='keep'),
                until=lines.spoken("em direção à lâmina")),
            Cue(0, limits.show(), until=lines.spoken("Uma roda")),
        ])
    two_jobs = Shot(Exhibition, {Exhibition.stage: mill}, until=lines.spoken("Para reconstruir"),
        model=Sawmill.run(460, 464), cues=[Cue(0, mill.move(Sawmill.wide, until=lines.spoken("Para reconstruir")))])
    document = Shot(Archive, {Archive.picture: drawing, Archive.note: drawing_source},
        until=lines.spoken("e usei a linguagem Python"), model=Sawmill.run(464, 470), transition=Dissolve(0.4), cues=[
            Cue(0, drawing.show(leave=0.2, view=[(0, (0.5, 0.34), 1.03),
                (lines.spoken("e usei a linguagem Python"), (0.5, 0.33), 1.1)]),
                drawing_source.show(enter=0.3, leave=0.2), until=lines.spoken("e usei a linguagem Python"))])
    python_language = Shot(Exhibition, {Exhibition.graphic: python},
        until=lines.spoken('From Machinome'), model=Sawmill.run(470, 472), transition=Dissolve(0.35))
    face_reveal = Shot(Workbench, {Workbench.stage: mill, Workbench.imports: imports, Workbench.code: assembly},
        until=lines.spoken("O código-fonte também permite"), model=Sawmill.run(472, 480), transition=Dissolve(0.4), cues=[
            Cue(0, mill.move(Sawmill.source, until=lines.spoken("Este é o Machinome")),
                imports.type(through_line=7, over=2.7)),
            Cue(lines.spoken("Este é o Machinome"), assembly.write(),
                until=lines.spoken("Este é o Machinome", plus=2.7)),
            Cue(lines.spoken("Este é o Machinome", plus=2.7), assembly.complete(),
                until=lines.spoken("O código-fonte também permite")),
            *relation_blinks(assembly),
        ])
    testing = Shot(TestBench, {TestBench.stage: test_view, TestBench.code: tests,
                               TestBench.note: test_note},
        until=lines.spoken("O código-fonte deste vídeo"), model=Sawmill.run(0, 4),
        transition=Dissolve(0.5), cues=[
            Cue(lines.spoken("Este teste verifica"), tests.blink(token='test_blade_clears_both_log_halves', line=606, occurrence=0),
                until=lines.spoken_end("Este teste verifica")),
            Cue(lines.spoken("a lâmina não"), test_view.highlight(Mill.saw.sash.blade, others='keep'),
                tests.blink(token='blade', line=608, occurrence=0), until=lines.spoken("intersecta")),
            Cue(lines.spoken("intersecta"), tests.blink(token='assertNotIntersecting', line=607, occurrence=0),
                until=lines.spoken_end("intersecta")),
            Cue(lines.spoken("nenhuma das duas metades"), tests.blink(token='log_left', line=608, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_left, others='keep'), until=lines.spoken_end("nenhuma das duas metades")),
            Cue(lines.spoken("da tora"), tests.blink(token='log_right', line=611, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_right, others='keep'), until=lines.spoken_end("da tora")),
            Cue(lines.spoken('Testing steps'), tests.blink(token='testing_steps', line=605, occurrence=0),
                until=lines.spoken_end('Testing steps')),
            Cue(lines.spoken("treze"), tests.blink(token='13', line=605, occurrence=0),
                until=lines.spoken_end("treze")),
            Cue(lines.spoken("zero a quatro segundos"), tests.blink(token='end=4', line=605, occurrence=0),
                until=lines.spoken_end("zero a quatro segundos")),
            Cue(lines.spoken('Testing steps'), test_note.show(), until=lines.spoken("O código-fonte deste vídeo")),
        ])
    behind_the_film = Shot(SourceRoom, {SourceRoom.code: film_code},
        until=lines.spoken("E aqui está o código"), model=Sawmill.run(480, 484), transition=Dissolve(0.35), cues=[
            Cue(lines.spoken("Uma cena"), film_code.focus(token='shot = Shot('), until=lines.spoken("uma câmera")),
            Cue(lines.spoken("uma câmera"), film_code.focus(token='view = View('), until=lines.spoken("uma voz")),
            Cue(lines.spoken("uma voz"), film_code.focus(token="Uma manivela e uma biela"), until=lines.spoken("As palavras que eu digo")),
            Cue(lines.spoken("As palavras que eu digo"), film_code.focus(token='stroke = lines.spoken('), until=lines.spoken("dizem à câmera")),
            Cue(lines.spoken("dizem à câmera"), film_code.focus(token='view.move('), until=lines.spoken("E aqui está o código")),
        ])
    mirror = ThisScene.shot
    open_source = Shot(Exhibition, {Exhibition.graphic: ecosystem},
        until=lines.spoken(RETURN), model=Sawmill.run(488, 492), transition=Dissolve(0.4), cues=[
            Cue(0, ecosystem.hub(), until=lines.spoken(RETURN)),
            *technology_cues(ecosystem),
            Cue(lines.spoken("E, por baixo de tudo"), ecosystem.drive(), until=lines.spoken(RETURN)),
        ])
    wheel_returns = Shot(Exhibition, {Exhibition.stage: returned}, until=lines.spoken("Eu sou o Machinome"),
        model=Sawmill.run(492, 496), transition=Dissolve(1.25))
    invitation = Shot(Exhibition, {Exhibition.graphic: signature}, until=lines.end(plus=2.5),
        model=Sawmill.run(496, 504), transition=Dissolve(0.8), fade_out=FadeOut(0.7), cues=[
            Cue(lines.spoken("O que VOCÊ quer"), signature.enter(), until=lines.end(plus=2.5))])


class Revolutions(Movie):
    title = 'Revoluções'
    status = 'release-candidate-4-pt-br'
    learning_goal = 'Meet Machinome through an ancestor, its mechanism, its code and this film.'
    format = Format(1920, 1080, fps=24)
    narrator = Narrator(provider=AUDIO['provider'], model=AUDIO['model'], voice=AUDIO['voice'],
                        label=AUDIO['voiceLabel'], output=AUDIO['outputFormat'], settings=AUDIO['voiceSettings'])
    style = Style(background='#101419', foreground='#eeeae3', accent='#e9b778',
                  font='Space Grotesk, sans-serif', safe_inset=0.05)
    evidence = Evidence(brief='brief.md', review='DIRECTION.md',
        reconstruction='../../models/hydraulic_sawmill/docs/reconstruction.md')
    credits = Credits(project='Leonardo da Vinci Gallery', creator='AI-directed release film',
        copyright='Copyright (C) 2026 Luis Henrique Cassis Fagundes', license='AGPL-3.0-only', license_file='../../LICENSE')
    release = Release(description='description.md')
    continuous = Continuous()


if __name__ == '__main__':
    output = HERE / '_build/movie.json'
    doc = evaluate(Revolutions, name='machinome-release-4-pt-br', out=output)
    doc['chapters'][0]['speechOffset'] = 3.0
    write(doc, output)
    print(output)
