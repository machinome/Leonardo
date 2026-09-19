"""MUST IGB-37 hydraulic saw: a source-led, connected reconstruction."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi
from machinome.node import AssemblyNode, FusionNode
from machinome.parameters import Length
from machinome.motion.joints import Prismatic
from machinome.motion.ports import RotationalPort, Time
from .parts import (Foundation, OakStructure, WaterChannel, WaterSurface, Wheel,
                    Crankshaft, ConnectingRod, SashWood, SawBlade, BladeClamp,
                    TensionNut, SashPin, CarriageBed, CarriageWheel, CarriageAxle,
                    LogHalf, EndGrain, RatchetDrum, Rocker, FeedTie, DrivingPawl,
                    HoldingPawl, FeedBearings, FixedPins, ReturnPulley,
                    PulleyBracket, PulleyPin, HaulRope, ReturnSpan, WindingRope, UncutTimber)
from .layout import (CRANK, FEED, AXLE_Z, LINK_Y, TIE_Y, PAWL_Y, RATCHET_X,
                     RATCHET_Z, ROCKER_X, ROCKER_Z, ROPE_Y, ROPE_TOP, PULLEY_X,
                     ANCHOR_X, INITIAL_WRAP, ROPE_PITCH_RADIUS, TIMBER_LENGTH,
                     CARRIAGE_START, PASS_ANGLE, PASS_SECONDS, CLEAT_Y, WIND_PITCH)
from .kinematics import (saw_height, rod_lean, rocker_angle, ratchet_angle,
                         pawl_pose, tie_pose, holding_angle, clip01, HOLD_X, HOLD_Z, carriage_advance)

def uncut_profile(advance):
    remaining=TIMBER_LENGTH*clip01((-10.2-CARRIAGE_START+TIMBER_LENGTH/2-advance)/TIMBER_LENGTH)
    half_height=28*clip01(remaining/0.1)
    return remaining,half_height,-half_height

class TimberStand(FusionNode):
    color='#A87944'
    table=OakStructure()
    feed_supports=FeedBearings()
    pulley_support=PulleyBracket()

class BladeAttachments(AssemblyNode):
    lower=BladeClamp()
    upper=BladeClamp(upper=True)
    nut=TensionNut()
    def render(self):
        self.lower.translate([0,0,15])
        self.upper.rotate(180,[0,1,0]).translate([0,0,285])
        self.nut.translate([0,0,305.2])

class SawSash(AssemblyNode):
    rise=Prismatic(axis=(0,0,1))
    frame=SashWood()
    blade=SawBlade()
    pin=SashPin()
    clamps=BladeAttachments()

class Timber(AssemblyNode):
    kerf=Length(3.2,min=2,max=5)
    log_left=LogHalf(positive=True,kerf=kerf,name='Left timber half')
    log_right=LogHalf(positive=False,kerf=kerf,name='Right timber half')
    uncut=UncutTimber(kerf=kerf,name='Uncut wood at the kerf')
    grain_left=EndGrain(positive=True,kerf=kerf).repeat(2)
    grain_right=EndGrain(positive=False,kerf=kerf).repeat(2)
    def render(self):
        self.uncut.rotate(90,[1,0,0]).translate([-TIMBER_LENGTH/2,self.kerf/2,408.2])
        for grains in (self.grain_left,self.grain_right):
            grains[0].translate([TIMBER_LENGTH/2+0.2,0,408.2])
            grains[1].rotate(180,[0,0,1]).translate([-TIMBER_LENGTH/2-0.2,0,408.2])

class RunningGear(AssemblyNode):
    outer_wheels=CarriageWheel().repeat(2)
    inner_wheels=CarriageWheel(positive=False).repeat(2)
    axles=CarriageAxle().repeat(2)
    def render(self):
        for wheels,y in ((self.outer_wheels,42),(self.inner_wheels,-42)):
            for wheel,x in zip(wheels,(-185,185)):
                wheel.translate([x,y,357.2])
        for axle,x in zip(self.axles,(-185,185)):
            axle.translate([x,0,357.2])

class TimberCarriage(AssemblyNode):
    kerf=Length(3.2,min=2,max=5)
    feed=Prismatic(axis=(1,0,0))
    bed=CarriageBed(kerf=kerf,name='Bed and slotted log cradles')
    timber=Timber(kerf=kerf,name='Timber')
    running_gear=RunningGear(name='Rollers and axles')
    feed.drives(running_gear.outer_wheels.spin,ratio=180/(12*pi))
    feed.drives(running_gear.inner_wheels.spin,ratio=180/(12*pi))

class Frame(AssemblyNode):
    foundation=Foundation(name='Foundation')
    timber_structure=TimberStand(name='Timber stand and guides')

class WaterDrive(AssemblyNode):
    channel=WaterChannel(name='Water channel')
    water=WaterSurface(name='Water surface')
    waterwheel=Wheel(name='Undershot waterwheel')
    crankshaft=Crankshaft(name='Keyed crankshaft')
    def render(self):
        self.waterwheel.translate([0,-151,AXLE_Z])
        self.crankshaft.translate([0,0,AXLE_Z])

class SawMechanism(AssemblyNode):
    connecting_rod=ConnectingRod(name='Connecting rod')
    sash=SawSash(name='Guided saw sash')
    def render(self):
        self.connecting_rod.translate([0,-34,AXLE_Z+CRANK])
        self.sash.translate([0,0,AXLE_Z])

class DrumWinding(AssemblyNode):
    shift=Prismatic(axis=(0,1,0))
    rope=WindingRope(name='Wound rope')
    def render(self):
        self.rope.rotate(-90,[1,0,0]).rotate(90,[0,1,0])

class FeedMechanism(AssemblyNode):
    feed_drum=RatchetDrum(name='Ratchet and winding drum')
    rocker=Rocker(name='Feed rocker')
    feed_tie=FeedTie(name='Saw-to-rocker tie')
    pawl=DrivingPawl(name='Driving pawl')
    holding_pawl=HoldingPawl(name='Holding pawl')
    rocker_pin=FixedPins(x=ROCKER_X,z=ROCKER_Z,name='Rocker pivot')
    holding_pin=FixedPins(x=HOLD_X,z=HOLD_Z,name='Holding-pawl pivot')
    return_pulley=ReturnPulley(name='Return pulley')
    pulley_pin=PulleyPin(name='Pulley axle')
    rope=HaulRope(name='Haul rope')
    return_span=ReturnSpan(name='Lower return span')
    winding=DrumWinding(name='Drum winding')
    def render(self):
        self.feed_drum.translate([RATCHET_X,0,RATCHET_Z])
        self.rocker.translate([ROCKER_X,LINK_Y,ROCKER_Z])
        self.feed_tie.translate([0,TIE_Y,AXLE_Z])
        self.pawl.translate([0,PAWL_Y,0])
        self.holding_pawl.translate([HOLD_X,PAWL_Y,HOLD_Z])
        self.return_pulley.translate([PULLEY_X,ROPE_Y,RATCHET_Z])
        self.pulley_pin.translate([PULLEY_X,ROPE_Y,RATCHET_Z])
        self.rope.translate([ANCHOR_X,ROPE_Y,ROPE_TOP])
        self.return_span.translate([PULLEY_X,ROPE_Y,RATCHET_Z-ROPE_PITCH_RADIUS])
        self.winding.translate([RATCHET_X,CLEAT_Y+WIND_PITCH*INITIAL_WRAP/360,RATCHET_Z-ROPE_PITCH_RADIUS])

class LeonardoHydraulicSawmill(AssemblyNode):
    kerf=Length(3.2,min=2,max=5)
    time=Time(loop=PASS_SECONDS)
    frame=Frame(name='Frame and guides')
    water_drive=WaterDrive(name='Water drive')
    saw=SawMechanism(name='Saw mechanism')
    carriage=TimberCarriage(kerf=kerf,name='Timber carriage')
    feed=FeedMechanism(name='Feed mechanism')
    cycle=RotationalPort(unit='deg')
    cycle.drives(water_drive.waterwheel.spin)
    water_drive.waterwheel.spin.drives(water_drive.crankshaft.spin)
    water_drive.crankshaft.spin.drives(saw.connecting_rod.orbit)
    water_drive.crankshaft.spin.drives(saw.connecting_rod.lean,law=lambda a,b:rod_lean)
    water_drive.crankshaft.spin.drives(saw.sash.rise,law=lambda a,b:saw_height)
    saw.sash.rise.drives(feed.rocker.turn,law=lambda a,b:rocker_angle)
    saw.sash.rise.drives(feed.feed_tie.turn,law=lambda a,b:tie_pose)
    saw.sash.rise.drives(feed.feed_tie.rise)
    cycle.drives((feed.pawl.turn,feed.pawl.shift_x,feed.pawl.shift_z),law=lambda a,b:pawl_pose)
    cycle.drives(feed.feed_drum.spin,law=lambda a,b:ratchet_angle)
    feed.feed_drum.spin.drives(feed.holding_pawl.turn,law=lambda a,b:holding_angle)
    feed.feed_drum.spin.drives(carriage.feed,law=lambda a,b:carriage_advance)
    carriage.feed.drives((carriage.timber.uncut.remaining,
                         carriage.timber.uncut.top,
                         carriage.timber.uncut.bottom),law=lambda a,b:uncut_profile)
    carriage.feed.drives(feed.return_pulley.spin,ratio=180/(pi*ROPE_PITCH_RADIUS))
    feed.feed_drum.spin.drives(feed.winding.shift,ratio=WIND_PITCH/360)
    feed.feed_drum.spin.drives(feed.winding.rope.turns,ratio=1/360,offset=INITIAL_WRAP/360)
    feed.feed_drum.spin.drives(feed.winding.rope.height,ratio=-WIND_PITCH/360,offset=-WIND_PITCH*INITIAL_WRAP/360)
    feed.feed_drum.spin.drives(feed.return_span.drum_y,ratio=WIND_PITCH/360,
                              offset=CLEAT_Y+WIND_PITCH*INITIAL_WRAP/360-ROPE_Y)
    carriage.feed.drives(feed.rope.to_pulley,ratio=-1,offset=PULLEY_X-ANCHOR_X)
    def render(self):
        self.carriage.translate([CARRIAGE_START,0,0])
    def simulate(self):
        self.cycle=PASS_ANGLE*clip01(self.time/PASS_SECONDS)
        # A flexible leaf's ports must exactly match its shape parameters;
        # its moving origin is therefore placed explicitly, using the same
        # take-up as the carriage relation (not a second independent input).
        self.feed.rope.translate([carriage_advance(ratchet_angle(self.cycle.value)),0,0])
