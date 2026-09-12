"""MUST IGB-37 hydraulic saw: a source-led, connected reconstruction."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi
from solid_node.node import AssemblyNode, FusionNode
from solid_node.parameters import Length
from solid_node.motion.joints import Prismatic
from solid_node.motion.ports import RotationalPort
from solid_node.simulation import Driver, Instruction
from .parts import (Foundation, OakStructure, WaterChannel, WaterSurface, Wheel,
                    Crankshaft, ConnectingRod, SashWood, SawBlade, BladeClamp,
                    TensionNut, SashPin, CarriageBed, CarriageWheel, CarriageAxle,
                    LogHalf, EndGrain, RatchetDrum, Rocker, FeedTie, DrivingPawl,
                    HoldingPawl, FeedBearings, FixedPins, ReturnPulley,
                    PulleyBracket, PulleyPin, HaulRope)
from .layout import (CRANK, FEED, AXLE_Z, LINK_Y, TIE_Y, PAWL_Y, RATCHET_X,
                     RATCHET_Z, ROCKER_X, ROCKER_Z, ROPE_Y, ROPE_TOP, PULLEY_X,
                     ANCHOR_X, INITIAL_WRAP, ROPE_PITCH_RADIUS)
from .kinematics import (saw_height, rod_lean, rocker_angle, ratchet_angle,
                         pawl_pose, tie_pose, holding_angle, clip01, HOLD_X, HOLD_Z)

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

class TimberCarriage(AssemblyNode):
    kerf=Length(3.2,min=2,max=5)
    feed=Prismatic(axis=(1,0,0))
    bed=CarriageBed()
    outer_wheels=CarriageWheel().repeat(2)
    inner_wheels=CarriageWheel(positive=False).repeat(2)
    axles=CarriageAxle().repeat(2)
    log_left=LogHalf(positive=True,kerf=kerf)
    log_right=LogHalf(positive=False,kerf=kerf)
    grain_left=EndGrain(positive=True,kerf=kerf).repeat(2)
    grain_right=EndGrain(positive=False,kerf=kerf).repeat(2)
    feed.drives(outer_wheels.spin,ratio=180/(12*pi))
    feed.drives(inner_wheels.spin,ratio=180/(12*pi))
    def render(self):
        for wheels,y in ((self.outer_wheels,42),(self.inner_wheels,-42)):
            for wheel,x in zip(wheels,(-125,125)):
                wheel.translate([x,y,357.2])
        for axle,x in zip(self.axles,(-125,125)):
            axle.translate([x,0,357.2])
        for grains in (self.grain_left,self.grain_right):
            grains[0].translate([175.2,0,408.2])
            grains[1].rotate(180,[0,0,1]).translate([-175.2,0,408.2])

class LeonardoHydraulicSawmill(AssemblyNode):
    kerf=Length(3.2,min=2,max=5)
    foundation=Foundation()
    timber_structure=TimberStand()
    channel=WaterChannel()
    water=WaterSurface()
    waterwheel=Wheel()
    crankshaft=Crankshaft()
    connecting_rod=ConnectingRod()
    sash=SawSash()
    carriage=TimberCarriage(kerf=kerf)
    feed_drum=RatchetDrum()
    rocker=Rocker()
    feed_tie=FeedTie()
    pawl=DrivingPawl()
    holding_pawl=HoldingPawl()
    rocker_pin=FixedPins(x=ROCKER_X,z=ROCKER_Z)
    holding_pin=FixedPins(x=HOLD_X,z=HOLD_Z)
    return_pulley=ReturnPulley()
    pulley_pin=PulleyPin()
    rope=HaulRope()
    phase=Driver(default=0,range=(0,1440),unit='deg')
    playback=Driver(default=1,range=(0,1))
    cycle=RotationalPort(unit='deg')
    instructions={
        'Start of pass':Instruction({'phase':0,'playback':0},duration=0.6),
        'Half stroke':Instruction({'phase':90,'playback':0},duration=1),
        'Bottom of cut':Instruction({'phase':180,'playback':0},duration=1),
        'Feed working':Instruction({'phase':270,'playback':0},duration=1),
        'Run four cycles':Instruction({'phase':1440,'playback':0},duration=16),
        'Timeline motion':Instruction({'phase':0,'playback':1},duration=0.6),
    }
    cycle.drives(waterwheel.spin)
    waterwheel.spin.drives(crankshaft.spin)
    crankshaft.spin.drives(connecting_rod.orbit)
    crankshaft.spin.drives(connecting_rod.lean,law=lambda a,b:rod_lean)
    crankshaft.spin.drives(sash.rise,law=lambda a,b:saw_height)
    sash.rise.drives(rocker.turn,law=lambda a,b:rocker_angle)
    sash.rise.drives(feed_tie.turn,law=lambda a,b:tie_pose)
    sash.rise.drives(feed_tie.rise)
    cycle.drives((pawl.turn,pawl.shift_x,pawl.shift_z),law=lambda a,b:pawl_pose)
    cycle.drives(feed_drum.spin,law=lambda a,b:ratchet_angle)
    feed_drum.spin.drives(holding_pawl.turn,law=lambda a,b:holding_angle)
    feed_drum.spin.drives(carriage.feed,ratio=pi*ROPE_PITCH_RADIUS/180)
    feed_drum.spin.drives(return_pulley.spin)
    feed_drum.spin.drives(rope.wrap,ratio=pi/180,offset=INITIAL_WRAP*pi/180)
    carriage.feed.drives(rope.to_pulley,ratio=-1,offset=PULLEY_X-ANCHOR_X)
    carriage.feed.drives(rope.to_drum,ratio=-1,offset=RATCHET_X-ANCHOR_X)
    def render(self):
        self.waterwheel.translate([0,-151,AXLE_Z])
        self.crankshaft.translate([0,0,AXLE_Z])
        self.connecting_rod.translate([0,-34,AXLE_Z+CRANK])
        self.sash.translate([0,0,AXLE_Z])
        self.carriage.translate([-70,0,0])
        self.feed_drum.translate([RATCHET_X,0,RATCHET_Z])
        self.rocker.translate([ROCKER_X,LINK_Y,ROCKER_Z])
        self.feed_tie.translate([0,TIE_Y,AXLE_Z])
        self.pawl.translate([0,PAWL_Y,0])
        self.holding_pawl.translate([HOLD_X,PAWL_Y,HOLD_Z])
        self.return_pulley.translate([PULLEY_X,ROPE_Y,RATCHET_Z])
        self.pulley_pin.translate([PULLEY_X,ROPE_Y,RATCHET_Z])
        self.rope.translate([ANCHOR_X,ROPE_Y,ROPE_TOP])
    def simulate(self):
        # Both advertised controls together remain inside the same four-pass
        # envelope: pause at the end, never wind a second overlapping layer.
        self.cycle=1440*clip01((self.phase+1440*self.time*self.playback)/1440)
        # A flexible leaf's ports must exactly match its shape parameters;
        # its moving origin is therefore placed explicitly, using the same
        # take-up as the carriage relation (not a second independent input).
        self.rope.translate([ratchet_angle(self.cycle.value)*pi*ROPE_PITCH_RADIUS/180,0,0])
