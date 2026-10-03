"""Revolutions — the ratified second cut, one voice and one machine."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path

from machinome_movie import (
    Action, Camera, Chapter, Credits, Cue, Dissolve, Element, Evidence,
    FadeIn, FadeOut, Format, Layer, Loop, Movie, Narrator, Picture,
    Release, Set, Shot, Slot, Source, Still, Style, Title, View, evaluate, write,
)
from models.hydraulic_sawmill.model import LeonardoHydraulicSawmill as Mill
from narration import AUDIO, lines
from scene_source import excerpt

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent / 'machinome-release-1/assets'
RETURN = 'The wheel makes revolutions, and humans build'


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


class Listing(Element):
    module = 'stage.jsx'
    focus = Action(token=str)


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
    export = '../../export/hydraulic_sawmill'
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
    not_wheel = Layer(Mill.frame, Mill.saw, Mill.carriage, Mill.feed,
                      Mill.water_drive.channel, Mill.water_drive.water,
                      Mill.water_drive.crankshaft, Mill.water_drive.crank,
                      Mill.water_drive.crank_retainer)
    drive_context = Layer(Mill.frame, Mill.carriage, Mill.feed)
    feed_context = Layer(Mill.frame, Mill.water_drive, Mill.carriage)
    rope_context = Layer(Mill.frame, Mill.water_drive, Mill.saw, Mill.feed.feed_drum)
    imports = Source('../../models/hydraulic_sawmill/model.py', lines=(7, 7))
    assembly = Source('../../models/hydraulic_sawmill/model.py', lines=(400, 416))
    drawing = Still('../../_reference/hydraulic_sawmill/atlanticus-1078r.jpg',
                    credit='Leonardo da Vinci, Codex Atlanticus 1078r; scan: e-Leo, Biblioteca Leonardiana.',
                    rights=None, upscale=1.5)
    museum = Still('../../_reference/hydraulic_sawmill/milan-overall.jpg',
                   credit='Museo Nazionale Scienza e Tecnologia Leonardo da Vinci, Milan: hydraulic saw IGB-37.',
                   rights=None, upscale=1.5)


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


class ThisScene:
    narration = "And here's the code of this exact scene! How cool is that?"
    code = Listing(**excerpt("ThisScene"))
    end = lines.spoken("And the best part")

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
            for name in ['OpenSCAD', 'SolidPython', 'OCCT', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD']]


class Continuous(Chapter):
    performance = lines
    wheel = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    mill = View(Sawmill, camera=Sawmill.wheel)
    ghost = View(Sawmill, camera=Sawmill.rear)
    drive = CrankStroke.view
    feed = View(Sawmill, camera=Sawmill.saw, hide=[Sawmill.feed_context])
    ropes = View(Sawmill, camera=Sawmill.pawls, hide=[Sawmill.rope_context])
    returned = View(Sawmill, camera=Sawmill.wheel, hide=[Sawmill.not_wheel])
    identity = Title('Hydraulic sawmill', subtitle='LEONARDO DA VINCI')
    disclosure = Title('AI content')
    limits = Title('Reconstructed motion · forces and cutting not simulated')
    drawing = Picture(Sawmill.drawing, fit='cover')
    museum = Picture(Sawmill.museum, fit='contain')
    drawing_source = Title('Codex Atlanticus · 1078r', subtitle='Source: e-Leo · Biblioteca Leonardiana')
    museum_source = Title('Hydraulic saw · Milan · IGB-37', subtitle='Source: Museo Nazionale Scienza e Tecnologia')
    python = Signature(svg=(HERE / 'assets/python-logo.svg').read_text(),
                       tagline='Python', question='', compact=True)
    imports = Source.panel(Sawmill.imports)
    assembly = Source.panel(Sawmill.assembly)
    film_code = Listing(**excerpt('CrankStroke'))
    mirror_code = ThisScene.code
    ecosystem = Constellation(
        names=['Three.js', 'OpenSCAD', 'SolidPython', 'OCCT', 'CadQuery', 'Build123d', 'FreeCAD', 'JSCAD'],
        driver='OpenSpec', mark=(BRAND / 'mark-white.svg').read_text(),
        title='OPEN SOURCE', arrival=0.6, acceleration=1.5, rate=26.0,
    )
    signature = Signature(svg=(BRAND / 'wordmark-white.svg').read_text(),
                          tagline='Source code for machines.',
                          question='What do you want to build next?', compact=False)

    revolution = Shot(Exhibition, {Exhibition.stage: wheel, Exhibition.note: disclosure},
        until=lines.spoken('Five centuries'), fade_in=FadeIn(0.5),
        model=Sawmill.run(400, 404),
        cues=[Cue(0, disclosure.show(), until=lines.spoken('Five centuries'))])
    ancestor = Shot(Exhibition, {Exhibition.stage: mill, Exhibition.heading: identity},
        until=lines.spoken('Water beneath'), transition=Dissolve(1.2),
        model=Sawmill.run(404, 424), cues=[
            Cue(0, identity.show(enter=0.6, leave=0.6), until=lines.spoken('I am a machine')),
            Cue(lines.spoken('designed'), mill.move(Sawmill.wide, until=lines.spoken('I am a machine'))),
            Cue(lines.spoken('I am a machine'), mill.move(Sawmill.side, until=lines.spoken('Let me show'))),
            Cue(lines.spoken('Let me show'), mill.move(Sawmill.rear, until=lines.spoken('Water beneath'))),
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
        until=lines.spoken('museum pictures'), model=Sawmill.run(464, 468), transition=Dissolve(0.4), cues=[
            Cue(0, drawing.show(leave=0.2, view=[(0, (0.5, 0.28), 1.03),
                (lines.spoken('museum pictures'), (0.5, 0.27), 1.12)]),
                drawing_source.show(enter=0.3, leave=0.2), until=lines.spoken('museum pictures'))])
    photograph = Shot(Archive, {Archive.picture: museum, Archive.note: museum_source},
        until=lines.spoken('and used the Python'), model=Sawmill.run(468, 470), cues=[
            Cue(0, museum.show(enter=0.2, leave=0.2, view=[(0, (0.5, 0.5), 1.0),
                (lines.spoken('and used the Python'), (0.5, 0.5), 1.04)]),
                museum_source.show(enter=0.2, leave=0.2), until=lines.spoken('and used the Python'))])
    python_language = Shot(Exhibition, {Exhibition.graphic: python},
        until=lines.spoken('From Machinome'), model=Sawmill.run(470, 472), transition=Dissolve(0.35))
    face_reveal = Shot(Workbench, {Workbench.stage: mill, Workbench.imports: imports, Workbench.code: assembly},
        until=lines.spoken("This video's source code"), model=Sawmill.run(472, 480), transition=Dissolve(0.4), cues=[
            Cue(0, mill.move(Sawmill.source, until=lines.spoken('This is Machinome')),
                imports.type(through_line=7, over=2.7)),
            Cue(lines.spoken('This is Machinome'), assembly.type(through_line=416, over=2.7)),
            Cue(lines.spoken('The waterwheel spin drives the crankshaft'),
                assembly.emphasize('waterwheel', ('spin', 'water_drive.waterwheel.spin'),
                                  'drives', 'crankshaft', line=415, hold=0.8)),
        ])
    behind_the_film = Shot(SourceRoom, {SourceRoom.code: film_code},
        until=lines.spoken("And here's the code"), model=Sawmill.run(480, 484), transition=Dissolve(0.35), cues=[
            Cue(lines.spoken('A scene'), film_code.focus(token='shot = Shot('), until=lines.spoken('a camera')),
            Cue(lines.spoken('a camera'), film_code.focus(token='view = View('), until=lines.spoken('a voice')),
            Cue(lines.spoken('a voice'), film_code.focus(token='A crank and connecting rod'), until=lines.spoken('The words I say')),
            Cue(lines.spoken('The words I say'), film_code.focus(token='stroke = lines.spoken('), until=lines.spoken('tell the camera')),
            Cue(lines.spoken('tell the camera'), film_code.focus(token='view.move('), until=lines.spoken("And here's the code")),
        ])
    mirror = ThisScene.shot
    open_source = Shot(Exhibition, {Exhibition.graphic: ecosystem},
        until=lines.spoken(RETURN), model=Sawmill.run(488, 492), transition=Dissolve(0.4), cues=[
            Cue(0, ecosystem.hub(), until=lines.spoken(RETURN)),
            Cue(lines.spoken('all open source'), ecosystem.reveal(name='Three.js'), until=lines.spoken(RETURN)),
            *technology_cues(ecosystem),
            Cue(lines.spoken('and so many others'), ecosystem.drive(), until=lines.spoken(RETURN)),
        ])
    wheel_returns = Shot(Exhibition, {Exhibition.stage: returned}, until=lines.spoken("I'm Machinome"),
        model=Sawmill.run(492, 496), transition=Dissolve(1.25))
    invitation = Shot(Exhibition, {Exhibition.graphic: signature}, until=lines.end(plus=2.5),
        model=Sawmill.run(496, 504), transition=Dissolve(0.8), fade_out=FadeOut(0.7), cues=[
            Cue(lines.spoken('What do you want'), signature.enter(), until=lines.end(plus=2.5))])


class Revolutions(Movie):
    title = 'Revolutions'
    status = 'ratified-second-cut'
    learning_goal = 'Meet Machinome through an ancestor, its mechanism, its code and this film.'
    format = Format(1920, 1080, fps=24)
    narrator = Narrator(provider=AUDIO['provider'], model=AUDIO['model'], voice=AUDIO['voice'],
                        label=AUDIO['voiceLabel'], output=AUDIO['outputFormat'], settings=AUDIO['voiceSettings'])
    style = Style(background='#101419', foreground='#eeeae3', accent='#e9b778',
                  font='Space Grotesk, sans-serif', safe_inset=0.05)
    evidence = Evidence(brief='brief.md', review='review-1.md',
        reconstruction='../../models/hydraulic_sawmill/docs/reconstruction.md')
    credits = Credits(project='Leonardo da Vinci Gallery', creator='AI-directed release film',
        copyright='Copyright (C) 2026 Luis Henrique Cassis Fagundes', license='AGPL-3.0-only', license_file='../../LICENSE')
    release = Release(description='description.md')
    continuous = Continuous()


if __name__ == '__main__':
    output = HERE / '_build/movie.json'
    doc = evaluate(Revolutions, name='machinome-release-2', out=output)
    doc['chapters'][0]['speechOffset'] = 3.0
    write(doc, output)
    print(output)
