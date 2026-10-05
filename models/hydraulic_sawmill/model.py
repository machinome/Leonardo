"""MUST IGB-37 hydraulic saw: a source-led, connected reconstruction."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi

from machinome.math import sin, cos
from machinome.node.assembly import AssemblyNode
from machinome.node.frames import Frame
from machinome.parameters import Length, Angle
from machinome.motion.joints import Prismatic, Revolute
from machinome.motion.ports import RotationalPort, Time

from .frame import MillStructure
from .parts import (
    WaterChannel,
    WaterSurface,
    Wheel,
    Crankshaft,
    Crank,
    CrankRetainer,
    ConnectingRod,
    SashWood,
    SawBlade,
    BladeClamp,
    TensionNut,
    SashPin,
    CarriageBed,
    CarriageWheel,
    CarriageAxle,
    LogHalf,
    EndGrain,
    RatchetDrum,
    Rocker,
    FeedTie,
    DrivingPawl,
    HoldingPawl,
    FixedPins,
    UpperRoller,
    ReductionShaft,
    UpperPin,
    DriveIdler,
    IdlerPin,
    DrumTie,
    HaulRope,
    HaulSpan,
    DriveRope,
    WindingRope,
    RadialWindingRope,
    UncutTimber,
    CarriageAnchor,
)
from .layout import (
    CRANK,
    AXLE_Z,
    TIE_Y,
    PAWL_Y,
    RATCHET_X,
    RATCHET_Z,
    ROCKER_X,
    ROCKER_Z,
    ROPE_Y,
    ANCHOR_X,
    ROPE_PITCH_RADIUS,
    TIMBER_LENGTH,
    CARRIAGE_START,
    WIND_PITCH,
    INPUT_RESERVE,
    ROD_Y,
    ROPE_ANCHOR_Z,
    UPPER_X,
    UPPER_Z,
    UPPER_RADIUS,
    REDUCER_X,
    REDUCER_Z,
    REDUCER_RADIUS,
    HAUL_RADIUS,
    IDLER_X,
    IDLER_Z,
    IDLER_RADIUS,
    DRIVE_START_Y,
    LARGE_START_Y,
    HAUL_TIE_Y,
    HAUL_INITIAL,
)
from .rope_drive import (
    PASS_ANGLE,
    PASS_SECONDS,
    shaft_angle,
    carriage_from_shaft,
    INPUT_PHASE,
    HAUL_PHASE,
    INPUT_CONTACT,
    HAUL_CONTACT,
    UPPER_EXIT,
    UPPER_EXIT_PHASE,
    approach,
    haul_consumed,
    input_consumed,
    GEAR_TIE_PHASE,
    SPIRAL_PORTS,
    spiral_coordinates,
    drive_profile,
    DRIVE_BEND_PORTS,
)
from .kinematics import (
    saw_height,
    rod_lean,
    rocker_angle,
    ratchet_angle,
    pawl_pose,
    tie_pose,
    holding_angle,
    clip01,
    HOLD_X,
    HOLD_Z,
)


def uncut_profile(advance):
    remaining = TIMBER_LENGTH * clip01(
        (-10.2 - CARRIAGE_START + TIMBER_LENGTH / 2 - advance) / TIMBER_LENGTH
    )
    half_height = 28 * clip01(remaining / 0.1)
    return remaining, half_height, -half_height


class BladeAttachments(AssemblyNode):
    """Pinned blade ends and the nut seated on the upper clamp."""

    lower_hole = Frame(at=(0, 0, 15))
    upper_hole = Frame(at=(0, 0, 285), z=(0, 0, -1), x=(-1, 0, 0))
    nut_seat = Frame(at=(0, 0, 305.2))
    lower = BladeClamp()
    upper = BladeClamp(upper=True)
    nut = TensionNut()

    lower_attachment = lower.blade_pin.on(lower_hole)
    upper_attachment = upper.blade_pin.on(upper_hole)
    tensioner = nut.seat.on(nut_seat)


class SawSash(AssemblyNode):
    guide = Frame()
    rise = Prismatic(axis=(0, 0, 1))
    frame = SashWood()
    blade = SawBlade()
    pin = SashPin()
    clamps = BladeAttachments()


class Timber(AssemblyNode):
    kerf = Length(3.2, min=2, max=5)
    kerf_start = Frame(
        at=(-TIMBER_LENGTH / 2, kerf / 2, 408.2),
        z=(0, -1, 0),
        x=(1, 0, 0),
    )
    log_left = LogHalf(positive=True, kerf=kerf, name="Left timber half")
    log_right = LogHalf(positive=False, kerf=kerf, name="Right timber half")
    uncut = UncutTimber(kerf=kerf, name="Uncut wood at the kerf")
    grain_left = EndGrain(positive=True, kerf=kerf).repeat(2)
    grain_right = EndGrain(positive=False, kerf=kerf).repeat(2)
    uncut_insert = uncut.start.on(kerf_start)

    def render(self):
        for grains in (self.grain_left, self.grain_right):
            grains[0].translate([TIMBER_LENGTH / 2 + 0.2, 0, 408.2])
            grains[1].rotate(180, [0, 0, 1]).translate(
                [-TIMBER_LENGTH / 2 - 0.2, 0, 408.2]
            )


class RunningGear(AssemblyNode):
    outer_wheels = CarriageWheel().repeat(2)
    inner_wheels = CarriageWheel(positive=False).repeat(2)
    axles = CarriageAxle().repeat(2)

    def render(self):
        for wheels, y in ((self.outer_wheels, 42), (self.inner_wheels, -42)):
            for wheel, x in zip(wheels, (-185, 185)):
                wheel.translate([x, y, 357.2])
        for axle, x in zip(self.axles, (-185, 185)):
            axle.translate([x, 0, 357.2])


class TimberCarriage(AssemblyNode):
    rail_datum = Frame()
    kerf = Length(3.2, min=2, max=5)
    feed = Prismatic(axis=(1, 0, 0))
    bed = CarriageBed(kerf=kerf, name="Bed and slotted log cradles")
    anchor = CarriageAnchor(name="Carriage rope knot")
    timber = Timber(kerf=kerf, name="Timber")
    running_gear = RunningGear(name="Rollers and axles")
    feed.drives(running_gear.outer_wheels.spin, ratio=180 / (12 * pi))
    feed.drives(running_gear.inner_wheels.spin, ratio=180 / (12 * pi))


class WaterDrive(AssemblyNode):
    """Wheel, shaft and crank share the same bearing line."""

    main_bearing = Frame(at=(0, 0, AXLE_Z), z=(0, 1, 0), x=(1, 0, 0))
    wheel_seat = Frame(at=(0, -151, AXLE_Z), z=(0, 1, 0), x=(1, 0, 0))
    channel = WaterChannel(name="Water channel")
    water = WaterSurface(name="Water surface")
    waterwheel = Wheel(name="Undershot waterwheel")
    crankshaft = Crankshaft(name="Keyed crankshaft")
    crank = Crank(name="Square-bored crank")
    crank_retainer = CrankRetainer(name="Crank retaining washer")

    wheel_mount = waterwheel.hub.on(wheel_seat, waterwheel.spin)
    shaft_mount = crankshaft.bearing.on(main_bearing, crankshaft.spin)
    crank_mount = crank.shaft_bore.on(main_bearing, crank.spin)
    retainer_mount = crank_retainer.shaft_bore.on(
        main_bearing, crank_retainer.spin
    )


class SawMechanism(AssemblyNode):
    """The crank's top position and the sash's guide datum."""

    base = Frame()
    crank_top = Frame(at=(0, ROD_Y, CRANK))
    sash_guide = Frame(x=(-1, 0, 0))
    connecting_rod = ConnectingRod(name="Connecting rod")
    sash = SawSash(name="Guided saw sash")

    rod_mount = connecting_rod.big_end.on(crank_top)
    sash_mount = sash.guide.on(sash_guide, sash.rise)


class DrumWinding(AssemblyNode):
    start = Frame()
    radius = Length()
    phase = Angle()
    shift = Prismatic(axis=(0, 1, 0))
    rope = WindingRope(radius=radius, name="Wound rope")

    def render(self):
        self.rope.rotate(-90, [1, 0, 0]).rotate(self.phase - 90, [0, 1, 0])


class DriveLine(AssemblyNode):
    shaft = Frame(at=(0, -DRIVE_START_Y, 0), z=(0, 1, 0), x=(1, 0, 0))
    shift_x = Prismatic(axis=(1, 0, 0))
    shift_z = Prismatic(axis=(0, 0, 1))
    rope = DriveRope(name="Drive rope around lower idler")


class RadialWinding(AssemblyNode):
    shaft = Frame(z=(0, 1, 0), x=(1, 0, 0))
    spin = Revolute(axis=(0, 1, 0))
    rope = RadialWindingRope(name="Radially stacked ratchet rope")

    def render(self):
        self.rope.rotate(GEAR_TIE_PHASE, [0, 1, 0]).translate(
            [
                ROPE_PITCH_RADIUS * sin(GEAR_TIE_PHASE),
                DRIVE_START_Y,
                ROPE_PITCH_RADIUS * cos(GEAR_TIE_PHASE),
            ]
        )


class HaulingLine(AssemblyNode):
    anchor = Frame()
    shift = Prismatic(axis=(1, 0, 0))
    rope = HaulRope(name="Top-centred carriage rope")


def haul_profile(advance):
    beta = approach(advance)
    x = UPPER_X - ANCHOR_X - advance
    return (
        x,
        x - UPPER_RADIUS * sin(beta),
        UPPER_Z + UPPER_RADIUS * cos(beta) - ROPE_ANCHOR_Z,
        (UPPER_EXIT_PHASE + beta) * pi / 180,
    )


def winding_ports(rope):
    return tuple(getattr(rope, name) for name in SPIRAL_PORTS)


def drive_ports(line):
    rope = line.rope
    return (
        line.shift_x,
        line.shift_z,
        rope.inlet_x,
        rope.inlet_z,
        rope.outlet_x,
        rope.outlet_y,
        rope.outlet_z,
    ) + tuple(getattr(rope, name) for name in DRIVE_BEND_PORTS)


class FeedMechanism(AssemblyNode):
    """Fixed journals locate the links; drum seats locate the ropes."""

    base = Frame()
    ratchet_bearing = Frame(
        at=(RATCHET_X, 0, RATCHET_Z), z=(0, 1, 0), x=(1, 0, 0)
    )
    reduction_bearing = Frame(
        at=(REDUCER_X, 0, REDUCER_Z), z=(0, 1, 0), x=(1, 0, 0)
    )
    saw_journal = Frame(at=(0, TIE_Y, AXLE_Z), z=(0, 1, 0), x=(1, 0, 0))
    pawl_plane = Frame(at=(0, PAWL_Y, 0), z=(0, 1, 0), x=(1, 0, 0))
    carriage_knot = Frame(at=(ANCHOR_X, ROPE_Y, ROPE_ANCHOR_Z))
    upper_exit = Frame(at=(UPPER_EXIT[0], ROPE_Y, UPPER_EXIT[1]))
    reserve_start = Frame(
        at=(INPUT_CONTACT[0], LARGE_START_Y, INPUT_CONTACT[1])
    )
    takeup_start = Frame(
        at=(
            HAUL_CONTACT[0],
            HAUL_TIE_Y + WIND_PITCH * HAUL_INITIAL,
            HAUL_CONTACT[1],
        )
    )
    feed_drum = RatchetDrum(name="Ratchet and slender winding axle")
    rocker = Rocker(name="Feed rocker")
    feed_tie = FeedTie(name="Saw-to-rocker tie")
    pawl = DrivingPawl(name="Driving pawl")
    holding_pawl = HoldingPawl(name="Holding pawl")
    rocker_pin = FixedPins(x=ROCKER_X, z=ROCKER_Z, name="Rocker pivot")
    holding_pin = FixedPins(
        x=HOLD_X,
        z=HOLD_Z,
        journal_y=PAWL_Y,
        head_offset=2.5,
        name="Holding-pawl pivot",
    )
    upper_roller = UpperRoller(name="Upper rope roller")
    upper_pin = UpperPin(name="Upper roller axle")
    reduction_shaft = ReductionShaft(name="Compound winding shaft")
    drive_idler = DriveIdler(name="Lower drive-rope pulley")
    idler_pin = IdlerPin(name="Lower pulley journal")
    haul = HaulingLine(name="Carriage haul")
    haul_span = HaulSpan(name="Upper roller to thin shaft")
    drive_line = DriveLine(name="Ratchet to reduction shaft")
    winding = RadialWinding(name="Ratchet winding")
    reserve = DrumWinding(
        radius=REDUCER_RADIUS,
        phase=INPUT_PHASE,
        name="Large-radius rope reserve",
    )
    takeup = DrumWinding(
        radius=HAUL_RADIUS,
        phase=HAUL_PHASE,
        name="Central small-radius take-up",
    )
    gear_tie = DrumTie(
        radius=ROPE_PITCH_RADIUS,
        lane=DRIVE_START_Y,
        phase=GEAR_TIE_PHASE,
        name="Ratchet rope tie",
    )
    input_tie = DrumTie(
        radius=REDUCER_RADIUS,
        lane=LARGE_START_Y + WIND_PITCH * INPUT_RESERVE,
        phase=INPUT_PHASE - 360 * INPUT_RESERVE,
        name="Large-drum rope tie",
    )
    haul_tie = DrumTie(
        radius=HAUL_RADIUS,
        lane=HAUL_TIE_Y,
        phase=HAUL_PHASE + 360 * HAUL_INITIAL,
        name="Central-shaft rope tie",
    )

    ratchet_mount = feed_drum.bearing.on(ratchet_bearing, feed_drum.spin)
    rocker_mount = rocker.pivot.on(rocker_pin.journal, rocker.turn)
    tie_mount = feed_tie.saw_pin.on(saw_journal)
    pawl_mount = pawl.pivot.on(pawl_plane)
    holding_mount = holding_pawl.pivot.on(
        holding_pin.journal, holding_pawl.turn
    )
    roller_mount = upper_roller.bore.on(upper_pin.journal, upper_roller.spin)
    reduction_mount = reduction_shaft.bearing.on(
        reduction_bearing, reduction_shaft.spin
    )
    idler_mount = drive_idler.bore.on(idler_pin.journal, drive_idler.spin)
    haul_mount = haul.anchor.on(carriage_knot, haul.shift)
    span_mount = haul_span.start.on(upper_exit)
    drive_mount = drive_line.shaft.on(ratchet_bearing)
    winding_mount = winding.shaft.on(ratchet_bearing, winding.spin)
    reserve_mount = reserve.start.on(reserve_start, reserve.shift)
    takeup_mount = takeup.start.on(takeup_start, takeup.shift)
    gear_knot = gear_tie.shaft.on(ratchet_bearing, gear_tie.spin)
    input_knot = input_tie.shaft.on(reduction_bearing, input_tie.spin)
    haul_knot = haul_tie.shaft.on(reduction_bearing, haul_tie.spin)

    def render(self):
        # Fixed axles establish the journals their moving mates use.
        self.upper_pin.translate([UPPER_X, ROPE_Y, UPPER_Z])
        self.idler_pin.translate([IDLER_X, 0, IDLER_Z])


class LeonardoHydraulicSawmill(AssemblyNode):
    kerf = Length(3.2, min=2, max=5)
    time = Time(loop=PASS_SECONDS)
    frame = MillStructure(name="Frame and guides")
    water_drive = WaterDrive(name="Water drive")
    saw = SawMechanism(name="Saw mechanism")
    carriage = TimberCarriage(kerf=kerf, name="Timber carriage")
    feed = FeedMechanism(name="Feed mechanism")
    saw_mount = saw.base.on(frame.saw_station)
    carriage_mount = carriage.rail_datum.on(
        frame.carriage_entry, carriage.feed
    )
    feed_mount = feed.base.on(frame.feed_station)
    cycle = RotationalPort(unit="deg")
    cycle.drives(water_drive.waterwheel.spin)
    water_drive.waterwheel.spin.drives(water_drive.crankshaft.spin)
    water_drive.crankshaft.spin.drives(water_drive.crank.spin)
    water_drive.crankshaft.spin.drives(water_drive.crank_retainer.spin)
    water_drive.crankshaft.spin.drives(saw.connecting_rod.orbit)
    water_drive.crankshaft.spin.drives(
        saw.connecting_rod.lean, law=lambda a, b: rod_lean
    )
    water_drive.crankshaft.spin.drives(
        saw.sash.rise, law=lambda a, b: saw_height
    )
    saw.sash.rise.drives(feed.rocker.turn, law=lambda a, b: rocker_angle)
    saw.sash.rise.drives(feed.feed_tie.turn, law=lambda a, b: tie_pose)
    saw.sash.rise.drives(feed.feed_tie.rise)
    cycle.drives(
        (feed.pawl.turn, feed.pawl.shift_x, feed.pawl.shift_z),
        law=lambda a, b: pawl_pose,
    )
    cycle.drives(feed.feed_drum.spin, law=lambda a, b: ratchet_angle)
    feed.feed_drum.spin.drives(
        feed.holding_pawl.turn, law=lambda a, b: holding_angle
    )
    feed.feed_drum.spin.drives(
        feed.reduction_shaft.spin, law=lambda a, b: shaft_angle
    )
    feed.reduction_shaft.spin.drives(
        carriage.feed, law=lambda a, b: carriage_from_shaft
    )
    carriage.feed.drives(
        (
            carriage.timber.uncut.remaining,
            carriage.timber.uncut.top,
            carriage.timber.uncut.bottom,
        ),
        law=lambda a, b: uncut_profile,
    )
    feed.reduction_shaft.spin.drives(
        feed.upper_roller.spin,
        law=lambda a, b: lambda q: haul_consumed(q)
        * 180
        / (pi * UPPER_RADIUS),
    )
    feed.feed_drum.spin.drives(
        feed.drive_idler.spin,
        law=lambda a, b: lambda q: input_consumed(q)
        * 180
        / (pi * IDLER_RADIUS),
    )
    feed.feed_drum.spin.drives(feed.gear_tie.spin)
    feed.reduction_shaft.spin.drives(feed.input_tie.spin)
    feed.reduction_shaft.spin.drives(feed.haul_tie.spin)
    (feed.feed_drum.spin & feed.reduction_shaft.spin).drives(
        drive_ports(feed.drive_line), law=lambda a, b: drive_profile
    )
    feed.feed_drum.spin.drives(feed.winding.spin)
    feed.feed_drum.spin.drives(
        winding_ports(feed.winding.rope), law=lambda a, b: spiral_coordinates
    )
    feed.reduction_shaft.spin.drives(
        feed.reserve.shift, ratio=WIND_PITCH / 360
    )
    feed.reduction_shaft.spin.drives(
        feed.reserve.rope.turns, ratio=1 / 360, offset=-INPUT_RESERVE
    )
    feed.reduction_shaft.spin.drives(
        feed.reserve.rope.height,
        ratio=-WIND_PITCH / 360,
        offset=WIND_PITCH * INPUT_RESERVE,
    )
    feed.reduction_shaft.spin.drives(feed.takeup.shift, ratio=WIND_PITCH / 360)
    feed.reduction_shaft.spin.drives(
        feed.takeup.rope.turns, ratio=1 / 360, offset=HAUL_INITIAL
    )
    feed.reduction_shaft.spin.drives(
        feed.takeup.rope.height,
        ratio=-WIND_PITCH / 360,
        offset=-WIND_PITCH * HAUL_INITIAL,
    )
    feed.reduction_shaft.spin.drives(
        feed.haul_span.lane,
        ratio=WIND_PITCH / 360,
        offset=HAUL_TIE_Y + WIND_PITCH * HAUL_INITIAL - ROPE_Y,
    )
    carriage.feed.drives(feed.haul.shift)
    carriage.feed.drives(
        (
            feed.haul.rope.centre_x,
            feed.haul.rope.tangent_x,
            feed.haul.rope.tangent_z,
            feed.haul.rope.wrap,
        ),
        law=lambda a, b: haul_profile,
    )

    def simulate(self):
        self.cycle = PASS_ANGLE * clip01(self.time / PASS_SECONDS)
