"""Leonardo's hydraulic sawmill: an original kinematic exhibit."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from solid_node.node import AssemblyNode
from solid_node.parameters import Length, Count
from solid_node.motion.joints import Prismatic
from solid_node.simulation import Driver, Instruction
from .parts import (Foundation, OakStructure, Wheel, WheelHoop, Crankshaft,
                    ConnectingRod, SashWood, SawBlade, SashPin, CarriageBed,
                    CarriageWheel, CarriageAxle, LogHalf, EndGrain, RatchetDrum,
                    PawlCarrier, Pawl, HaulRope, Tailrace, FlumeWater, Plaque)
from .kinematics import CRANK, FEED, TEETH, DRUM_RADIUS, saw_height, rod_lean, feed_steps, pawl_lift

class SawSash(AssemblyNode):
    rise = Prismatic(axis=(0, 0, 1))
    frame = SashWood()
    blade = SawBlade()
    pin = SashPin()

class TimberCarriage(AssemblyNode):
    kerf = Length(3.2, min=2, max=5)
    feed = Prismatic(axis=(1, 0, 0))
    bed = CarriageBed()
    wheels = CarriageWheel().repeat(4)
    axles = CarriageAxle().repeat(2)
    log_left = LogHalf(positive=True, kerf=kerf)
    log_right = LogHalf(positive=False, kerf=kerf)
    grain_left = EndGrain(positive=True, kerf=kerf).repeat(2)
    grain_right = EndGrain(positive=False, kerf=kerf).repeat(2)
    feed.drives(wheels.spin, ratio=180 / (12 * 3.141592653589793))

    def render(self):
        for wheel, (x, y) in zip(self.wheels, ((-125, -41), (-125, 41), (125, -41), (125, 41))):
            wheel.translate([x, y, 302.2])
        for axle, x in zip(self.axles, (-125, 125)):
            axle.translate([x, 0, 302.2])
        for grains in (self.grain_left, self.grain_right):
            grains[0].translate([175.2, 0, 353.2])
            grains[1].rotate(180, [0, 0, 1]).translate([-175.2, 0, 353.2])

class LeonardoHydraulicSawmill(AssemblyNode):
    kerf = Length(3.2, min=2, max=5)
    paddles = Count(16, min=12, max=24)
    foundation = Foundation()
    timber_structure = OakStructure()
    waterwheel = Wheel(paddles=paddles)
    hoops = WheelHoop().repeat(2)
    crankshaft = Crankshaft()
    connecting_rod = ConnectingRod()
    sash = SawSash()
    carriage = TimberCarriage(kerf=kerf)
    feed_drum = RatchetDrum()
    pawl_carrier = PawlCarrier()
    pawl = Pawl()
    rope = HaulRope()
    tailrace = Tailrace()
    flume_water = FlumeWater()
    plaque = Plaque()
    phase = Driver(default=0, range=(0, 1440), unit='deg')
    playback = Driver(default=1, range=(0, 1))
    instructions = {
        'Start of pass': Instruction({'phase': 0, 'playback': 0}, duration=0.6),
        'Half stroke': Instruction({'phase': 90, 'playback': 0}, duration=1),
        'Bottom of cut': Instruction({'phase': 180, 'playback': 0}, duration=1),
        'Run four cycles': Instruction({'phase': 1440, 'playback': 0}, duration=16),
        'Timeline motion': Instruction({'phase': 0, 'playback': 1}, duration=0.6),
    }

    def render(self):
        self.waterwheel.translate([0, -151, 120])
        for hoop, y in zip(self.hoops, (-176, -126)):
            hoop.translate([0, y, 120])
        self.crankshaft.translate([0, 0, 120])
        self.connecting_rod.translate([0, -84, 120 + CRANK])
        self.sash.translate([0, 0, 120])
        self.carriage.translate([-70, 0, 0])
        for part in (self.feed_drum, self.pawl_carrier, self.pawl):
            part.translate([240, 0, 330])
        self.rope.rotate(-90, [0, 1, 0]).translate([240, 0, 330 - DRUM_RADIUS - 1.2])

    def simulate(self):
        angle = self.phase + 1440 * self.time * self.playback
        progress = feed_steps(angle)
        self.waterwheel.spin = angle
        self.crankshaft.spin = angle
        for hoop in self.hoops:
            hoop.spin = angle
        self.connecting_rod.orbit = angle
        self.connecting_rod.lean = rod_lean(angle)
        self.sash.rise = saw_height(angle)
        self.carriage.feed = FEED * progress
        ratchet = -360 / TEETH * progress
        self.feed_drum.spin = ratchet
        self.pawl_carrier.spin = ratchet
        self.pawl.carry = ratchet
        self.pawl.lift = pawl_lift(angle)
        self.rope.reach = 240 - (104 + FEED * progress)
