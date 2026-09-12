# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import numpy as np

from solid_node.test import TestCase, testing_steps
from .model import LeonardoHydraulicSawmill


class LeonardoHydraulicSawmillTest(TestCase):
    node = LeonardoHydraulicSawmill

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(33)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_saw_has_full_stroke(self):
        self.node.set_state(time=0, phase=0, playback=0)
        upper = self.node.sash.frame.mesh.bounds[:, 2].mean()
        self.node.set_state(phase=180)
        lower = self.node.sash.frame.mesh.bounds[:, 2].mean()
        self.assertAlmostEqual(upper - lower, 48.0, delta=0.01)

    @testing_steps(13, end=0.25)
    def test_blade_clears_both_log_halves(self):
        self.assertNotIntersecting(self.node.sash.blade, self.node.carriage.log_left)
        self.assertNotIntersecting(self.node.sash.blade, self.node.carriage.log_right)

    def test_feed_dwells_then_advances(self):
        positions = []
        for phase in (0, 90, 180, 270, 360):
            self.node.set_state(time=0, phase=phase, playback=0)
            positions.append(self.node.carriage.bed.mesh.bounds[:, 0].mean())
        self.assertAlmostEqual(positions[0], positions[2], delta=0.01)
        self.assertGreater(positions[3], positions[2])
        self.assertAlmostEqual(positions[4] - positions[0], 8.0, delta=0.01)

    def test_reposing_is_reproducible(self):
        self.node.set_state(time=0, phase=73, playback=0)
        first = self.node.sash.frame.mesh.bounds.copy()
        self.node.set_state(phase=1100)
        self.node.set_state(phase=73)
        np.testing.assert_allclose(self.node.sash.frame.mesh.bounds, first, atol=1e-6)

    @testing_steps(9, end=0.25)
    def test_crank_pin_captures_rod(self):
        self.assertFreeWithin(self.node.connecting_rod, 0.3, self.node.crankshaft, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.connecting_rod, 1.5, self.node.crankshaft, along=(1, 0, 0))

    @testing_steps(9, end=0.25)
    def test_sash_stays_in_guide_slots(self):
        self.assertFreeWithin(self.node.sash.frame, 0.3, self.node.timber_structure, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.sash.frame, 1.3, self.node.timber_structure, along=(1, 0, 0))

    def test_waterwheel_is_keyed_to_shaft(self):
        self.assertFreeWithin(self.node.waterwheel, 1, self.node.crankshaft, axis=(0, 1, 0))
        self.assertBlockedBeyond(self.node.waterwheel, 10, self.node.crankshaft, axis=(0, 1, 0))

    def test_seated_pawl_engages_ratchet(self):
        self.node.set_state(time=0, phase=0, playback=0)
        self.assertFreeWithin(self.node.feed_drum, 0.3, self.node.pawl, axis=(0, 1, 0))
        self.assertBlockedBeyond(self.node.feed_drum, 5, self.node.pawl, axis=(0, -1, 0), directions='forward')
