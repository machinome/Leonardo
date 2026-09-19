"""Continuous material route: unwinding warp, upper guide and wound cloth.

The finite winding coordinate changes wrapped material length. Yarn forces,
compaction and newly interlacing material are not solved by this construction.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
from molejo import Shape, Circle, Polygon, Line, Arc, P
from machinome.node import AssemblyNode, MolejoNode
from machinome.parameters import Count
from machinome.motion.joints import Free, Prismatic
from machinome.motion.ports import RotationalPort, TranslationalPort
from machinome.math import sin, cos
from .parts import ClothPick
from .winding import CENTERS

BEAM_PITCH = 14.8
GUIDE_PITCH = 4.8
FRONT_Y = 72 - CENTERS
CLOTH_GUIDE = FRONT_Y + BEAM_PITCH + GUIDE_PITCH
CLOTH_RUN = 45 - CLOTH_GUIDE
TANGENT = math.degrees(math.atan2(313.2, 233) - math.acos(10 / math.hypot(233, 313.2)))
GUIDE_CONTACT_Y = 233 + GUIDE_PITCH * math.cos(math.radians(TANGENT))
GUIDE_CONTACT_Z = 313.2 + GUIDE_PITCH * math.sin(math.radians(TANGENT))


class WarpSupply(MolejoNode):
    low_y = TranslationalPort()
    low_z = TranslationalPort()
    high_y = TranslationalPort()
    high_z = TranslationalPort()
    guide_y = TranslationalPort()
    guide_z = TranslationalPort()
    wrap = RotationalPort(unit="rad")
    color = "#d2c29c"

    def render(self):
        return Shape(
            Circle(0.48),
            [
                Arc((0, P.low_y, P.low_z), (1, 0, 0), P.wrap),
                Line((0, P.high_y, P.high_z)),
                Arc((0, P.guide_y, P.guide_z), (1, 0, 0), math.radians(90 - TANGENT)),
            ],
            path_samples=180,
            profile_samples=8,
        )


class WarpAnchor(AssemblyNode):
    pose = Free()
    cord = WarpSupply()


class WarpRollEnd(AssemblyNode):
    unwind = RotationalPort()
    anchor = WarpAnchor()
    unwind.drives(
        anchor.pose.y, law=lambda a, b: lambda t: BEAM_PITCH * cos(TANGENT - 180 + t)
    )
    unwind.drives(
        anchor.pose.z, law=lambda a, b: lambda t: BEAM_PITCH * sin(TANGENT - 180 + t)
    )
    unwind.drives(
        anchor.cord.low_y,
        law=lambda a, b: lambda t: -BEAM_PITCH * cos(TANGENT - 180 + t),
    )
    unwind.drives(
        anchor.cord.low_z,
        law=lambda a, b: lambda t: -BEAM_PITCH * sin(TANGENT - 180 + t),
    )
    unwind.drives(
        anchor.cord.high_y,
        law=lambda a, b: lambda t: GUIDE_CONTACT_Y
        - BEAM_PITCH * cos(TANGENT - 180 + t),
    )
    unwind.drives(
        anchor.cord.high_z,
        law=lambda a, b: lambda t: GUIDE_CONTACT_Z
        - BEAM_PITCH * sin(TANGENT - 180 + t),
    )
    unwind.drives(
        anchor.cord.guide_y,
        law=lambda a, b: lambda t: 233 - BEAM_PITCH * cos(TANGENT - 180 + t),
    )
    unwind.drives(
        anchor.cord.guide_z,
        law=lambda a, b: lambda t: 313.2 - BEAM_PITCH * sin(TANGENT - 180 + t),
    )
    unwind.drives(anchor.cord.wrap, ratio=-math.pi / 180, offset=math.pi)


class ClothWeb(MolejoNode):
    wrap = RotationalPort(unit="rad")
    color = "#bdae87"

    def render(self):
        return Shape(
            Polygon([(-72, -0.25), (72, -0.25), (72, 0.25), (-72, 0.25)]),
            [
                Line((0, -CLOTH_RUN, 0)),
                Arc((0, -CLOTH_RUN, -GUIDE_PITCH), (1, 0, 0), math.pi / 2),
                Line((0, -CLOTH_RUN - GUIDE_PITCH, -414)),
                Arc((0, FRONT_Y - 45, -414), (1, 0, 0), P.wrap),
            ],
            path_samples=160,
            profile_samples=4,
        )


class TravellingPick(AssemblyNode):
    parity = Count(0)
    travel = Prismatic(axis=(0, 1, 0))
    yarn = ClothPick(parity=parity)
