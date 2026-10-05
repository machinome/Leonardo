"""Taut-cord completion of the loom's hidden haul and weighted return
routes.

Lengths and attachment motion are kinematic constraints. No claim is
made
that a rope force, spring force, friction or impact solver is running.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

import cadquery as cq
from molejo import Shape, Circle, Line, Arc, P
from machinome.node.assembly import AssemblyNode
from machinome.node.cadquery import CadQueryNode
from machinome.node.molejo import MolejoNode
from machinome.parameters import Scalar, Length
from machinome.motion.joints import Revolute, Prismatic
from machinome.motion.ports import TranslationalPort

from .parts import box
from .head import y_cylinder
from .reeding import (
    REED_TIE_X,
    REED_STEM_TOP,
    REED_SHEAVE_Z,
    REED_TRAVEL,
    REED_TIE_Z,
    REED_RETURN_X,
)

PULLEY_R = 3.5
ROPE_R = 0.6


class CordPulley(CadQueryNode):
    color = "#ac8a55"
    turn = Revolute(axis=(0, 1, 0))

    def render(self):
        body = y_cylinder(2.7, -0.9, 0.9)
        for y in (-1.7, 0.9):
            body = body.union(y_cylinder(4.5, y, y + 0.8))
        body = body.union(y_cylinder(1, -3, 10))
        for y in (2, 8.3):
            body = body.union(y_cylinder(2.2, y, y + 1.7))
        return body


class ArmHaul(MolejoNode):
    side = Scalar(-1)
    anchor_x = Length(-298.2)
    upper = TranslationalPort()
    top = TranslationalPort()
    lower = TranslationalPort()
    end_z = TranslationalPort()
    end_x = TranslationalPort()
    color = "#d4bd84"

    def render(self):
        s = self.side
        a = self.anchor_x
        corner = s * 326.5 - a
        outer = s * 330 - a
        return Shape(
            Circle(ROPE_R),
            [
                Line((0, 0, P.upper)),
                Arc((s * 3.5, 0, P.upper), (0, 1, 0), s * math.pi / 2),
                Line((corner, 0, P.top)),
                Arc((corner, 0, P.upper), (0, 1, 0), s * math.pi / 2),
                Line((outer, 0, P.lower)),
                Arc((corner, 0, P.lower), (0, 1, 0), s * math.pi / 2),
                Line((P.end_x, 0, P.end_z)),
            ],
            path_samples=128,
            profile_samples=8,
        )


class ArmHaulAttachment(AssemblyNode):
    side = Scalar(-1)
    anchor_x = Length(-298.2)
    rise = Prismatic(axis=(0, 0, 1))
    cord = ArmHaul(side=side, anchor_x=anchor_x)
    rise.drives(cord.upper, ratio=-1, offset=123.5)
    rise.drives(cord.top, ratio=-1, offset=127)
    rise.drives(cord.lower, ratio=-1, offset=90.5)
    rise.drives(cord.end_z, ratio=-1, offset=87)


class ReturnCord(MolejoNode):
    side = Scalar(-1)
    to_pulley = TranslationalPort()
    to_weight = TranslationalPort()
    drop = TranslationalPort()
    color = "#d4bd84"

    def render(self):
        s = self.side
        return Shape(
            Circle(ROPE_R),
            [
                Line((P.to_pulley, 0, 0)),
                Arc((P.to_pulley, 0, -3.5), (0, 1, 0), -s * math.pi / 2),
                Line((P.to_weight, 0, P.drop)),
            ],
            path_samples=96,
            profile_samples=8,
        )


class ReturnAttachment(AssemblyNode):
    side = Scalar(-1)
    slide = Prismatic(axis=(1, 0, 0))
    cord = ReturnCord(side=side)
    slide.drives(cord.to_pulley, ratio=-1, offset=-side * 40)
    slide.drives(cord.to_weight, ratio=-1, offset=-side * 43.5)
    slide.drives(cord.drop, ratio=side, offset=-170)


class ReturnWeight(CadQueryNode):
    color = "#77614a"
    rise = Prismatic(axis=(0, 0, 1), range=(-REED_TRAVEL - 0.01, 130.01))

    def render(self):
        return cq.Workplane("XY").circle(5.5).extrude(14)


class SideCords(AssemblyNode):
    side = Scalar(-1)
    anchor_x = Length(-298.2)
    lift = TranslationalPort()
    travel = TranslationalPort()
    haul = ArmHaulAttachment(side=side, anchor_x=anchor_x)
    returning = ReturnAttachment(side=side)
    first = CordPulley()
    corner = CordPulley()
    lower = CordPulley()
    return_pulley = CordPulley()
    weight = ReturnWeight()
    lift.drives(haul.rise)
    travel.drives(haul.cord.end_x, offset=side * 185 - anchor_x)
    travel.drives(returning.slide)
    travel.drives(weight.rise, law=lambda a, b: lambda x: a.side * x)
    lift.drives(
        first.turn,
        law=lambda a, b: lambda z: a.side * z / PULLEY_R * 180 / math.pi,
    )
    lift.drives(
        corner.turn,
        law=lambda a, b: lambda z: a.side * z / PULLEY_R * 180 / math.pi,
    )
    lift.drives(
        lower.turn,
        law=lambda a, b: lambda z: a.side * z / PULLEY_R * 180 / math.pi,
    )
    travel.drives(return_pulley.turn, ratio=180 / (math.pi * PULLEY_R))

    def render(self):
        s = self.side
        self.haul.translate([self.anchor_x, 240, 433])
        self.returning.translate([s * 185, 260, 520])
        self.first.translate([self.anchor_x + s * 3.5, 240, 556.5])
        self.corner.translate([s * 326.5, 240, 556.5])
        self.lower.translate([s * 326.5, 240, 523.5])
        self.return_pulley.translate([s * 145, 260, 516.5])
        self.weight.translate([s * 141.5, 260, 336])


class ReedHaul(MolejoNode):
    upper = TranslationalPort()
    top = TranslationalPort()
    lower = TranslationalPort()
    end_y = TranslationalPort()
    end_z = TranslationalPort()
    color = "#d4bd84"

    def render(self):
        return Shape(
            Circle(ROPE_R),
            [
                Line((0, 0, P.upper)),
                Arc((0, -3.5, P.upper), (1, 0, 0), math.pi / 2),
                Line((0, -176.5, P.top)),
                Arc((0, -176.5, P.upper), (1, 0, 0), math.pi / 2),
                Line((0, -180, P.lower)),
                Arc((0, -176.5, P.lower), (1, 0, 0), math.pi / 2),
                Line((0, P.end_y, P.end_z)),
            ],
            path_samples=128,
            profile_samples=8,
        )


class ReedHaulAttachment(AssemblyNode):
    rise = Prismatic(axis=(0, 0, 1))
    cord = ReedHaul()
    # The raised sheaves stay above the stem throughout its longer
    # stroke.
    rise.drives(cord.upper, ratio=-1, offset=REED_SHEAVE_Z - REED_STEM_TOP)
    rise.drives(cord.top, ratio=-1, offset=REED_SHEAVE_Z + 3.5 - REED_STEM_TOP)
    rise.drives(cord.lower, ratio=-1, offset=REED_TIE_Z + 3.5 - REED_STEM_TOP)
    rise.drives(cord.end_z, ratio=-1, offset=REED_TIE_Z - REED_STEM_TOP)
    rise.drives(cord.end_y, offset=-132)


class ReedCordReturn(MolejoNode):
    to_pulley = TranslationalPort()
    to_weight = TranslationalPort()
    drop = TranslationalPort()
    color = "#d4bd84"

    def render(self):
        return Shape(
            Circle(ROPE_R),
            [
                Line((0, P.to_pulley, 0)),
                Arc((0, P.to_pulley, -3.5), (1, 0, 0), -math.pi / 2),
                Line((0, P.to_weight, P.drop)),
            ],
            path_samples=96,
            profile_samples=8,
        )


class ReedReturnAttachment(AssemblyNode):
    slide = Prismatic(axis=(0, 1, 0))
    cord = ReedCordReturn()
    slide.drives(cord.to_pulley, ratio=-1, offset=152)
    slide.drives(cord.to_weight, ratio=-1, offset=155.5)
    slide.drives(cord.drop, ratio=-1, offset=-145)


class ReedCords(AssemblyNode):
    lift = TranslationalPort()
    haul = ReedHaulAttachment()
    returning = ReedReturnAttachment()
    first = CordPulley()
    corner = CordPulley()
    lower = CordPulley()
    return_pulley = CordPulley()
    weight = ReturnWeight()
    lift.drives(haul.rise)
    lift.drives(returning.slide)
    lift.drives(weight.rise, ratio=-1)
    lift.drives(first.turn, ratio=-180 / (math.pi * PULLEY_R))
    lift.drives(corner.turn, ratio=-180 / (math.pi * PULLEY_R))
    lift.drives(lower.turn, ratio=-180 / (math.pi * PULLEY_R))
    lift.drives(return_pulley.turn, ratio=180 / (math.pi * PULLEY_R))

    def render(self):
        self.haul.translate([REED_TIE_X, 180, REED_STEM_TOP])
        self.returning.translate([REED_RETURN_X, 48, REED_TIE_Z])
        for pulley, y, z in (
            (self.first, 176.5, REED_SHEAVE_Z),
            (self.corner, 3.5, REED_SHEAVE_Z),
            (self.lower, 3.5, REED_TIE_Z + 3.5),
            (self.return_pulley, 200, REED_TIE_Z - 3.5),
        ):
            x = REED_RETURN_X if pulley is self.return_pulley else REED_TIE_X
            pulley.rotate(-90, [0, 0, 1]).translate([x, y, z])
        self.weight.translate([REED_RETURN_X, 203.5, REED_TIE_Z - 159])


class CordSupports(CadQueryNode):
    color = "#765032"

    def render(self):
        pieces = []
        holes = []
        for s, anchor in ((-1, -298.2), (1, 311.8)):
            pieces.append(box(180, 4, 12, (s * 250, 246, 556.5)))
            pieces.append(box(12, 4, 45, (s * 326.5, 246, 540)))
            for x, z in (
                (anchor + s * 3.5, 556.5),
                (s * 326.5, 556.5),
                (s * 326.5, 523.5),
            ):
                holes.append(y_cylinder(1.3, 243, 249, x, z))
            pieces.append(box(40, 4, 12, (s * 160, 266, 516.5)))
            holes.append(y_cylinder(1.3, 263, 269, s * 145, 516.5))
            pieces.append(box(12, 48, 98, (s * 170, 224, 513.5)))
        # A left-side upright carries the reed's three changes of
        # direction.
        x = REED_TIE_X + 6
        pieces.append(box(4, 220, 12, (x, 102.5, REED_SHEAVE_Z)))
        for seat_x, y, z in (
            (x, 176.5, REED_SHEAVE_Z),
            (x, 3.5, REED_SHEAVE_Z),
            (x, 3.5, REED_TIE_Z + 3.5),
            (REED_RETURN_X + 6, 200, REED_TIE_Z - 3.5),
        ):
            pieces.append(box(4, 12, 12, (seat_x, y, z)))
            holes.append(
                cq.Workplane("YZ")
                .circle(1.3)
                .extrude(6)
                .translate((seat_x - 3, y, z))
            )
        pieces.append(box(4, 12, 168.5, (x, 3.5, 651.75)))
        pieces.append(box(4, 12, 175.5, (REED_RETURN_X + 6, 200, 648.25)))
        pieces.append(box(38, 12, 12, (-338, 200, REED_SHEAVE_Z)))
        pieces.append(box(20, 12, 12, (-345, 186, REED_SHEAVE_Z)))
        body = pieces[0]
        for p in pieces[1:]:
            body = body.union(p)
        for h in holes:
            body = body.cut(h)
        return body


class CordTransmission(AssemblyNode):
    left = SideCords(side=-1, anchor_x=-298.2)
    right = SideCords(side=1, anchor_x=311.8)
    reed = ReedCords()
