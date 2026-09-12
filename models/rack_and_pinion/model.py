"""Leonardo's rack-lifting study, interpreted as an original desktop machine."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi

import cadquery as cq
from solid_node.math import cos
from solid_node.node import AssemblyNode, CadQueryNode, FusionNode
from solid_node.parameters import Length
from solid_node.motion.joints import Prismatic, Revolute
from solid_node.motion.ports import RotationalPort
from solid_node.simulation import Driver, Instruction

from .profiles import hook_outline, pinion_outline, rack_outline


def box(x, y, z, at=(0, 0, 0)):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    return cq.Workplane("XZ").circle(radius).extrude(length / 2, both=True).translate(at)


class TimberStand(CadQueryNode):
    module = Length(min=2.5, max=3.5)
    color = "#93633f"

    def render(self):
        m = self.module
        frame = box(64*m, 36*m, 4*m, (6*m, 0, 2*m))
        for x in (-16*m, 28*m):
            for y in (-6*m, 6*m):
                frame = frame.union(box(5*m, 5*m, 114*m, (x, y, 60*m)))
        for y in (-6*m, 6*m):
            for z in (12*m, 114*m):
                frame = frame.union(box(49*m, 5*m, 5*m, (6*m, y, z)))
            frame = frame.union(box(24*m, 5*m, 7*m, (-6*m, y, 80*m)))
        for z in (64*m, 102*m):
            sleeve = box(21*m, 8*m, 4*m, (18.5*m, 0, z))
            # The rectangular channel surrounds even the tooth tips;
            # its backing and side cheeks guide the complete rack.
            channel = box(7.2*m, 4.2*m, 6*m, (12.5*m, 0, z))
            frame = frame.union(sleeve.cut(channel))
        return frame.cut(axle(1.7*m, 24*m, (0, 0, 80*m)))


class PinionProfile(CadQueryNode):
    module = Length(min=2.5, max=3.5)
    linear_deflection = 0.01
    angular_deflection = 0.04

    def render(self):
        m = self.module
        gear = cq.Workplane("XZ").polyline(pinion_outline(m)).close().extrude(2*m, both=True)
        for angle in (0, 90, 180, 270):
            hole = axle(1.8*m, 6*m, (5.5*m, 0, 0))
            gear = gear.cut(hole.rotate((0, 0, 0), (0, 1, 0), angle))
        return gear


class CapturedAxle(CadQueryNode):
    module = Length(min=2.5, max=3.5)

    def render(self):
        m = self.module
        shaft = axle(1.6*m, 20*m)
        for y in (-8.95*m, 8.95*m):
            shaft = shaft.union(axle(2.7*m, 0.7*m, (0, y, 0)))
        return shaft


class CrankWeb(CadQueryNode):
    module = Length(min=2.5, max=3.5)

    def render(self):
        m = self.module
        return box(14*m, 2*m, 2.4*m, (-6.5*m, -10.4*m, 0)).union(
            axle(2.5*m, 2*m, (0, -10.4*m, 0)))


class CrankGrip(CadQueryNode):
    module = Length(min=2.5, max=3.5)

    def render(self):
        m = self.module
        return axle(1.4*m, 8*m, (-13*m, -14*m, 0))


class HandCrank(FusionNode):
    module = Length(min=2.5, max=3.5)
    web = CrankWeb(module=module)
    grip = CrankGrip(module=module)


class Pinion(FusionNode):
    module = Length(min=2.5, max=3.5)
    color = "#d3a755"
    linear_deflection = 0.01
    angular_deflection = 0.04
    spin = Revolute(axis=(0, -1, 0))
    profile = PinionProfile(module=module)
    shaft = CapturedAxle(module=module)
    crank = HandCrank(module=module)


class RackBar(CadQueryNode):
    module = Length(min=2.5, max=3.5)

    def render(self):
        return cq.Workplane("XZ").polyline(rack_outline(self.module)).close().extrude(2*self.module, both=True)


class RackHook(CadQueryNode):
    module = Length(min=2.5, max=3.5)

    def render(self):
        m = self.module
        curve = cq.Workplane("XZ").polyline(hook_outline(m)).close().extrude(m, both=True)
        return curve.union(box(2*m, 2*m, 9*m, (14*m, 0, -52*m)))


class StopShoulders(CadQueryNode):
    """A connected backing rib with a shoulder at either travel limit."""
    module = Length(min=2.5, max=3.5)

    def render(self):
        m = self.module
        rib = box(m, 2*m, 76*m, (15.4*m, 0, -9*m))
        for z in (-45*m, 27*m):
            rib = rib.union(box(5*m, 4*m, 4*m, (17.5*m, 0, z)))
        return rib


class Rack(FusionNode):
    module = Length(min=2.5, max=3.5)
    color = "#536c73"
    bar = RackBar(module=module)
    hook = RackHook(module=module)
    stops = StopShoulders(module=module)


class DemonstratorWeight(CadQueryNode):
    module = Length(min=2.5, max=3.5)
    color = "#a9947a"
    linear_deflection = 0.02
    angular_deflection = 0.04

    def render(self):
        m = self.module
        eye = (cq.Workplane("YZ").circle(3.2*m).circle(1.8*m)
               .extrude(m, both=True).translate((18*m, 0, -60.1*m)))
        return eye.union(box(8*m, 6*m, 8*m, (18*m, 0, -67*m)))


class LiftCarriage(AssemblyNode):
    module = Length(min=2.5, max=3.5)
    slide = Prismatic(axis=(0, 0, 1), range=lambda n: (0, 24*n.module + 1e-9))
    rack = Rack(module=module)
    load = DemonstratorWeight(module=module)


class RackAndPinion(AssemblyNode):
    module = Length(3, min=2.5, max=3.5)
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    crank_angle = RotationalPort(unit="deg")
    frame = TimberStand(module=module)
    pinion = Pinion(module=module)
    carriage = LiftCarriage(module=module)
    crank_angle.drives(pinion.spin)
    pinion.spin.drives(carriage.slide, ratio=10*module*pi/180)

    instructions = {
        "Bottom": Instruction({"phase": 0, "run": 0}, duration=0.6),
        "Mid-lift": Instruction({"phase": 90, "run": 0}, duration=0.6),
        "Top": Instruction({"phase": 180, "run": 0}, duration=0.6),
        "Run": Instruction({"phase": 0, "run": 1}, duration=0.6),
    }

    def render(self):
        self.pinion.translate([0, 0, 80*self.module])
        self.carriage.translate([0, 0, 80*self.module])

    def simulate(self):
        # Both terms close at t=0/1. Fractional run changes excursion,
        # not timeline speed, so all slider combinations loop continuously.
        cosine = (1-self.run)*cos(self.phase) + self.run*cos(self.phase + 360*self.time)
        self.crank_angle = (24/10) * (180/pi) * (1-cosine)/2
