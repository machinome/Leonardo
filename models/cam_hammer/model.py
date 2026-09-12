"""Astra's original cam hammer: cam contact with a prescribed released drop."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq

from solid_node.node import AssemblyNode, CadQueryNode, FusionNode
from solid_node.parameters import Angle
from solid_node.motion.joints import Revolute
from solid_node.motion.ports import RotationalPort
from solid_node.simulation import Driver, Instruction

from .kinematics import cam_outline, follower_law


def box(x, y, z, at=(0, 0, 0)):
    return cq.Workplane("XY").box(x, y, z).translate(at)


def axle(radius, length, at=(0, 0, 0)):
    return cq.Workplane("XZ").circle(radius).extrude(length / 2, both=True).translate(at)


class TimberFrame(CadQueryNode):
    color = "#93633f"

    def render(self):
        frame = box(290, 130, 12, (0, 0, 6))
        for y in (-24, 24):
            # Offset the column, with a bearing beam at its top, so the
            # shoe is visible along the shaft as well as isometrically.
            frame = frame.union(box(22, 18, 176, (-108, y, 96)))
            frame = frame.union(box(78, 18, 22, (-80, y, 170)))
            frame = frame.union(box(22, 18, 122, (0, y, 67)))
            frame = frame.union(box(130, 18, 14, (-54, y, 28)))
            # Overlapping diagonal timber brace into each tall post/base.
            brace = box(14, 18, 94).rotate((0, 0, 0), (0, 1, 0), 17)
            frame = frame.union(brace.translate((-121, y, 56)))
        frame = frame.cut(axle(5.35, 90, (-60, 0, 170)))
        return frame.cut(axle(5.35, 90, (0, 0, 110)))


class CapturedShaft(CadQueryNode):
    """10 mm journal with collars 0.3 mm clear of the post outer faces."""

    def render(self):
        shaft = axle(5, 80)
        for y in (-34, 34):
            shaft = shaft.union(axle(9, 1.4, (0, y, 0)))
        return shaft


class CamProfile(CadQueryNode):
    lift_angle = Angle(min=16, max=20)
    linear_deflection = 0.025
    angular_deflection = 0.04

    def render(self):
        cam = cq.Workplane("XZ").polyline(cam_outline(self.lift_angle)).close().extrude(5, both=True)
        # Three open windows make the shaft and direction easy to follow.
        for angle in (30, 150, 270):
            window = axle(9, 14, (25, 0, 0)).rotate((0, 0, 0), (0, 1, 0), angle)
            cam = cam.cut(window)
        return cam


class HandCrank(CadQueryNode):
    def render(self):
        arm = box(39, 6, 10, (17, -42, 0))
        arm = arm.union(axle(9, 6, (0, -42, 0)))
        return arm.union(axle(4.5, 26, (35, -55, 0)))


class Cam(FusionNode):
    color = "#c89a51"
    lift_angle = Angle(min=16, max=20)
    spin = Revolute(axis=(0, -1, 0))
    profile = CamProfile(lift_angle=lift_angle)
    shaft = CapturedShaft()
    crank = HandCrank()


class LeverCore(CadQueryNode):
    def render(self):
        # Recess the tail behind the rounded shoe: the cam's retreating
        # flank sweeps across this region during release. This keeps an
        # 8 mm deep continuous arm below that envelope.
        outline = [(-60, -4), (-48, -10), (-16, -10), (0, -4),
                   (111, -4), (111, 4), (0, 4), (-16, -2),
                   (-48, -2), (-60, 3)]
        beam = cq.Workplane("XZ").polyline(outline).close().extrude(5, both=True)
        return beam.union(axle(10, 12))


class FollowerShoe(CadQueryNode):
    linear_deflection = 0.01
    angular_deflection = 0.03

    def render(self):
        return axle(6, 12)


class HammerHead(CadQueryNode):
    def render(self):
        return box(24, 24, 28)


class HammerLever(FusionNode):
    color = "#46575e"
    linear_deflection = 0.01
    angular_deflection = 0.03
    swing = Revolute(axis=(0, -1, 0), range=(0, 20.001))
    core = LeverCore()
    shoe = FollowerShoe()
    head = HammerHead()
    shaft = CapturedShaft()

    def render(self):
        self.shoe.translate([-60, 0, 0])
        self.head.translate([100, 0, -5])


class Anvil(CadQueryNode):
    color = "#67787e"

    def render(self):
        # Foot seats 0.2 mm above the frame; face is exactly z=91.
        foot = box(54, 48, 8, (100, 0, 16.2))
        waist = box(22, 24, 65, (100, 0, 51))
        face = box(36, 34, 12, (100, 0, 85))
        return foot.union(waist).union(face)


class CamHammer(AssemblyNode):
    lift_angle = Angle(18, min=16, max=20)
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    cycle = RotationalPort()
    frame = TimberFrame()
    cam = Cam(lift_angle=lift_angle)
    lever = HammerLever()
    anvil = Anvil()
    cycle.drives(cam.spin)
    cycle.drives(lever.swing, law=follower_law)

    instructions = {
        "Lift": Instruction({"phase": 120, "run": 0}, duration=0.6),
        "Release": Instruction({"phase": 250, "run": 0}, duration=0.6),
        "Strike": Instruction({"phase": 320, "run": 0}, duration=0.6),
        "Run": Instruction({"phase": 0, "run": 1}, duration=0.6),
    }

    def render(self):
        self.cam.translate([-60, 0, 170])
        self.lever.translate([0, 0, 110])

    def simulate(self):
        self.cycle = self.phase + 360 * self.run * self.time
