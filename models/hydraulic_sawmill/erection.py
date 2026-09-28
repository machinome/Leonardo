"""Reversible fixture-assisted disassembly of the same fitted frame.

This is a carpenter's handling sequence, not a gravity simulation. Work
on
trestles and hold members while withdrawing their pegs. Reverse to
erect.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.math import ramp

STAGES = (
    "Assembled frame",
    "Withdraw wooden pins",
    "Lift rails and outer bearing",
    "Lift tower crosshead",
    "Lift upper crossmembers",
    "Open the side frames",
    "Withdraw shoulder ties and pivot bearers",
    "Release grooved uprights",
    "Lift wooden bearings",
    "Lift lower crossmembers",
    "Lift side rails",
    "Withdraw legs from stretchers",
)


def displacement(code, stage):
    x = y = z = 0
    if code in ("R1", "R2"):
        z += 100 * ramp(stage, 1, 2)
    if code == "A1":
        z += 140 * ramp(stage, 1, 2)
    if code == "T4":
        z += 100 * ramp(stage, 2, 3)
    if code in ("C3", "C4"):
        z += 60 * ramp(stage, 3, 4)
    if code in ("L1", "L2", "B1", "S1"):
        y -= 100 * ramp(stage, 4, 5)
    if code in ("L3", "L4", "B2", "S2"):
        y += 100 * ramp(stage, 4, 5)
    if code in ("T5", "T6"):
        y += (-1 if code == "T5" else 1) * 60 * ramp(stage, 5, 6)
    if code in ("F1", "F2"):
        y += 40 * ramp(stage, 5, 6)
    if code in ("T2", "T3"):
        x += 70 * ramp(stage, 6, 7)
    if code == "A2":
        z += 60 * ramp(stage, 7, 8)
    if code in ("C1", "C2"):
        z += 100 * ramp(stage, 8, 9)
    if code == "T1":
        z += 30 * ramp(stage, 8, 9)
    if code in ("B1", "B2"):
        z += 60 * ramp(stage, 9, 10)
    if code in ("L1", "L2", "L3", "L4"):
        x += (-1 if code in ("L1", "L3") else 1) * 50 * ramp(stage, 10, 11)
    return (x, y, z)


def peg_displacement(spec, stage):
    index = "xyz".index(spec.axis)
    vector = [0, 0, 0]
    sign = -1 if spec.axis != "z" and spec.centre[index] < 0 else 1
    if spec.axis == "x" and spec.centre[0] == 0:
        # Pull tower pins toward the clear side, away from the feed
        # bearers.
        sign = -1
    vector[index] = (
        sign * (160 if spec.axis == "z" else 300) * ramp(stage, 0, 1)
    )
    return vector
