"""Independent parity probe for the harmonic cam-lift migration."""

import math

from machinome.core.expressions import parse, render
from machinome.scad_expression import get_animation_time

from models.cam_hammer.kinematics import cam_outline, lift_envelope
from models.cam_hammer.model import CamHammer


ANGLES = (-720.1, -360, -0.1, 0, 0.1, 30, 120, 239.9, 240, 240.1,
          250, 262.5, 280, 284.9, 285, 285.1, 319.9, 320, 320.1, 360, 720.1)


def legacy_lift(angle, amplitude, return_span):
    theta = 180 + math.degrees(math.atan2(
        math.sin(math.radians(angle - 180)),
        math.cos(math.radians(angle - 180)),
    ))

    def clip01(value):
        positive = (value + math.sqrt(value * value)) / 2
        excess = positive - 1
        return positive - (excess + math.sqrt(excess * excess)) / 2

    up = clip01(theta / 240)
    down = clip01((theta - 240) / return_span)
    return amplitude * (
        math.cos(math.radians(180 * down))
        - math.cos(math.radians(180 * up))
    ) / 2


def legacy_pitch_point(angle, amplitude):
    beta = legacy_lift(angle, amplitude, 45)
    x = 60 - 60 * math.cos(math.radians(beta))
    z = -60 - 60 * math.sin(math.radians(beta))
    return (
        x * math.cos(math.radians(angle)) + z * math.sin(math.radians(angle)),
        -x * math.sin(math.radians(angle)) + z * math.cos(math.radians(angle)),
    )


def legacy_cam_outline(amplitude):
    points = []
    for i in range(720):
        theta = i / 2
        x, z = legacy_pitch_point(theta, amplitude)
        before = legacy_pitch_point(theta - 0.001, amplitude)
        after = legacy_pitch_point(theta + 0.001, amplitude)
        dx, dz = after[0] - before[0], after[1] - before[1]
        length = math.hypot(dx, dz)
        nx, nz = -dz / length, dx / length
        points.append((x - 6.3 * nx, z - 6.3 * nz))
    return points


def close(actual, expected, tolerance=1e-11):
    assert math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (
        actual, expected
    )


def evaluate(expression, animation_time):
    source = render(parse(str(expression))).replace("$t", repr(animation_time))
    functions = {
        "abs": abs,
        "cos": lambda angle: math.cos(math.radians(angle)),
        "floor": math.floor,
        "max": max,
        "min": min,
        "sqrt": math.sqrt,
    }
    return eval(source, {"__builtins__": {}}, functions)


numeric = 0
for amplitude in (16, 18, 20, -18):
    for return_span in (80, 45):
        for angle in ANGLES:
            close(lift_envelope(angle, amplitude, return_span),
                  legacy_lift(angle, amplitude, return_span))
            numeric += 1

machine = CamHammer()
follower_relation = machine._relations[1]
assert follower_relation.driven_end.node is machine.lever
assert follower_relation.driven_end.slot.name == "swing"
time = get_animation_time()
deferred = follower_relation.law.forward(time)
for angle in ANGLES:
    close(evaluate(deferred, angle), legacy_lift(angle, 18, 80))

profile_points = 0
for amplitude in (16, 18, 20):
    actual = cam_outline(amplitude)
    legacy = legacy_cam_outline(amplitude)
    assert len(actual) == len(legacy) == 720
    for actual_point, legacy_point in zip(actual, legacy):
        close(actual_point[0], legacy_point[0], tolerance=1e-8)
        close(actual_point[1], legacy_point[1], tolerance=1e-8)
        profile_points += 1

print(
    f"PASS: {numeric} numeric adapter values, {len(ANGLES)} actual bound-law "
    f"deferred values, {profile_points} profile points"
)
