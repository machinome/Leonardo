"""Explicit inferred completion of the concealed weaving-head
transmission.

Seven captured face-cam tracks on the common shaft drive two heddles,
two
5:1 slotted rocking levers, the reed and two grip selectors. The lever
and
cord closure, not a second animation clock, determines each carrier's
travel.
These concealed profiles are our construction, not observed museum
details.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import cadquery as cq
from molejo import Shape, Polygon, Spline, P
from machinome.node.assembly import AssemblyNode
from machinome.node.cadquery import CadQueryNode
from machinome.node.fusion import FusionNode
from machinome.node.molejo import MolejoNode
from machinome.parameters import Length, Scalar, Count
from machinome.motion.joints import Revolute, Prismatic
from machinome.motion.ports import RotationalPort, TranslationalPort
from machinome.math import sin, cos, sqrt, asin, atan2

from .timing import SingleToothInput, cylinder, clip
from .winding import FeedTimingTrain
from .parts import (
    box,
    axle,
    HeddleCage,
    CarrierArm,
    WeftSpool,
    Reed,
    shuttle_x,
)
from .profiles import polar
from .reeding import (
    REED_CAM_X,
    REED_CAM_BASE,
    REED_TIE_X,
    REED_TIE_Z,
    REED_TRAVEL,
    reed_lift,
)


def reaches(angle):
    x = shuttle_x(angle)
    distance = sqrt(x * x)
    # Both hands must clear the entire ribbon before the shed closes.
    # The empty hand's initial release retreat continues into full
    # parking.
    return -distance, distance


def arm_radius(angle, side):
    left, right = reaches(angle)
    return 26 + (130 + (left if side < 0 else -right)) / 5


def selector_lift(angle, side):
    p = 180 + atan2(sin(angle - 180), cos(angle - 180))

    def rise(start, end):
        return (1 - cos(180 * clip((p - start) / (end - start), 0, 1))) / 2

    if side < 0:
        return 14 * (rise(95, 120) - rise(240, 265))
    return 14 * (1 - rise(60, 85) + rise(275, 300))


def shed_fraction(angle):
    p = 180 + atan2(sin(angle - 180), cos(angle - 180))

    def rise(start, end):
        return (1 - cos(180 * clip((p - start) / (end - start), 0, 1))) / 2

    # Early opening and a full-shed dwell keep the lower support fingers
    # clear of real warp surfaces during both entry and exit.
    return rise(0, 50) - rise(130, 180) - rise(180, 230) + rise(310, 360)


def face_cam(x, radius_law, maximum, groove_half_width=2.5):
    body = cylinder(maximum + 4, x - 1, x + 4)
    outlines = []
    for side in (1, -1):
        points = [
            polar(float(radius_law(angle)) + side * groove_half_width, -angle)
            for angle in range(360)
        ]
        outlines.append(
            cq.Workplane("YZ")
            .polyline(points)
            .close()
            .extrude(4.2)
            .translate((x, 0, 0))
        )
    groove = outlines[0].cut(outlines[1])
    return body.cut(groove)


def reed_cam(x):
    # Offset the roller-centre path normally, not merely radially: on
    # the
    # steep beat flanks a radial band would pinch the physical roller.
    points = [
        polar(REED_CAM_BASE + float(reed_lift(i)), -i) for i in range(360)
    ]
    outlines = [
        cq.Workplane("YZ")
        .spline(points, periodic=True)
        .close()
        .offset2D(offset, "arc")
        .extrude(4.2)
        .translate((x, 0, 0))
        for offset in (1.65, -1.65)
    ]
    return cylinder(REED_CAM_BASE + REED_TRAVEL + 4, x - 1, x + 4).cut(
        outlines[0].cut(outlines[1])
    )


class LoomInput(SingleToothInput):
    shed_lift = Length(18, min=16, max=20)

    def render(self):
        body = super().render()
        body = body.union(cylinder(5, -585, -16.3)).union(
            cylinder(3, -18, -15)
        )
        # Coordinates in this component are relative to the right drive
        # face.
        cams = [
            (
                -152.5,
                lambda a: 42 + self.shed_lift * shed_fraction(a),
                42 + self.shed_lift,
            ),
            (
                137.5,
                lambda a: 42 - self.shed_lift * shed_fraction(a),
                42 + self.shed_lift,
            ),
            (-235, lambda a: arm_radius(a, -1), 52),
            (235, lambda a: arm_radius(a, 1), 52),
            (-24.8, lambda a: 42 + selector_lift(a, -1), 56),
            (11.2, lambda a: 42 + selector_lift(a, 1), 56),
        ]
        # The right arm cam lies beyond the timing train on the same
        # shaft.
        body = body.union(cylinder(3, 20, 49))
        for x, law, maximum in cams:
            body = body.union(
                face_cam(x - 195, law, maximum, 2.6 if abs(x) == 235 else 2.5)
            )
        body = body.union(reed_cam(REED_CAM_X - 195))
        for x in (-126.3, -108.7, 105.7, 123.3):
            body = body.union(cylinder(9, x - 195, x - 192))
        wheel = cylinder(46, -474, -470).cut(cylinder(39, -475, -469))
        wheel = wheel.union(cylinder(9, -475, -469))
        for angle in range(0, 180, 30):
            spoke = box(4, 84, 5, (-472, 0, 0)).rotate(
                (0, 0, 0), (1, 0, 0), angle
            )
            wheel = wheel.union(spoke)
        wheel = wheel.union(cylinder(3, -484, -471, 0, 38))
        return body.union(wheel.translate((-110, 0, 0)))


class LoomTiming(FeedTimingTrain):
    shed_lift = Length(18, min=16, max=20)
    input = LoomInput(shed_lift=shed_lift)


class HeddleFollower(CadQueryNode):
    side = Scalar(-1)
    station = Length(20)

    def render(self):
        x = self.side * 145
        y = 30 - self.station
        stem = box(6, 7, 120, (x, y, -25))
        bridge = box(64, abs(y) + 8, 8, (self.side * 116, y / 2, 35))
        pin = cylinder(1.5, x - 6.5, x + 1, y, -78)
        return stem.union(bridge).union(pin)


class DrivenHeddle(FusionNode):
    side = Scalar(-1)
    station = Length(20)
    parity = Count(0)
    color = "#368d8e"
    rise = Prismatic(axis=(0, 0, 1), range=(-20.01, 20.01))
    cage = HeddleCage(parity=parity)
    follower = HeddleFollower(side=side, station=station)


def y_cylinder(radius, start, end, x=0, z=0):
    return (
        cq.Workplane("XZ")
        .circle(radius)
        .extrude(end - start)
        .translate((x, end, z))
    )


class ArmFollower(CadQueryNode):
    side = Scalar(-1)
    color = "#776346"
    rise = Prismatic(axis=(0, 0, 1), range=(-0.01, 26.01))

    def render(self):
        # Cam roller is 6 mm above the short-lever pin's horizontal
        # slot.
        body = cylinder(1.5, -6.5, 1, 0, 6)
        body = body.union(box(3, 69, 4, (0, 33, -4)))
        center = -self.side * 2.4
        ring = box(13, 3, 6, (center, 65, 0)).cut(
            box(7.4, 5, 2.6, (center, 65, 0))
        )
        return body.union(ring).union(box(3, 4, 75, (0, 0, 35)))


class RockingLever(CadQueryNode):
    side = Scalar(-1)
    color = "#a37843"
    turn = Revolute(axis=(0, 1, 0))

    def render(self):
        lever = box(105, 3, 6, (self.side * 50, 0, 0))
        lever = lever.union(y_cylinder(3, -12, 12))
        for y in (-10, -3.7, 2, 8.3):
            lever = lever.union(y_cylinder(5, y, y + 1.7))
        for x in (self.side * 20, self.side * 100):
            lever = lever.union(y_cylinder(1, -7, 1, x))
        return lever


class ArmOutput(CadQueryNode):
    side = Scalar(-1)
    color = "#74543c"
    rise = Prismatic(axis=(0, 0, 1), range=(-65.01, 65.01))

    def render(self):
        ring = box(34, 3, 6, (0, 0, 0)).cut(
            box(26.7, 5, 2.6, (-self.side * 2, 0, 0))
        )
        # A plain guided stem also provides the haul-rope attachment.
        return ring.union(box(4, 4, 200, (0, -5, -100))).union(
            box(6, 8, 4, (0, -2, -4.5))
        )


class LeverStand(CadQueryNode):
    side = Scalar(-1)
    color = "#785537"

    def render(self):
        # Local origin at lever pivot, fixture reaches an outrigger
        # below.
        body = box(12, 4, 24, (0, 6, -6)).union(box(12, 4, 24, (0, -6, -6)))
        body = body.union(box(12, 32, 6, (0, 6, -15))).cut(
            y_cylinder(3.3, -9, 9)
        )
        body = body.union(box(12, 8, 180, (0, 18, -50)))
        body = body.union(box(108, 96, 10, (self.side * 50, -26, -135)))
        # Separate guide collars connect by an outboard horizontal
        # bearer.
        for x, y, z, w in (
            (self.side * 20, -70, 40, 3.6),
            (self.side * 90, -10, -100, 4.6),
        ):
            body = body.union(box(12, 14, 10, (x, y, z)))
            body = body.union(box(abs(x) + 8, 5, 8, (x / 2, 18, z)))
            body = body.union(box(8, abs(y - 18) + 4, 8, (x, (y + 18) / 2, z)))
            body = body.cut(box(w, 4.6, 12, (x, y, z)))
        body = body.cut(box(4.6, 4.6, 12, (self.side * 90, -10, -135)))
        return body


class ArmMechanism(AssemblyNode):
    side = Scalar(-1)
    radius = TranslationalPort()
    follower = ArmFollower(side=side)
    lever = RockingLever(side=side)
    output = ArmOutput(side=side)
    stand = LeverStand(side=side)
    radius.drives(follower.rise, offset=-26)
    follower.rise.drives(
        lever.turn, law=lambda a, b: lambda z: -b.side * asin((z - 13) / 20)
    )
    lever.turn.drives(
        output.rise, law=lambda a, b: lambda t: -a.side * 100 * sin(t)
    )

    def render(self):
        # The follower pin and each lever pin meet in a real horizontal
        # slot.
        self.follower.translate([self.side * 20, -70, -13])
        self.output.translate([self.side * 90, -5, 0])


class ReedFollower(CadQueryNode):
    color = "#776346"
    rise = Prismatic(axis=(0, 0, 1), range=(-0.01, REED_TRAVEL + 0.01))

    def render(self):
        return cylinder(1.5, -6.5, 1).union(box(3, 4, 135, (0, 0, 65)))


class Selector(CadQueryNode):
    side = Scalar(-1)
    color = "#695644"
    rise = Prismatic(axis=(0, 0, 1), range=(-0.01, 14.01))

    def render(self):
        # The cam stem is at X=side*18; the jaw's actuator is outside
        # the warp at X=side*185. A low cross-tie joins the two.
        # The 42 mm base track keeps the cam's rim below the lowest
        # heddle crossbar even at the advertised 20 mm shed lift.
        body = cylinder(1.5, -6.5, 1, z=28)
        body = body.union(box(3, 4, 100, (0, 0, 48)))
        body = body.union(box(3, 28, 4, (0, -10, 30)))
        # Raise only the cross-shed tie above the extended reed tracks.
        # Keep the rear bridge low enough to clear a fully lowered
        # heddle.
        # Cross behind the reed's parked feet, not through their travel.
        body = body.union(box(171, 4, 4, (self.side * 83.5, -22, 52)))
        for x in (0, self.side * 167):
            body = body.union(box(3 if x == 0 else 4, 4, 26, (x, -22, 41)))
        body = body.union(box(4, 63, 4, (self.side * 167, -51.5, 30)))
        # Compound plane: vertical selector rise produces equal Y
        # opening;
        # withdrawing the arm lowers that opening by half its X retreat.
        low, high = (-32, 4) if self.side < 0 else (-4, 32)
        front, back = (-4, 18) if self.side < 0 else (-18, 4)

        def profile(x):
            return [
                (front, 19),
                (back, 19),
                (back, 65 + self.side * back - 0.5 * self.side * x),
                (front, 65 + self.side * front - 0.5 * self.side * x),
            ]

        wedge = (
            cq.Workplane("YZ", origin=(low, 0, 0))
            .polyline(profile(low))
            .close()
            .workplane(offset=high - low)
            .polyline(profile(high))
            .close()
            .loft(ruled=True)
            .translate((self.side * 167, -81, 0))
        )
        return body.union(wedge)


class Jaw(CadQueryNode):
    side = Scalar(-1)
    color = "#6f6758"
    opening = Prismatic(axis=(0, 1, 0), range=(-14.01, 14.01))

    def render(self):
        s = self.side
        # The hands own opposite halves of the shed and open away from
        # each other. Their upper fingers never sweep through the other
        # jaw.
        body = box(8, 6, 1, (s * 21, -s * 4.5, 3.8))
        for lane, tip in ((3.5, 11.8), (5, 10.3)):
            y = -s * lane
            body = body.union(
                box(22 + tip, 1, 1, (s * (21 - tip) / 2, y, 3.8))
            )
            body = body.union(box(1, 1, 6.8, (-s * tip, y, 0.9)))
        body = body.union(box(4, 1, 6.8, (s * 5, -s * 6.8, 0.9)))
        body = body.union(box(18, 1, 1, (s * 12, -s * 6.8, 3.8)))
        # Route the crossbar forward around the closed timber arm guide.
        # At Y=-16 it swept into the cap when the left jaw opened.
        if s < 0:
            body = body.union(box(3, 24, 1, (s * 18, -4, 3.8)))
            # Keep the inboard span in the wider shed, then dogleg only
            # outside the ribbon to pass the timber guide cap.
            body = body.union(box(84, 2, 1, (s * 58.5, -16, 3.8)))
            body = body.union(box(88, 2, 1, (s * 142.5, -24.5, 3.8)))
            body = body.union(box(2, 10.5, 1, (s * 99.5, -20.25, 3.8)))
            body = body.union(box(2, 10.5, 1, (s * 185, -20.25, 3.8)))
        else:
            body = body.union(box(3, 20, 1, (s * 18, -2, 3.8)))
            body = body.union(box(170, 2, 1, (s * 101.5, -11, 3.8)))
            body = body.union(box(2, 7, 1, (s * 185, -13.5, 3.8)))
        body = body.union(box(2, 2, 43, (s * 185, -16, -17.2)))
        length, centre, stop = (44, 2, 21.3) if s < 0 else (58, 9, 6.7)
        body = body.union(box(2, length, 2, (s * 185, centre, -10)))
        body = body.union(box(5, 2, 5, (s * 185, stop, -10)))
        foot = cq.Workplane("XY").sphere(0.8).translate((s * 185, -16, -39.35))
        return body.union(foot)


class GrippingArmBody(CarrierArm):
    def render(self):
        s = self.side
        body = super().render()
        # The cheek opposite the opening direction stays fixed to the
        # hand.
        body = body.union(box(4, 1, 6.5, (s * 5, s * 6.8, -0.25)))
        body = body.union(box(14, 1, 1, (s * 10, s * 6.8, -3.8)))
        body = body.union(box(3, 5.3, 2.8, (s * 15, s * 4.65, -2.9)))
        # Rigid attachment rail stays outside the textile and heddle
        # frames.
        rail_length, rail_y = (149, 71.5) if s < 0 else (194, 49)
        body = body.union(box(4, rail_length, 4, (s * 185, rail_y, 0)))
        body = body.union(box(7, 17, 5, (s * 18, -6, 0)))
        body = body.union(box(12, 3, 3, (s * 22, -13, 0)))
        guide = box(7, 12, 7, (s * 185, 14, -10)).union(
            box(4, 4, 14, (s * 185, 14, -5))
        )
        guide = guide.cut(box(2.6, 14, 2.6, (s * 185, 14, -10)))
        # The external vertical actuator passes a short slot in the
        # arm's
        # outer rail. It never crosses a warp end to reach the selector.
        slot_length, slot_y = (17, -9) if s < 0 else (32, -16)
        return body.union(guide).cut(
            box(2.6, slot_length, 6, (s * 185, slot_y, 0))
        )


class JawSpring(MolejoNode):
    side = Scalar(-1)
    tip_y = TranslationalPort()
    color = "#55504a"

    def render(self):
        s = self.side
        return Shape(
            Polygon([(-1, -0.15), (1, -0.15), (1, 0.15), (-1, 0.15)]),
            [Spline([(0, s * 8, 12), (0, s * 16, 12), (0, P.tip_y, 2.3)])],
            path_samples=36,
            profile_samples=4,
        )


class GrippingArm(AssemblyNode):
    side = Scalar(-1)
    slide = Prismatic(axis=(1, 0, 0))
    body = GrippingArmBody(side=side)
    jaw = Jaw(side=side)
    spring = JawSpring(side=side)
    jaw.opening.drives(
        spring.tip_y,
        law=lambda jaw, spring: lambda opening: opening
        + (-41 if spring.side < 0 else 29),
    )

    def render(self):
        # Closing leaves and their actual bearings stay outside every
        # warp
        # end. An inboard bowed leaf crossed yarn despite rigid-only
        # green.
        self.spring.translate(
            [self.side * 185, 25 if self.side < 0 else -45, 2]
        )


class GrippingCarrier(AssemblyNode):
    handoff = RotationalPort()
    left = GrippingArm(side=-1)
    right = GrippingArm(side=1)
    spool = WeftSpool()
    # Ownership transfers only while both hands dwell at the same
    # position.
    # Outside that dwell the boat follows the enclosing hand exactly;
    # the
    # independent retention contracts test which hand actually encloses
    # it.
    (handoff & left.slide & right.slide).drives(
        spool.slide,
        law=lambda a, b: lambda t, left, right: left * clip(0.5 + cos(t), 0, 1)
        + right * (1 - clip(0.5 + cos(t), 0, 1)),
    )


class DrivenReed(Reed):
    def render(self):
        start, end = REED_TIE_X - 2, -94.2
        # The haul tie crosses above both grip selectors, whose wedges
        # occupy the former lower tie's new, longer path.
        body = super().render().union(box(4, 4, 16, (-93, 0, 44)))
        return body.union(
            box(end - start, 4, 4, ((start + end) / 2, 0, REED_TIE_Z - 520))
        )


class HeadDrive(AssemblyNode):
    angle = RotationalPort()
    shed_lift = Length(18, min=16, max=20)
    heddle_a = DrivenHeddle(side=-1, station=20, parity=0)
    heddle_b = DrivenHeddle(side=1, station=40, parity=1)
    left = ArmMechanism(side=-1)
    right = ArmMechanism(side=1)
    reed = ReedFollower()
    selector_a = Selector(side=-1)
    selector_b = Selector(side=1)
    angle.drives(
        heddle_a.rise,
        law=lambda a, b: lambda t: a.shed_lift * shed_fraction(t + 270),
    )
    angle.drives(
        heddle_b.rise,
        law=lambda a, b: lambda t: -a.shed_lift * shed_fraction(t + 270),
    )
    angle.drives(
        left.radius, law=lambda a, b: lambda t: arm_radius(t + 270, -1)
    )
    angle.drives(
        right.radius, law=lambda a, b: lambda t: arm_radius(t + 270, 1)
    )
    angle.drives(reed.rise, law=lambda a, b: lambda t: reed_lift(t + 270))
    angle.drives(
        selector_a.rise, law=lambda a, b: lambda t: selector_lift(t + 270, -1)
    )
    angle.drives(
        selector_b.rise, law=lambda a, b: lambda t: selector_lift(t + 270, 1)
    )

    def render(self):
        self.heddle_a.translate([0, 170, 520])
        self.heddle_b.translate([0, 190, 520])
        self.left.translate([-208.2, 250, 433])
        self.right.translate([221.8, 250, 433])
        self.reed.translate([REED_TIE_X, 180, 400 + REED_CAM_BASE])
        self.selector_a.translate([-18, 180, 414])
        self.selector_b.translate([18, 180, 414])
