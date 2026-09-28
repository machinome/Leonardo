"""Lower winding train and its indexed descending feed."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

import cadquery as cq
from molejo import Shape, Polygon, Line, Wrap
from machinome.node import AssemblyNode, CadQueryNode, MolejoNode
from machinome.parameters import Flag
from machinome.motion.joints import Revolute, Prismatic, Free
from machinome.motion.ports import RotationalPort, TranslationalPort
from machinome.math import sin, cos, atan2

from .profiles import cycloidal_outline, cycloidal_rack, polar
from .timing import TimingBench, TimingTrain, TwelveToothWheel, cylinder, clip

RADIUS = 48
PITCH = math.pi * 4
CENTERS = 20 * PITCH
LOOP = 64 * PITCH
CAM_RISE = 0.06  # millimetres per output-wheel degree; finite 120-degree cam


def box(x, y, z, at):
    return cq.Workplane("XY").box(x, y, z).translate(at)


class FeedWheel(TwelveToothWheel):
    """The visible scroll face: captured radial follower, not a
    decorative line."""

    def render(self):
        wheel = super().render()
        face = cylinder(31, 7, 12)
        # Local polar angle -90-turn meets the vertical follower below
        # centre.
        points = []
        for side, turns in ((-1, range(-10, 131)), (1, range(130, -11, -1))):
            for turn in turns:
                radius = 14 + CAM_RISE * turn + side * 1.8
                points.append(polar(radius, -90 - turn))
        groove = (
            cq.Workplane("YZ")
            .polyline(points)
            .close()
            .extrude(5)
            .translate((8, 0, 0))
        )
        return wheel.union(face.cut(groove))


class FeedTimingTrain(TimingTrain):
    twelve = FeedWheel()


class DescendingRack(CadQueryNode):
    color = "#514337"
    slide = Prismatic(axis=(0, 0, 1), range=(-7.21, 0.01))

    def render(self):
        rack = cq.Workplane("YZ").polyline(cycloidal_rack()).close().extrude(6)
        # Backing reaches the cam without crossing the lower wheel's
        # teeth.
        rack = rack.union(box(6, 4, 276, (3, 56, 92)))
        # Pin lies on Y=54, Z=256: fourteen below the upper cam centre.
        rack = rack.union(box(18, 4, 6, (8, 56, 226)))
        rack = rack.union(box(4, 4, 32, (15, 56, 242)))
        rack = rack.union(box(4, 6, 5, (15, 55, 256)))
        rack = rack.union(cylinder(1.5, 8.3, 15, 54, 256))
        return rack


class WindingWheel(CadQueryNode):
    color = "#b98d54"
    sprocket = Flag(False)
    beam = Flag(False)
    turn = Revolute(axis=(1, 0, 0))

    def render(self):
        gear = (
            cq.Workplane("YZ")
            .polyline(cycloidal_outline(24, module=4))
            .close()
            .extrude(6)
        )
        body = gear.union(cylinder(3, -376, 23))
        for x in (-364.7, -352.7, -15.7, -3.7):
            body = body.union(cylinder(6, x, x + 3.4))
        body = body.union(cylinder(9, 21, 23))
        body = body.union(cylinder(0.9, 22.5, 24.5, 8, 0))
        if self.beam:
            body = body.union(cylinder(14, -277, -113))
            for x in (-280, -113):
                body = body.union(cylinder(18, x, x + 3))
        if self.sprocket:
            body = body.union(cylinder(43, 14, 18))
            for i in range(24):
                peg = (
                    cq.Workplane("XY")
                    .circle(1.5)
                    .extrude(10)
                    .translate((16, 0, 41))
                )
                body = body.union(
                    peg.rotate((0, 0, 0), (1, 0, 0), -97.5 + 15 * i)
                )
        return body


class WindingBearings(CadQueryNode):
    color = "#735137"

    def render(self):
        # Two connected bearing standards; the full model seats their
        # feet
        # on timber. This bench connects them with two long
        # cross-bearers.
        pieces = []
        for x in (-8, -357):
            side = box(8, CENTERS + 22, 12, (x, -CENTERS / 2, -60))
            for y in (0, -CENTERS):
                upright = box(8, 14, 174, (x, y, 21))
                for z in (0, 96):
                    upright = upright.cut(cylinder(3.3, x - 5, x + 5, y, z))
                side = side.union(upright)
            pieces.append(side)
        for y in (0, -CENTERS):
            pieces.append(box(358, 14, 12, (-182.5, y, -60)))
        # Descending bar guide: four faces capture the rack's plain
        # backing.
        guide = box(15, 15, 12, (3, 56, 160)).cut(
            box(6.6, 4.6, 14, (3, 56, 160))
        )
        pieces.append(guide.union(box(8, 64, 12, (-8, 26, 160))))
        pieces.append(box(8, 14, 64, (-8, 0, 132)))
        result = pieces[0]
        for part in pieces[1:]:
            result = result.union(part)
        return result


class BeltBand(MolejoNode):
    color = "#56452e"

    def render(self):
        return Shape(
            Polygon([(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]),
            [
                Wrap(
                    around=[
                        {"center": (0, 0), "radius": 48},
                        {"center": (CENTERS, 0), "radius": 48},
                    ]
                )
            ],
            loop=True,
            path_samples=256,
            profile_samples=4,
        )


class BeltBridge(MolejoNode):
    """Leather between punched holes, transported with the belt
    material."""

    color = "#56452e"

    def render(self):
        return Shape(
            Polygon([(-4.5, -2), (4.5, -2), (4.5, 2), (-4.5, 2)]),
            [Line((0, 0, 1))],
            path_samples=2,
            profile_samples=4,
        )


class BeltRung(AssemblyNode):
    pose = Free()
    leather = BeltBridge()

    def render(self):
        self.leather.translate([0, 0, -0.5])


def belt_pose(distance):
    # The half-pitch offset keeps the finite envelope away from atan2's
    # seam.
    s = (
        LOOP / 2
        + LOOP
        / (2 * math.pi)
        * atan2(
            sin(360 * distance / LOOP - 180), cos(360 * distance / LOOP - 180)
        )
        * math.pi
        / 180
    )
    top = clip(s, 0, CENTERS)
    a = 180 * clip((s - CENTERS) / (math.pi * RADIUS), 0, 1)
    bottom = clip(s - CENTERS - math.pi * RADIUS, 0, CENTERS)
    b = 180 * clip(
        (s - 2 * CENTERS - math.pi * RADIUS) / (math.pi * RADIUS), 0, 1
    )
    return (
        -CENTERS + top - bottom + RADIUS * sin(a) - RADIUS * sin(b),
        96 + RADIUS * (1 + cos(a) - cos(b)),
        -a - b,
    )


class PerforatedBelt(AssemblyNode):
    travel = TranslationalPort()
    left = BeltBand()
    right = BeltBand()
    rungs = BeltRung().repeat(64)
    travel.drives(
        rungs.pose.y,
        law=lambda a, b: lambda t: belt_pose((b.index + 0.5) * PITCH + t)[0],
    )
    travel.drives(
        rungs.pose.z,
        law=lambda a, b: lambda t: belt_pose((b.index + 0.5) * PITCH + t)[1],
    )
    travel.drives(
        rungs.pose.roll,
        law=lambda a, b: lambda t: belt_pose((b.index + 0.5) * PITCH + t)[2],
    )

    def render(self):
        for band, x in ((self.left, -4), (self.right, 4)):
            band.rotate(120, [1, 1, 1]).translate([x, -CENTERS, 96])


class WindingTrain(AssemblyNode):
    feed = TranslationalPort()
    rack = DescendingRack()
    rear_lower = WindingWheel()
    rear_upper = WindingWheel(sprocket=True, beam=True)
    front_upper = WindingWheel(sprocket=True)
    front_lower = WindingWheel(beam=True)
    bearings = WindingBearings()
    belt = PerforatedBelt()
    feed.drives(rack.slide, ratio=-1)
    rack.slide.drives(rear_lower.turn, ratio=180 / (math.pi * RADIUS))
    rear_lower.turn.drives(rear_upper.turn, ratio=-1, offset=7.5)
    rear_upper.turn.drives(
        belt.travel,
        ratio=-math.pi * RADIUS / 180,
        offset=7.5 * math.pi * RADIUS / 180,
    )
    belt.travel.drives(
        front_upper.turn, ratio=-180 / (math.pi * RADIUS), offset=7.5
    )
    front_upper.turn.drives(front_lower.turn, ratio=-1, offset=7.5)

    def render(self):
        self.rear_upper.translate([0, 0, 96])
        self.front_upper.translate([0, -CENTERS, 96])
        self.front_lower.translate([0, -CENTERS, 0])
        self.belt.translate([16, 0, 0])


class WindingBench(TimingBench):
    train = FeedTimingTrain()
    winding = WindingTrain()
    train.twelve.turn.drives(winding.feed, ratio=CAM_RISE)

    def render(self):
        self.train.translate([0, 108, 270])
