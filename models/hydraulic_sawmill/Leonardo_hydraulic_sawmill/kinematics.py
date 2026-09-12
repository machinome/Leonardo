"""Symbolic degree-based motion shared with the browser export."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from solid_node.math import asin, sin, cos, sqrt, atan2

CRANK = 24.0
ROD = 146.0
FEED = 8.0
TEETH = 16
DRUM_RADIUS = FEED * TEETH / (2 * 3.141592653589793)

def rod_height(angle):
    return sqrt(ROD * ROD - (CRANK * sin(angle)) ** 2)

def saw_height(angle):
    return CRANK * cos(angle) + rod_height(angle)

def rod_lean(angle):
    return atan2(-CRANK * sin(angle), rod_height(angle))

def feed_steps(angle):
    # Dwell during the downstroke; cycloidal index during the return.
    q = (angle - asin(sin(angle - 90)) - 90) / 360
    return q - sin(360 * q) / (2 * 3.141592653589793)

def pawl_lift(angle):
    s = sin(angle)
    return 70 * (s + sqrt(s * s)) / 2
