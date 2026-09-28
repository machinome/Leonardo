"""Geometry, not timing metadata, must retain the accompanied spool."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.test import TestCase

from .checks import sampled_poses
from .grip_bench import GripBench


class GripBenchTest(TestCase):
    node = GripBench

    def test_spool_is_enclosed_in_all_three_directions(self):
        for phase in (
            0,
            30,
            60,
            89,
            90,
            91,
            120,
            180,
            240,
            269,
            270,
            271,
            300,
            360,
        ):
            self.node.set_state(phase=phase, run=0, time=0)
            active = (
                self.node.carrier.left
                if phase < 90 or phase >= 270
                else self.node.carrier.right
            )
            for along in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                try:
                    for part in (active.body, active.jaw):
                        self.assertFreeWithin(
                            self.node.carrier.spool, 0.1, part, along=along
                        )
                except AssertionError as error:
                    raise AssertionError(
                        f"phase {phase}, direction {along}: {error}"
                    ) from error
            s = active.side
            for part, along in (
                (active.body, (s, 0, 0)),
                (active.jaw, (-s, 0, 0)),
                (active.jaw, (0, -s, 0)),
                (active.body, (0, s, 0)),
                (active.jaw, (0, 0, 1)),
                (active.body, (0, 0, -1)),
            ):
                try:
                    self.assertBlockedBeyond(
                        self.node.carrier.spool,
                        0.8,
                        part,
                        along=along,
                        directions="forward",
                    )
                except AssertionError as error:
                    raise AssertionError(
                        f"phase {phase}, direction {along}: {error}"
                    ) from error

    def test_connected_solids(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_opening_jaw_is_held_by_its_actual_selector_ramp(self):
        for phases, arm, ramp in (
            (
                (60, 70, 80, 280, 290, 300, 305, 310, 315),
                self.node.carrier.right,
                self.node.selector_b,
            ),
            (
                (100, 110, 120, 125, 130, 135, 240, 250, 260),
                self.node.carrier.left,
                self.node.selector_a,
            ),
        ):
            for phase in phases:
                self.node.set_state(phase=phase, run=0, time=0)
                self.assertFreeWithin(arm.jaw, 0.1, ramp, along=(0, 1, 0))
                self.assertBlockedBeyond(
                    arm.jaw,
                    0.7,
                    ramp,
                    along=(0, arm.side, 0),
                    directions="forward",
                )

    @sampled_poses(73)
    def test_clear_through_both_exchanges(self):
        try:
            self.assertNoSolidInterference(self.node)
        except AssertionError as error:
            raise AssertionError(
                f"phase {self.node.time * 360}: {error}"
            ) from error
