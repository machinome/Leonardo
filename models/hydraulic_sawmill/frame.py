"""The fixed timbers fitted together as separate physical parts."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq
from machinome.node import AssemblyNode, CadQueryNode
from machinome.parameters import Count
from machinome.simulation import Driver, Instruction
from .carpentry import MEMBERS, PEGS
from .erection import STAGES, displacement, peg_displacement
from .parts import Foundation


def feature_shape(feature):
    if feature[0] == 'box':
        _, size, centre = feature
        return cq.Workplane('XY').box(*size).translate(centre)
    _, radius, length, centre, axis = feature
    shape = cq.Workplane('XY').circle(radius).extrude(length/2, both=True)
    if axis == 'x':
        shape = shape.rotate((0, 0, 0), (0, 1, 0), 90)
    elif axis == 'y':
        shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)
    return shape.translate(centre)


class CutTimber(CadQueryNode):
    member = Count()
    color = '#AD7D48'

    def render(self):
        spec = MEMBERS[self.member]
        shape = feature_shape(('box', spec.stock, spec.centre))
        for feature in spec.additions:
            shape = shape.union(feature_shape(feature))
        for feature in spec.cuts:
            shape = shape.cut(feature_shape(feature))
        return shape


class HardwoodPeg(CadQueryNode):
    peg = Count()
    color = '#69492F'
    linear_deflection = 0.02

    def render(self):
        spec = PEGS[self.peg]
        shape = feature_shape(('bore', spec.radius, spec.length, spec.centre, spec.axis))
        if spec.axis == 'z':
            # Whittled headed pin: gravity retention without assumed friction.
            x, y, z = spec.centre
            top = z+spec.length/2
            shape = shape.union(feature_shape(('bore', spec.radius, 0.4, (x,y,top), 'z')))
            shape = shape.union(feature_shape(('bore', spec.radius+1, 2, (x,y,top+1.1), 'z')))
        return shape


class TimberBed(AssemblyNode):
    timbers = [CutTimber(member=i, name=f'{s.code} · {s.label}')
               for i, s in enumerate(MEMBERS) if s.group == 'bed']


class FixedSawTower(AssemblyNode):
    timbers = [CutTimber(member=i, name=f'{s.code} · {s.label}')
               for i, s in enumerate(MEMBERS) if s.group == 'tower' and s.code != 'A2']
    inner_bearing = CutTimber(member=next(i for i,s in enumerate(MEMBERS) if s.code == 'A2'),
                              name='A2 · Inner wooden bearing')


class TimberStand(AssemblyNode):
    bed = TimberBed(name='Horizontal bed frame')
    saw_tower = FixedSawTower(name='Fixed saw tower and shaft seats')
    pegs = [HardwoodPeg(peg=i, name=f'{s.code} · Peg {s.members[0]} / {s.members[1]}')
            for i, s in enumerate(PEGS)]


class Frame(AssemblyNode):
    foundation = Foundation(name='Foundation')
    timber_structure = TimberStand(name='Fixed timber structure')


class FrameCarpentry(AssemblyNode):
    """The working frame, reversibly separated in a carpenter's order."""
    disassembly = Driver(default=0, range=(0, 11), unit='stage')
    frame = Frame(name='Buildable sawmill frame')
    instructions = {f'{i:02d} · {label}': Instruction({'disassembly': i}, duration=2)
                    for i, label in enumerate(STAGES)}

    def simulate(self):
        stand = self.frame.timber_structure
        timbers = [*stand.bed.timbers, *stand.saw_tower.timbers, stand.saw_tower.inner_bearing]
        for node in timbers:
            node.translate(displacement(MEMBERS[node.member].code, self.disassembly))
        for node in stand.pegs:
            node.translate(peg_displacement(PEGS[node.peg], self.disassembly))
