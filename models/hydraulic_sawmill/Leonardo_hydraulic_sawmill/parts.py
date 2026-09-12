"""Original exact geometry for the Leonardo sawmill exhibit."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import cadquery as cq
from molejo import Shape, Circle, Line, P
from solid_node.node import CadQueryNode, MolejoNode
from solid_node.parameters import Length, Count, Flag
from solid_node.motion.joints import Revolute, Orbit
from solid_node.motion.ports import TranslationalPort
from .kinematics import CRANK, ROD, DRUM_RADIUS, TEETH

IRON = '#39464B'

def box(x, y, z, at=(0, 0, 0)):
    return cq.Workplane('XY').box(x, y, z).translate(at)

def cylinder_y(radius, length, at=(0, 0, 0)):
    return (cq.Workplane('XY').circle(radius).extrude(length)
            .rotate((0, 0, 0), (1, 0, 0), -90)
            .translate((at[0], at[1] - length / 2, at[2])))

def profile_xz(points, depth, y=0):
    return (cq.Workplane('XY').polyline(points).close().extrude(depth)
            .rotate((0, 0, 0), (1, 0, 0), 90)
            .translate((0, y + depth / 2, 0)))

def beam_between(a, b, width, depth):
    dx, dz = b[0] - a[0], b[2] - a[2]
    return (box(width, depth, math.hypot(dx, dz))
            .rotate((0, 0, 0), (0, 1, 0), math.degrees(math.atan2(dx, dz)))
            .translate(tuple((v + w) / 2 for v, w in zip(a, b))))

class Foundation(CadQueryNode):
    color = '#51443A'
    def render(self):
        return box(660, 390, 12, (0, -30, 6)).edges('|Z').chamfer(5)

class OakStructure(CadQueryNode):
    color = '#93623C'
    def render(self):
        shape = box(590, 14, 12, (0, 80, 18)).union(box(590, 14, 12, (0, -80, 18)))
        for x in (-240, 0, 240):
            shape = shape.union(box(18, 180, 12, (x, 0, 18)))
        for x in (-44, 44):
            for y in (-80, 80):
                shape = shape.union(box(18, 18, 448, (x, y, 248)))
            shape = shape.union(box(18, 180, 18, (x, 0, 470)))
        for y in (-80, 80):
            shape = shape.union(box(106, 18, 18, (0, y, 470)))
            for z in (310, 380):
                shape = shape.union(box(106, 18, 16, (0, y, z)))
                guide = box(28, 32, 16, (0, y / 80 * 67, z))
                guide = guide.cut(box(17.2, 9.2, 20, (0, y / 80 * 56, z)))
                shape = shape.union(guide)
            for sign in (-1, 1):
                shape = shape.union(beam_between((sign * 44, y, 364), (sign * 114, y, 282), 12, 12))
        for x in (-240, 240):
            for y in (-40, 40):
                shape = shape.union(box(18, 18, 252, (x, y, 150)))
            shape = shape.union(box(22, 118, 14, (x, 0, 277)))
        for y in (-40, 40):
            shape = shape.union(box(600, 12, 10, (0, y, 285)))
        for y in (-191, -111):
            stand = box(25, 18, 108, (0, y, 66)).union(box(42, 18, 18, (0, y, 120)))
            stand = stand.cut(cylinder_y(6.6, 24, (0, y, 120)))
            shape = shape.union(stand).union(box(18, abs(y) + 10, 1.5, (0, y / 2, 12.75)))
        for y in (-65, 65):
            stand = box(18, 16, 306, (240, y, 177)).union(box(32, 16, 18, (240, y, 330)))
            shape = shape.union(stand.cut(cylinder_y(5.6, 22, (240, y, 330))))
        floor = profile_xz([(-270, 263), (-22, 238), (-22, 244), (-270, 269)], 54, -151)
        for y in (-178, -124):
            floor = floor.union(profile_xz([(-270, 263), (-22, 238), (-22, 260), (-270, 285)], 6, y))
        shape = shape.union(floor)
        for y in (-174, -128):
            shape = shape.union(box(12, 12, 250, (-258, y, 138)))
        shape = shape.union(box(20, 116, 12, (-258, -126, 18)))
        return shape.cut(box(18, 116, 18, (0, 0, 285)))

class Wheel(CadQueryNode):
    color = '#B57B46'
    spin = Revolute(axis=(0, 1, 0))
    paddles = Count(16, min=12, max=24)
    def render(self):
        shape = cylinder_y(15, 60).cut(cylinder_y(6.6, 64))
        for y in (-25, 25):
            shape = shape.union(cylinder_y(100, 6, (0, y, 0)).cut(cylinder_y(88, 10, (0, y, 0))))
            for angle in range(0, 360, 45):
                shape = shape.union(box(11, 6, 84, (0, y, 48)).rotate((0, 0, 0), (0, 1, 0), angle))
        for i in range(self.paddles):
            shape = shape.union(box(6, 52, 17, (0, 0, 91)).rotate((0, 0, 0), (0, 1, 0), i * 360 / self.paddles))
        return shape.cut(box(4.4, 64, 8.8, (0, 0, 4.4)))

class WheelHoop(CadQueryNode):
    color = IRON
    spin = Revolute(axis=(0, 1, 0))
    def render(self):
        return cylinder_y(102.2, 4).cut(cylinder_y(100.4, 6))

class Crankshaft(CadQueryNode):
    color = IRON
    spin = Revolute(axis=(0, 1, 0))
    def render(self):
        shape = cylinder_y(6, 110, (0, -149, 0))
        disk = cylinder_y(32, 8, (0, -97, 0))
        for a in (70, 190, 310):
            disk = disk.cut(cylinder_y(6, 12, (18 * math.sin(math.radians(a)), -97, 18 * math.cos(math.radians(a)))))
        shape = shape.union(box(3.2, 50, 2.8, (0, -151, 6.4)))
        return shape.union(disk).union(cylinder_y(4.2, 21, (0, -86.5, CRANK)))

class ConnectingRod(CadQueryNode):
    color = '#B5955F'
    lean = Revolute(axis=(0, 1, 0))
    orbit = Orbit(axis=(0, 1, 0), at=(0, 0, -CRANK))
    def render(self):
        shape = box(8, 6, ROD, (0, 0, ROD / 2))
        for z in (0, ROD):
            shape = shape.union(cylinder_y(9, 6, (0, 0, z))).cut(cylinder_y(4.8, 10, (0, 0, z)))
        return shape

class SashWood(CadQueryNode):
    color = '#784938'
    def render(self):
        shape = box(16, 120, 10).union(box(16, 120, 10, (0, 0, 156)))
        for y in (-56, 56):
            shape = shape.union(box(16, 8, 156, (0, y, 78)))
        return shape.cut(cylinder_y(4.8, 124))

class SawBlade(CadQueryNode):
    color = '#9BA8A7'
    def render(self):
        points = [(-5, 5.6), (5, 5.6)]
        for z in range(8, 146, 6):
            points.extend([(5, z), (10, z + 1), (5, z + 4)])
        points.extend([(5, 150.4), (-5, 150.4)])
        return profile_xz(points, 1.2)

class SashPin(CadQueryNode):
    color = IRON
    def render(self):
        return cylinder_y(4.2, 43, (0, -70.5, 0)).union(cylinder_y(7, 2, (0, -92, 0)))

class CarriageBed(CadQueryNode):
    color = '#A57348'
    def render(self):
        shape = box(360, 12, 10, (0, -29, 319.4)).union(box(360, 12, 10, (0, 29, 319.4)))
        for x in (-125, 125):
            shape = shape.union(box(18, 100, 10, (x, 0, 319.4)))
            for y in (-29, 29):
                bracket = box(16, 10, 19, (x, y, 308.8)).cut(cylinder_y(3.6, 15, (x, y, 302.2)))
                shape = shape.union(bracket)
        shape = shape.union(box(14, 66, 10, (174, 0, 319.4)))
        shape = shape.union(box(14, 10, 16, (174, 0, 310.4)))
        return shape.cut(cq.Workplane('YZ').circle(1.5).extrude(20).translate((164, 0, 330 - DRUM_RADIUS - 1.2)))

class CarriageWheel(CadQueryNode):
    color = IRON
    spin = Revolute(axis=(0, 1, 0))
    def render(self):
        return cylinder_y(12, 8).cut(cylinder_y(3.6, 12))

class CarriageAxle(CadQueryNode):
    color = IRON
    def render(self):
        return cylinder_y(3, 96)

class LogHalf(CadQueryNode):
    color = '#745238'
    positive = Flag(True)
    kerf = Length(3.2, min=2.0, max=5.0)
    def render(self):
        points = []
        for i in range(32):
            a = 2 * math.pi * i / 32
            radius = 28 + 0.6 * math.sin(5 * a) ** 2
            points.append((radius * math.cos(a), radius * math.sin(a)))
        shape = cq.Workplane('YZ').polyline(points).close().extrude(350).translate((-175, 0, 353.2))
        cut_y = (-100 + self.kerf / 2) if self.positive else (100 - self.kerf / 2)
        return shape.cut(box(354, 200, 100, (0, cut_y, 353.2)))

class EndGrain(CadQueryNode):
    color = '#D5AD73'
    positive = Flag(True)
    kerf = Length(3.2, min=2.0, max=5.0)
    def render(self):
        shape = cq.Workplane('YZ').circle(27.7).extrude(0.5)
        for r in (6, 11, 17, 23):
            groove = cq.Workplane('YZ').circle(r + 0.25).circle(r).extrude(0.25).translate((0.3, 0, 0))
            shape = shape.cut(groove)
        cut_y = (-100 + self.kerf / 2) if self.positive else (100 - self.kerf / 2)
        return shape.cut(box(4, 200, 100, (0, cut_y, 0)))

class RatchetDrum(CadQueryNode):
    color = IRON
    spin = Revolute(axis=(0, 1, 0))
    def render(self):
        shape = cylinder_y(5, 192, (0, 22, 0)).union(cylinder_y(DRUM_RADIUS, 18))
        for y in (-11, 11):
            shape = shape.union(cylinder_y(DRUM_RADIUS + 4, 4, (0, y, 0)))
        points = []
        for i in range(TEETH):
            for da, r in ((0, 34), (0.7, 39), (360 / TEETH - 0.7, 34)):
                a = math.radians(i * 360 / TEETH + da)
                points.append((r * math.sin(a), r * math.cos(a)))
        gear = profile_xz(points, 6, 105)
        for a in (45, 135, 225, 315):
            gear = gear.cut(cylinder_y(8, 10, (21 * math.sin(math.radians(a)), 105, 21 * math.cos(math.radians(a)))))
        return shape.union(gear)

class PawlCarrier(CadQueryNode):
    color = '#BA8845'
    spin = Revolute(axis=(0, 1, 0))
    def render(self):
        shape = cylinder_y(10, 5, (0, 115, 0)).cut(cylinder_y(5.6, 8, (0, 115, 0)))
        shape = shape.union(box(7, 5, 43, (-2, 115, 24)))
        shape = shape.union(cylinder_y(2, 15, (-2, 109, 45)))
        return shape.cut(cylinder_y(5.6, 8, (0, 115, 0)))

class Pawl(CadQueryNode):
    color = '#C7A061'
    lift = Revolute(axis=(0, 1, 0), at=(-2, 0, 45))
    carry = Revolute(axis=(0, 1, 0))
    def render(self):
        shape = profile_xz([(-0.9, 35.5), (-0.9, 42), (1.5, 48), (-4, 49), (-7, 44)], 4, 105)
        return shape.cut(cylinder_y(2.5, 8, (-2, 105, 45)))

class HaulRope(MolejoNode):
    color = '#D3B989'
    reach = TranslationalPort(unit='mm')
    def render(self):
        return Shape(profile=Circle(radius=1.1), path=[Line(to=(0, 0, P.reach))], path_samples=2, profile_samples=10)

class Tailrace(CadQueryNode):
    color = '#527F88'
    def render(self):
        return box(525, 56, 2, (37.5, -151, 15))

class FlumeWater(CadQueryNode):
    color = '#73A2AB'
    def render(self):
        return profile_xz([(-266, 269.3), (-24, 244.9), (-24, 246.1), (-266, 270.5)], 45, -151)

class Plaque(CadQueryNode):
    color = '#B6945C'
    def render(self):
        plate = box(156, 35, 2, (190, -204, 13.2)).edges('|Z').chamfer(2)
        lettering = cq.Workplane('XY').text('LEONARDO / 1078r', 7, 0.6).translate((190, -204, 13.7))
        return plate.cut(lettering)
