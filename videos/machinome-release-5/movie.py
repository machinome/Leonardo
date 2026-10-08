"""Revolutions — fifth cut, live preview."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path

from machinome_movie import (
    Action, Camera, Chapter, Credits, Cue, Dissolve, Element, Evidence,
    FadeIn, FadeOut, Format, Layer, Loop, Movie, Narrator, Picture,
    Reframe, Release, Set, Shot, Slot, Source, Still, Style, Title, View, evaluate, write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill
from narration import AUDIO, lines
from scene_source import excerpt, model_excerpt, token_line

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent / 'machinome-release-3/assets'
RETURN = 'The wheel... makes revolutions... and humans... build'
HANDOFF = 'And beneath it all'


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
    approach = Action()
    reveal = Action(name=str)
    drive = Action()


class Signature(Element):
    module = 'stage.jsx'
    enter = Action()


class Curtain(Element):
    module = 'stage.jsx'
    darken = Action()


class Sawmill(Loop):
    model = Mill
    export = '../machinome-release-3/_build/model'
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
        "A crank and connecting rod turn that rotation "
        "into the saw's up-and-down stroke."
    )
    view = View(Sawmill, camera=Sawmill.rear,
                hide=[Sawmill.drive_context])
    stroke = lines.spoken("the saw's up-and-down stroke")
    end = lines.spoken("But the timber")
    shot = Shot(
        Mechanism, {Mechanism.stage: view},
        until=end, model=Sawmill.run(424, 432),
        cues=[
            Cue(0, view.move(Sawmill.saw, until=stroke)),
            Cue(lines.spoken("A crank"),
                view.highlight(Mill.water_drive.crank, others="keep"),
                until=lines.spoken("connecting rod", plus=-0.12)),
            Cue(lines.spoken("connecting rod"),
                view.highlight(Mill.saw.connecting_rod, others="keep"),
                until=lines.spoken("turn that rotation", plus=-0.1)),
            Cue(stroke, view.highlight(Mill.saw.sash, others="keep"),
                until=lines.spoken("But the timber", plus=-0.2)),
        ])


def source_cues(element, scene, entries):
    return [Cue(lines.spoken(phrase),
                element.blink(token=token, line=token_line(scene, row, token), occurrence=0),
                until=lines.spoken_end(phrase))
            for phrase, row, token in entries]


class ThisScene:
    narration = "And here's the code of this exact scene! How cool is that?"
    code = Listing(**excerpt("ThisScene"))
    end = lines.spoken("And the best part")

    shot = Shot(
        SourceRoom, {SourceRoom.code: code},
        until=end, model=Sawmill.run(484, 488),
        cues=source_cues(code, 'ThisScene', [
                ("And here's", 'narration =', 'narration'),
                ("code of this exact", 'code = Listing', 'code'),
                ("this exact scene", 'class ThisScene', 'ThisScene'),
                ("How cool is that", 'narration =', 'How cool is that?'),
            ]),
    )


def technology_cues(element):
    return [Cue(lines.spoken(name), element.reveal(name=name), until=lines.spoken(HANDOFF))
            for name in ['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh']]


def relation_blinks(element):
    # This take's crankshaft interval is only 10 ms, immediately before the
    # next shot. Give it one preceding frame; do not invent audio timestamps.
    return [Cue(lines.spoken(word, plus=-1/24 if word == 'crankshaft' else 0),
                element.blink(token=word, line=416, occurrence=0),
                until=lines.spoken_end(word))
            for word in ['waterwheel', 'spin', 'drives', 'crankshaft']]


class Continuous(Chapter):
    performance = lines
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    ghost = View(Sawmill, camera=Sawmill.rear)
    drive = CrankStroke.view
    feed = View(Sawmill, camera=Sawmill.saw, hide=[Sawmill.feed_context])
    ropes = View(Sawmill, camera=Sawmill.pawls, hide=[Sawmill.rope_context])
    returned = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    wheel_exit = Curtain()
    identity = Title('Hydraulic sawmill', subtitle='LEONARDO DA VINCI')
    limits = Title('Reconstructed motion · forces and cutting not simulated')
    drawing = Picture(Sawmill.drawing, fit='cover')
    drawing_source = Title('Source: Codex Atlanticus · 1078r')
    python = Signature(svg=(HERE.parent / 'machinome-release-2/assets/python-logo.svg').read_text(),
                       tagline='Python', url='', question='', compact=True)
    imports = Source.panel(Sawmill.imports)
    assembly = Listing(**model_excerpt('models/hydraulic_sawmill/model.py', [(401, 417)]))
    tests = Listing(**model_excerpt('models/hydraulic_sawmill/test_model.py',
                                   [(8, 8), (25, 27), (604, 612)]))
    test_view = View(Sawmill, camera=Sawmill.test, hide=[Sawmill.test_context])
    test_note = Title('13 sampled positions · 0–4 seconds')
    film_code = Listing(**excerpt('CrankStroke'))
    mirror_code = ThisScene.code
    ecosystem = Constellation(
        names=['OpenSCAD', 'SolidPython', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD', 'OCCT', 'Trimesh'],
        drivers=['Three.js', 'NumPy', 'SciPy', 'Manifold', 'FastAPI', 'React', 'OpenSpec'],
        spacing=310.0, mark=(BRAND / 'mark-orange.svg').read_text(),
        title='OPEN SOURCE', arrival=1.65, stagger=0.45, streamDuration=5.8,
        angularAcceleration=7.0, entrySpeedFraction=0.65, timeOffset=0.0, fadeDuration=0.0,
    )
    signature = Signature(svg=(BRAND / 'wordmark-orange.svg').read_text(),
                          tagline='Source code for machines.',
                          url='https://github.com/machinome/machinome/',
                          question='', compact=False)

    revolution = Shot(Exhibition, {Exhibition.stage: wheel},
        until=lines.spoken('Five centuries'), fade_in=FadeIn(0.5),
        model=Sawmill.run(400, 404))
    # Keep the wheel as an opaque base while the full machine fades over it.
    # Reframe draws this live; a composed dissolve is a cut in the player.
    ancestor = Shot(Exhibition, {Exhibition.backdrop: wheel, Exhibition.stage: mill,
                                Exhibition.heading: identity},
        until=lines.spoken('Water beneath'), transition=Reframe(1.2),
        model=Sawmill.run(404, 424), cues=[
            Cue(0, identity.show(enter=0.6, leave=0.6), until=lines.spoken('I am a machine')),
            # finish.mjs samples one continuous orbit on the measured take.
            Cue(lines.spoken('designed'), mill.move(Sawmill.rear, until=lines.spoken('Water beneath'))),
        ])
    water = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: drive, Mechanism.note: limits},
        until=lines.spoken('A crank'), model=Sawmill.run(424, 428), cues=[
            Cue(0, drive.move(Sawmill.crank, until=lines.spoken('turns this shaft')),
                ghost.move(Sawmill.crank, until=lines.spoken('turns this shaft'))),
            Cue(lines.spoken('the wheel turns'), drive.highlight(Mill.water_drive.waterwheel, others='keep'),
                until=lines.spoken('this shaft', plus=-0.12)),
            Cue(lines.spoken('this shaft'), drive.highlight(Mill.water_drive.crankshaft, others='keep'),
                until=lines.spoken('A crank', plus=-0.2)),
            Cue(0, limits.show(), until=lines.spoken('A crank')),
        ])
    # This real shot is the source revealed later. Add the synchronized context
    # plate in the document finishing pass; its camera duplicates this view.
    crank = CrankStroke.shot
    feed_motion = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: feed, Mechanism.note: limits},
        until=lines.spoken('That small step'), model=Sawmill.run(432, 440), cues=[
            Cue(0, feed.move(Sawmill.pawls, until=lines.spoken('On the cutting stroke')),
                ghost.move(Sawmill.pawls, until=lines.spoken('On the cutting stroke'))),
            Cue(lines.spoken('this long lever'), feed.highlight(Mill.feed.rocker, others='keep'),
                until=lines.spoken('pulls a pawl', plus=-0.12)),
            Cue(lines.spoken('pulls a pawl'), feed.highlight(Mill.feed.pawl, others='keep'),
                until=lines.spoken('one tooth', plus=-0.12)),
            Cue(lines.spoken('one tooth'), feed.highlight(Mill.feed.feed_drum, others='keep'),
                until=lines.spoken('A second pawl', plus=-0.25)),
            Cue(lines.spoken('A second pawl'), feed.highlight(Mill.feed.holding_pawl, others='keep'),
                until=lines.spoken('while the first returns')),
            Cue(lines.spoken('while the first returns'), feed.highlight(Mill.feed.pawl, others='keep'),
                until=lines.spoken_end('while the first returns')),
            Cue(0, limits.show(), until=lines.spoken('That small step')),
        ])
    transmission = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken('The second rope'), model=Sawmill.run(440, 452), cues=[
            Cue(lines.spoken('winds a rope'), ropes.highlight(Mill.feed.winding, others='keep'),
                until=lines.spoken('Follow it', plus=-0.25)),
            Cue(lines.spoken('Follow it'), ropes.move(Sawmill.ropes, until=lines.spoken('It turns')),
                ghost.move(Sawmill.ropes, until=lines.spoken('It turns'))),
            Cue(lines.spoken('down, and across'), ropes.highlight(Mill.feed.drive_line, others='keep'),
                until=lines.spoken('It turns', plus=-0.1)),
            Cue(lines.spoken('It turns'), ropes.move(Sawmill.drum, until=lines.spoken('a broad drum')),
                ghost.move(Sawmill.drum, until=lines.spoken('a broad drum'))),
            Cue(lines.spoken('a compound shaft'), ropes.highlight(Mill.feed.reduction_shaft, others='keep'),
                until=lines.spoken('a broad drum', plus=-0.1)),
            Cue(lines.spoken('a broad drum'), ropes.highlight(Mill.feed.reserve, others='keep'),
                until=lines.spoken('while a thinner', plus=-0.12)),
            Cue(lines.spoken('while a thinner'), ropes.highlight(Mill.feed.takeup, others='keep'),
                until=lines.spoken('The second rope', plus=-0.25)),
            Cue(0, limits.show(), until=lines.spoken('The second rope')),
        ])
    consequence = Shot(Mechanism, {Mechanism.ghost: ghost, Mechanism.stage: ropes, Mechanism.note: limits},
        until=lines.spoken('One wheel'), model=Sawmill.run(452, 460), cues=[
            Cue(0, ropes.move(Sawmill.carriage, until=lines.spoken('towards the blade')),
                ghost.move(Sawmill.carriage, until=lines.spoken('towards the blade'))),
            Cue(lines.spoken('The second rope'), ropes.highlight(Mill.feed.haul_span, others='keep'),
                until=lines.spoken('draws the timber', plus=-0.1)),
            Cue(lines.spoken('draws the timber'), ropes.highlight(Mill.carriage.timber, others='keep'),
                until=lines.spoken('towards the blade')),
            Cue(0, limits.show(), until=lines.spoken('One wheel')),
        ])
    two_jobs = Shot(Exhibition, {Exhibition.stage: mill}, until=lines.spoken('To reconstruct'),
        model=Sawmill.run(460, 464), cues=[Cue(0, mill.move(Sawmill.wide, until=lines.spoken('To reconstruct')))])
    document = Shot(Archive, {Archive.picture: drawing, Archive.note: drawing_source},
        until=lines.spoken('and used the Python'), model=Sawmill.run(464, 470), transition=Dissolve(0.4), cues=[
            Cue(0, drawing.show(view=[(0, (0.51, 0.26), 1.75),
                (lines.spoken('and used the Python'), (0.5, 0.35), 1.0, 'out')]),
                drawing_source.show(enter=0.3, leave=0.2), until=lines.spoken('and used the Python'))])
    python_language = Shot(Exhibition, {Exhibition.graphic: python},
        until=lines.spoken('From Machinome'), model=Sawmill.run(470, 472), transition=Dissolve(0.35))
    face_reveal = Shot(Workbench, {Workbench.stage: mill, Workbench.imports: imports, Workbench.code: assembly},
        until=lines.spoken('With Machinome'), model=Sawmill.run(472, 480), transition=Dissolve(0.4), cues=[
            Cue(0, mill.move(Sawmill.source, until=lines.spoken('This is Machinome')),
                imports.type(through_line=7, over=2.7)),
            Cue(lines.spoken('This is Machinome'), assembly.write(),
                until=lines.spoken('This is Machinome', plus=2.7)),
            Cue(lines.spoken('This is Machinome', plus=2.7), assembly.complete(),
                until=lines.spoken('With Machinome')),
            *relation_blinks(assembly),
        ])
    testing = Shot(TestBench, {TestBench.stage: test_view, TestBench.code: tests,
                               TestBench.note: test_note},
        until=lines.spoken("This video's source code"), model=Sawmill.run(0, 4),
        transition=Dissolve(1.8), cues=[
            Cue(lines.spoken('This test checks'), tests.blink(token='test_blade_clears_both_log_halves', line=606, occurrence=0),
                until=lines.spoken_end('This test checks')),
            Cue(lines.spoken('the blade does not'), test_view.highlight(Mill.saw.sash.blade, others='keep'),
                tests.blink(token='blade', line=608, occurrence=0), until=lines.spoken('intersect')),
            Cue(lines.spoken('intersect'), tests.blink(token='assertNotIntersecting', line=607, occurrence=0),
                until=lines.spoken_end('intersect')),
            Cue(lines.spoken('either half'), tests.blink(token='log_left', line=608, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_left, others='keep'), until=lines.spoken_end('either half')),
            Cue(lines.spoken('of the timber'), tests.blink(token='log_right', line=611, occurrence=0),
                test_view.highlight(Mill.carriage.timber.log_right, others='keep'), until=lines.spoken_end('of the timber')),
            Cue(lines.spoken('Testing steps'), tests.blink(token='testing_steps', line=605, occurrence=0),
                until=lines.spoken_end('Testing steps')),
            Cue(lines.spoken('thirteen'), tests.blink(token='13', line=605, occurrence=0),
                until=lines.spoken_end('thirteen')),
            Cue(lines.spoken('zero to four seconds'), tests.blink(token='end=4', line=605, occurrence=0),
                until=lines.spoken_end('zero to four seconds')),
            Cue(lines.spoken('Testing steps'), test_note.show(), until=lines.spoken("This video's source code")),
        ])
    behind_the_film = Shot(SourceRoom, {SourceRoom.code: film_code},
        until=lines.spoken("And here's the code"), model=Sawmill.run(480, 484), transition=Dissolve(0.9),
        cues=source_cues(film_code, 'CrankStroke', [
                ('narration, a camera', 'narration =', 'narration'),
                ('camera, a shot', 'view = View', 'camera'),
                ('shot. Cues', 'shot =', 'shot'),
                ('Cues move', 'cues=[', 'cues'),
                ('move the camera', 'Cue(0,', 'move'),
                ('highlight the saw', 'Cue(stroke,', 'highlight'),
                ('spoken words', 'stroke =', 'spoken'),
            ]))
    mirror = ThisScene.shot
    open_source = Shot(Exhibition, {Exhibition.graphic: ecosystem},
        until=lines.spoken(HANDOFF), model=Sawmill.run(488, 492), transition=Dissolve(0.4), cues=[
            Cue(0, ecosystem.hub(), until=lines.spoken(HANDOFF)),
            Cue(0, ecosystem.approach(), until=lines.spoken('OpenSCAD')),
            *technology_cues(ecosystem),
            Cue(lines.spoken('Trimesh'), ecosystem.drive(), until=lines.spoken(HANDOFF)),
        ])
    wheel_returns = Shot(Exhibition, {Exhibition.stage: returned, Exhibition.veil: wheel_exit},
        until=lines.spoken_end('their own'),
        model=Sawmill.run(492, 496), transition=Dissolve(1.25), cues=[
            Cue(lines.spoken('and humans...'),
                returned.move(Sawmill.hub, until=lines.spoken_end('their own'), ease='linear')),
            Cue(lines.spoken_end('their own', plus=-0.5), wheel_exit.darken(),
                until=lines.spoken_end('their own')),
        ])
    invitation = Shot(Exhibition, {Exhibition.graphic: signature}, until=lines.end(plus=2.5),
        model=Sawmill.run(496, 504), fade_out=FadeOut(0.7), cues=[
            Cue(0, signature.enter(), until=0.8)])


class Revolutions(Movie):
    title = 'Revolutions'
    status = 'preview-5'
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
    doc = evaluate(Revolutions, name='machinome-release-5', out=output)
    doc['chapters'][0]['speechOffset'] = 3.0
    write(doc, output)
    print(output)
