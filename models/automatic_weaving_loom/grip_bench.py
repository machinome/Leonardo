"""Fixture for both real gripping hands and the opposed selector
ramps."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.node.assembly import AssemblyNode
from machinome.simulation import Driver
from machinome.motion.ports import RotationalPort

from .head import GrippingCarrier, Selector, reaches, selector_lift
from .timing import clip


class GripBench(AssemblyNode):
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    angle = RotationalPort()
    carrier = GrippingCarrier()
    selector_a = Selector(side=-1)
    selector_b = Selector(side=1)
    angle.drives(carrier.handoff)
    angle.drives(carrier.left.slide, law=lambda a, b: lambda t: reaches(t)[0])
    angle.drives(carrier.right.slide, law=lambda a, b: lambda t: reaches(t)[1])
    angle.drives(
        selector_a.rise, law=lambda a, b: lambda t: selector_lift(t, -1)
    )
    angle.drives(
        selector_b.rise, law=lambda a, b: lambda t: selector_lift(t, 1)
    )
    (selector_a.rise & carrier.left.slide).drives(
        carrier.left.jaw.opening,
        law=lambda a, b: lambda z, x: clip(z + 0.5 * x, 0, 14),
    )
    (selector_b.rise & carrier.right.slide).drives(
        carrier.right.jaw.opening,
        law=lambda a, b: lambda z, x: -clip(z - 0.5 * x, 0, 14),
    )

    def render(self):
        self.carrier.translate([0, 115, 520])
        self.selector_a.translate([-18, 180, 414])
        self.selector_b.translate([18, 180, 414])

    def simulate(self):
        self.angle = clip(self.phase + 360 * self.run * self.time, 0, 360)
