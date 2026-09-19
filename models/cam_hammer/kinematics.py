"""Designed pitch envelope and periodic symbolic motion, all angles in degrees."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.math import sin, cos, atan2, sqrt


def clip01(value):
    positive = (value + sqrt(value * value)) / 2
    excess = positive - 1
    return positive - (excess + sqrt(excess * excess)) / 2


def cycle_angle(angle):
    return 180 + atan2(sin(angle - 180), cos(angle - 180))


def lift_envelope(angle, amplitude, return_span=80):
    """Half-cosine rise then return, with a closed rest interval."""
    theta = cycle_angle(angle)
    up = clip01(theta / 240)
    down = clip01((theta - 240) / return_span)
    return amplitude * (cos(180 * down) - cos(180 * up)) / 2


def pitch_point(angle, amplitude):
    """Nose centre in cam coordinates; the cam retreats before the hammer."""
    beta = lift_envelope(angle, amplitude, return_span=45)
    x = 60 - 60 * cos(beta)
    z = -60 - 60 * sin(beta)
    return (x * cos(angle) + z * sin(angle),
            -x * sin(angle) + z * cos(angle))


def cam_outline(amplitude):
    """Inward normal offset of the pitch curve by the 6 mm nose + 0.3 gap.

    0.5-degree chords approximate the smooth envelope. The central difference
    finds its tangent without an independent, potentially divergent lift law.
    Tests measure the resulting surfaces independently at and between samples.
    """
    points = []
    for i in range(720):
        theta = i / 2
        x, z = pitch_point(theta, amplitude)
        before = pitch_point(theta - 0.001, amplitude)
        after = pitch_point(theta + 0.001, amplitude)
        dx, dz = after[0] - before[0], after[1] - before[1]
        length = sqrt(dx * dx + dz * dz)
        # Pitch path is clockwise, so its left normal points outward.
        nx, nz = -dz / length, dx / length
        points.append((x - 6.3 * nx, z - 6.3 * nz))
    return points


def follower_law(machine, lever):
    return lambda angle: lift_envelope(angle, machine.lift_angle)
