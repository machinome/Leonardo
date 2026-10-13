"""Revoluções — fifth cut, live preview."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path
import base64
import json

from machinome_movie import (
    Action, Camera, Chapter, Credits, Cue, Dissolve, Element, Evidence,
    FadeIn, FadeOut, Format, Layer, Loop, Movie, Narrator, Picture,
    Reframe, Release, Set, Shot, Slot, Source, Still, Style, Title, View, evaluate, write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill
from narration import AUDIO, lines
from scene_source import excerpt, model_excerpt, token_line
from scene_source import cue_token_lines

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent / 'machinome-release-3/assets'
RETURN = 'A roda faz revoluções... e os humanos constroem'
HANDOFF = lines.spoken('por baixo de tudo', plus=2.01)  # First pass, then ~1.25s of graphic-only spin.


class Exhibition(Set):
    module = 'stage.jsx'
    stage = Slot()
    ghost = Slot()
    backdrop = Slot()
    heading = Slot()
    note = Slot()
    graphic = Slot()
    veil = Slot()


class Mechanism(Set):
    module = 'stage.jsx'
    backdrop = Slot()
    plate = Slot()
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
    surface = Slot()


class Studio(Set):
    module = 'stage.jsx'
    surface = Slot()
    stage = Slot()


class StudioSurface(Element):
    module = 'stage.jsx'
    reveal = Action()
    arrive = Action()
    settled = Action()
    focus = Action(area=str)
    type_prompt = Action()
    prompt_complete = Action()
    model_clock = Action(start=float, end=float)
    depart = Action()
    departed = Action()


class SourceRoom(Set):
    module = 'stage.jsx'
    code = Slot()


class TestBench(Set):
    module = 'stage.jsx'
    stage = Slot()
    code = Slot()
    note = Slot()
    surface = Slot()
    detail = Slot()


class Listing(Element):
    module = 'stage.jsx'
    focus = Action(token=str)
    blink = Action(token=str, line=int, occurrence=int)
    blink_all = Action(token=str)
    write = Action()
    complete = Action()
    conceal = Action()


class Constellation(Element):
    module = 'stage.jsx'
    hub = Action()
    approach = Action()
    reveal = Action(name=str)
    drive = Action()


class Signature(Element):
    module = 'stage.jsx'
    enter = Action()
    wait = Action()
    approach = Action()
    link = Action()
    linked = Action()


class Shade(Element):
    module = 'stage.jsx'


class Curtain(Element):
    module = 'stage.jsx'
    darken = Action()


class Sawmill(Loop):
    model = Mill
    export = '_build/model'
    readiness = 'Posed reconstruction of a museum interpretation; no fluid, force or cutting physics.'
    wheel = Camera(position=(0, -575, 120), target=(0, -151, 120), fov=37)
    hub = Camera(position=(0, -154, 120), target=(0, -151, 120), fov=37)
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
                    upscale=3.4)


class CrankStroke:
    narration = (
        "Uma manivela e uma biela transformam esse giro "
        "no movimento de subida e descida da serra."
    )
    view = View(Sawmill, camera=Sawmill.rear,
                hide=[Sawmill.drive_context])
    shot = Shot(
        Mechanism, {Mechanism.stage: view},
        until=lines.spoken("Mas a tora"),
        model=Sawmill.run(424, 432),
        cues=[
            Cue(0, view.move(Sawmill.saw,
                until=lines.spoken("movimento de subida e descida da serra"))),
            Cue(lines.spoken("Uma manivela"),
                view.highlight(Mill.water_drive.crank, others="keep"),
                until=lines.spoken("uma biela", plus=-0.12)),
            Cue(lines.spoken("uma biela"),
                view.highlight(Mill.saw.connecting_rod, others="keep"),
                until=lines.spoken("transformam esse giro", plus=-0.1)),
            Cue(lines.spoken("movimento de subida e descida da serra"),
                view.highlight(Mill.saw.sash, others="keep"),
                until=lines.spoken("Mas a tora", plus=-0.2)),
        ])


def source_cues(element, scene, entries):
    return [Cue(lines.spoken(phrase),
                element.blink_all(token=token) if row is None else
                element.blink(token=token, line=token_line(scene, row, token), occurrence=0),
                until=lines.spoken_end(phrase))
            for phrase, row, token in entries]


class ThisScene:
    narration = "E aqui está o código desta exata cena! Olha que legal!"
    code = Listing(**excerpt("ThisScene"))
    end = lines.spoken("E a melhor parte")

    shot = Shot(
        SourceRoom, {SourceRoom.code: code},
        until=end, model=Sawmill.run(484, 488),
        cues=source_cues(code, 'ThisScene', [
                ("E aqui está", 'narration =', 'narration'),
                ("código desta exata", 'code = Listing', 'code'),
                ("desta exata cena", 'class ThisScene', 'ThisScene'),
                ("Olha que legal", 'narration =', 'Olha que legal!'),
            ]),
    )


def technology_cues(element):
    return [Cue(lines.spoken(name), element.reveal(name=name), until=HANDOFF)
            for name in ['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh']]


def relation_blinks(element):
    # finish.mjs applies the take-bound local alignment in relation-timing.json.
    # Keep the provider timestamps and narration intact.
    return [Cue(lines.spoken(word),
                element.blink(token=word, line=416, occurrence=0),
                until=lines.spoken_end(word))
            for word in ['waterwheel', 'spin', 'drives', 'crankshaft']]


def cue_blinks(element, scene, token):
    return [element.blink(token=token, line=row, occurrence=0)
            for row in cue_token_lines(scene, token)]


class Continuous(Chapter):
    performance = lines
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    ghost = View(Sawmill, camera=Sawmill.rear)
    shade = Shade()
    drive = CrankStroke.view
    feed = View(Sawmill, camera=Sawmill.saw, hide=[Sawmill.feed_context])
    ropes = View(Sawmill, camera=Sawmill.pawls, hide=[Sawmill.rope_context])
    returned = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    wheel_exit = Curtain()
    identity = Title('Serraria hidráulica', subtitle='LEONARDO DA VINCI')
    limits = Title('Movimento reconstruído · forças e corte não simulados')
    drawing = Picture(Sawmill.drawing, fit='cover')
    drawing_source = Title('Fonte: Codex Atlanticus 1078r · Wikimedia Commons')
    python = Signature(svg=(HERE.parent / 'machinome-release-2/assets/python-logo.svg').read_text(),
                       tagline='Python', url='', license='', question='', compact=True)
    imports = Source.panel(Sawmill.imports)
    assembly = Listing(**model_excerpt('models/hydraulic_sawmill/model.py', [(401, 417)], type_in=True))
    studio_ui = StudioSurface(
        screenshot='data:image/png;base64,' + base64.b64encode(
            (HERE / 'assets/studio-background.png').read_bytes()).decode(),
        geometry=json.loads((HERE / 'assets/studio-capture.json').read_text()),
        prompt="Há mais um ajuste:",
        duration=1460.0, seconds_unit='s', departureFade=0.6,
    )
    tests = Listing(**model_excerpt('models/hydraulic_sawmill/test_model.py',
                                   [(8, 8), (25, 27), (604, 612)], type_in=True))
    test_view = View(Sawmill, camera=Sawmill.test, hide=[Sawmill.test_context])
    test_note = Title('13 posições amostradas · 0–4 segundos')
    film_code = Listing(**excerpt('CrankStroke', type_in=True))
    mirror_code = ThisScene.code
    ecosystem = Constellation(
        names=['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh'],
        drivers=['Three.js', 'NumPy', 'SciPy', 'Manifold', 'FastAPI', 'React', 'OpenSpec'],
        spacing=310.0, mark=(BRAND / 'mark-orange.svg').read_text(),
        title='CÓDIGO ABERTO', arrival=1.65, hold=0.0, spinDelay=1.65, stagger=0.45, streamDuration=5.8,
        # Keep gaining speed through the hub zoom: about 1.4 turns/s at exit.
        angularAcceleration=56.0, entrySpeedFraction=0.65, streamDelay=0.0, timeOffset=0.0, fadeDuration=0.0,
    )
    signature = Signature(svg=(BRAND / 'wordmark-orange.svg').read_text(),
                          tagline='',
                          url='https://github.com/machinome/machinome/',
                          license='GPL-2.0-or-later OR CERN-OHL-S-2.0+',
                          question='', compact=False)

    revolution = Shot(Exhibition, {Exhibition.stage: wheel},
        until=lines.spoken('Há cinco séculos'), fade_in=FadeIn(0.5),
        model=Sawmill.run(400, 404))
    # Keep the wheel as an opaque base while the full machine fades over it.
    # Reframe draws this live; a composed dissolve is a cut in the player.
    ancestor = Shot(Exhibition, {Exhibition.backdrop: wheel, Exhibition.stage: mill,
                                Exhibition.heading: identity},
        until=lines.spoken('A água sob'), transition=Reframe(1.2),
        model=Sawmill.run(404, 424), cues=[
            Cue(0, identity.show(enter=0.6, leave=0.6), until=lines.spoken('Eu também sou uma máquina')),
            # finish.mjs samples one continuous orbit on the measured take.
            Cue(lines.spoken('projetou'), mill.move(Sawmill.rear, until=lines.spoken('A água sob'))),
        ])
    water = Shot(Mechanism, {Mechanism.backdrop: mill, Mechanism.plate: shade,
                            Mechanism.ghost: ghost, Mechanism.stage: drive, Mechanism.note: limits},
        until=lines.spoken('Uma manivela'), model=Sawmill.run(424, 428), transition=Reframe(1.2), cues=[
            Cue(0, drive.move(Sawmill.crank, until=lines.spoken('gira este eixo')),
                mill.move(Sawmill.crank, until=lines.spoken('gira este eixo')),
                ghost.move(Sawmill.crank, until=lines.spoken('gira este eixo'))),
            Cue(lines.spoken('sob a roda'), drive.highlight(Mill.water_drive.waterwheel, others='keep'),
                until=lines.spoken('este eixo', plus=-0.12)),
            Cue(lines.spoken('este eixo'), drive.highlight(Mill.water_drive.crankshaft, others='keep'),
                until=lines.spoken('Uma manivela', plus=-0.2)),
            Cue(0, limits.show(), until=lines.spoken('Uma manivela')),
        ])
    # This real shot is the source revealed later. Add the synchronized context
    # plate in the document finishing pass; its camera duplicates this view.
    crank = CrankStroke.shot
    feed_motion = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: feed, Mechanism.note: limits},
        until=lines.spoken('Esse pequeno passo'), model=Sawmill.run(432, 440), cues=[
            Cue(0, feed.move(Sawmill.pawls, until=lines.spoken('Durante o corte')),
                ghost.move(Sawmill.pawls, until=lines.spoken('Durante o corte'))),
            Cue(lines.spoken('esta alavanca comprida'), feed.highlight(Mill.feed.rocker, others='keep'),
                until=lines.spoken('puxa uma lingueta', plus=-0.12)),
            Cue(lines.spoken('puxa uma lingueta'), feed.highlight(Mill.feed.pawl, others='keep'),
                until=lines.spoken('um dente', plus=-0.12)),
            Cue(lines.spoken('um dente'), feed.highlight(Mill.feed.feed_drum, others='keep'),
                until=lines.spoken('Uma segunda lingueta', plus=-0.25)),
            Cue(lines.spoken('Uma segunda lingueta'), feed.highlight(Mill.feed.holding_pawl, others='keep'),
                until=lines.spoken('enquanto a primeira retorna')),
            Cue(lines.spoken('enquanto a primeira retorna'), feed.highlight(Mill.feed.pawl, others='keep'),
                until=lines.spoken_end('enquanto a primeira retorna')),
            Cue(0, limits.show(), until=lines.spoken('Esse pequeno passo')),
        ])
    transmission = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken('A segunda corda'), model=Sawmill.run(440, 452), cues=[
            Cue(lines.spoken('enrola uma corda nesse eixo'), ropes.highlight(Mill.feed.winding, others='keep'),
                until=lines.spoken('Siga a corda', plus=-0.25)),
            Cue(lines.spoken('Siga a corda'), ropes.move(Sawmill.ropes, until=lines.spoken('Ela gira')),
                ghost.move(Sawmill.ropes, until=lines.spoken('Ela gira'))),
            Cue(lines.spoken('para baixo e para o outro lado'), ropes.highlight(Mill.feed.drive_line, others='keep'),
                until=lines.spoken('Ela gira', plus=-0.1)),
            Cue(lines.spoken('Ela gira'), ropes.move(Sawmill.drum, until=lines.spoken('um tambor largo')),
                ghost.move(Sawmill.drum, until=lines.spoken('um tambor largo'))),
            Cue(lines.spoken('um eixo composto'), ropes.highlight(Mill.feed.reduction_shaft, others='keep'),
                until=lines.spoken('um tambor largo', plus=-0.1)),
            Cue(lines.spoken('um tambor largo'), ropes.highlight(Mill.feed.reserve, others='keep'),
                until=lines.spoken('enquanto uma seção mais fina', plus=-0.12)),
            Cue(lines.spoken('enquanto uma seção mais fina'), ropes.highlight(Mill.feed.takeup, others='keep'),
                until=lines.spoken('A segunda corda', plus=-0.25)),
            Cue(0, limits.show(), until=lines.spoken('A segunda corda')),
        ])
    consequence = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken('Uma roda, duas tarefas'), model=Sawmill.run(452, 460), cues=[
            Cue(0, ropes.move(Sawmill.carriage, until=lines.spoken('em direção à lâmina')),
                ghost.move(Sawmill.carriage, until=lines.spoken('em direção à lâmina'))),
            Cue(lines.spoken('A segunda corda'),
                ropes.highlight(Mill.feed.takeup, Mill.feed.haul_span, Mill.feed.haul, others='keep'),
                until=lines.spoken('puxa a tora', plus=-0.1)),
            Cue(lines.spoken('puxa a tora'), ropes.highlight(Mill.carriage.timber, others='keep'),
                until=lines.spoken('em direção à lâmina')),
            Cue(0, limits.show(), until=lines.spoken('Uma roda, duas tarefas')),
        ])
    two_jobs = Shot(Exhibition, {Exhibition.stage: mill}, until=lines.spoken('A reconstrução'),
        model=Sawmill.run(460, 464), cues=[Cue(0, mill.move(Sawmill.wide, until=lines.spoken('A reconstrução')))])
    document = Shot(Archive, {Archive.picture: drawing, Archive.note: drawing_source},
        until=lines.spoken('usando a linguagem Python'), model=Sawmill.run(464, 470), transition=Dissolve(0.4), cues=[
            Cue(0, drawing.show(view=[(0, (0.51, 0.26), 1.75),
                (lines.spoken('usando a linguagem Python'), (0.5, 0.35), 1.0, 'out')]),
                drawing_source.show(enter=0.3, leave=0.2), until=lines.spoken('usando a linguagem Python'))])
    python_language = Shot(Exhibition, {Exhibition.graphic: python},
        until=lines.spoken('From Machinome'), model=Sawmill.run(470, 472), transition=Dissolve(0.35))
    face_reveal = Shot(Workbench, {Workbench.stage: mill, Workbench.imports: imports,
                                  Workbench.code: assembly, Workbench.surface: studio_ui},
        until=lines.spoken('Você também pode criar modelos', plus=1.2), model=Sawmill.run(472, 480), transition=Dissolve(0.4), cues=[
            Cue(0, mill.move(Sawmill.source, until=lines.spoken('Este é o Machinome, o framework')),
                imports.type(through_line=7, over=2.7)),
            Cue(lines.spoken('Este é o Machinome, o framework'), assembly.write(),
                until=lines.spoken('Este é o Machinome, o framework', plus=2.7)),
            Cue(lines.spoken('Este é o Machinome, o framework', plus=2.7), assembly.complete(),
                until=lines.spoken('Você também pode criar modelos', plus=1.2)),
            Cue(lines.spoken('Você também pode criar modelos'), studio_ui.reveal(),
                until=lines.spoken('Você também pode criar modelos', plus=1.2)),
            *relation_blinks(assembly),
        ])
    studio = Shot(Studio, {Studio.surface: studio_ui, Studio.stage: mill},
        until=lines.spoken('O Machinome também oferece'), model=Sawmill.run(480, 488), cues=[
            Cue(0, studio_ui.arrive(), until=2.8),
            Cue(2.8, studio_ui.settled(), until=lines.spoken('O Machinome também oferece')),
            Cue(lines.spoken('conversa com seus agentes'), studio_ui.focus(area='chat'),
                studio_ui.type_prompt(), until=lines.spoken('vê o código-fonte')),
            Cue(lines.spoken('vê o código-fonte'), studio_ui.prompt_complete(),
                until=lines.spoken('O Machinome também oferece')),
            Cue(lines.spoken('vê o código-fonte'), studio_ui.focus(area='code'),
                until=lines.spoken_end('vê o código-fonte')),
            Cue(lines.spoken('constrói o projeto'), studio_ui.focus(area='build'),
                until=lines.spoken_end('constrói o projeto')),
            Cue(lines.spoken('interage com o modelo'), studio_ui.focus(area='model'),
                until=lines.spoken('e momentos')),
            # The finishing pass samples the shortest spherical turn so the
            # camera cannot cut through the machine on a straight chord.
            Cue(lines.spoken('interage com o modelo', plus=0.35),
                mill.move(Sawmill.test, until=lines.spoken_end('diferentes ângulos'))),
            Cue(lines.spoken('e momentos'), studio_ui.focus(area='timeline'),
                until=lines.spoken_end('momentos da animação')),
        ])
    testing = Shot(TestBench, {TestBench.stage: mill, TestBench.detail: test_view,
                               TestBench.surface: studio_ui, TestBench.code: tests,
                               TestBench.note: test_note},
        until=lines.spoken("O código-fonte deste vídeo"), model=Sawmill.run(0, 4),
        cues=[
            Cue(0, studio_ui.settled(), studio_ui.prompt_complete(),
                until=lines.spoken("O código-fonte deste vídeo")),
            Cue(0, studio_ui.depart(), until=2.75),
            Cue(2.75, studio_ui.departed(),
                until=lines.spoken("O código-fonte deste vídeo")),
            # Type on the left during the final half-second of model travel.
            # No source panel participates in the outgoing browser fade.
            Cue(0, tests.conceal(), until=2.25),
            Cue(2.25, tests.write(),
                until=lines.spoken('Este teste verifica')),
            Cue(lines.spoken('Este teste verifica'), tests.complete(), until=lines.spoken("O código-fonte deste vídeo")),
            Cue(lines.spoken('Este teste verifica'), tests.blink(token='test_blade_clears_both_log_halves', line=606, occurrence=0),
                until=lines.spoken_end('Este teste verifica')),
            Cue(lines.spoken('a lâmina não'), test_view.highlight(Mill.saw.sash.blade, others='keep'),
                tests.blink(token='blade', line=608, occurrence=0), until=lines.spoken('intersecta')),
            Cue(lines.spoken('intersecta'), tests.blink(token='assertNotIntersecting', line=607, occurrence=0),
                until=lines.spoken_end('intersecta')),
            Cue(lines.spoken('nenhuma das duas metades'), tests.blink(token='log_left', line=608, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_left, others='keep'), until=lines.spoken_end('nenhuma das duas metades')),
            Cue(lines.spoken('da tora'), tests.blink(token='log_right', line=611, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_right, others='keep'), until=lines.spoken_end('da tora')),
            Cue(lines.spoken('Testing steps'), tests.blink(token='testing_steps', line=605, occurrence=0),
                until=lines.spoken_end('Testing steps')),
            Cue(lines.spoken('treze'), tests.blink(token='13', line=605, occurrence=0),
                until=lines.spoken_end('treze')),
            Cue(lines.spoken('zero a quatro segundos'), tests.blink(token='end=4', line=605, occurrence=0),
                until=lines.spoken_end('zero a quatro segundos')),
            Cue(lines.spoken('Testing steps'), test_note.show(), until=lines.spoken("O código-fonte deste vídeo")),
        ])
    behind_the_film = Shot(SourceRoom, {SourceRoom.code: film_code},
        until=lines.spoken("E aqui está o código"), model=Sawmill.run(480, 484), transition=Dissolve(0.9),
        cues=[Cue(0, film_code.write(), until=2),
              Cue(2, film_code.complete(), until=lines.spoken("E aqui está o código")),
              *source_cues(film_code, 'CrankStroke', [
                ('Narration, Camera', 'narration =', 'narration'),
                ('Camera, Shot', 'view = View', 'camera'),
                ('Shot. As Cues', 'shot =', 'Shot'),
                ('Cues movem', None, 'Cue'),
                ('movem a câmera', 'Cue(0,', 'move'),
                ('destacam a serra', None, 'highlight'),
            ]),
              Cue(lines.spoken('palavras faladas'),
                  *cue_blinks(film_code, 'CrankStroke', 'spoken'),
                  until=lines.spoken_end('palavras faladas'))])
    mirror = ThisScene.shot
    open_source = Shot(Exhibition, {Exhibition.graphic: ecosystem},
        until=HANDOFF, model=Sawmill.run(488, 492), transition=Dissolve(0.4), cues=[
            Cue(0, ecosystem.hub(), until=HANDOFF),
            Cue(0, ecosystem.approach(), until=lines.spoken('OpenSCAD')),
            *technology_cues(ecosystem),
            Cue(lines.spoken('Trimesh', plus=-0.85), ecosystem.drive(), until=HANDOFF),  # Shared clock; stream waits for beneath.
        ])
    wheel_returns = Shot(Exhibition, {Exhibition.stage: returned, Exhibition.veil: wheel_exit},
        until=lines.spoken_end('as suas'),
        model=Sawmill.run(492, 496), transition=Dissolve(1.25), cues=[
            Cue(lines.spoken('e os humanos constroem'),
                returned.move(Sawmill.hub, until=lines.spoken_end('as suas'), ease='linear')),
            Cue(lines.spoken_end('as suas', plus=-0.5), wheel_exit.darken(),
                until=lines.spoken_end('as suas')),
        ])
    invitation = Shot(Exhibition, {Exhibition.graphic: signature}, until=lines.end(plus=2.5),
        model=Sawmill.run(496, 504), fade_out=FadeOut(0.7), cues=[
            Cue(0, signature.wait(), until=lines.spoken("Eu sou Machinome")),
            Cue(lines.spoken("Eu sou Machinome"), signature.approach(),
                until=lines.spoken("Eu sou Machinome", plus=1.2)),
            Cue(lines.spoken('máquinas sejam de código aberto'), signature.link(), until=lines.spoken_end('máquinas sejam de código aberto')),
            Cue(lines.spoken_end('máquinas sejam de código aberto'), signature.linked(), until=lines.end(plus=2.5))])


class Revoluções(Movie):
    title = 'Revoluções'
    status = 'pt-br-render'
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
    doc = evaluate(Revoluções, name='machinome-release-5-pt-br', out=output)
    doc['chapters'][0]['speechOffset'] = 3.0
    write(doc, output)
    print(output)
