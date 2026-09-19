"""Original CAD reconstructing MUST IGB-37; dimensions are documented choices."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import cadquery as cq
from molejo import Shape, Circle, Polygon, Line, Arc, Helix, P
from machinome.node import CadQueryNode, MolejoNode
from machinome.parameters import Length, Flag
from machinome.motion.joints import Revolute, Orbit, Prismatic
from machinome.motion.ports import TranslationalPort, RotationalPort
from .layout import (CRANK, ROD, SASH_HEIGHT, TEETH, DRUM_RADIUS, ROPE_RADIUS,
                     ROPE_PITCH_RADIUS, RATCHET_ROOT, RATCHET_TIP, PAWL_LENGTH,
                     ROCKER_LONG, TIE_LENGTH, ROCKER_BRANCH, LINK_Y, TIE_Y,
                     PAWL_Y, ROPE_Y, ROPE_TOP, PULLEY_X, RATCHET_X, RATCHET_Z,
                     TIMBER_LENGTH, CRADLE_X, INITIAL_WRAP, CLEAT_Y, DRUM_Y)
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

class OakStructure(CadQueryNode):
    color='#A87944'
    def render(self):
        shape=box(720,18,20,(0,-99,72))
        for y in (-99,115):
            shape=shape.union(box(720,18,20,(0,y,72)))
            shape=shape.union(box(720,18,18,(0,y,330)))
            for x in (-335,335):
                shape=shape.union(box(22,22,320,(x,y,178)))
        for x in (-335,0,335):
            shape=shape.union(box(22,235,18,(x,8,72)))
        for x in (-335,335):
            shape=shape.union(box(22,235,16,(x,8,330)))
        # Only TWO continuous guide posts, as on the reference object.
        for y in (-78,78):
            post=box(26,20,627,(0,y,331.5))
            post=post.cut(box(17.2,12.4,405,(0,66*(1 if y>0 else -1),416.5)))
            post=post.cut(box(17.2,24,66,(0,y,267)))
            shape=shape.union(post)
        shape=shape.union(box(26,176,16,(0,0,637)))
        for y in (-42,42):
            shape=shape.union(box(760,12,10,(0,y,340)))
        # Under-table shaft and rocker pivot bores.
        for x,z,r in ((RATCHET_X,330,5.6),(-235,330,3.6)):
            shape=shape.cut(cylinder_y(r,260,(x,0,z)))
        for y in (-207,-95):
            stand=box(25,14,108,(0,y,72)).union(box(38,14,18,(0,y,120)))
            shape=shape.union(stand.cut(cylinder_y(6.6,24,(0,y,120))))
        # The bearing feet pass BELOW the channel, not through its trough.
        shape=shape.union(box(24,330,1.8,(0,-42,18.9)))
        shape=shape.cut(cylinder_y(6.6,28,(0,-78,120)))
        return shape.cut(box(18,112,18,(0,0,340)))

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
        shape=cylinder_y(6,170,(0,-131,0))
        shape=shape.union(box(3.2,50,2.8,(0,-151,6.4)))
        for y in (-183.5,-118.5):
            shape=shape.union(cylinder_y(9,3,(0,y,0)))
        web=eyed_link(CRANK,17,8,0.01).translate((0,-47,0))
        shape=shape.union(web).union(cylinder_y(4.2,24,(0,-34,CRANK)))
        shape=shape.union(cylinder_y(7,2,(0,-21,CRANK)))
        return shape.union(cylinder_y(9,3,(0,-217.5,0)))

class ConnectingRod(CadQueryNode):
    color=IRON
    lean=Revolute(axis=(0,1,0))
    orbit=Orbit(axis=(0,1,0),at=(0,0,-CRANK))
    def render(self):
        return eyed_link(ROD,15,6,4.8)

class SashWood(CadQueryNode):
    color='#A67742'
    def render(self):
        shape=box(16,142,10).union(box(16,142,10,(0,0,SASH_HEIGHT)))
        for y in (-66,66):
            shape=shape.union(box(16,10,SASH_HEIGHT,(0,y,SASH_HEIGHT/2)))
        shape=shape.cut(cylinder_y(4.8,146))
        shape=shape.cut(box(22,8,26,(0,-34,-5)))
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
        length=TIE_Y+13+76
        shape=cylinder_y(4.2,length,(0,(TIE_Y+13-76)/2,0))
        return shape.union(cylinder_y(7,2,(0,-77,0))).union(cylinder_y(7,2,(0,TIE_Y+14,0)))

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
        shape=shape.union(box(14,132,10,(204,34,370)))
        shape=shape.union(box(14,8,21,(204,ROPE_Y,355.5)))
        return shape.cut(cq.Workplane('YZ').circle(1.3).extrude(20).translate((194,ROPE_Y,ROPE_TOP)))

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
        return cylinder_y(3,110).union(cylinder_y(5,2,(0,-56,0))).union(cylinder_y(5,2,(0,56,0)))

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
        shape=cylinder_y(5,PAWL_Y+132,(0,(PAWL_Y-126)/2,0)).union(cylinder_y(DRUM_RADIUS,22,(0,DRUM_Y,0)))
        for y in (DRUM_Y-12,DRUM_Y+12):
            shape=shape.union(cylinder_y(27.5,2,(0,y,0)))
        from .contact import tooth_profile
        pts=tooth_profile(START_CONTACT)
        wheel=profile_xz(pts,6,PAWL_Y)
        for a in (45,135,225,315):
            wheel=wheel.cut(cylinder_y(8,10,(24*math.sin(math.radians(a)),PAWL_Y,24*math.cos(math.radians(a)))))
        shape=shape.union(wheel)
        # Rope end seats in a radial hole in this rotating iron cleat.
        cleat=box(6,3.2,6,(ROPE_PITCH_RADIUS,CLEAT_Y,0))
        cleat=cleat.cut(cq.Workplane('XY').circle(1.3).extrude(9).translate((ROPE_PITCH_RADIUS,CLEAT_Y,-4.5)))
        return shape.union(cleat.rotate((0,ROPE_Y,0),(0,ROPE_Y+1,0),INITIAL_WRAP-270))

class Rocker(CadQueryNode):
    color=IRON
    turn=Revolute(axis=(0,1,0))
    def render(self):
        shape=eyed_link(ROCKER_LONG,9,5,4.8)
        arm=eyed_link(SHORT_ARM,10,5,3.6).rotate((0,0,0),(0,1,0),ROCKER_BRANCH)
        shape=shape.union(arm)
        shape=shape.cut(cylinder_y(3.6,9))
        # Retained pins are rigid parts of the bell crank, bore in moving mate.
        for x,z,r,y,length in ((0,ROCKER_LONG,4.2,TIE_Y-LINK_Y,20),
                (SHORT_ARM*math.sin(math.radians(ROCKER_BRANCH)),
                 SHORT_ARM*math.cos(math.radians(ROCKER_BRANCH)),3,PAWL_Y-LINK_Y,35)):
            shape=shape.union(cylinder_y(r+1,5,(x,0,z)))
            shape=shape.union(cylinder_y(r,length,(x,y-5,z)))
            shape=shape.union(cylinder_y(r+2,2,(x,y+length/2-4,z)))
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

class FeedBearings(CadQueryNode):
    color='#A87944'
    def render(self):
        shape=box(330,12,12,(-145,115,347))
        for x,z,r in ((-235,330,3.6),(HOLD_X,HOLD_Z,3.6),(RATCHET_X,330,5.6)):
            arm=box(14,36,z-334+12,(x,130,(334+z+12)/2)) if z>334 else box(18,36,24,(x,130,335))
            shape=shape.union(arm.cut(cylinder_y(r,50,(x,134,z))))
        return shape

class FixedPins(CadQueryNode):
    color=IRON
    x=Length()
    z=Length()
    def render(self):
        return cylinder_y(3,74,(self.x,145,self.z)).union(cylinder_y(6,2,(self.x,183,self.z)))

class ReturnPulley(CadQueryNode):
    color=IRON
    spin=Revolute(axis=(0,1,0))
    def render(self):
        shape=cylinder_y(DRUM_RADIUS,10)
        for y in (-6,6):
            shape=shape.union(cylinder_y(27.5,3,(0,y,0)))
        return shape.cut(cylinder_y(3.6,20))

class PulleyBracket(CadQueryNode):
    color='#A87944'
    def render(self):
        shape=box(34,42,12,(PULLEY_X,ROPE_Y,294))
        for y in (ROPE_Y-16,ROPE_Y+16):
            shape=shape.union(box(16,8,43,(PULLEY_X,y,321)))
        shape=shape.union(box(80,14,10,(PULLEY_X-34,104,295)))
        return shape.cut(cylinder_y(3.6,50,(PULLEY_X,ROPE_Y,330)))

class PulleyPin(CadQueryNode):
    color=IRON
    def render(self):
        return cylinder_y(3,44).union(cylinder_y(5,2,(0,-23,0))).union(cylinder_y(5,2,(0,23,0)))

class HaulRope(MolejoNode):
    color='#D3B989'
    to_pulley=TranslationalPort(unit='mm')
    def render(self):
        r=ROPE_PITCH_RADIUS
        return Shape(Circle(ROPE_RADIUS),[
            Line((P.to_pulley,0,0)),
            Arc((P.to_pulley,0,-r),(0,1,0),math.pi),
        ],path_samples=72,profile_samples=12)

class ReturnSpan(MolejoNode):
    """Separate straight sweep keeps the fleet-angle span analytic."""
    color='#D3B989'
    drum_y=TranslationalPort(unit='mm')
    def render(self):
        return Shape(Circle(ROPE_RADIUS),
                     [Line((RATCHET_X-PULLEY_X,P.drum_y,0))],
                     path_samples=1,profile_samples=12)

class WindingRope(MolejoNode):
    color='#D3B989'
    turns=RotationalPort(unit='rev')
    height=TranslationalPort(unit='mm')
    def render(self):
        return Shape(Circle(ROPE_RADIUS),
                     [Helix(ROPE_PITCH_RADIUS,P.turns,P.height)],
                     path_samples=240,profile_samples=12)
