"""Original three-coordinate crane with an engaged screw and continuous hoist."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi, sin, cos, radians

import cadquery as cq
from molejo import Shape, Circle, Line, Arc, P
from solid_node.math import sqrt
from solid_node.node import AssemblyNode, CadQueryNode, MolejoNode
from solid_node.motion.joints import Prismatic, Revolute
from solid_node.motion.ports import TranslationalPort, RotationalPort
from solid_node.simulation import Driver, Instruction


def box(x, y, z, at):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    return cq.Workplane("XZ").circle(radius).extrude(length/2, both=True).translate(at)


def xshaft(radius, start, end, y=0, z=0):
    return cq.Workplane("YZ").circle(radius).extrude(end-start).translate((start, y, z))


def thread(start, length, clearance=0):
    """12 mm lead with explicit ruled stations, avoiding periodic BREP seams.

    Each 20-degree station has a polygonal square-thread section. Positive
    cutter clearance covers the small chord error between mating stations.
    This is deliberate original geometry, identical in STL and exact tests.
    """
    half_angle = radians(45+clearance*360/12)
    inner, outer = 3.7, 6+clearance
    steps = round(length/12*18)
    wires = []
    for step in range(steps+1):
        theta = step*2*pi/18
        angles = [-half_angle+i*half_angle/2 for i in range(5)]
        points = [(r*cos(a+theta), r*sin(a+theta), step*12/18)
                  for r, seq in ((outer, angles), (inner, angles[::-1])) for a in seq]
        wires.append(cq.Wire.makePolygon([cq.Vector(*p) for p in points], close=True))
    rib = cq.Workplane("XY").newObject([cq.Solid.makeLoft(wires, ruled=True)])
    return rib.rotate((0, 0, 0), (0, 1, 0), 90).translate((start, 0, 0))


def clipped(value):
    positive = (value+sqrt(value*value))/2
    extra = positive-1
    return positive-(extra+sqrt(extra*extra))/2


def demonstration(t):
    """Lift, swing/traverse, place, then visibly retrace; continuous loop."""
    up = clipped(t/.16)-clipped((t-.42)/.16)
    up += clipped((t-.58)/.16)-clipped((t-.90)/.10)
    across = clipped((t-.16)/.26)-clipped((t-.74)/.16)
    return -45+90*across, 60*across, 25*up


class Footing(CadQueryNode):
    color = "#655b4e"

    def render(self):
        base = cq.Workplane("XY").circle(62).extrude(10)
        collar = cq.Workplane("XY").circle(18).circle(12.35).extrude(40).translate((0, 0, 10))
        base = base.union(collar)
        for x in (-24, 24):
            base = base.union(box(5, 16, 54, (x, 0, 36)))
            base = base.union(box(16, 16, 12, (x*.8, 0, 15)))
        cap = cq.Workplane("XY").circle(27).circle(12.35).extrude(5.3).translate((0, 0, 56.7))
        return base.union(cap).cut(cq.Workplane("XY").circle(12.35).extrude(60).translate((0, 0, 10)))


class MastAndJib(CadQueryNode):
    color = "#94643d"

    def render(self):
        mast = cq.Workplane("XY").circle(12).extrude(230).translate((0, 0, 10.35))
        mast = mast.union(cq.Workplane("XY").circle(21).extrude(6).translate((0, 0, 50.35)))
        mast = mast.union(box(24, 24, 180, (0, 0, 153)))
        for y in (-18, 18):
            mast = mast.union(box(254, 10, 12, (110, y, 239)))
            mast = mast.union(xshaft(3, 36, 224, y, 260))
        for x in (0, 36, 224):
            brace = box(8, 50, 24, (x, 0, 254))
            if x:
                brace = brace.cut(xshaft(4.35, x-5, x+5, 0, 260))
            mast = mast.union(brace)
        for y in (-18, 18):
            brace = (cq.Workplane("XZ").polyline([(5, 175), (8, 175), (182, 238), (182, 244), (176, 244)])
                     .close().extrude(3, both=True).translate((0, y, 0)))
            mast = mast.union(brace)
        return mast


class LeadScrew(CadQueryNode):
    color = "#bda064"
    linear_deflection = 0.025
    angular_deflection = 0.2
    spin = Revolute(axis=(1, 0, 0))

    def render(self):
        screw = xshaft(4, 22, 232).union(thread(60, 108))
        for lo, hi in ((40.35, 44), (216, 219.65)):
            screw = screw.union(xshaft(7, lo, hi))
        wheel = cq.Workplane("YZ").circle(17).circle(13).extrude(3).translate((24, 0, 0))
        wheel = wheel.union(box(3, 33, 3, (25.5, 0, 0)))
        wheel = wheel.union(box(3, 3, 33, (25.5, 0, 0)))
        return screw.union(wheel)


class TrolleyCarrier(CadQueryNode):
    """Integral nut, guide sleeves and offset hoist journals."""
    color = "#577477"
    linear_deflection = 0.025
    angular_deflection = 0.2

    def render(self):
        body = box(24, 50, 18, (0, -3, 0))
        # Phase at world x=80 matches the screw starting at x=60.
        cutter = thread(-20, 48, .4)
        # Cut the helical pocket before the bore: the inverse order can
        # silently leave this pocket uncut in OCCT. Mesh fit tests guard it.
        body = body.cut(cutter).cut(xshaft(4.35, -13, 13))
        for y in (-18, 18):
            body = body.cut(xshaft(3.35, -13, 13, y))
        for y in (-42.4, -25.6):
            body = body.union(box(94, 4, 6, (28, y, -12)))
            body = body.union(box(12, 4, 32, (0, y, -5)))
            for x, z in ((24, -20), (68, -26)):
                body = body.union(box(8, 4, 22, (x, y, z+7)))
        body = body.union(axle(3, 21.4, (24, -34, -20)))
        body = body.union(axle(3, 21.4, (68, -34, -26)))
        socket = box(6, 21, 8, (-12, -34, -14))
        bore = cq.Workplane("XY").circle(1.3).extrude(6).translate((-12, -34, -18.1))
        return body.union(socket.cut(bore))


class HoistSheave(CadQueryNode):
    color = "#d9ad57"
    linear_deflection = .015
    angular_deflection = .05
    spin = Revolute(axis=(0, 1, 0))

    def render(self):
        profile = [(3.3, -6), (14.5, -6), (14.5, -3), (10.6, -1.5),
                   (10.6, 1.5), (14.5, 3), (14.5, 6), (3.3, 6)]
        shape = cq.Workplane("XY").polyline(profile).close().revolve(360, (0, 0), (0, 1))
        for a in (0, 120, 240):
            shape = shape.cut(axle(1.7, 14, (7, 0, 0)).rotate((0, 0, 0), (0, 1, 0), a))
        return shape


class WindingDrum(CadQueryNode):
    color = "#b47c49"
    linear_deflection = .015
    spin = Revolute(axis=(0, 1, 0))

    def render(self):
        profile = [(3.3, -6), (21, -6), (21, -3), (16.6, -1.5),
                   (16.6, 1.5), (21, 3), (21, 6), (3.3, 6)]
        drum = cq.Workplane("XY").polyline(profile).close().revolve(360, (0, 0), (0, 1))
        socket = box(5, 8, 6, (18, 0, -2))
        bore = cq.Workplane("XY").circle(1.3).extrude(5).translate((18, 0, -3.5))
        drum = drum.union(socket).cut(bore)
        for a in (0, 120, 240):
            drum = drum.cut(axle(2.4, 14, (10, 0, 0)).rotate((0, 0, 0), (0, 1, 0), a))
        return drum


class HookCarrier(CadQueryNode):
    color = "#4e6569"

    def render(self):
        carrier = box(16, 18, 6, (0, 0, -19))
        for y in (-8.4, 8.4):
            carrier = carrier.union(box(8, 4, 28, (0, y, -8)))
            carrier = carrier.union(box(8, 4, 13, (0, y, -26)))
        return carrier.union(axle(3, 23)).union(axle(3, 23, (0, 0, -29)))


class Stone(CadQueryNode):
    color = "#aaa69c"
    linear_deflection = .015

    def render(self):
        stone = box(26, 24, 23, (0, 0, -50))
        eye = cq.Workplane("XZ").circle(6).circle(3.3).extrude(3, both=True).translate((0, 0, -29))
        neck = box(6, 6, 13, (0, 0, -37))
        return stone.union(neck).union(eye).cut(axle(3.3, 8, (0, 0, -29)))


class MovingBlock(AssemblyNode):
    rise = Prismatic(axis=(0, 0, 1))
    carrier = HookCarrier()
    sheave = HoistSheave()
    stone = Stone()
    rise.drives(sheave.spin, ratio=-180/(12*pi))


class HoistRope(MolejoNode):
    color = "#d96d2c"
    lower = TranslationalPort(unit="mm")
    wrap = RotationalPort(unit="rad")

    def render(self):
        return Shape(Circle(1), [
            Line((0, 0, P.lower)),
            Arc((12, 0, P.lower), (0, -1, 0), pi),
            Line((24, 0, -6)),
            Arc((36, 0, -6), (0, 1, 0), pi/2),
            Line((80, 0, 6)),
            Arc((80, 0, -12), (0, 1, 0), P.wrap),
        ], path_samples=48, profile_samples=16)


class Trolley(AssemblyNode):
    travel = Prismatic(axis=(1, 0, 0))
    lift = TranslationalPort(unit="mm")
    carrier = TrolleyCarrier()
    upper = HoistSheave()
    drum = WindingDrum()
    block = MovingBlock()
    rope = HoistRope()
    lift.drives(block.rise)
    lift.drives(drum.spin, ratio=2*180/(18*pi))
    lift.drives(upper.spin, ratio=2*180/(12*pi))

    def render(self):
        self.upper.translate([24, -34, -20])
        self.drum.translate([68, -34, -26])
        self.block.translate([0, -34, -110])
        self.rope.translate([-12, -34, -14])

    def simulate(self):
        self.rope.lower = -96+self.lift.value
        self.rope.wrap = pi/2+2*self.lift.value/18


class RotatingCrane(AssemblyNode):
    slew = Revolute(axis=(0, 0, 1))
    mast = MastAndJib()
    screw = LeadScrew()
    trolley = Trolley()
    trolley.travel.drives(screw.spin, ratio=-360/12)

    def render(self):
        self.screw.translate([0, 0, 260])
        self.trolley.translate([80, 0, 260])


class SwivelCrane(AssemblyNode):
    slew = Driver(default=-45, range=(-60, 60), unit="deg")
    traverse = Driver(default=0, range=(0, 60), unit="mm")
    hoist = Driver(default=0, range=(0, 25), unit="mm")
    run = Driver(default=1, range=(0, 1), unit="play")
    turn = RotationalPort(unit="deg")
    reach = TranslationalPort(unit="mm")
    raise_load = TranslationalPort(unit="mm")
    footing = Footing()
    rotor = RotatingCrane()
    turn.drives(rotor.slew)
    reach.drives(rotor.trolley.travel)
    raise_load.drives(rotor.trolley.lift)

    instructions = {
        "Pick up": Instruction({"slew": -45, "traverse": 0, "hoist": 0, "run": 0}, duration=.7),
        "Lift clear": Instruction({"slew": -45, "traverse": 0, "hoist": 25, "run": 0}, duration=.7),
        "Swing": Instruction({"slew": 45, "traverse": 60, "hoist": 25, "run": 0}, duration=1.5),
        "Place": Instruction({"slew": 45, "traverse": 60, "hoist": 0, "run": 0}, duration=.7),
        "Demonstrate": Instruction({"run": 1}, duration=.7),
    }

    def simulate(self):
        a, x, z = demonstration(self.time)
        self.turn = (1-self.run)*self.slew+self.run*a
        self.reach = (1-self.run)*self.traverse+self.run*x
        self.raise_load = (1-self.run)*self.hoist+self.run*z
