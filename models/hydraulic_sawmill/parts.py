"""Original CAD reconstructing MUST IGB-37; dimensions are documented choices."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import cadquery as cq
from molejo import Shape, Circle, Polygon, Line, Arc, Helix, Spline, P
from machinome.node import CadQueryNode, MolejoNode
from machinome.parameters import Length, Angle, Flag
from machinome.motion.joints import Revolute, Orbit, Prismatic
from machinome.motion.ports import TranslationalPort, RotationalPort
from .layout import (CRANK, ROD, SASH_HEIGHT, TEETH, RATCHET_AXLE_RADIUS, ROPE_RADIUS,
                     ROPE_PITCH_RADIUS, RATCHET_ROOT, RATCHET_TIP, PAWL_LENGTH,
                     ROCKER_LONG, TIE_LENGTH, ROCKER_BRANCH, LINK_Y, TIE_Y,
                     PAWL_Y, ROPE_Y, RATCHET_X, RATCHET_Z,
                     TIMBER_LENGTH, CRADLE_X, INITIAL_WRAP, DRUM_Y,
                     ROD_Y, CRANK_Y, ROPE_ANCHOR_Z, ANCHOR_LOCAL_X,
                     FEED_OFFSET_Y, CARRIAGE_ROPE_Y, FRAME_END,
                     UPPER_X, UPPER_Z, UPPER_RADIUS, REDUCER_X, REDUCER_Z,
                     REDUCER_RADIUS, HAUL_RADIUS, IDLER_X, IDLER_Z, IDLER_RADIUS,
                     DRIVE_START_Y, LARGE_START_Y, IDLER_Y, INPUT_RESERVE, WIND_PITCH,
                     SPIRAL_POINTS,
                     HAUL_TIE_Y, HAUL_INITIAL)
from .rope_drive import (GEAR_PHASE, INPUT_PHASE, HAUL_PHASE, GEAR_CONTACT,
                        IDLER_IN, IDLER_OUT, INPUT_CONTACT, IDLER_SWEEP,
                        UPPER_EXIT, HAUL_CONTACT, GEAR_TIE_PHASE, RADIAL_LEAD, SPIRAL_PORTS,
                        DRIVE_BEND_POINTS, DRIVE_BEND_PORTS, IDLER_OUT_PHASE)
from .kinematics import SHORT_ARM, START_CONTACT, HOLD_LENGTH, HOLD_X, HOLD_Z

IRON = '#39464B'
def box(x,y,z,at=(0,0,0)):
    return cq.Workplane('XY').box(x,y,z).translate(at)

def cylinder_y(radius,length,at=(0,0,0)):
    return (cq.Workplane('XY').circle(radius).extrude(length)
            .rotate((0,0,0),(1,0,0),-90)
            .translate((at[0],at[1]-length/2,at[2])))

def profile_xz(points,depth,y=0):
    return (cq.Workplane('XY').polyline(points).close().extrude(depth)
            .rotate((0,0,0),(1,0,0),90).translate((0,y+depth/2,0)))

def beam_between(a,b,width,depth):
    return (box(width,depth,math.hypot(b[0]-a[0],b[2]-a[2]))
            .rotate((0,0,0),(0,1,0),math.degrees(math.atan2(b[0]-a[0],b[2]-a[2])))
            .translate(tuple((v+w)/2 for v,w in zip(a,b))))

def eyed_link(length,width,depth,bore):
    shape=box(width,depth,length,(0,0,length/2))
    for z in (0,length):
        shape=shape.union(cylinder_y(width/2,depth,(0,0,z)))
        shape=shape.cut(cylinder_y(bore,depth+2,(0,0,z)))
    return shape

class Foundation(CadQueryNode):
    color='#51443A'
    def render(self):
        return box(875,505,18,(0,-30,9)).edges('|Z').chamfer(4)

class WaterChannel(CadQueryNode):
    color='#BD9156'
    def render(self):
        floor=[(-355,20),(94,20),(350,106),(350,112),(94,26),(-355,26)]
        shape=profile_xz(floor,70,-151)
        for y in (-188,-114):
            wall=[(-355,20),(94,20),(350,106),(350,138),(94,52),(-355,52)]
            shape=shape.union(profile_xz(wall,6,y))
        for y in (-180,-122):
            shape=shape.union(box(14,12,86,(338,y,61)))
        shape=shape.union(box(16,70,12,(338,-151,24)))
        return shape

class WaterSurface(CadQueryNode):
    color='#537E84'
    def render(self):
        # A surface just below the lowest paddle; no water-force geometry.
        return profile_xz([(-351,26.5),(94,26.5),(346,111.2),
                           (346,111.8),(94,27.1),(-351,27.1)],62,-151)

class Wheel(CadQueryNode):
    color='#B78549'
    spin=Revolute(axis=(0,1,0))
    def render(self):
        shape=cylinder_y(15,60).cut(cylinder_y(6.6,64))
        for y in (-25,25):
            shape=shape.union(cylinder_y(80,6,(0,y,0)).cut(cylinder_y(68,10,(0,y,0))))
            for a in range(0,360,45):
                shape=shape.union(box(9,6,70,(0,y,39)).rotate((0,0,0),(0,1,0),a))
        for a in range(0,360,45):
            shape=shape.union(box(5,52,22,(0,0,81)).rotate((0,0,0),(0,1,0),a))
        return shape.cut(cylinder_y(6.6,64)).cut(box(4.4,64,8.8,(0,0,4.4)))

class Crankshaft(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        end=CRANK_Y-4
        shape=cylinder_y(6,end+216,(0,(end-216)/2,0))
        shape=shape.union(box(3.2,50,2.8,(0,-151,6.4)))
        for y in (-183.5,-118.5):
            shape=shape.union(cylinder_y(9,3,(0,y,0)))
        # Square tenon emerges from the round shaft into the separate crank.
        shape=shape.union(box(8,14,8,(0,CRANK_Y+2,0)))
        shape=shape.union(cylinder_y(9,3,(0,CRANK_Y-5.5,0)))
        shape=shape.union(cylinder_y(7,3,(0,CRANK_Y+8,0)))
        return shape.union(cylinder_y(9,3,(0,-217.5,0)))

class Crank(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        web=eyed_link(CRANK,19,6,0.01).translate((0,CRANK_Y,0))
        web=web.cut(box(8.6,10,8.6,(0,CRANK_Y,0)))
        web=web.union(cylinder_y(4.2,20,(0,ROD_Y-4,CRANK)))
        return web.union(cylinder_y(7,2,(0,ROD_Y+5,CRANK)))

class CrankRetainer(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        y=CRANK_Y+5
        return cylinder_y(8,2,(0,y,0)).cut(box(8.6,6,8.6,(0,y,0)))

class ConnectingRod(CadQueryNode):
    color=IRON
    lean=Revolute(axis=(0,1,0))
    orbit=Orbit(axis=(0,1,0),at=(0,0,-CRANK))
    def render(self):
        # Centered rod; two upper ears straddle the blade's lower clamp.
        # The force line stays on the saw centre, not on a long cantilever pin.
        shape=eyed_link(ROD,15,6,4.8).cut(box(20,20,30,(0,0,ROD+5)))
        shape=shape.union(box(15,15,8,(0,0,ROD-12)))
        for y in (-6,6):
            ear=box(15,3,12,(0,y,ROD-6)).union(cylinder_y(7.5,3,(0,y,ROD)))
            shape=shape.union(ear.cut(cylinder_y(4.8,5,(0,y,ROD))))
        return shape

class SashWood(CadQueryNode):
    color='#A67742'
    def render(self):
        shape=box(16,142,10).union(box(16,142,10,(0,0,SASH_HEIGHT)))
        for y in (-66,66):
            shape=shape.union(box(16,10,SASH_HEIGHT,(0,y,SASH_HEIGHT/2)))
        shape=shape.cut(cylinder_y(4.8,146))
        # Central iron fork, blade fork and adjacent feed tie share a journal.
        shape=shape.cut(box(22,30,26,(0,-3,-5)))
        shape=shape.cut(box(6.6,5.6,12,(0,0,2)))
        return shape.cut(cq.Workplane('XY').circle(2.6).extrude(24).translate((0,0,292)))

class SawBlade(CadQueryNode):
    color='#9BA8A7'
    def render(self):
        points=[(5,10),(-5,10)]
        for z in range(20,278,6):
            # Teeth project toward the incoming log (-X); steep edge down.
            points.extend([(-5,z),(-10,z+1),(-5,z+4)])
        points.extend([(-5,290),(5,290)])
        shape=profile_xz(points,1.2)
        for z in (15,285):
            shape=shape.cut(cylinder_y(1.6,5,(0,0,z)))
        return shape

class BladeClamp(CadQueryNode):
    color=IRON
    upper=Flag(False)
    def render(self):
        shape=box(14,1.5,14,(0,-1.75,0)).union(box(14,1.5,14,(0,1.75,0)))
        shape=shape.union(box(14,5,3,(0,0,-8.4 if self.upper else -8.5)))
        shape=shape.union(cylinder_y(1.1,6))
        if self.upper:
            shape=shape.union(cq.Workplane('XY').circle(2).extrude(22.2).translate((0,0,-30)))
        else:
            shape=shape.union(box(6,5,8.5,(0,0,-13.75)))
            shape=shape.cut(cylinder_y(4.8,8,(0,0,-15)))
        return shape

class TensionNut(CadQueryNode):
    color=IRON
    def render(self):
        return cq.Workplane('XY').polygon(6,11).circle(2.4).extrude(5)

class SashPin(CadQueryNode):
    color=IRON
    def render(self):
        lo,hi=-76,76
        shape=cylinder_y(4.2,hi-lo,(0,(hi+lo)/2,0))
        return shape.union(cylinder_y(7,2,(0,lo-1,0))).union(cylinder_y(7,2,(0,hi+1,0)))

class CarriageBed(CadQueryNode):
    color='#A57348'
    kerf=Length(3.2,min=2,max=5)
    def render(self):
        shape=box(420,10,22,(0,-31,373.4)).union(box(420,10,22,(0,31,373.4)))
        for x in (-CRADLE_X,CRADLE_X):
            saddle=box(18,72,51,(x,0,388.5))
            recess=cq.Workplane('YZ').circle(29.3).extrude(24).translate((x-12,0,408.2))
            saddle=saddle.cut(recess).cut(box(20,self.kerf,60,(x,0,388.5)))
            shape=shape.union(saddle)
        for x in (-185,185):
            for y in (-31,31):
                shape=shape.union(box(16,10,24,(x,y,366)))
            shape=shape.cut(cylinder_y(3.6,105,(x,0,357.2)))
        for x in (-188,188):
            shape=shape.union(box(10,72,10,(x,0,ROPE_ANCHOR_Z)))
        return shape.cut(cq.Workplane('YZ').circle(1.3).extrude(16)
                         .translate((181,0,ROPE_ANCHOR_Z)))

class CarriageAnchor(CadQueryNode):
    """Rope through timber, with a compact stopper-knot envelope, not iron."""
    color='#D3B989'
    def render(self):
        cord=cq.Workplane('YZ').circle(ROPE_RADIUS).extrude(ANCHOR_LOCAL_X-179.5)
        cord=cord.translate((179.5,0,ROPE_ANCHOR_Z))
        knot=cq.Workplane('XY').sphere(2.4).translate((179.5,0,ROPE_ANCHOR_Z))
        return cord.union(knot)

class CarriageWheel(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    positive=Flag(True)
    def render(self):
        return (cylinder_y(12,8).union(cylinder_y(5,12,(0,2 if self.positive else -2,0)))
                .union(cylinder_y(14,2,(0,7.3 if self.positive else -7.3,0)))
                .cut(cylinder_y(3.6,20)))

class CarriageAxle(CadQueryNode):
    color=IRON
    def render(self):
        return cylinder_y(3,104).union(cylinder_y(5,2,(0,-52.5,0))).union(cylinder_y(5,2,(0,52.5,0)))

class LogHalf(CadQueryNode):
    color='#745238'
    positive=Flag(True)
    kerf=Length(3.2,min=2,max=5)
    def render(self):
        pts=[]
        for i in range(64):
            a=2*math.pi*i/64
            r=28+0.6*math.sin(5*a)**2
            pts.append((r*math.cos(a),r*math.sin(a)))
        shape=cq.Workplane('YZ').polyline(pts).close().extrude(TIMBER_LENGTH).translate((-TIMBER_LENGTH/2,0,408.2))
        y=-100+self.kerf/2 if self.positive else 100-self.kerf/2
        return shape.cut(box(354,200,100,(0,y,408.2)))

class EndGrain(CadQueryNode):
    color='#D5AD73'
    positive=Flag(True)
    kerf=Length(3.2,min=2,max=5)
    def render(self):
        shape=cq.Workplane('YZ').circle(27.7).extrude(0.5)
        for r in (6,11,17,23):
            shape=shape.cut(cq.Workplane('YZ').circle(r+0.25).circle(r).extrude(0.25).translate((0.3,0,0)))
        y=-100+self.kerf/2 if self.positive else 100-self.kerf/2
        return shape.cut(box(4,200,100,(0,y,0)))

class UncutTimber(MolejoNode):
    """Display material ahead of the teeth; collapsed mesh when fully cut.

    Sweep across the kerf so the Line never degenerates. The profile shrinks
    along the timber, then closes to zero area over its final 0.1 mm.
    The conservative 56 mm height stays inside the bark outline.
    """
    color='#745238'
    kerf=Length(3.2,min=2,max=5)
    remaining=TranslationalPort(unit='mm')
    top=TranslationalPort(unit='mm')
    bottom=TranslationalPort(unit='mm')
    def render(self):
        return Shape(Polygon([(0,P.bottom),(P.remaining,P.bottom),
                              (P.remaining,P.top),(0,P.top)]),
                     [Line((0,0,self.kerf))],path_samples=1,profile_samples=4)

class RatchetDrum(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        lo,hi=FEED_OFFSET_Y-126,FEED_OFFSET_Y+126
        shape=cylinder_y(RATCHET_AXLE_RADIUS,hi-lo,(0,(hi+lo)/2,0))
        for y in (FEED_OFFSET_Y-104.5,FEED_OFFSET_Y+104.5):
            shape=shape.union(cylinder_y(7,2,(0,y,0)))
        from .contact import tooth_profile
        pts=tooth_profile(START_CONTACT)
        wheel=profile_xz(pts,6,PAWL_Y)
        for a in (45,135,225,315):
            wheel=wheel.cut(cylinder_y(8,10,(24*math.sin(math.radians(a)),PAWL_Y,24*math.cos(math.radians(a)))))
        shape=shape.union(wheel)
        y=DRIVE_START_Y
        hole=cq.Workplane('XY').circle(1.3).extrude(60,both=True).translate((0,y,0))
        return shape.cut(hole.rotate((0,0,0),(0,1,0),GEAR_TIE_PHASE))

class Rocker(CadQueryNode):
    color=IRON
    turn=Revolute(axis=(0,1,0))
    def render(self):
        shape=eyed_link(ROCKER_LONG,9,5,4.8)
        offset=PAWL_Y-LINK_Y+10
        # The short iron arm is cranked outward; its working journal still
        # has only a 10 mm adjacent-layer offset, not an unsupported long pin.
        arm=(cq.Workplane('XY').rect(10,5).workplane(offset=20).rect(10,5)
             .workplane(offset=SHORT_ARM-20).center(0,offset).rect(10,5)
             .loft(ruled=True))
        arm=arm.union(cylinder_y(5,5,(0,offset,SHORT_ARM)))
        arm=arm.cut(cylinder_y(3.6,9,(0,offset,SHORT_ARM)))
        arm=arm.rotate((0,0,0),(0,1,0),ROCKER_BRANCH)
        shape=shape.union(arm)
        shape=shape.cut(cylinder_y(3.6,9))
        # Retained pins are rigid parts of the bell crank, bore in moving mate.
        for x,z,r,y,base in ((0,ROCKER_LONG,4.2,TIE_Y-LINK_Y,0),
                (SHORT_ARM*math.sin(math.radians(ROCKER_BRANCH)),
                 SHORT_ARM*math.cos(math.radians(ROCKER_BRANCH)),3,PAWL_Y-LINK_Y,offset)):
            shape=shape.union(cylinder_y(r+1,5,(x,base,z)))
            shape=shape.union(cylinder_y(r,24,(x,(y+base)/2,z)))
            shape=shape.union(cylinder_y(r+2,2,(x,y+(5 if y>0 else -5),z)))
        return shape

class FeedTie(CadQueryNode):
    color=IRON
    turn=Revolute(axis=(0,1,0))
    rise=Prismatic(axis=(0,0,1))
    def render(self):
        return eyed_link(TIE_LENGTH,11,3,4.8)

class DrivingPawl(CadQueryNode):
    color=IRON
    turn=Revolute(axis=(0,1,0))
    shift_x=Prismatic(axis=(1,0,0))
    shift_z=Prismatic(axis=(0,0,1))
    def render(self):
        from .contact import drive_profile
        shape=cylinder_y(5.5,4).union(profile_xz(drive_profile(),4))
        return shape.cut(cylinder_y(3.6,8))

class HoldingPawl(CadQueryNode):
    color=IRON
    turn=Revolute(axis=(0,1,0))
    def render(self):
        from .contact import hold_profile
        shape=cylinder_y(5.5,4).union(profile_xz(hold_profile(HOLD_LENGTH),4))
        return shape.cut(cylinder_y(3.6,8))

class FixedPins(CadQueryNode):
    color=IRON
    x=Length()
    z=Length()
    journal_y=Length(LINK_Y)
    head_offset=Length(5)
    def render(self):
        lo,hi=FEED_OFFSET_Y-126,self.journal_y+self.head_offset
        return (cylinder_y(3,hi-lo,(self.x,(hi+lo)/2,self.z))
                .union(cylinder_y(6,2,(self.x,lo-1,self.z)))
                .union(cylinder_y(6,2,(self.x,hi+1,self.z))))

class UpperRoller(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        return cylinder_y(UPPER_RADIUS-1.2,66).cut(cylinder_y(3.6,70))

class ReductionShaft(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        lo,hi=FEED_OFFSET_Y-117,FEED_OFFSET_Y+101
        shape=cylinder_y(HAUL_RADIUS-1.2,hi-lo,(0,(lo+hi)/2,0))
        for y in (FEED_OFFSET_Y-100,FEED_OFFSET_Y+84):
            shape=shape.union(cylinder_y(9,3,(0,y,0)))
        shape=shape.union(cylinder_y(REDUCER_RADIUS-1.2,32,(0,DRUM_Y,0)))
        for y in (DRUM_Y-17,DRUM_Y+17):
            shape=shape.union(cylinder_y(REDUCER_RADIUS+3.1,2,(0,y,0)))
        for y,phase in ((LARGE_START_Y+WIND_PITCH*INPUT_RESERVE,INPUT_PHASE-360*INPUT_RESERVE),
                        (HAUL_TIE_Y,HAUL_PHASE+360*HAUL_INITIAL)):
            hole=cq.Workplane('XY').circle(1.3).extrude(60,both=True).translate((0,y,0))
            shape=shape.cut(hole.rotate((0,0,0),(0,1,0),phase))
        return shape

class UpperPin(CadQueryNode):
    color=IRON
    def render(self):
        return cylinder_y(3,108).union(cylinder_y(5,2,(0,-54.5,0))).union(cylinder_y(5,2,(0,54.5,0)))

class DriveIdler(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        shape=cylinder_y(IDLER_RADIUS-1.2,10)
        for y in (-6,6):
            shape=shape.union(cylinder_y(IDLER_RADIUS+3.6,2,(0,y,0)))
        return shape.cut(cylinder_y(4.8,18))

class IdlerPin(CadQueryNode):
    color=IRON
    def render(self):
        lo,hi=FEED_OFFSET_Y-90,FEED_OFFSET_Y-41.5
        return (cylinder_y(4.2,hi-lo,(0,(hi+lo)/2,0))
                .union(cylinder_y(7,2,(0,lo,0)))
                .union(cylinder_y(7,2,(0,FEED_OFFSET_Y-58.5,0)))
                .union(cylinder_y(7,2,(0,hi,0))))

class DrumTie(CadQueryNode):
    """Through-bore rope termination; knot shown as a compact envelope."""
    color='#D3B989'
    spin=Revolute(axis=(0,1,0))
    radius=Length()
    lane=Length()
    phase=Angle()
    def render(self):
        r=self.radius
        cord=cq.Workplane('XY').circle(ROPE_RADIUS).extrude(2*r+3.6).translate((0,self.lane,-r-3.6))
        knot=cq.Workplane('XY').sphere(2.4).translate((0,self.lane,-r-3.6))
        return cord.union(knot).rotate((0,0,0),(0,1,0),self.phase)

class HaulRope(MolejoNode):
    color='#D3B989'
    centre_x=TranslationalPort(unit='mm')
    tangent_x=TranslationalPort(unit='mm')
    tangent_z=TranslationalPort(unit='mm')
    wrap=RotationalPort(unit='rad')
    def render(self):
        return Shape(Circle(ROPE_RADIUS),[
            Line((P.tangent_x,0,P.tangent_z)),
            Arc((P.centre_x,0,UPPER_Z-ROPE_ANCHOR_Z),(0,1,0),P.wrap),
        ],path_samples=72,profile_samples=12)

class HaulSpan(MolejoNode):
    color='#D3B989'
    lane=TranslationalPort(unit='mm')
    def render(self):
        return Shape(Circle(ROPE_RADIUS),
                     [Line((HAUL_CONTACT[0]-UPPER_EXIT[0],P.lane,HAUL_CONTACT[1]-UPPER_EXIT[1]))],
                     path_samples=1,profile_samples=12)

class DriveRope(MolejoNode):
    color='#D3B989'
    inlet_x=TranslationalPort(unit='mm')
    inlet_z=TranslationalPort(unit='mm')
    outlet_x=TranslationalPort(unit='mm')
    outlet_y=TranslationalPort(unit='mm')
    outlet_z=TranslationalPort(unit='mm')
    for coordinate in DRIVE_BEND_PORTS:
        locals()[coordinate]=TranslationalPort(unit='mm')
    del coordinate
    def render(self):
        return Shape(Circle(ROPE_RADIUS),[
            Line((P.inlet_x,IDLER_Y-DRIVE_START_Y,P.inlet_z)),
            # A supported spline sweep for the bend between fleeting spans.
            # Its radius and arc-length error remain independently tested;
            # no exact-kernel failure is hidden by changing the test kernel.
            Spline(points=[(getattr(P,f'bx{i}'),IDLER_Y-DRIVE_START_Y,getattr(P,f'bz{i}'))
                           for i in range(1,DRIVE_BEND_POINTS+1)],
                   start_tangent=(P.tx,0,P.tz),
                   end_tangent=(-math.cos(math.radians(IDLER_OUT_PHASE)),0,
                                 math.sin(math.radians(IDLER_OUT_PHASE)))),
            Line((P.outlet_x,P.outlet_y,P.outlet_z)),
        ],path_samples=6,profile_samples=12)

class RadialWindingRope(MolejoNode):
    """One planar rope coil, with successive turns stacked radially.

    Spline slots are ordinary declared ports, computed by the driving law;
    molejo parameters themselves intentionally contain no expressions.
    """
    color='#D3B989'
    for coordinate in SPIRAL_PORTS:
        locals()[coordinate]=TranslationalPort(unit='mm')
    del coordinate

    def render(self):
        return Shape(Circle(ROPE_RADIUS),[Spline(
            points=[(getattr(P,f'x{i}'),0,getattr(P,f'z{i}'))
                    for i in range(1,SPIRAL_POINTS+1)],
            start_tangent=(ROPE_PITCH_RADIUS,0,RADIAL_LEAD),
            end_tangent=(P.tx,0,P.tz))],
            path_samples=4,profile_samples=12)

class WindingRope(MolejoNode):
    color='#D3B989'
    radius=Length()
    turns=RotationalPort(unit='rev')
    height=TranslationalPort(unit='mm')
    def render(self):
        return Shape(Circle(ROPE_RADIUS),
                     [Helix(self.radius,P.turns,P.height)],
                     path_samples=720,profile_samples=12)
