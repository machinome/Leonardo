"""Original educational reconstruction of Leonardo's loom, CA f.985r-v.

The eccentric/yoke drive is geometrically captured. Carrier and reed laws
represent the synchronized transmission; intermediate gearing, latches and
yarn/contact dynamics are not reconstructed.
"""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq
from molejo import Shape, Circle, Line, Spline, P
from solid_node.node import AssemblyNode, FusionNode, CadQueryNode, MolejoNode
from solid_node.parameters import Length, Scalar, Count
from solid_node.motion.joints import Revolute, Prismatic
from solid_node.motion.ports import RotationalPort, TranslationalPort
from solid_node.simulation import Driver, Instruction
from solid_node.math import sin, cos, sqrt


def box(x, y, z, at=(0, 0, 0)):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    """Cylinder on X, centred on at."""
    return cq.Workplane("YZ").circle(radius).extrude(length / 2, both=True).translate(at)


def united(parts):
    result = parts[0]
    for part in parts[1:]:
        result = result.union(part)
    return result


class TimberFrame(CadQueryNode):
    color = "#805333"

    def render(self):
        pieces = []
        for x in (-170, 170):
            for y in (-155, 155):
                pieces.append(box(20, 22, 255, (x, y, 127.5)))
            for z in (18, 130, 245):
                pieces.append(box(18, 320, 16, (x, 0, z)))
        for y in (-155, 155, 30):
            pieces.append(box(340, 16, 18, (0, y, 18)))
        pieces.append(box(340, 16, 16, (0, 155, 245)))
        for x in (-116, 116):
            pieces.append(box(14, 20, 48, (x, 30, 42)))
        for x in (-170, 170):
            pieces.append(box(18, 18, 112, (x, -83, 74)))
        # The separate reed bed seats 0.2 mm above this bearer.
        pieces.append(box(340, 16, 12, (0, -83, 77.8)))
        for x in (-170, 170):
            pieces.append(box(18, 18, 52, (x, -35, 155)))
            pieces.append(box(18, 18, 12, (x, -35, 180)))
        for side in (-1, 1):
            guide = box(43, 16, 12, (side * 157.5, 30, 120))
            guide = guide.cut(box(6.6, 7.6, 16, (side * 145, 30, 120)))
            pieces.append(guide)
        frame = united(pieces).cut(axle(5.4, 300, (0, 30, 60)))
        # Swept handwheel/handle clearance in the lower stretcher.
        frame = frame.cut(axle(47, 30, (94, 30, 60)))
        for y in (-155, 155):
            frame = frame.cut(axle(5.4, 400, (0, y, 165)))
        return frame.cut(box(400, 8.6, 5.6, (0, -35, 180)))


class CrankCore(CadQueryNode):
    def render(self):
        parts = [axle(5, 270)]
        for x in (-132, 132):
            parts.append(axle(25, 8, (x, 0, 0)))
        ring = cq.Workplane("YZ").circle(46).circle(39).extrude(4, both=True)
        wheel = ring.union(axle(10, 10))
        for angle in range(0, 180, 30):
            wheel = wheel.union(box(7, 84, 5).rotate((0, 0, 0), (1, 0, 0), angle))
        parts.append(wheel.translate((102, 0, 0)))
        parts.append(axle(4, 20, (90, 0, 38)))
        return united(parts)


class EccentricPin(CadQueryNode):
    def render(self):
        return axle(3, 20)


class Crank(FusionNode):
    color = "#bb884b"
    eccentricity = Length(min=0)
    turn = Revolute(axis=(1, 0, 0))
    core = CrankCore()
    pin_a = EccentricPin()
    pin_b = EccentricPin()

    def render(self):
        self.pin_a.translate([-140, self.eccentricity, 0])
        self.pin_b.translate([140, -self.eccentricity, 0])


class HeddleCage(CadQueryNode):
    parity = Count(0)

    def render(self):
        frame = box(188, 6, 78).cut(box(172, 10, 62))
        for i in range(12):
            x = -69 + 6 * self.parity + 12 * i
            needle = box(0.9, 2, 64, (x, 0, 0))
            eye = cq.Workplane("XZ").center(x, 0).circle(2.6).extrude(1, both=True)
            needle = needle.union(eye)
            bore = cq.Workplane("XZ").center(x, 0).circle(1.5).extrude(4, both=True)
            frame = frame.union(needle.cut(bore))
        return frame


class SlottedYoke(CadQueryNode):
    side = Scalar(-1)
    station = Length(20)

    def render(self):
        x, y = self.side * 145, 30 - self.station
        ring = box(6, 56, 14, (x, y, -120))
        ring = ring.cut(box(10, 46.6, 6.6, (x, y, -120)))
        stem = box(6, 7, 153, (x, y, -37.5))
        bridge = box(64, abs(y) + 8, 8, (self.side * 116, y / 2, 35))
        return ring.union(stem).union(bridge)


class Heddle(FusionNode):
    side = Scalar(-1)
    station = Length(20)
    parity = Count(0)
    color = "#368d8e"
    rise = Prismatic(axis=(0, 0, 1), range=(-20.01, 20.01))
    cage = HeddleCage(parity=parity)
    yoke = SlottedYoke(side=side, station=station)


class Reed(CadQueryNode):
    color = "#bfa76d"
    stroke = Prismatic(axis=(0, 1, 0), range=(-37.01, 0.01))

    def render(self):
        frame = box(194, 7, 78).cut(box(178, 11, 62))
        for x in range(-72, 73, 6):
            frame = frame.union(box(0.7, 2, 64, (x, 0, 0)))
        for x in (-93, 93):
            frame = frame.union(box(8, 7, 58, (x, 0, -55)))
        return frame


class ReedTracks(CadQueryNode):
    color = "#563e2b"

    def render(self):
        base = box(206, 75, 8, (0, -83, 88))
        for x in (-93, 93):
            wall = box(15, 75, 12, (x, -83, 98))
            wall = wall.cut(box(8.6, 80, 14, (x, -83, 102.7)))
            base = base.union(wall)
        return base


class CarrierArm(CadQueryNode):
    side = Scalar(-1)
    color = "#a76537"
    slide = Prismatic(axis=(1, 0, 0))

    def render(self):
        arm = box(180, 8, 5, (self.side * 102.5, 0, 0))
        # Interleaved fingers support the bobbin through handoff. Left outer
        # fingers and right inner fingers can pass at the centre without
        # shared volume. The bobbin sits 0.3 mm above the finger tops.
        lanes = (-2.5, 2.5) if self.side < 0 else (-0.8, 0.8)
        for y in lanes:
            arm = arm.union(box(3, 1, 2.8, (self.side * 15, y, -2.9)))
            arm = arm.union(box(20.5, 1, 1, (self.side * 6.25, y, -3.8)))
        return arm


class WeftSpool(CadQueryNode):
    color = "#bb473b"
    slide = Prismatic(axis=(1, 0, 0))

    def render(self):
        outline = [(-12, -2), (-8, -6), (8, -6), (12, -2),
                   (12, 2), (8, 6), (-8, 6), (-12, 2)]
        body = cq.Workplane("XY").polyline(outline).close().extrude(3, both=True)
        body = body.cut(box(14, 6, 4, (0, 0, 2)))
        return body.union(axle(2.5, 12, (0, 0, 0)))


def shuttle_x(angle):
    return -130 * cos(angle)


def left_reach(angle):
    x = shuttle_x(angle)
    return (x - sqrt(x * x + 0.0001)) / 2


def right_reach(angle):
    x = shuttle_x(angle)
    return (x + sqrt(x * x + 0.0001)) / 2


def weft_selvedge(angle):
    # Exchange the illustrated yarn's anchored edge during the closed shed.
    s = sin(angle)
    return -72 * s / sqrt(s * s + 0.0025)


class Carrier(AssemblyNode):
    angle = RotationalPort()
    left = CarrierArm(side=-1)
    right = CarrierArm(side=1)
    spool = WeftSpool()
    angle.drives(left.slide, law=lambda a, b: left_reach)
    angle.drives(right.slide, law=lambda a, b: right_reach)
    angle.drives(spool.slide, law=lambda a, b: shuttle_x)


class Roller(CadQueryNode):
    color = "#c5a777"
    turn = Revolute(axis=(1, 0, 0))

    def render(self):
        roller = axle(14, 164).union(axle(5, 354))
        for x in (-84, 84):
            roller = roller.union(axle(18, 4, (x, 0, 0)))
        return roller.cut(box(145, 2, 2, (0, 0, 14)))


class YarnSegment(MolejoNode):
    reach = Length(min=1)
    end_height = TranslationalPort()
    color = "#ded3ad"

    def render(self):
        return Shape(Circle(0.48), [Line((0, -self.reach, P.end_height))],
                     path_samples=120, profile_samples=8)


class WarpEnd(AssemblyNode):
    station = Length(20)
    warp_y = Length(155)
    fell_offset = Length(105)
    lift = TranslationalPort()
    rear = YarnSegment(reach=warp_y - station)
    front = YarnSegment(reach=station + fell_offset)

    def render(self):
        self.front.translate([0, self.station - 155, 0])

    def simulate(self):
        z = self.lift.value
        self.rear.end_height = z
        self.front.end_height = -z
        self.front.translate([0, 0, z])


class BlueYarn(YarnSegment):
    color = "#4c9fa9"


class BlueWarpEnd(WarpEnd):
    rear = BlueYarn(reach=WarpEnd.warp_y - WarpEnd.station)
    front = BlueYarn(reach=WarpEnd.station + WarpEnd.fell_offset)


class ClothWarp(MolejoNode):
    color = "#dfcda5"

    def render(self):
        return Shape(Circle(0.48), [Line((0, -49, 0))],
                     path_samples=20, profile_samples=8)


class ClothPick(MolejoNode):
    parity = Count(0)
    color = "#b95347"

    def render(self):
        points = [(3 + 6 * i, 0, 1.2 * (-1) ** (i + self.parity))
                  for i in range(24)]
        points.append((144, 0, 0))
        return Shape(Circle(0.42), [Spline(points)],
                     path_samples=160, profile_samples=8)


class WeftTail(MolejoNode):
    tip_x = TranslationalPort()
    color = "#d66c4a"

    def render(self):
        return Shape(Circle(0.45), [Line((P.tip_x, 70, 0))],
                     path_samples=80, profile_samples=8)


class AutomaticWeavingLoom(AssemblyNode):
    """One timeline revolution = two alternating picks (illustrative speed)."""
    phase = Driver(default=0.0, range=(0, 360), unit="deg")
    run = Driver(default=1.0, range=(0, 1), unit="play")
    cycle = RotationalPort()
    shed_lift = Length(18, min=16, max=20)
    frame = TimberFrame()
    crank = Crank(eccentricity=shed_lift)
    heddle_a = Heddle(side=-1, station=20, parity=0)
    heddle_b = Heddle(side=1, station=40, parity=1)
    carrier = Carrier()
    reed = Reed()
    reed_tracks = ReedTracks()
    warp_beam = Roller()
    cloth_beam = Roller()
    warp_a = WarpEnd(station=20).repeat(12)
    warp_b = BlueWarpEnd(station=40).repeat(12)
    cloth_ends = ClothWarp().repeat(24)
    cloth_picks_a = ClothPick(parity=0).repeat(4)
    cloth_picks_b = ClothPick(parity=1).repeat(4)
    weft = WeftTail()

    cycle.drives(crank.turn)
    cycle.drives(heddle_a.rise, law=lambda a, b: lambda angle: a.shed_lift * sin(angle))
    cycle.drives(heddle_b.rise, law=lambda a, b: lambda angle: -a.shed_lift * sin(angle))
    cycle.drives(carrier.angle)
    cycle.drives(reed.stroke, law=lambda a, b: lambda angle: -18.5 * (1 + cos(2 * angle)))
    cycle.drives(warp_a.lift, law=lambda a, b: lambda angle: a.shed_lift * sin(angle))
    cycle.drives(warp_b.lift, law=lambda a, b: lambda angle: -a.shed_lift * sin(angle))
    cycle.drives(warp_beam.turn, ratio=1 / 36)
    cycle.drives(cloth_beam.turn, ratio=1 / 36)
    cycle.drives(weft.tip_x, law=lambda a, b: lambda angle: shuttle_x(angle) - weft_selvedge(angle))

    instructions = {
        "Beat left": Instruction({"phase": 0.0, "run": 0.0}, duration=0.6),
        "Open shed": Instruction({"phase": 60.0, "run": 0.0}, duration=0.6),
        "Handoff": Instruction({"phase": 90.0, "run": 0.0}, duration=0.6),
        "Beat right": Instruction({"phase": 180.0, "run": 0.0}, duration=0.6),
        "Return pick": Instruction({"phase": 270.0, "run": 0.0}, duration=0.6),
        "Run": Instruction({"phase": 0.0, "run": 1.0}, duration=0.6),
    }

    def render(self):
        self.crank.translate([0, 30, 60])
        self.heddle_a.translate([0, 20, 180])
        self.heddle_b.translate([0, 40, 180])
        self.carrier.translate([0, -35, 180])
        self.reed.translate([0, -65, 180])
        for beam, y in [(self.warp_beam, 155), (self.cloth_beam, -155)]:
            beam.translate([0, y, 165])
        for i, (a, b) in enumerate(zip(self.warp_a, self.warp_b)):
            a.translate([-69 + 12 * i, 155, 180])
            b.translate([-63 + 12 * i, 155, 180])
        for i, end in enumerate(self.cloth_ends):
            end.translate([-69 + 6 * i, -105, 180])
        for i, (a, b) in enumerate(zip(self.cloth_picks_a, self.cloth_picks_b)):
            a.translate([-72, -110 - 12 * i, 180])
            b.translate([-72, -116 - 12 * i, 180])
        self.weft.translate([0, -105, 180])

    def simulate(self):
        angle = self.phase + 360 * self.run * self.time
        self.cycle = angle
        self.weft.translate([weft_selvedge(angle), 0, 0])
