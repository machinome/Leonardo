"""One-pin / six / twelve intermittent drive, original reconstructed
surfaces.

The tooth counts come from Atlanticus 985r. Radial pin slots,
complementary
dwell lands and cycloidal flanks are the explicit geometric completion
used
here; the manuscript does not dimension those concealed contact
surfaces.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq
from machinome.node import AssemblyNode, CadQueryNode
from machinome.motion.joints import Revolute
from machinome.motion.ports import RotationalPort
from machinome.simulation import Driver
from machinome.math import sin, cos, sqrt, atan2

from .profiles import cycloidal_outline, polar


def cylinder(radius, start, end, y=0, z=0):
    return (
        cq.Workplane("YZ")
        .circle(radius)
        .extrude(end - start)
        .translate((start, y, z))
    )


def shaft():
    core = cylinder(3, -16, 21)
    core = core.union(cylinder(6, -16, -12.3))
    core = core.union(cylinder(6, -3.7, -2.7))
    core = core.union(cylinder(9.3, 19, 21))
    return core.union(cylinder(0.9, 20.5, 22.5, y=8))


def clip(value, low, high):
    return (
        low + high + sqrt((value - low) ** 2) - sqrt((value - high) ** 2)
    ) / 2


def index_angle(angle):
    """Pin-in-radial-slot closure, summed over the bounded four-turn
    exhibit."""
    total = 0
    for cycle in range(4):
        local = clip(angle - 180 - 360 * cycle, -60, 60)
        total += 30 + atan2(12 * sin(local), 24 - 12 * cos(local))
    return total


class TimingBearings(CadQueryNode):
    color = "#755137"

    def render(self):
        body = cq.Workplane("XY").box(8, 80, 14).translate((-8, -27, 0))
        body = body.union(
            cq.Workplane("XY").box(8, 14, 38).translate((-8, 0, 12))
        )
        for y, z in ((0, 24), (0, 0), (-54, 0)):
            body = body.cut(cylinder(3.3, -13, -3, y=y, z=z))
        return body


class SingleToothInput(CadQueryNode):
    color = "#b2854d"
    turn = Revolute(axis=(1, 0, 0))

    def render(self):
        body = shaft().union(cylinder(13.8, 16.6, 20))
        body = body.union(cylinder(1.5, 6.2, 18, y=12))
        locking = cylinder(11, 12, 15)
        locking = locking.cut(cylinder(9.6, 11, 16, y=12))
        return body.union(locking)


class SixToothWheel(CadQueryNode):
    color = "#9f7140"
    turn = Revolute(axis=(1, 0, 0))

    def render(self):
        gear = (
            cq.Workplane("YZ")
            .polyline(cycloidal_outline(6))
            .close()
            .extrude(6)
        )
        star = cylinder(20.7, 6.3, 11)
        for i in range(6):
            # Slots are radial: their centerline sweeps with the actual
            # pin.
            slot = cq.Workplane("XY").box(7, 26, 3.6).translate((8.5, 23, 0))
            star = star.cut(slot.rotate((0, 0, 0), (1, 0, 0), 210 + 60 * i))
        lands = cylinder(20.7, 12, 15)
        for i in range(6):
            y, z = polar(24, 180 + 60 * i)
            lands = lands.cut(cylinder(11.3, 11, 16, y, z))
            slot = cq.Workplane("XY").box(7, 26, 3.6).translate((13.5, 23, 0))
            lands = lands.cut(slot.rotate((0, 0, 0), (1, 0, 0), 210 + 60 * i))
        return shaft().union(gear).union(star).union(lands)


class TwelveToothWheel(CadQueryNode):
    color = "#b28b53"
    turn = Revolute(axis=(1, 0, 0))

    def render(self):
        gear = (
            cq.Workplane("YZ")
            .polyline(cycloidal_outline(12))
            .close()
            .extrude(6)
        )
        return shaft().union(gear)


class TimingTrain(AssemblyNode):
    angle = RotationalPort()
    input = SingleToothInput()
    six = SixToothWheel()
    twelve = TwelveToothWheel()
    bearings = TimingBearings()
    angle.drives(input.turn, offset=-270)
    input.turn.drives(
        six.turn, law=lambda a, b: lambda t: -index_angle(t + 270) - 90
    )
    six.turn.drives(twelve.turn, ratio=-0.5, offset=-45)

    def render(self):
        self.input.translate([0, 0, 24])
        self.twelve.translate([0, -54, 0])


class TimingBench(AssemblyNode):
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    drive = RotationalPort()
    train = TimingTrain()
    drive.drives(train.angle)

    def simulate(self):
        self.drive = clip(self.phase + 360 * self.run * self.time, 0, 1440)
