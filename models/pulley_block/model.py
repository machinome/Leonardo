"""Original three-part tackle: one rope, three supporting spans, 3:1
travel."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi

import cadquery as cq
from molejo import Shape, Circle, Line, Arc, P
from machinome.math import cos
from machinome.node import AssemblyNode, CadQueryNode, MolejoNode
from machinome.motion.joints import Prismatic, Revolute
from machinome.motion.ports import TranslationalPort
from machinome.simulation import Driver, Instruction


def box(x, y, z, at):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    return (
        cq.Workplane("XZ")
        .circle(radius)
        .extrude(length / 2, both=True)
        .translate(at)
    )


class TimberFrame(CadQueryNode):
    """Grounded stand with integral bearing supports and captive stub
    axles."""

    color = "#936640"

    def render(self):
        frame = box(190, 76, 8, (0, 0, 4))
        for x in (-82, 82):
            for y in (-22, 22):
                frame = frame.union(box(12, 12, 266, (x, y, 139)))
        for y in (-22, 22):
            frame = frame.union(box(176, 12, 12, (0, y, 266)))
        for x in (-36, 36):
            frame = frame.union(box(12, 52, 10, (x, 0, 262)))
            for y in (-7.3, 7.3):
                frame = frame.union(box(12, 4, 42, (x, y, 245)))
            frame = frame.union(axle(3, 20, (x, 0, 230)))
        return frame


class Sheave(CadQueryNode):
    color = "#d5aa59"
    linear_deflection = 0.015
    angular_deflection = 0.05
    spin = Revolute(axis=(0, 1, 0))

    def render(self):
        # Radial X / axial Y section. A 0.35 mm bottom gap under the
        # 1.25 mm rope is deliberate; sloped flanges capture axial
        # escape.
        section = [
            (3.25, -5),
            (20.7, -5),
            (20.7, -3.4),
            (16.4, -1.6),
            (16.4, 1.6),
            (20.7, 3.4),
            (20.7, 5),
            (3.25, 5),
        ]
        wheel = (
            cq.Workplane("XY")
            .polyline(section)
            .close()
            .revolve(360, (0, 0), (0, 1))
        )
        for angle in (0, 90, 180, 270):
            hole = axle(3.1, 12, (10, 0, 0)).rotate(
                (0, 0, 0), (0, 1, 0), angle
            )
            wheel = wheel.cut(hole)
        return wheel


class MovingCarrier(CadQueryNode):
    """One connected yoke, anchor-pin cheek and pinned load hanger."""

    color = "#526c70"

    def render(self):
        carrier = box(92, 20, 6, (-20, 0, -28))
        for y in (-7.3, 7.3):
            carrier = carrier.union(box(12, 4, 38, (0, y, -10)))
            carrier = carrier.union(box(12, 4, 18, (-18, y, -36)))
            carrier = carrier.union(box(4, 4, 50, (-66, y, -3)))
            carrier = carrier.union(box(14, 4, 4, (-61, y, 21)))
            carrier = carrier.union(box(4, 4, 8, (-58, y, 18)))
        carrier = carrier.union(axle(3, 20))
        carrier = carrier.union(axle(3, 20, (-18, 0, -39)))
        carrier = carrier.union(axle(2.5, 20, (-58, 0, 16)))
        # Tail socket faces down; the hairpin routes around the separate
        # anchor peg before entering the first supporting lane.
        socket = box(6, 14, 6, (-62, 0, 21))
        bore = (
            cq.Workplane("XY").circle(1.5).extrude(4.3).translate((-62, 0, 18))
        )
        return carrier.union(socket.cut(bore))


class DemonstratorLoad(CadQueryNode):
    color = "#b2a18a"
    linear_deflection = 0.015

    def render(self):
        eye = (
            cq.Workplane("XZ")
            .circle(6)
            .circle(3.3)
            .extrude(3, both=True)
            .translate((-18, 0, -39))
        )
        neck = box(6, 6, 10, (-18, 0, -46))
        weight = box(24, 20, 20, (-18, 0, -56))
        # Bore the complete joined eye/shank: the neck must not refill
        # the bottom sector of the eye's clearance around its support
        # pin.
        return eye.union(neck).union(weight).cut(axle(3.3, 8, (-18, 0, -39)))


class MovingBlock(AssemblyNode):
    lift = Prismatic(axis=(0, 0, 1), range=(0, 40))
    carrier = MovingCarrier()
    wheel = Sheave()
    load = DemonstratorLoad()
    lift.drives(wheel.spin, ratio=-2 * 180 / (18 * pi))


class EffortGrip(CadQueryNode):
    color = "#b56b43"
    travel = Prismatic(axis=(0, 0, 1), range=(-120, 0))
    linear_deflection = 0.015

    def render(self):
        socket = (
            cq.Workplane("XY").circle(3.5).extrude(12).translate((0, 0, -4))
        )
        bore = (
            cq.Workplane("XY").circle(1.5).extrude(9.3).translate((0, 0, -0.3))
        )
        ring = (
            cq.Workplane("XZ")
            .circle(8)
            .circle(5)
            .extrude(3, both=True)
            .translate((0, 0, -10))
        )
        return socket.cut(bore).union(ring)


class ContinuousRope(MolejoNode):
    color = "#d67432"
    top = TranslationalPort(unit="mm")
    end = TranslationalPort(unit="mm")

    def render(self):
        return Shape(
            Circle(1.25),
            [
                Line((0, 0, -6)),
                Arc((4, 0, -6), (0, -1, 0), pi),
                Line((8, 0, P.top)),
                Arc((26, 0, P.top), (0, 1, 0), pi),
                Line((44, 0, -22)),
                Arc((62, 0, -22), (0, -1, 0), pi),
                Line((80, 0, P.top)),
                Arc((98, 0, P.top), (0, 1, 0), pi),
                Line((116, 0, P.end)),
            ],
            path_samples=48,
            profile_samples=16,
        )


class PulleyBlock(AssemblyNode):
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    rise = TranslationalPort(unit="mm")
    frame = TimberFrame()
    first = Sheave()
    second = Sheave()
    block = MovingBlock()
    effort = EffortGrip()
    rope = ContinuousRope()

    rise.drives(block.lift)
    block.lift.drives(effort.travel, ratio=-3)
    block.lift.drives(first.spin, ratio=180 / (18 * pi))
    block.lift.drives(second.spin, ratio=3 * 180 / (18 * pi))

    instructions = {
        "Low": Instruction({"phase": 0, "run": 0}, duration=0.6),
        "Mid": Instruction({"phase": 90, "run": 0}, duration=0.6),
        "High": Instruction({"phase": 180, "run": 0}, duration=0.6),
        "Run": Instruction({"phase": 0, "run": 1}, duration=0.6),
    }

    def render(self):
        self.first.translate([-36, 0, 230])
        self.second.translate([36, 0, 230])
        self.block.translate([0, 0, 90])
        self.effort.translate([54, 0, 200])
        self.rope.translate([-62, 0, 112])

    def simulate(self):
        cosine = (1 - self.run) * cos(self.phase) + self.run * cos(
            self.phase + 360 * self.time
        )
        height = 20 * (1 - cosine)
        self.rise = height
        self.rope.top = 118 - height
        self.rope.end = 88 - 4 * height
        self.rope.translate([0, 0, height])
