"""Unregistered development fixture for the inferred, common-shaft
head."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.node import AssemblyNode
from machinome.simulation import Driver
from machinome.motion.ports import RotationalPort

from .head import LoomInput, HeadDrive
from .timing import clip


class HeadBench(AssemblyNode):
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    angle = RotationalPort()
    input = LoomInput()
    head = HeadDrive()
    angle.drives(input.turn, offset=-270)
    input.turn.drives(head.angle)

    def render(self):
        self.input.translate([195, 180, 400])

    def simulate(self):
        self.angle = clip(self.phase + 360 * self.run * self.time, 0, 360)
