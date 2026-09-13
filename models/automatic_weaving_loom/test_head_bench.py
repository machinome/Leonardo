"""Independent contact sampling for all seven inferred cam tracks."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from solid_node.test import TestCase
from .checks import sampled_poses
from .head_bench import HeadBench


class HeadBenchTest(TestCase):
    node = HeadBench

    def test_all_followers_match_their_cam_tracks(self):
        h = self.node.head
        pairs = (
            ("heddle A", h.heddle_a.follower),
            ("heddle B", h.heddle_b.follower),
            ("left arm", h.left.follower),
            ("right arm", h.right.follower),
            ("reed", h.reed),
            ("selector A", h.selector_a),
            ("selector B", h.selector_b),
        )
        for phase in range(0, 361, 10):
            self.node.set_state(phase=phase, run=0, time=0)
            for name, follower in pairs:
                try:
                    self.assertNotIntersecting(follower, self.node.input)
                    self.assertFreeWithin(
                        follower, 0.1, self.node.input, along=(0, 0, 1)
                    )
                    self.assertBlockedBeyond(
                        follower, 1.5, self.node.input, along=(0, 0, 1)
                    )
                except AssertionError as error:
                    raise AssertionError(f"{name}, phase {phase}: {error}") from error

    def test_connected_solids(self):
        self.assertNoDisconnectedSolids(self.node)

    @sampled_poses(37)
    def test_complete_head_clearance(self):
        self.assertNoSolidInterference(self.node)
