"""Two conserved ropes and the photographed compound winding shaft.

Pitch radii include the rope; degrees are used by all exported
expressions.
Tangencies are solved from circles, not tuned offsets or feed
multipliers.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

from machinome.math import sqrt, sin, cos, asin, acos, atan2
from numpy.polynomial.legendre import leggauss

from .layout import (
    RATCHET_X,
    RATCHET_Z,
    ROPE_PITCH_RADIUS,
    REDUCER_X,
    REDUCER_Z,
    REDUCER_RADIUS,
    HAUL_RADIUS,
    IDLER_X,
    IDLER_Z,
    IDLER_RADIUS,
    UPPER_X,
    UPPER_Z,
    UPPER_RADIUS,
    ANCHOR_X,
    ROPE_ANCHOR_Z,
    ROPE_Y,
    DRIVE_START_Y,
    LARGE_START_Y,
    IDLER_Y,
    RADIAL_PITCH,
    WIND_PITCH,
    HAUL_TIE_Y,
    HAUL_INITIAL,
    PITCH,
    TURN_SECONDS,
    CARRIAGE_START,
    TIMBER_LENGTH,
    INITIAL_WRAP,
    SPIRAL_POINTS,
)


def tangent(a, ra, b, rb, side):
    """Common external tangent, side +/-1 viewed in feed-local XZ."""
    dx, dz = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dz)
    phi = math.atan2(dz, dx) + side * math.acos((ra - rb) / d)
    n = (math.cos(phi), math.sin(phi))
    return (
        (a[0] + ra * n[0], a[1] + ra * n[1]),
        (b[0] + rb * n[0], b[1] + rb * n[1]),
    )


G = (RATCHET_X, RATCHET_Z)
IDLER_CENTRE = (IDLER_X, IDLER_Z)
S = (REDUCER_X, REDUCER_Z)
U = (UPPER_X, UPPER_Z)
IDLER_OUT, INPUT_CONTACT = tangent(
    IDLER_CENTRE, IDLER_RADIUS, S, REDUCER_RADIUS, -1
)
UPPER_EXIT, HAUL_CONTACT = tangent(U, UPPER_RADIUS, S, HAUL_RADIUS, 1)


def polar(point, centre):
    return math.degrees(math.atan2(point[0] - centre[0], point[1] - centre[1]))


INPUT_PHASE = polar(INPUT_CONTACT, S)
HAUL_PHASE = polar(HAUL_CONTACT, S)
UPPER_EXIT_PHASE = polar(UPPER_EXIT, U)
IDLER_OUT_PHASE = polar(IDLER_OUT, IDLER_CENTRE)
RADIAL_LEAD = RADIAL_PITCH / (2 * math.pi)
GEAR_DISTANCE = math.hypot(IDLER_CENTRE[0] - G[0], IDLER_CENTRE[1] - G[1])
GEAR_BEARING = polar(IDLER_CENTRE, G)


def contact_phase(radius):
    # Tangent to the spiral, not a circle with the same outer radius.
    normal_radius = radius * radius / sqrt(radius * radius + RADIAL_LEAD**2)
    return (
        GEAR_BEARING
        - acos((IDLER_RADIUS + normal_radius) / GEAR_DISTANCE)
        + atan2(RADIAL_LEAD, radius)
    )


GEAR_PHASE = contact_phase(
    ROPE_PITCH_RADIUS + RADIAL_PITCH * INITIAL_WRAP / 360
)
GEAR_TIE_PHASE = GEAR_PHASE - INITIAL_WRAP


def winding_angle(ratchet):
    angle = INITIAL_WRAP - ratchet
    for _ in range(6):
        radius = ROPE_PITCH_RADIUS + RADIAL_PITCH * angle / 360
        angle = contact_phase(radius) - GEAR_TIE_PHASE - ratchet
    return angle


def input_geometry(ratchet):
    angle = winding_angle(ratchet)
    radius = ROPE_PITCH_RADIUS + RADIAL_PITCH * angle / 360
    phase = GEAR_TIE_PHASE + ratchet + angle
    normal = phase - atan2(RADIAL_LEAD, radius)
    gear = (G[0] + radius * sin(phase), G[1] + radius * cos(phase))
    inlet = (
        IDLER_CENTRE[0] - IDLER_RADIUS * sin(normal),
        IDLER_CENTRE[1] - IDLER_RADIUS * cos(normal),
    )
    sweep = IDLER_OUT_PHASE - normal - 180
    return gear, inlet, sweep


GEAR_CONTACT, IDLER_IN, IDLER_SWEEP = input_geometry(0)

# Gaussian integration keeps the length law in the public exported
# algebra
# (sqrt, arithmetic); an independent asinh antiderivative is used in
# tests.
_nodes, _weights = leggauss(12)
QUADRATURE = tuple(
    (float((x + 1) / 2), float(w / 2)) for x, w in zip(_nodes, _weights)
)


def spiral_length(angle):
    radians = angle * math.pi / 180
    return radians * sum(
        w
        * sqrt(
            (ROPE_PITCH_RADIUS + RADIAL_LEAD * radians * x) ** 2
            + RADIAL_LEAD**2
        )
        for x, w in QUADRATURE
    )


SPIRAL_PORTS = tuple(
    name for i in range(1, SPIRAL_POINTS + 1) for name in (f"x{i}", f"z{i}")
) + ("tx", "tz")
DRIVE_BEND_POINTS = 16
DRIVE_BEND_PORTS = tuple(
    name
    for i in range(1, DRIVE_BEND_POINTS + 1)
    for name in (f"bx{i}", f"bz{i}")
) + ("tx", "tz")


def spiral_coordinates(ratchet):
    angle = winding_angle(ratchet)
    values = []
    for i in range(1, SPIRAL_POINTS + 1):
        a = angle * i / SPIRAL_POINTS
        r = ROPE_PITCH_RADIUS + RADIAL_PITCH * a / 360
        values.extend((r * sin(a), r * cos(a) - ROPE_PITCH_RADIUS))
    values.extend(
        (
            RADIAL_LEAD * sin(angle) + r * cos(angle),
            RADIAL_LEAD * cos(angle) - r * sin(angle),
        )
    )
    return values


def drive_profile(ratchet, shaft):
    gear, inlet, sweep = input_geometry(ratchet)
    x, z = gear
    values = [
        x - G[0],
        z - G[1],
        inlet[0] - x,
        inlet[1] - z,
        INPUT_CONTACT[0] - x,
        LARGE_START_Y + shaft * WIND_PITCH / 360 - DRIVE_START_Y,
        INPUT_CONTACT[1] - z,
    ]
    start = IDLER_OUT_PHASE - sweep
    for i in range(1, DRIVE_BEND_POINTS + 1):
        phase = start + sweep * i / DRIVE_BEND_POINTS
        values.extend(
            (
                IDLER_CENTRE[0] + IDLER_RADIUS * sin(phase) - x,
                IDLER_CENTRE[1] + IDLER_RADIUS * cos(phase) - z,
            )
        )
    values.extend((-cos(start), sin(start)))
    return values


def shaft_angle(ratchet):
    """Conserve the first rope, including both changing fleet spans."""
    taken = input_consumed(ratchet)
    angle = taken * 180 / (math.pi * LARGE_EFFECTIVE_RADIUS)
    for _ in range(4):
        lane = LARGE_START_Y + angle * WIND_PITCH / 360 - IDLER_Y
        span = sqrt(INPUT_SPAN_SQUARED + lane * lane)
        released = (
            angle * math.pi / 180 * LARGE_EFFECTIVE_RADIUS
            - span
            + large_span(0)
        )
        derivative = (
            math.pi / 180 * LARGE_EFFECTIVE_RADIUS
            - lane * WIND_PITCH / (360 * span)
        )
        angle = angle + (taken - released) / derivative
    return angle


INPUT_SPAN_SQUARED = (INPUT_CONTACT[0] - IDLER_OUT[0]) ** 2 + (
    INPUT_CONTACT[1] - IDLER_OUT[1]
) ** 2
LARGE_EFFECTIVE_RADIUS = math.hypot(REDUCER_RADIUS, WIND_PITCH / (2 * math.pi))


def gear_span(ratchet):
    gear, inlet, _ = input_geometry(ratchet)
    return sqrt(
        (gear[0] - inlet[0]) ** 2
        + (gear[1] - inlet[1]) ** 2
        + (IDLER_Y - DRIVE_START_Y) ** 2
    )


def large_span(shaft):
    return sqrt(
        INPUT_SPAN_SQUARED
        + (LARGE_START_Y + shaft * WIND_PITCH / 360 - IDLER_Y) ** 2
    )


def input_consumed(ratchet):
    _, _, sweep = input_geometry(ratchet)
    return (
        spiral_length(winding_angle(ratchet))
        - spiral_length(INITIAL_WRAP)
        + gear_span(ratchet)
        - gear_span(0)
        - IDLER_RADIUS * (sweep - IDLER_SWEEP) * math.pi / 180
    )


def haul_y(shaft):
    return HAUL_TIE_Y + WIND_PITCH * (HAUL_INITIAL + shaft / 360)


def approach(advance):
    d = UPPER_X - ANCHOR_X - advance
    h = ROPE_ANCHOR_Z - UPPER_Z
    return asin(UPPER_RADIUS / sqrt(d * d + h * h)) - atan2(h, d)


def upper_path(advance):
    d = UPPER_X - ANCHOR_X - advance
    h = ROPE_ANCHOR_Z - UPPER_Z
    return (
        sqrt(d * d + h * h - UPPER_RADIUS**2)
        + UPPER_RADIUS * (UPPER_EXIT_PHASE + approach(advance)) * math.pi / 180
    )


def descending_span(shaft):
    return sqrt(
        (UPPER_EXIT[0] - HAUL_CONTACT[0]) ** 2
        + (UPPER_EXIT[1] - HAUL_CONTACT[1]) ** 2
        + (haul_y(shaft) - ROPE_Y) ** 2
    )


HAUL_EFFECTIVE_RADIUS = math.hypot(HAUL_RADIUS, WIND_PITCH / (2 * math.pi))


def haul_consumed(shaft):
    return (
        shaft * math.pi / 180 * HAUL_EFFECTIVE_RADIUS
        + descending_span(shaft)
        - descending_span(0)
    )


def carriage_from_shaft(shaft):
    """Invert upper free length; fixed Newton steps export as
    expressions.

    d(length)/d(advance) is -cos(approach). Six steps converge to far
    below 0.001 mm across the complete, explicitly bounded cut.
    """
    target = upper_path(0) - haul_consumed(shaft)
    advance = haul_consumed(shaft)
    for _ in range(6):
        advance = advance + (upper_path(advance) - target) / cos(
            approach(advance)
        )
    return advance


def carriage_advance(ratchet):
    return carriage_from_shaft(shaft_angle(ratchet))


# Complete the timber plus 3 mm behind the blade's -5 mm back edge.
# The first whole ratchet tooth reaching this distance ends the pass.
REQUIRED_TRAVEL = -CARRIAGE_START + TIMBER_LENGTH / 2 + 5 + 3
PASS_TURNS = next(
    n
    for n in range(1, 5000)
    if carriage_advance(-n * PITCH) >= REQUIRED_TRAVEL
)
PASS_ANGLE = PASS_TURNS * 360.0
PASS_SECONDS = PASS_TURNS * TURN_SECONDS
