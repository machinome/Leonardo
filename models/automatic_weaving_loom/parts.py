"""Reusable timber, heddles, reed, spool and textile from the gallery model.

The reconstructed transmissions and gripping hardware live in timing.py,
winding.py and head.py. The free weft span remains a schematic indicator.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq
from molejo import Shape, Circle, Line, Spline, P
from solid_node.node import AssemblyNode, CadQueryNode, MolejoNode
from solid_node.parameters import Length, Scalar, Count
from solid_node.motion.joints import Prismatic
from solid_node.motion.ports import TranslationalPort
from solid_node.math import sin, cos, sqrt, atan2
from .timing import clip
from .reeding import REED_TRAVEL


def box(x, y, z, at=(0, 0, 0)):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    """Cylinder on X, centred on at."""
    return (
        cq.Workplane("YZ").circle(radius).extrude(length / 2, both=True).translate(at)
    )


def united(parts):
    result = parts[0]
    for part in parts[1:]:
        result = result.union(part)
    return result


class TimberFrame(CadQueryNode):
    color = "#805333"
    drive_bearer_z = Length(18)
    guide_z = Length(120)

    def render(self):
        pieces = []
        for x in (-170, 170):
            for y in (-155, 155):
                pieces.append(box(20, 22, 255, (x, y, 127.5)))
            for z in (18, 130, 245):
                pieces.append(box(18, 320, 16, (x, 0, z)))
        for y in (-155, 155):
            pieces.append(box(340, 16, 18, (0, y, 18)))
        pieces.append(box(340, 16, 18, (0, 30, self.drive_bearer_z)))
        pieces.append(box(340, 16, 16, (0, 155, 245)))
        for x in (-116, 116):
            pieces.append(box(14, 20, 48, (x, 30, 42)))
            pieces.append(
                box(
                    14,
                    20,
                    24 - self.drive_bearer_z,
                    (x, 30, (18 + self.drive_bearer_z) / 2),
                )
            )
        for x in (-170, 170):
            pieces.append(box(18, 18, 112, (x, -83, 74)))
        # The separate reed bed seats 0.2 mm above this bearer.
        pieces.append(box(340, 16, 12, (0, -83, 77.8)))
        for x in (-170, 170):
            pieces.append(box(18, 18, 52, (x, -35, 155)))
            pieces.append(box(18, 18, 12, (x, -35, 180)))
        for side in (-1, 1):
            guide = box(43, 16, 12, (side * 157.5, 30, self.guide_z))
            guide = guide.cut(box(6.6, 7.6, 16, (side * 145, 30, self.guide_z)))
            pieces.append(guide)
            pieces.append(
                box(
                    18,
                    16,
                    abs(self.guide_z - 130) + 8,
                    (side * 170, 30, (self.guide_z + 130) / 2),
                )
            )
        frame = united(pieces).cut(axle(5.4, 300, (0, 30, 60)))
        # Swept handwheel/handle clearance in the lower stretcher.
        frame = frame.cut(axle(47, 30, (94, 30, 60)))
        for y in (-155, 155):
            frame = frame.cut(axle(5.4, 400, (0, y, 165)))
        return frame.cut(box(400, 8.6, 5.6, (0, -35, 180)))


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


class Reed(CadQueryNode):
    color = "#bfa76d"
    stroke = Prismatic(axis=(0, 1, 0), range=(-REED_TRAVEL - 0.01, 0.01))

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
        # A U-shaped bed: the front bearer joins both rails, while the
        # open rear centre clears the shaft's selector cams underneath.
        base = box(206, 16, 8, (0, -83, 88))
        for x in (-93, 93):
            base = base.union(box(15, 132, 8, (x, -52, 88)))
            wall = box(15, 132, 12, (x, -52, 98))
            wall = wall.cut(box(8.6, 136, 14, (x, -52, 102.7)))
            base = base.union(wall)
        return base


class CarrierArm(CadQueryNode):
    side = Scalar(-1)
    color = "#a76537"

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
        outline = [
            (-12, -2),
            (-8, -6),
            (8, -6),
            (12, -2),
            (12, 2),
            (8, 6),
            (-8, 6),
            (-12, 2),
        ]
        body = cq.Workplane("XY").polyline(outline).close().extrude(3, both=True)
        body = body.cut(box(14, 6, 4, (0, 0, 2)))
        return body.union(axle(2.5, 12, (0, 0, 0)))


def shuttle_x(angle):
    p = 180 + atan2(sin(angle - 180), cos(angle - 180))

    def rise(start, end):
        return (1 - cos(180 * clip((p - start) / (end - start), 0, 1))) / 2

    # Smooth approaches with a 60-degree receiving/closing/releasing dwell.
    return 130 * (-1 + rise(10, 60) + rise(120, 170) - rise(190, 240) - rise(300, 350))


def weft_selvedge(angle):
    # Exchange the illustrated yarn's anchored edge during the closed shed.
    s = sin(angle)
    return -72 * s / sqrt(s * s + 0.0025)


class YarnSegment(MolejoNode):
    reach = Length(min=1)
    end_height = TranslationalPort()
    color = "#ded3ad"

    def render(self):
        return Shape(
            Circle(0.48),
            [Line((0, -self.reach, P.end_height))],
            path_samples=120,
            profile_samples=8,
        )


class MovingYarn(AssemblyNode):
    reach = Length(min=1)
    rise = Prismatic(axis=(0, 0, 1))
    end_height = TranslationalPort()
    fiber = YarnSegment(reach=reach)
    end_height.drives(fiber.end_height)


class WarpEnd(AssemblyNode):
    station = Length(20)
    warp_y = Length(155)
    fell_offset = Length(105)
    lift = TranslationalPort()
    rear = YarnSegment(reach=warp_y - station)
    front = MovingYarn(reach=station + fell_offset)
    lift.drives(rear.end_height)
    lift.drives(front.end_height, ratio=-1)
    lift.drives(front.rise)

    def render(self):
        self.front.translate([0, self.station - 155, 0])


class BlueYarn(YarnSegment):
    color = "#4c9fa9"


class MovingBlueYarn(MovingYarn):
    fiber = BlueYarn(reach=MovingYarn.reach)


class BlueWarpEnd(WarpEnd):
    rear = BlueYarn(reach=WarpEnd.warp_y - WarpEnd.station)
    front = MovingBlueYarn(reach=WarpEnd.station + WarpEnd.fell_offset)


class ClothWarp(MolejoNode):
    color = "#dfcda5"
    reach = Length(49, min=1)

    def render(self):
        return Shape(
            Circle(0.48),
            [Line((0, -self.reach, 0))],
            path_samples=20,
            profile_samples=8,
        )


class ClothPick(MolejoNode):
    parity = Count(0)
    color = "#b95347"

    def render(self):
        points = [(3 + 6 * i, 0, 1.2 * (-1) ** (i + self.parity)) for i in range(24)]
        points.append((144, 0, 0))
        return Shape(
            Circle(0.42), [Spline(points)], path_samples=160, profile_samples=8
        )


class WeftTail(MolejoNode):
    tip_x = TranslationalPort()
    contact_x = TranslationalPort()
    contact_y = TranslationalPort()
    color = "#d66c4a"

    def render(self):
        return Shape(
            Circle(0.45),
            [Line((P.contact_x, P.contact_y, 0)), Line((P.tip_x, 70, 0))],
            path_samples=40,
            profile_samples=8,
        )
