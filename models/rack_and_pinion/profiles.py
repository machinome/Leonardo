"""Original sampled involute and straight conjugate rack, dimensions in
mm."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math


def pinion_outline(module):
    """20 teeth, 20-degree pressure angle; 0.1 module tooth thinning.

    Each flank samples the analytic involute in 20 radial intervals.
    Root extensions below the base circle are radial, with a round root
    polygon between teeth. This is a modern educational tooth profile.
    """
    r = 10 * module
    base = r * math.cos(math.radians(20))
    root, tip = 8.75 * module, 11 * module
    inv_pitch = math.tan(math.radians(20)) - math.radians(20)
    half_pitch = (math.pi * module / 2 - 0.1 * module) / (2 * r)

    def half(radius):
        a = math.acos(base / radius)
        return half_pitch + inv_pitch - (math.tan(a) - a)

    def point(radius, angle):
        return (radius * math.cos(angle), radius * math.sin(angle))

    points = []
    for tooth in range(20):
        centre = tooth * math.tau / 20
        points.append(point(root, centre - half(base)))
        for i in range(21):
            radius = base + (tip - base) * i / 20
            points.append(point(radius, centre - half(radius)))
        for i in range(1, 5):
            points.append(
                point(tip, centre - half(tip) + 2 * half(tip) * i / 4)
            )
        for i in range(19, -1, -1):
            radius = base + (tip - base) * i / 20
            points.append(point(radius, centre + half(radius)))
        points.append(point(root, centre + half(base)))
        for i in range(1, 6):
            angle = (
                centre + half(base) + (math.tau / 20 - 2 * half(base)) * i / 6
            )
            points.append(point(root, angle))
    return points


def rack_outline(module):
    pitch = math.pi * module
    half = (pitch / 2 - 0.1 * module) / 2
    slope = math.tan(math.radians(20))
    root_half = half + 1.25 * module * slope
    tip_half = half - module * slope
    points = [(16 * module, -48 * module), (11.25 * module, -48 * module)]
    for tooth in range(-15, 11):
        centre = (tooth + 0.5) * pitch
        points.extend(
            [
                (11.25 * module, centre - root_half),
                (9 * module, centre - tip_half),
                (9 * module, centre + tip_half),
                (11.25 * module, centre + root_half),
            ]
        )
    points.extend([(11.25 * module, 36 * module), (16 * module, 36 * module)])
    return points


def hook_outline(module):
    """Open lower semicircle with a two-module section, centred
    (18,-56)."""
    points = []
    for radius, angles in ((5, range(180, 361, 3)), (3, range(360, 179, -3))):
        for angle in angles:
            a = math.radians(angle)
            points.append(
                (
                    (18 + radius * math.cos(a)) * module,
                    (-56 + radius * math.sin(a)) * module,
                )
            )
    return points
