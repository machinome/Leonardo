"""Measurements of flexible surfaces; rigid integrity cannot certify ropes."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import numpy as np
from solid_node.test import TestCase
from .cord_bench import CordBench


def centerline(part, profile=8):
    """Measure the actual sweep rings, checking the endpoint-cap convention."""
    v = part.mesh.vertices
    assert (len(v) - 2) % profile == 0
    centers = v[:-2].reshape((-1, profile, 3)).mean(axis=1)
    assert np.allclose(centers[0], v[-2], atol=0.001)
    assert np.allclose(centers[-1], v[-1], atol=0.001)
    return centers


def length(part, profile=8):
    return np.linalg.norm(np.diff(centerline(part, profile), axis=0), axis=1).sum()


class CordBenchTest(TestCase):
    node = CordBench

    def test_counterweight_rises_exactly_as_its_driving_end_descends(self):
        # Pilot-observed failure: equal-direction vertical endpoints would
        # create or destroy rope. Measure the evaluated surfaces themselves.
        for phase in range(0, 361, 5):
            self.node.set_state(phase=phase, run=0, time=0)
            c = self.node.cords
            for group, total in ((c.left, 848), (c.right, 848), (c.reed, 832.5)):
                driven = centerline(group.haul.cord)[0, 2]
                weight_top = group.weight.mesh.bounds[1, 2]
                self.assertAlmostEqual(driven + weight_top, total, delta=0.002)

    def test_all_six_operating_cords_keep_their_length(self):
        c = self.node.cords
        quarter = 3.5 * math.pi / 2
        cords = (
            (c.left.haul.cord, 257.8 + 3 * quarter),
            (c.right.haul.cord, 244.2 + 3 * quarter),
            (c.reed.haul.cord, 349.5 + 3 * quarter),
            (c.left.returning.cord, 206.5 + quarter),
            (c.right.returning.cord, 206.5 + quarter),
            (c.reed.returning.cord, 203.5 + quarter),
        )
        for phase in range(0, 361, 5):
            self.node.set_state(phase=phase, run=0, time=0)
            for part, expected in cords:
                # Each circular primitive has at least 96 intervals. The
                # total circular chord error is below 0.001 mm here.
                self.assertAlmostEqual(length(part), expected, delta=0.002)

    def test_return_ends_reach_the_actual_weights(self):
        for phase in (0, 45, 60, 85, 90, 95, 120, 180, 240, 265, 270, 275, 300, 360):
            self.node.set_state(phase=phase, run=0, time=0)
            c = self.node.cords
            for group in (c.left, c.right, c.reed):
                end = centerline(group.returning.cord)[-1]
                bounds = group.weight.mesh.bounds
                target = bounds.mean(axis=0)
                target[2] = bounds[1, 2]
                np.testing.assert_allclose(end, target, atol=0.002)
                haul = centerline(group.haul.cord)[-1]
                start = centerline(group.returning.cord)[0]
                if group is c.reed:
                    np.testing.assert_allclose(haul, start, atol=0.002)
                else:
                    np.testing.assert_allclose(haul - start, (0, -20, 0), atol=0.002)

    def test_warp_unwinds_as_the_same_length_of_cloth_is_taken_up(self):
        self.node.set_state(phase=0, run=0, time=0)
        warp0 = length(self.node.warp.anchor.cord)
        cloth0 = length(self.node.cloth, 4)
        for time, expected in ((0.25, 0.555), (0.5, 1.11), (0.75, 1.665), (1, 2.22)):
            self.node.set_state(phase=0, run=1, time=time)
            self.assertAlmostEqual(
                warp0 - length(self.node.warp.anchor.cord), expected, delta=0.003
            )
            self.assertAlmostEqual(
                length(self.node.cloth, 4) - cloth0, expected, delta=0.003
            )
            np.testing.assert_allclose(
                centerline(self.node.warp.anchor.cord)[-1], (0, 305, 520), atol=0.002
            )
            np.testing.assert_allclose(
                centerline(self.node.cloth, 4)[0], (0, 45, 520), atol=0.002
            )
            self.assertAlmostEqual(
                np.ptp(self.node.cloth.mesh.vertices[:, 0]), 144, delta=0.002
            )

    def test_actual_flexible_surfaces_clear_their_rolls_and_guides(self):
        from .textile import FRONT_Y, CLOTH_GUIDE

        for time in np.linspace(0, 1, 17):
            self.node.set_state(phase=0, run=1, time=float(time))
            for part, circles in (
                (self.node.warp.anchor.cord, ((72, 202, 14), (305, 515.2, 4))),
                (self.node.cloth, ((FRONT_Y, 106, 14), (CLOTH_GUIDE, 515.2, 4))),
            ):
                yz = part.mesh.vertices[:, 1:]
                for y, z, radius in circles:
                    minimum = np.linalg.norm(yz - (y, z), axis=1).min()
                    self.assertGreaterEqual(minimum, radius + 0.3)
