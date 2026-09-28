"""Reconstruction dimensions in mm; provenance:
docs/reconstruction.md."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from math import pi

CRANK = 24.0
ROD = 146.0
AXLE_Z = 120.0
SASH_HEIGHT = 300.0
TEETH = 32
PITCH = 360 / TEETH
RATCHET_AXLE_RADIUS = 5.0
ROPE_RADIUS = 0.9
ROPE_PITCH_RADIUS = RATCHET_AXLE_RADIUS + ROPE_RADIUS + 0.3
RATCHET_X, RATCHET_Z = -115.0, 330.0
RATCHET_ROOT, RATCHET_TIP = 42.0, 48.0
CONTACT_RADIUS = 48.0
HOLD_RADIUS = 44.5
ROCKER_X, ROCKER_Z = -235.0, 330.0
ROCKER_LONG = 235.0
TIE_LENGTH = 50.0
PAWL_LENGTH = 75.0
ROCKER_BRANCH = 20.0
# Feed-local coordinates: rotated 180 degrees about Z, then offset
# across
# the timber. Both ratchet and first rope are on the gear side.
FEED_OFFSET_Y = 52.0
LINK_Y, TIE_Y, PAWL_Y = 30.0, 40.0, -6.0
ROD_Y, CRANK_Y = 0.0, -13.0
BEARING_Y = -32.0
CARRIAGE_ROPE_Y = 0.0
ROPE_Y = CARRIAGE_ROPE_Y + FEED_OFFSET_Y
FRAME_END = 335.0
UPPER_X, UPPER_Z, UPPER_RADIUS = 370.0, 340.0, 7.4
REDUCER_X, REDUCER_Z = FRAME_END, 285.0
REDUCER_RADIUS, HAUL_RADIUS = 26.4, 7.2
IDLER_X, IDLER_Z, IDLER_RADIUS = 0.0, AXLE_Z, 11.4
IDLER_Y = FEED_OFFSET_Y - 50.0
WIND_PITCH = 3.2
# Radial packing, not a traversing helix: nominal rope diameter plus
# 0.02 mm
# modelling clearance. Stacking stability and compression are not
# simulated.
RADIAL_PITCH = 2 * ROPE_RADIUS + 0.02
SPIRAL_POINTS = 512
# Stay just inside the ratchet face, in one fixed winding plane.
DRIVE_START_Y = FEED_OFFSET_Y - 52.0
LARGE_START_Y = FEED_OFFSET_Y - 80.0
DRUM_Y = FEED_OFFSET_Y - 68.0
INPUT_RESERVE = 7.5
HAUL_INITIAL = 0.5
HAUL_TIE_Y = FEED_OFFSET_Y - 12.0
TIMBER_LENGTH = 320.0
CRADLE_X = 120.0
CARRIAGE_START = -171.0
ANCHOR_LOCAL_X = 194.0
ANCHOR_X = CARRIAGE_START + ANCHOR_LOCAL_X
ROPE_ANCHOR_Z = 370.0
INITIAL_WRAP = 15.0
TURN_SECONDS = 4.0
