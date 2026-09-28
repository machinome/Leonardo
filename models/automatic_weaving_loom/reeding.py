"""Reconstructed reed layout and beat dwell, in millimetres and
degrees."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.math import acos, cos

from .timing import clip

REED_TRAVEL = 100
REED_REST_Y = 148
REED_CAM_X = -365
REED_CAM_BASE = 70
REED_TIE_X = REED_CAM_X + 8
REED_STEM_TOP = 602.5
REED_SHEAVE_Z = 730
REED_TIE_Z = 570
REED_RETURN_X = -331


def reed_lift(angle):
    """Rear dwell during insertion; full beat at each half-turn
    boundary."""
    distance = acos(cos(2 * angle)) / 2
    return REED_TRAVEL * (1 - cos(180 * clip(distance / 26, 0, 1))) / 2
