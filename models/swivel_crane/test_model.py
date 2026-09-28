"""Independent contracts on crane geometry, including compound
placements."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import itertools
import math

import numpy as np
from scipy.spatial.distance import cdist
from machinome.test import TestCase, testing_steps
from machinome.simulation import ScenarioTest

from .model import SwivelCrane


class SwivelCraneTest(TestCase):
    node = SwivelCrane

    def pose(self, slew=0, traverse=0, hoist=0):
        self.node.set_state(
            slew=slew, traverse=traverse, hoist=hoist, run=0, time=0
        )

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(17)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_three_independent_coordinates_move_actual_stone(self):
        self.assertTrue(
            hasattr(self.node, "rotor"),
            "The crane needs its rotating mast and load",
        )
        self.pose()
        stone = self.node.rotor.trolley.block.stone
        initial = stone.mesh.vertices.copy()
        fixed = self.node.footing.mesh.vertices.copy()
        for slew, traverse, hoist in itertools.product(
            (-60, -17, 0, 60), (0, 23, 60), (0, 11, 25)
        ):
            self.pose(slew, traverse, hoist)
            angle = math.radians(slew)
            rotation = np.array(
                [
                    [math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0],
                    [0, 0, 1],
                ]
            )
            expected = (initial + (traverse, 0, hoist)) @ rotation.T
            np.testing.assert_allclose(
                stone.mesh.vertices, expected, atol=0.001
            )
            np.testing.assert_allclose(
                self.node.footing.mesh.vertices, fixed, atol=1e-9
            )
            self.assertNoSolidInterference(self.node)
        self.pose()
        np.testing.assert_allclose(stone.mesh.vertices, initial, atol=1e-9)

    def test_screw_lead_engagement_and_phase(self):
        self.pose()
        screw = self.node.rotor.screw
        nut = self.node.rotor.trolley.carrier
        initial = screw.mesh.vertices.copy()
        for travel in (0, 1, 2, 3, 5, 7, 9, 11, 12, 23, 60):
            self.pose(traverse=travel)
            self.assertAlmostEqual(
                float(nut.mesh.bounds[:, 0].mean()),
                80 + travel + 28,
                delta=0.01,
            )
            a = -travel * 2 * math.pi / 12
            rotation = np.array(
                [
                    [1, 0, 0],
                    [0, math.cos(a), -math.sin(a)],
                    [0, math.sin(a), math.cos(a)],
                ]
            )
            np.testing.assert_allclose(
                screw.mesh.vertices,
                (initial - (0, 0, 260)) @ rotation.T + (0, 0, 260),
                atol=0.001,
            )
            self.assertNotIntersecting(screw, nut)
            self.assertFreeWithin(nut, 0.12, screw, along=(1, 0, 0))
            self.assertBlockedBeyond(nut, 0.85, screw, along=(1, 0, 0))

    def rope_centres(self):
        return (
            self.node.rotor.trolley.rope.mesh.vertices[:-2]
            .reshape(-1, 16, 3)
            .mean(axis=1)
        )

    def test_hoist_length_route_and_take_up(self):
        for height in (0, 0.01, 3, 7, 12.5, 19, 24.99, 25):
            self.pose(hoist=height)
            trolley = self.node.rotor.trolley
            centres = self.rope_centres()
            self.assertEqual(centres.shape, (289, 3))
            angle = math.pi / 2 + 2 * height / 18
            endpoints = [
                (68, -34, 246),
                (68, -34, 150 + height),
                (92, -34, 150 + height),
                (92, -34, 240),
                (104, -34, 252),
                (148, -34, 252),
                (148 + 18 * math.sin(angle), -34, 234 + 18 * math.cos(angle)),
            ]
            np.testing.assert_allclose(centres[::48], endpoints, atol=0.001)
            total = 0
            arcs = {
                1: ((80, -34, 150 + height), 12, math.pi),
                3: ((104, -34, 240), 12, math.pi / 2),
                5: ((148, -34, 234), 18, angle),
            }
            for i in range(6):
                points = centres[i * 48 : (i + 1) * 48 + 1]
                if i in arcs:
                    centre, radius, sweep = arcs[i]
                    vectors = points - centre
                    radii = np.linalg.norm(vectors, axis=1)
                    np.testing.assert_allclose(radii, radius, atol=0.001)
                    vectors /= radii[:, None]
                    measured = np.arccos(
                        np.clip(
                            (vectors[1:] * vectors[:-1]).sum(axis=1), -1, 1
                        )
                    ).sum()
                    self.assertAlmostEqual(measured, sweep, delta=0.001)
                    total += radii.mean() * measured
                    if i == 5:
                        rise = trolley.block.stone.mesh.bounds[0, 2] - 88.5
                        self.assertAlmostEqual(
                            radius * (measured - math.pi / 2),
                            2 * rise,
                            delta=0.01,
                        )
                else:
                    total += np.linalg.norm(points[-1] - points[0])
            self.assertAlmostEqual(total, 230 + 27 * math.pi, delta=0.01)
            self.assertTrue(trolley.rope.mesh.is_watertight)
            self.assertEqual(
                len(trolley.rope.mesh.split(only_watertight=False)), 1
            )
            chain = np.r_[
                0, np.cumsum(np.linalg.norm(np.diff(centres, axis=0), axis=1))
            ]
            remote = abs(chain[:, None] - chain[None, :]) > 5
            self.assertGreater(
                float(cdist(centres, centres)[remote].min()), 2.5
            )

    def test_rope_clears_rigids_through_envelope(self):
        for slew, traverse, hoist in itertools.product(
            (-60, 0, 60), (0, 30, 60), (0, 12.5, 25)
        ):
            self.pose(slew, traverse, hoist)
            t = self.node.rotor.trolley
            for rigid in (
                self.node.footing,
                self.node.rotor.mast,
                self.node.rotor.screw,
                t.carrier,
                t.upper,
                t.drum,
                t.block.carrier,
                t.block.sheave,
                t.block.stone,
            ):
                self.assertNotIntersecting(t.rope, rigid)

    def test_drum_and_sheave_rotations_from_actual_vertices(self):
        self.pose()
        t = self.node.rotor.trolley
        parts = (t.drum, t.upper, t.block.sheave)
        initial = [p.mesh.vertices.copy() for p in parts]
        for height in (3, 11, 19, 25):
            self.pose(hoist=height)
            for part, vertices, factor, centre in zip(
                parts,
                initial,
                (2 / 18, 2 / 12, -1 / 12),
                ((148, -34, 234), (104, -34, 240), (80, -34, 150)),
            ):
                a = height * factor
                rotation = np.array(
                    [
                        [math.cos(a), 0, math.sin(a)],
                        [0, 1, 0],
                        [-math.sin(a), 0, math.cos(a)],
                    ]
                )
                expected = (vertices - centre) @ rotation.T + centre
                if part is t.block.sheave:
                    expected[:, 2] += height
                np.testing.assert_allclose(
                    part.mesh.vertices, expected, atol=0.001
                )

    def test_bearing_rail_and_load_capture(self):
        for slew, traverse, hoist in ((0, 0, 0), (23, 23, 11), (-60, 60, 25)):
            self.pose(slew, traverse, hoist)
            r = self.node.rotor
            t = r.trolley
            # Local axes compose through every ancestor placement.
            for moving, support, axes in (
                (r.mast, self.node.footing, ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
                (r.screw, r.mast, ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
                (t.carrier, r.mast, ((0, 1, 0), (0, 0, 1))),
                (t.upper, t.carrier, ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
                (t.drum, t.carrier, ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
                (
                    t.block.sheave,
                    t.block.carrier,
                    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                ),
            ):
                for axis in axes:
                    self.assertFreeWithin(moving, 0.1, support, along=axis)
                    self.assertBlockedBeyond(moving, 0.8, support, along=axis)
            self.assertFreeWithin(
                t.block.stone, 0.1, t.block.carrier, along=(0, 0, 1)
            )
            self.assertBlockedBeyond(
                t.block.stone,
                0.7,
                t.block.carrier,
                along=(0, 0, -1),
                directions="forward",
            )

    def test_rope_attachments_and_groove_capture(self):
        for height in (0, 8, 17, 25):
            self.pose(hoist=height)
            t = self.node.rotor.trolley
            # Both endpoints sit in blind tangent sockets of their
            # parts.
            for solid in (t.carrier, t.drum):
                self.assertFreeWithin(t.rope, 0.1, solid, along=(0, 1, 0))
                self.assertBlockedBeyond(t.rope, 0.7, solid, along=(0, 1, 0))
            for wheel in (t.upper, t.block.sheave):
                self.assertFreeWithin(t.rope, 0.1, wheel, along=(0, 1, 0))
                self.assertBlockedBeyond(t.rope, 1.9, wheel, along=(0, 1, 0))

    def test_declared_support_fixtures(self):
        self.pose()
        t = self.node.rotor.trolley
        # Bolted footing, held mast/trolley and ideal taut-rope
        # suspension:
        # lateral cantilever reactions and flexible tension are outside
        # this solver.
        self.assertAssemblySupported(
            self.node,
            ground=[self.node.footing],
            supports=[
                (self.node.rotor.mast, self.node.footing),
                (t.carrier, self.node.rotor.mast),
                (t.block.carrier, t.carrier),
            ],
            max_drop=0.8,
        )

    def test_demonstration_transitions_blends_and_return(self):
        times = sorted(
            set(
                [i / 24 for i in range(25)]
                + [
                    v + d
                    for v in (0.16, 0.42, 0.58, 0.74, 0.9)
                    for d in (-0.0001, 0, 0.0001)
                ]
            )
        )
        for blend in (0, 0.3, 1):
            self.node.set_state(
                slew=17, traverse=19, hoist=7, run=blend, time=0
            )
            start = self.node.rotor.trolley.block.stone.mesh.vertices.copy()
            for t in times:
                self.node.set_state(time=t)
                self.assertNoSolidInterference(self.node)
            self.node.set_state(time=1)
            np.testing.assert_allclose(
                self.node.rotor.trolley.block.stone.mesh.vertices,
                start,
                atol=1e-8,
            )


class SwivelCraneScenarioTest(ScenarioTest):
    node = SwivelCrane
    dt = 0.05
    meshes = True

    def test_named_stages(self):
        sim = self.simulation()
        stages = (
            ("Pick up", -45, 0, 0),
            ("Lift clear", -45, 0, 25),
            ("Swing", 45, 60, 25),
            ("Place", 45, 60, 0),
            ("Pick up", -45, 0, 0),
        )
        for i, (name, _, _, _) in enumerate(stages):
            sim.at(i * 2).trigger(name)
        sim.every(0.25, self.assertNoSolidInterference, self.node)
        for _, slew, traverse, hoist in stages:
            sim.run(2)
            for key, value in (
                ("slew", slew),
                ("traverse", traverse),
                ("hoist", hoist),
                ("run", 0),
            ):
                self.assertAlmostEqual(sim.state[key], value, delta=1e-6)
