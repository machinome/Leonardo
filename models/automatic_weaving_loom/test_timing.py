"""Geometry contracts for the historical one/six/twelve timing train."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import numpy as np
from machinome.test import TestCase
from .checks import sampled_poses
from .timing import TimingBench


def marker_angle(node, center):
    vertices = node.mesh.vertices
    # A shallow radial marker on the outer shaft end uniquely measures angle.
    rim = vertices[vertices[:, 0] > vertices[:, 0].max() - 0.01]
    delta = rim[:, 1:].mean(axis=0) - np.asarray(center)
    return math.degrees(math.atan2(delta[1], delta[0]))


class TimingBenchTest(TestCase):
    node = TimingBench

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @sampled_poses(73)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_indexing_and_dwell_are_measured_on_the_shafts(self):
        records = []
        for phase in (0, 90, 120, 150, 180, 210, 240, 270, 360):
            self.node.set_state(phase=phase, run=0, time=0)
            records.append(
                (
                    phase,
                    marker_angle(self.node.train.six, (0, 0)),
                    marker_angle(self.node.train.twelve, (-54, 0)),
                )
            )
        for index in (1, 2):
            self.assertAlmostEqual(records[index][1], records[0][1], delta=0.01)
        for index in (6, 7, 8):
            self.assertAlmostEqual(records[index][1] - records[0][1], -60, delta=0.01)
            self.assertAlmostEqual(records[index][2] - records[0][2], 30, delta=0.01)
        for (_, six, twelve), (_, s0, t0) in zip(records[3:6], records[:1] * 3):
            self.assertAlmostEqual(twelve - t0, -(six - s0) / 2, delta=0.01)

    def test_pin_engages_the_six_tooth_wheel(self):
        for phase in (125, 140, 160, 180, 200, 220, 235):
            self.node.set_state(phase=phase, run=0, time=0)
            self.assertFreeWithin(
                self.node.train.six, 0.1, self.node.train.input, axis=(1, 0, 0)
            )
            self.assertBlockedBeyond(
                self.node.train.six, 3, self.node.train.input, axis=(1, 0, 0)
            )

    def test_six_and_twelve_mesh_across_a_tooth_pitch(self):
        for phase in np.linspace(120, 240, 25):
            self.node.set_state(phase=float(phase), run=0, time=0)
            self.assertFreeWithin(
                self.node.train.twelve, 0.1, self.node.train.six, axis=(1, 0, 0)
            )
            self.assertBlockedBeyond(
                self.node.train.twelve, 2, self.node.train.six, axis=(1, 0, 0)
            )

    def test_index_wheel_is_held_during_dwell(self):
        for phase in (0, 60, 100, 260, 300, 360):
            self.node.set_state(phase=phase, run=0, time=0)
            self.assertFreeWithin(
                self.node.train.six, 0.1, self.node.train.input, axis=(1, 0, 0)
            )
            self.assertBlockedBeyond(
                self.node.train.six, 3, self.node.train.input, axis=(1, 0, 0)
            )

    def test_journals_and_axial_retention(self):
        for part in (
            self.node.train.input,
            self.node.train.six,
            self.node.train.twelve,
        ):
            self.assertFreeWithin(part, 0.1, self.node.train.bearings, along=(0, 1, 0))
            self.assertBlockedBeyond(
                part, 0.7, self.node.train.bearings, along=(0, 1, 0)
            )
            self.assertFreeWithin(part, 0.1, self.node.train.bearings, along=(1, 0, 0))
            self.assertBlockedBeyond(
                part, 0.7, self.node.train.bearings, along=(1, 0, 0)
            )
