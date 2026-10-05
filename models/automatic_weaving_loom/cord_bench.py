"""Fixture for measuring the flexible haul, return and winding
geometry."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

from machinome.node.assembly import AssemblyNode
from machinome.simulation import Driver
from machinome.motion.ports import RotationalPort

from .head import reaches
from .cords import CordTransmission
from .textile import WarpRollEnd, ClothWeb
from .timing import clip, index_angle
from .reeding import reed_lift


class CordBench(AssemblyNode):
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    angle = RotationalPort()
    winding = RotationalPort()
    cords = CordTransmission()
    warp = WarpRollEnd()
    cloth = ClothWeb()
    angle.drives(
        cords.left.lift, law=lambda a, b: lambda t: reaches(t)[0] + 65
    )
    angle.drives(
        cords.right.lift, law=lambda a, b: lambda t: 65 - reaches(t)[1]
    )
    angle.drives(cords.left.travel, law=lambda a, b: lambda t: reaches(t)[0])
    angle.drives(cords.right.travel, law=lambda a, b: lambda t: reaches(t)[1])
    angle.drives(cords.reed.lift, law=lambda a, b: reed_lift)
    angle.drives(
        winding,
        law=lambda a, b: lambda t: index_angle(t)
        * 0.5
        * 0.06
        / 48
        * 180
        / math.pi,
    )
    winding.drives(warp.unwind)
    winding.drives(cloth.wrap, ratio=-math.pi / 180, offset=-math.pi / 2)

    def render(self):
        self.warp.translate([0, 72, 202])
        self.cloth.translate([0, 45, 520])

    def simulate(self):
        self.angle = clip(self.phase + 1440 * self.run * self.time, 0, 1440)
