"""Closed geometric linkage; the same degree expressions drive the viewer."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi
from machinome.math import acos, sin, cos, sqrt, atan2
from .layout import (CRANK, ROD, AXLE_Z, TEETH, PITCH,
                     ROCKER_X, ROCKER_Z, ROCKER_LONG, TIE_LENGTH,
                     ROCKER_BRANCH, PAWL_LENGTH, CONTACT_RADIUS,
                     RATCHET_X, RATCHET_Z, HOLD_RADIUS)
from .rope_drive import carriage_advance
from .contact import tooth_profile, drive_profile, hold_profile, transformed, lift_for, table_value, follow_lift

def clip01(x):
    positive = (x + sqrt(x*x))/2
    over = positive-1
    return positive-(over+sqrt(over*over))/2

def cycle_angle(angle):
    return 180+atan2(sin(angle-180), cos(angle-180))

def saw_height(angle):
    return CRANK*cos(angle)+sqrt(ROD*ROD-(CRANK*sin(angle))**2)

def rod_lean(angle):
    return atan2(-CRANK*sin(angle), sqrt(ROD*ROD-(CRANK*sin(angle))**2))

def rocker_angle(height):
    """Intersection of the rocker-tip and saw-journal tie circles."""
    dx, dz = -ROCKER_X, AXLE_Z+height-ROCKER_Z
    distance = sqrt(dx*dx+dz*dz)
    return atan2(dx,dz)+acos((ROCKER_LONG**2+distance**2-TIE_LENGTH**2)/(2*ROCKER_LONG*distance))

def contact_angle(rocker, arm, radius=CONTACT_RADIUS):
    """Near-side intersection of pawl-length and wheel-contact circles."""
    dx = ROCKER_X+arm*sin(rocker+ROCKER_BRANCH)-RATCHET_X
    dz = ROCKER_Z+arm*cos(rocker+ROCKER_BRANCH)-RATCHET_Z
    d = sqrt(dx*dx+dz*dz)
    return atan2(dx,dz)+acos((radius*radius+d*d-PAWL_LENGTH**2)/(2*radius*d))

def _short_arm():
    # Construction dimension: the two extreme closures differ by one tooth.
    lo, hi = 40.0, 60.0
    top, bottom = rocker_angle(ROD+CRANK), rocker_angle(ROD-CRANK)
    for _ in range(60):
        arm = (lo+hi)/2
        if contact_angle(top,arm)-contact_angle(bottom,arm) < PITCH:
            lo = arm
        else:
            hi = arm
    return (lo+hi)/2

SHORT_ARM = _short_arm()
START_CONTACT = contact_angle(rocker_angle(ROD+CRANK),SHORT_ARM)
# Seat after the departing tooth has cleared, before the wheel's dwell.
# The previous +1 degree reach left the pawl on the crest at the seam.
HOLD_CONTACT = START_CONTACT+10*PITCH+3.0
HOLD_X, HOLD_Z = RATCHET_X+78.0, RATCHET_Z+10.0
HOLD_LENGTH = sqrt((RATCHET_X+HOLD_RADIUS*sin(HOLD_CONTACT)-HOLD_X)**2
                  +(RATCHET_Z+HOLD_RADIUS*cos(HOLD_CONTACT)-HOLD_Z)**2)

def ratchet_angle(angle):
    local = cycle_angle(angle)
    completed = (angle-local)/360
    # The descending short arm PULLS its hook away from the wheel.
    # The wheel holds at bottom while the hook rises over the next tooth.
    active = 180*clip01(local/180)
    return -completed*PITCH+contact_angle(rocker_angle(saw_height(active)),SHORT_ARM)-START_CONTACT

def feed_steps(angle):
    return -ratchet_angle(angle)/PITCH

def _drive_at_radius(angle,radius):
    rocker = rocker_angle(saw_height(angle))
    dx = ROCKER_X+SHORT_ARM*sin(rocker+ROCKER_BRANCH)
    dz = ROCKER_Z+SHORT_ARM*cos(rocker+ROCKER_BRANCH)
    g = contact_angle(rocker,SHORT_ARM,radius)
    return (atan2(RATCHET_X+radius*sin(g)-dx,RATCHET_Z+radius*cos(g)-dz),dx,dz)

def pawl_pose(angle):
    fraction=clip01((cycle_angle(angle)-180)/180)
    radius=CONTACT_RADIUS+table_value(fraction,DRIVE_LIFTS,clip01)
    return _drive_at_radius(angle,radius)

def tie_pose(height):
    rocker = rocker_angle(height)
    bx = ROCKER_X+ROCKER_LONG*sin(rocker)
    bz = ROCKER_Z+ROCKER_LONG*cos(rocker)
    return atan2(bx,bz-AXLE_Z-height)

def _hold_at_radius(radius):
    dx, dz = HOLD_X-RATCHET_X, HOLD_Z-RATCHET_Z
    d = sqrt(dx*dx+dz*dz)
    g = atan2(dx,dz)-acos((radius*radius+d*d-HOLD_LENGTH**2)/(2*radius*d))
    return atan2(RATCHET_X+radius*sin(g)-HOLD_X,RATCHET_Z+radius*cos(g)-HOLD_Z)

def holding_angle(spin):
    fraction=cycle_angle(-spin*TEETH)/360
    return _hold_at_radius(HOLD_RADIUS+table_value(fraction,HOLD_LIFTS,clip01))

# Construction-time contact sampling. Circle closure is retained at every
# intermediate viewer pose; only contact/gravity seating is approximated.
_teeth=tooth_profile(START_CONTACT)
DRIVE_LIFTS=tuple(lift_for(
    lambda radius,a=180+i: (
        lambda turn,x,z:(turn,x-RATCHET_X,z-RATCHET_Z))(*_drive_at_radius(a,radius)),
    drive_profile(),transformed(_teeth,-PITCH),CONTACT_RADIUS) for i in range(181))
# Clearance-envelope interpolation must cover both sides of a tooth-tip
# transition: anticipate its rise and retain its lift before lowering.
# This is prescribed seating, not a gravity/contact-force simulation.
def _holding_envelope():
    values=[]
    retained=0.0
    # Warm through a tooth first: a fresh low landing is not necessarily
    # reachable from the preceding tooth. Keep the steady periodic branch.
    for i in range(360):
        retained=follow_lift(
            lambda radius:(_hold_at_radius(radius),HOLD_X-RATCHET_X,HOLD_Z-RATCHET_Z),
            hold_profile(HOLD_LENGTH),transformed(_teeth,-i*PITCH/180),HOLD_RADIUS,retained)
        if i>=180:
            values.append(retained)
    envelope=tuple(max(values[(i-1)%180],values[i],values[(i+1)%180]) for i in range(180))
    # Identical seam values make roundoff either side of a completed tooth
    # harmless in Python and the exported browser relation, without an
    # epsilon phase shift or a second animation law.
    return envelope+(envelope[0],)

HOLD_LIFTS=_holding_envelope()
