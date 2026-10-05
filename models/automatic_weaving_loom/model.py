"""Vinci accompanied-spool loom: one input and explicit connected
transmissions."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

from machinome_mechanics import rolling_travel
from machinome.node.assembly import AssemblyNode
from machinome.node.cadquery import CadQueryNode
from machinome.parameters import Length
from machinome.motion.ports import RotationalPort, Time
from machinome.simulation import Driver, Instruction
from machinome.math import sqrt

from .parts import (
    TimberFrame,
    ReedTracks,
    WarpEnd,
    BlueWarpEnd,
    ClothWarp,
    WeftTail,
    box,
    axle,
    shuttle_x,
    weft_selvedge,
)
from .head import LoomTiming, HeadDrive, GrippingCarrier, DrivenReed
from .cords import CordTransmission, CordSupports
from .textile import (
    WarpRollEnd,
    ClothWeb,
    TravellingPick,
    CLOTH_GUIDE,
    CLOTH_RUN,
    BEAM_PITCH,
)
from .timing import clip
from .winding import WindingTrain, CAM_RISE, CENTERS
from .reeding import REED_REST_Y, REED_TRAVEL, REED_TIE_X


def weft_route(angle, stroke):
    """Schematic yarn contact with the reed; the free end stays on the
    boat.

    A bend just outside the 144 mm ribbon follows the reed's working
    face.
    While withdrawn, both segments lie on the original straight free
    span.
    This illustrates beat-up, without claiming yarn dynamics or new
    cloth.
    """
    anchor = weft_selvedge(angle)
    tip = shuttle_x(angle) - anchor
    edge = 75 * tip / sqrt(tip * tip + 0.0001)
    fraction = clip((edge - anchor) * tip / (tip * tip + 0.0001), 0.05, 0.95)
    face = REED_REST_Y + stroke - 45 - 1.46
    return tip, fraction * tip, clip(70 * fraction, 0, face)


class MuseumFrame(CadQueryNode):
    color = "#805333"

    def render(self):
        frame = TimberFrame(drive_bearer_z=-15.2, guide_z=150).render()
        frame = frame.intersect(box(500, 500, 210, (0, 0, 75))).translate(
            (0, 150, 340)
        )
        for x in (-170, 170):
            for y in (-210, 305, -5):
                frame = frame.union(box(20, 22, 520, (x, y, 260)))
            for z in (18, 340, 510):
                frame = frame.union(box(18, 535, 16, (x, 47.5, z)))
        for y in (-210, 305):
            frame = frame.union(box(350, 18, 16, (0, y, 18)))
        for y in (72, 72 - CENTERS):
            frame = frame.union(box(390, 18, 12, (7.5, y, 33.8)))
            for x in (-170, 170):
                frame = frame.union(box(18, 18, 34, (x, y, 17)))
        frame = frame.union(box(34, 90, 16, (176, 150, 360.8)))
        # Outriggers carry the inferred rocking-lever fixtures without
        # pretending that a free-floating bearing is grounded.
        for x in (-208.2, 221.8):
            s = -1 if x < 0 else 1
            frame = frame.union(box(165, 100, 16, (s * 237.5, 226, 284.8)))
            frame = frame.union(box(18, 26, 57, (s * 170, 259, 313.3)))
        # Plain vertical guides for reed and selector followers.
        for x, width in ((-18, 3.6), (18, 3.6)):
            support = box(abs(x) + 20, 12, 10, (x / 2, 180, 490))
            guide = box(12, 12, 10, (x, 180, 490))
            support = support.union(guide).cut(
                box(width, 4.6, 12, (x, 180, 490))
            )
            frame = frame.union(support)
        # Support the outboard reed cam's extended shaft and raised
        # guide.
        frame = frame.union(box(184, 12, 12, (-253, 180, 330)))
        frame = frame.union(box(12, 12, 406, (-345, 186, 533)))
        bearing = box(12, 24, 20, (-345, 180, 400))
        frame = frame.union(bearing).cut(axle(5.4, 16, (-345, 180, 400)))
        guide = box(32, 12, 10, (-349, 180, 590))
        frame = frame.union(guide).cut(
            box(3.6, 4.6, 12, (REED_TIE_X, 180, 590))
        )
        frame = frame.union(box(350, 12, 10, (0, 180, 490)))
        for x in (-93, 93):
            frame = frame.union(box(14, 132, 12, (x, 98, 417.8)))
        # Two material guides at the upper cloth/warp turns.
        for y in (CLOTH_GUIDE, 305):
            frame = frame.union(axle(4, 340, (0, y, 515.2)))
        for x in (-170, 170):
            frame = frame.union(box(18, 16, 183, (x, CLOTH_GUIDE, 426.5)))
            # Closed guide caps resist the overhanging arm's pitching
            # moment.
            # The inherited truncated frame only supplied their lower
            # halves.
            frame = frame.union(box(18, 18, 12, (x, 115, 520)))
        frame = frame.union(box(350, 8, 8, (0, 180, 510)))
        for x in (-155, 155):
            frame = frame.union(box(8, 8, 105, (x, 180, 562.5)))
        frame = frame.union(box(318, 8, 10, (0, 180, 610)))
        frame = frame.union(CordSupports().render())
        frame = frame.union(box(18, 18, 98, (-170, 180, 513)))
        for x, w, d in (
            (-228.2, 3.6, 4.6),
            (-145, 6.6, 7.6),
            (-18, 3.6, 4.6),
            (18, 3.6, 4.6),
            (145, 6.6, 7.6),
        ):
            for z in (490, 510):
                frame = frame.cut(box(w, d, 12, (x, 180, z)))
        for x in (-298.2, 311.8):
            frame = frame.cut(box(4.6, 4.6, 18, (x, 240, 284.8)))
        # Local timber bridges carry the side rails over the selector
        # ties.
        for x in (-170, 170):
            frame = frame.union(box(18, 24, 28, (x, 158, 482)))
            frame = frame.cut(box(20, 4.6, 22, (x, 158, 473)))
        # Mortise for the left winding standard's continuous foot where
        # it
        # passes the intermediate timber post; 0.2 mm assembly
        # clearance.
        frame = frame.cut(box(8.4, 24, 12.4, (-162, -5, 46)))
        return frame.cut(box(800, 8.6, 5.6, (0, 115, 520)))


class AutomaticWeavingLoom(AssemblyNode):
    time = Time(loop=60)
    phase = Driver(default=0, range=(0, 360), unit="deg")
    run = Driver(default=1, range=(0, 1), unit="play")
    cycle = RotationalPort()
    shed_lift = Length(18, min=16, max=20)
    frame = MuseumFrame()
    timing = LoomTiming(shed_lift=shed_lift)
    winding = WindingTrain()
    head_drive = HeadDrive(shed_lift=shed_lift)
    cords = CordTransmission()
    carrier = GrippingCarrier()
    reed = DrivenReed()
    reed_tracks = ReedTracks()
    warp_a = WarpEnd(station=20).repeat(12)
    warp_b = BlueWarpEnd(station=40).repeat(12)
    cloth_ends = ClothWarp(reach=CLOTH_RUN).repeat(24)
    cloth_picks_a = TravellingPick(parity=0).repeat(4)
    cloth_picks_b = TravellingPick(parity=1).repeat(4)
    cloth_web = ClothWeb()
    weft = WeftTail()
    warp_leads = WarpRollEnd().repeat(24)

    cycle.drives(timing.angle)
    timing.input.turn.drives(carrier.handoff, offset=270)
    timing.twelve.turn.drives(winding.feed, ratio=CAM_RISE)
    winding.rear_upper.turn.drives(warp_leads.unwind, offset=-7.5)
    winding.front_lower.turn.drives(
        cloth_web.wrap, ratio=math.pi / 180, offset=-math.pi / 2
    )
    winding.front_lower.turn.drives(
        cloth_picks_a.travel, ratio=rolling_travel(1, BEAM_PITCH)
    )
    winding.front_lower.turn.drives(
        cloth_picks_b.travel, ratio=rolling_travel(1, BEAM_PITCH)
    )
    timing.input.turn.drives(head_drive.angle)
    head_drive.left.output.rise.drives(carrier.left.slide, offset=-65)
    head_drive.right.output.rise.drives(
        carrier.right.slide, ratio=-1, offset=65
    )
    head_drive.reed.rise.drives(reed.stroke, offset=-REED_TRAVEL)
    head_drive.left.output.rise.drives(cords.left.lift)
    head_drive.right.output.rise.drives(cords.right.lift)
    carrier.left.slide.drives(cords.left.travel)
    carrier.right.slide.drives(cords.right.travel)
    head_drive.reed.rise.drives(cords.reed.lift)
    (head_drive.selector_a.rise & carrier.left.slide).drives(
        carrier.left.jaw.opening,
        law=lambda a, b: lambda z, x: clip(z + 0.5 * x, 0, 14),
    )
    (head_drive.selector_b.rise & carrier.right.slide).drives(
        carrier.right.jaw.opening,
        law=lambda a, b: lambda z, x: -clip(z - 0.5 * x, 0, 14),
    )
    head_drive.heddle_a.rise.drives(warp_a.lift)
    head_drive.heddle_b.rise.drives(warp_b.lift)
    (cycle & reed.stroke).drives(
        (weft.tip_x, weft.contact_x, weft.contact_y),
        law=lambda a, b: weft_route,
    )

    instructions = {
        "Beat left": Instruction({"phase": 0, "run": 0}, duration=0.6),
        "Open shed": Instruction({"phase": 60, "run": 0}, duration=0.6),
        "Handoff": Instruction({"phase": 90, "run": 0}, duration=0.6),
        "Beat right": Instruction({"phase": 180, "run": 0}, duration=0.6),
        "Return pick": Instruction({"phase": 270, "run": 0}, duration=0.6),
        "Run": Instruction({"phase": 0, "run": 1}, duration=0.6),
    }

    def render(self):
        self.timing.translate([195, 180, 376])
        self.winding.translate([195, 72, 106])
        self.carrier.translate([0, 115, 520])
        self.reed.translate([0, REED_REST_Y, 520])
        self.reed_tracks.translate([0, 150, 340])
        for i, (a, b) in enumerate(zip(self.warp_a, self.warp_b)):
            a.translate([-69 + 12 * i, 305, 520])
            b.translate([-63 + 12 * i, 305, 520])
        for i, end in enumerate(self.cloth_ends):
            end.translate([-69 + 6 * i, 45, 520])
        for i, (a, b) in enumerate(
            zip(self.cloth_picks_a, self.cloth_picks_b)
        ):
            a.translate([-72, 40 - 12 * i, 520])
            b.translate([-72, 34 - 12 * i, 520])
        for i, a in enumerate(self.warp_leads):
            a.translate([-69 + 6 * i, 72, 202])
        self.cloth_web.translate([0, 45, 520])
        self.weft.translate([0, 45, 520])

    def simulate(self):
        # Four turns in sixty machine seconds. Publishing Time makes
        # this
        # same clock available to Studio, with its native speed
        # controls.
        angle = clip(self.phase + 24 * self.run * self.time, 0, 1440)
        self.cycle = angle
        self.weft.translate([weft_selvedge(angle), 0, 0])
