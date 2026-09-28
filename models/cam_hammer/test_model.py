"""Independent measurements of the commissioned hammer, not its pose
formulas."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

from trimesh.proximity import closest_point
from machinome.test import TestCase, testing_steps
from machinome.simulation import ScenarioTest

from .model import CamHammer


def expected_lift(phase, amplitude):
    phase %= 360
    if phase <= 240:
        return amplitude * (1 - math.cos(math.pi * phase / 240)) / 2
    if phase < 320:
        return amplitude * (1 + math.cos(math.pi * (phase - 240) / 80)) / 2
    return 0.0


class CamHammerTest(TestCase):
    node = CamHammer

    def pose(self, angle):
        self.node.set_state(phase=angle, run=0, time=0)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(37)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_transition_neighborhoods_and_driver_combinations(self):
        phases = (
            0,
            0.1,
            239.9,
            240,
            240.1,
            245,
            250,
            260,
            270,
            280,
            284.9,
            285,
            285.1,
            300,
            310,
            319.9,
            320,
            320.1,
            359.9,
            360,
        )
        for angle in phases:
            self.pose(angle)
            self.assertNoSolidInterference(self.node)
        for phase in (0, 120, 250, 360):
            for run in (0, 0.5, 1):
                for time in (0, 0.25, 0.7, 1):
                    self.node.set_state(phase=phase, run=run, time=time)
                    self.assertNoSolidInterference(self.node)
                    self.check_hammer_position(phase + 360 * run * time)

    def check_hammer_position(self, phase):
        beta = math.radians(expected_lift(phase, self.node.lift_angle))
        # The head is a symmetric box at (100,0,-5), measured via its
        # own
        # ingredient mesh inside the complete rigid hammer lever.
        centre = self.node.lever.head.mesh.bounds.mean(axis=0)
        self.assertAlmostEqual(
            centre[0], 100 * math.cos(beta) + 5 * math.sin(beta), delta=0.01
        )
        self.assertAlmostEqual(
            centre[2],
            110 + 100 * math.sin(beta) - 5 * math.cos(beta),
            delta=0.01,
        )

    def test_intermediate_lift_and_return(self):
        for angle in (
            0,
            30,
            60,
            90,
            120,
            180,
            210,
            240,
            250,
            270,
            300,
            320,
            360,
        ):
            self.pose(angle)
            self.check_hammer_position(angle)

    def test_cam_contact_during_lift(self):
        for angle in range(0, 241, 10):
            self.pose(angle)
            # Feature-rich cam vertices against the round shoe, not two
            # algebraic coordinates copied from the implementation.
            shoe = self.node.lever.shoe.mesh
            vertices = self.node.cam.profile.mesh.vertices
            # Spatial pruning only: a surface within the specified 0.42
            # mm
            # contact gap necessarily has vertices in this 2 mm window.
            nearby = vertices[
                (
                    (vertices >= shoe.bounds[0] - 2)
                    & (vertices <= shoe.bounds[1] + 2)
                ).all(axis=1)
            ]
            self.assertGreater(len(nearby), 0, f"cam lost the shoe at {angle}")
            distances = closest_point(shoe, nearby)[1]
            gap = distances.min()
            self.assertGreater(gap, 0.20, f"cam clearance at {angle}")
            self.assertLess(gap, 0.42, f"cam lost contact at {angle}")
            self.assertFreeWithin(
                self.node.lever,
                0.12,
                self.node.cam,
                axis=(0, 1, 0),
                directions="forward",
            )
            self.assertBlockedBeyond(
                self.node.lever,
                0.8,
                self.node.cam,
                axis=(0, 1, 0),
                directions="forward",
            )

    def test_release_opens_a_real_gap(self):
        for angle in (260, 270, 280, 290, 300):
            self.pose(angle)
            gap = closest_point(
                self.node.lever.shoe.mesh, self.node.cam.profile.mesh.vertices
            )[1].min()
            self.assertGreater(gap, 1.0, f"no release at {angle}")

    def test_strike_face_and_footprint(self):
        for angle in (0, 320, 340, 360):
            self.pose(angle)
            hammer = self.node.lever.head.mesh.bounds
            anvil = self.node.anvil.mesh.bounds
            self.assertAlmostEqual(hammer[0, 2], anvil[1, 2], delta=0.01)
            self.assertAlmostEqual(hammer[0, 2], 91, delta=0.01)
            self.assertGreaterEqual(hammer[0, 0], 82)
            self.assertLessEqual(hammer[1, 0], 118)
            self.assertFreeWithin(
                self.node.lever,
                0.1,
                self.node.anvil,
                axis=(0, -1, 0),
                directions="forward",
            )
            self.assertBlockedBeyond(
                self.node.lever,
                0.1,
                self.node.anvil,
                axis=(0, 1, 0),
                directions="forward",
            )

    @testing_steps(9)
    def test_journals_capture_both_shafts(self):
        for body in (self.node.cam, self.node.lever):
            for axis in ((1, 0, 0), (0, 0, 1)):
                self.assertFreeWithin(body, 0.2, self.node.frame, along=axis)
                self.assertBlockedBeyond(
                    body, 0.7, self.node.frame, along=axis
                )
            self.assertFreeWithin(body, 0.15, self.node.frame, along=(0, 1, 0))
            self.assertBlockedBeyond(
                body, 0.7, self.node.frame, along=(0, 1, 0)
            )

    def test_ground_and_anvil_seating(self):
        self.pose(0)
        self.assertAlmostEqual(
            self.node.frame.mesh.bounds[0, 2], 0, delta=0.01
        )
        self.assertAlmostEqual(
            self.node.anvil.mesh.bounds[0, 2], 12.2, delta=0.01
        )
        self.assertAssemblySupported(
            self.node, ground=self.node.frame, max_drop=0.8
        )

    def test_lift_limits_are_guarded(self):
        for value in (15.9, 20.1):
            with self.assertRaises(ValueError):
                CamHammer(lift_angle=value)


class CamHammerScenarioTest(ScenarioTest):
    node = CamHammer
    dt = 0.05
    meshes = True

    def test_instructions_land_and_remain_clear(self):
        sim = self.simulation()
        stages = [
            ("Lift", 120, 0),
            ("Release", 250, 0),
            ("Strike", 320, 0),
            ("Run", 0, 1),
        ]
        self.assertEqual(set(self.node.instructions), {s[0] for s in stages})
        for i, (name, _, _) in enumerate(stages):
            sim.at(i).trigger(name)
        sim.every(0.1, self.assertNoSolidInterference, self.node)
        for _, phase, run in stages:
            sim.run(1)
            self.assertAlmostEqual(sim.state["phase"], phase, delta=0.00001)
            self.assertAlmostEqual(sim.state["run"], run, delta=0.00001)
