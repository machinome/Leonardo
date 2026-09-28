"""Original conjugate profiles; historical tooth counts, reconstructed
flanks."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math


def polar(radius, angle):
    return radius * math.cos(math.radians(angle)), radius * math.sin(
        math.radians(angle)
    )


def cycloidal_outline(teeth, module=6.0, rolling_radius=9.0, backlash=0.4):
    """Epicycloidal addenda and hypocycloidal dedenda with a shared
    generator.

    Coordinates are in the wheel's radial plane. Tooth centers start at
    zero.
    A common rolling circle gives mating profiles even for six teeth,
    where
    an unmodified modern involute would have severe undercut. The flanks
    are
    sampled to a polygon, not claimed to be Leonardo's measured tooth
    shape.
    """
    radius = teeth * module / 2
    rho = rolling_radius
    tip, root = radius + module * 0.5, radius - module * 0.5 - 0.4
    half = (math.pi * module / 2 - backlash / 2) / (2 * radius)

    def cycloid(phi, outside):
        if outside:
            a = radius + rho
            return (
                a * math.cos(phi) - rho * math.cos(a / rho * phi),
                a * math.sin(phi) - rho * math.sin(a / rho * phi),
            )
        a = radius - rho
        return (
            a * math.cos(phi) + rho * math.cos(a / rho * phi),
            a * math.sin(phi) - rho * math.sin(a / rho * phi),
        )

    def offset(r, outside):
        lo, hi = 0.0, 0.8
        for _ in range(55):
            mid = (lo + hi) / 2
            p = cycloid(mid, outside)
            if (math.hypot(*p) < r) == outside:
                lo = mid
            else:
                hi = mid
        return math.atan2(*reversed(cycloid((lo + hi) / 2, outside)))

    def width(r):
        return (
            half - offset(r, True) if r >= radius else half + offset(r, False)
        )

    def point(r, angle):
        return r * math.cos(angle), r * math.sin(angle)

    radii = [root + (radius - root) * i / 16 for i in range(16)]
    radii += [radius + (tip - radius) * i / 24 for i in range(25)]
    points = []
    for tooth in range(teeth):
        center = tooth * math.tau / teeth
        points.extend(point(r, center - width(r)) for r in radii)
        points.extend(
            point(tip, center - width(tip) + 2 * width(tip) * i / 6)
            for i in range(1, 7)
        )
        points.extend(
            point(r, center + width(r)) for r in reversed(radii[:-1])
        )
        start = center + width(root)
        span = math.tau / teeth - 2 * width(root)
        points.extend(point(root, start + span * i / 8) for i in range(1, 8))
    return points


def cycloidal_rack(radius=48, module=4, rolling_radius=9, count=7):
    """Straight conjugate of the same generating circle, facing negative
    Y.

    The pitch-line tooth half-width is thinned by 0.1 mm on each mate;
    an extra 0.4 mm at the dedendum is real root clearance.
    """
    half = (math.pi * module / 2 - 0.2) / 2

    def width(depth):
        t = math.acos(1 - abs(depth) / rolling_radius)
        offset = rolling_radius * (t - math.sin(t))
        return half - offset if depth > 0 else half + offset

    depths = [-module / 2 - 0.4 + (module + 0.4) * i / 40 for i in range(41)]
    pitch = math.pi * module
    points = [(radius + 10, -count * pitch / 2)]
    for i in range(-(count // 2), count // 2):
        center = (i + 0.5) * pitch
        points.extend((radius - d, center - width(d)) for d in depths)
        points.extend(
            (radius - d, center + width(d)) for d in reversed(depths)
        )
    points.append((radius + 10, count * pitch / 2))
    return points
