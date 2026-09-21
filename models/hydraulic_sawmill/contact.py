"""Planar tooth-contact construction, independent of the CAD comparison kernel.

The exported motion is a piecewise-linear cam table. Values are constructed
from the actual two-dimensional profiles, with 0.25 mm running clearance;
they are not an independent timed ratchet animation or a dynamics solver.
"""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
from .layout import TEETH, RATCHET_ROOT, RATCHET_TIP, PAWL_LENGTH


def tooth_profile(start):
    return [(r*math.sin(math.radians(start-360/TEETH-1.0+i*360/TEETH+a)),
             r*math.cos(math.radians(start-360/TEETH-1.0+i*360/TEETH+a)))
            for i in range(TEETH)
            for a,r in ((0,RATCHET_ROOT),(360/TEETH-0.7,RATCHET_TIP),
                        (360/TEETH-0.05,RATCHET_ROOT))]


def drive_profile():
    length=PAWL_LENGTH
    # A returning hook: outside shank, crown and downward-facing toe.
    # The underside of the toe (z=length) carries the pulling reaction.
    return [(-1.5,0),(1.5,0),(1.5,length-25),(-5,length-12),
            (-5,length+1),(-1,length+1),(-1,length),(3,length),
            (3,length+2),(-7,length+2),(-7,length-12),(-1.5,length-25)]


def hold_profile(length):
    return [(-1.5,0),(1.5,0),(1.5,length-9),
            (0.7,length),(0,length+0.4),(-0.7,length),(-1.5,length-9)]


def transformed(points,angle,x=0,z=0):
    s,c=math.sin(math.radians(angle)),math.cos(math.radians(angle))
    return [(x+c*u+s*v,z-s*u+c*v) for u,v in points]


def _cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def _point_segment(p,a,b):
    dx,dz=b[0]-a[0],b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz)))
    return (p[0]-a[0]-t*dx)**2+(p[1]-a[1]-t*dz)**2


def _inside(point,polygon):
    x,z=point
    inside=False
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        if (a[1]>z)!=(b[1]>z) and x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:
            inside=not inside
    return inside


def clear(pawl,teeth,gap=0.25):
    """Disjoint polygons with a positive edge clearance (millimetres)."""
    if any(_inside(p,teeth) for p in pawl):
        return False
    for a,b in zip(pawl,pawl[1:]+pawl[:1]):
        for c,d in zip(teeth,teeth[1:]+teeth[:1]):
            if (max(a[0],b[0])+gap<min(c[0],d[0]) or max(c[0],d[0])+gap<min(a[0],b[0])
                    or max(a[1],b[1])+gap<min(c[1],d[1]) or max(c[1],d[1])+gap<min(a[1],b[1])):
                continue
            if _cross(a,b,c)*_cross(a,b,d)<=0 and _cross(c,d,a)*_cross(c,d,b)<=0:
                return False
            if min(_point_segment(a,c,d),_point_segment(b,c,d),
                   _point_segment(c,a,b),_point_segment(d,a,b))<gap*gap:
                return False
    return True


def lift_for(pose,profile,teeth,base):
    def fits(lift):
        turn,x,z=pose(base+lift)
        return clear(transformed(profile,turn,x,z),teeth)
    if fits(0):
        return 0.0
    # Find the first clear branch, not an arbitrary distant circle solution.
    lo,hi=0.0,0.2
    while not fits(hi):
        lo,hi=hi,hi+0.2
        if hi>9:
            raise ValueError('Pawl cannot clear the tooth within its physical reach')
    for _ in range(12):
        mid=(lo+hi)/2
        if fits(mid):
            hi=mid
        else:
            lo=mid
    return hi


def table_value(fraction,values,clip):
    """Hinge-basis interpolation uses only supported symbolic arithmetic."""
    segments=len(values)-1
    terms=[(b-a)*clip(fraction*segments-i)
           for i,(a,b) in enumerate(zip(values,values[1:]))]
    # Keep the symbolic tree shallow enough for the builder to copy.
    while len(terms)>1:
        terms=[terms[i]+terms[i+1] if i+1<len(terms) else terms[i]
               for i in range(0,len(terms),2)]
    return values[0]+(terms[0] if terms else 0)


def follow_lift(pose,profile,teeth,base,previous):
    """Follow the current contact branch; never teleport through a tooth.

    A free low landing may be separated from the current pose by solid
    tooth material. Descend only through the connected clear interval.
    """
    def fits(lift):
        turn,x,z=pose(base+lift)
        return clear(transformed(profile,turn,x,z),teeth)
    high=previous
    while not fits(high):
        high+=0.1
        if high>9:
            raise ValueError('Holding pawl cannot follow the passing tooth')
    while high>0:
        low=max(0,high-0.05)
        if fits(low):
            high=low
            continue
        for _ in range(12):
            mid=(low+high)/2
            if fits(mid):
                high=mid
            else:
                low=mid
        break
    return high
