"""Contracts for the descending feed and lower four-wheel transmission."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import numpy as np
from machinome.test import TestCase
from .checks import sampled_poses
from .winding import WindingBench, CENTERS, PITCH, RADIUS
from .test_timing import marker_angle


class WindingBenchTest(TestCase):
    node = WindingBench

    def test_feed_reaches_both_beams_through_physical_mates(self):
        self.assertTrue(
            hasattr(self.node, "winding"),
            "Indexed cam, descending rack, four wheels and connecting belt are absent",
        )

    def test_connected_solids(self):
        self.assertNoDisconnectedSolids(self.node)

    @sampled_poses(73, end=4)
    def test_whole_train_clears(self):
        self.assertNoSolidInterference(self.node)

    def test_scroll_face_captures_the_descending_pin(self):
        for time in np.linspace(0, 4, 49):
            self.node.set_state(phase=0, run=1, time=float(time))
            self.assertFreeWithin(
                self.node.winding.rack, 0.1, self.node.train.twelve, along=(0, 0, 1)
            )
            self.assertBlockedBeyond(
                self.node.winding.rack, 0.7, self.node.train.twelve, along=(0, 0, 1)
            )

    def test_rack_and_all_four_lower_gears_engage(self):
        for time in np.linspace(0, 4, 49):
            self.node.set_state(phase=0, run=1, time=float(time))
            w = self.node.winding
            for moving, fixed in (
                (w.rear_lower, w.rack),
                (w.rear_upper, w.rear_lower),
                (w.front_lower, w.front_upper),
            ):
                self.assertFreeWithin(moving, 0.1, fixed, axis=(1, 0, 0))
                self.assertBlockedBeyond(moving, 1.2, fixed, axis=(1, 0, 0))

    def test_feed_and_take_up_are_measured_on_real_parts(self):
        self.node.set_state(phase=0, run=0, time=0)
        initial = self.node.winding.rack.mesh.bounds.copy()
        for time in (1, 2, 3, 4):
            self.node.set_state(phase=0, run=1, time=time)
            self.assertAlmostEqual(
                self.node.winding.rack.mesh.bounds[1, 2] - initial[1, 2],
                -1.8 * time,
                delta=0.01,
            )
            for wheel, center, sign, offset in (
                (self.node.winding.rear_lower, (0, 0), -1, 0),
                (self.node.winding.rear_upper, (0, 96), 1, 7.5),
                (self.node.winding.front_upper, (-CENTERS, 96), 1, 7.5),
                (self.node.winding.front_lower, (-CENTERS, 0), -1, 0),
            ):
                measured = marker_angle(wheel, center)
                self.assertAlmostEqual(
                    measured,
                    offset + sign * 1.8 * time / RADIUS * 180 / math.pi,
                    delta=0.02,
                )

    def test_rack_guide_and_shaft_retention(self):
        w = self.node.winding
        for along in ((1, 0, 0), (0, 1, 0)):
            self.assertFreeWithin(w.rack, 0.1, w.bearings, along=along)
            self.assertBlockedBeyond(w.rack, 0.7, w.bearings, along=along)
        for wheel in (w.rear_lower, w.rear_upper, w.front_upper, w.front_lower):
            for along in ((1, 0, 0), (0, 0, 1)):
                self.assertFreeWithin(wheel, 0.1, w.bearings, along=along)
                self.assertBlockedBeyond(wheel, 0.7, w.bearings, along=along)

    def test_perforated_belt_is_continuous_and_its_holes_engage_both_sprockets(self):
        # Flexible material is deliberately checked separately: whole-root
        # rigid interference does not inspect the leather.
        w = self.node.winding
        for time in np.linspace(0, 4, 17):
            self.node.set_state(phase=0, run=1, time=float(time))
            bridges = [rung.leather for rung in w.belt.rungs]
            for leather in bridges:
                for band in (w.belt.left, w.belt.right):
                    self.assertIntersecting(leather, band)
                for wheel in (w.rear_upper, w.front_upper):
                    self.assertNotIntersecting(leather, wheel)
            for wheel, outer in ((w.rear_upper, max), (w.front_upper, min)):
                leather = outer(bridges, key=lambda part: part.mesh.bounds[:, 1].mean())
                self.assertFreeWithin(wheel, 0.1, leather, axis=(1, 0, 0))
                self.assertBlockedBeyond(wheel, 6, leather, axis=(1, 0, 0))
                for band in (w.belt.left, w.belt.right):
                    self.assertNotIntersecting(wheel, band)
