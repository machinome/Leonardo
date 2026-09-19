"""Measure the built lift independently of its tooth and motion generators."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

import numpy as np
from machinome.test import TestCase, testing_steps
from machinome.simulation import ScenarioTest

from .model import RackAndPinion


class RackAndPinionTest(TestCase):
    node = RackAndPinion

    def pose(self, phase):
        self.node.set_state(phase=phase, run=0, time=0)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(37)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def check_position(self, phase, run=0, time=0):
        m = self.node.module
        fixed = (1 - math.cos(math.radians(phase))) / 2
        cycling = (1 - math.cos(math.radians(phase) + 2 * math.pi * time)) / 2
        travel = 24 * m * ((1 - run) * fixed + run * cycling)
        rack = self.node.carriage.rack.bar.mesh.bounds
        load = self.node.carriage.load.mesh.bounds
        self.assertAlmostEqual(rack[0, 2], 32 * m + travel, delta=0.01)
        self.assertAlmostEqual(rack[1, 2], 116 * m + travel, delta=0.01)
        self.assertAlmostEqual(load[0, 2], 9 * m + travel, delta=0.01)
        self.assertAlmostEqual(rack[1, 0], 16 * m, delta=0.01)
        # The grip is a symmetric cylinder, whose centre measures the
        # actual crank angle. No joint value is used as an expectation.
        grip = self.node.pinion.crank.grip.mesh.bounds.mean(axis=0)
        angle = travel / (10 * m)
        self.assertAlmostEqual(grip[0], -13 * m * math.cos(angle), delta=0.01)
        self.assertAlmostEqual(grip[2], 80 * m - 13 * m * math.sin(angle), delta=0.01)

    def test_travel_and_crank_rotation(self):
        for phase in (0, 30, 60, 90, 120, 150, 180, 210, 270, 330, 360):
            self.pose(phase)
            self.check_position(phase)

    def test_tooth_pitch_engagement_and_backlash(self):
        m = self.node.module
        for degrees in np.linspace(0, 18, 19):
            phase = math.degrees(math.acos(1 - math.radians(degrees) * 10 / 12))
            self.pose(phase)
            self.assertNoSolidInterference(self.node)
            # Total tangential backlash 0.2*m, shared equally between
            # tooth thinning of the two members. Centred play is 0.1*m.
            self.assertFreeWithin(self.node.carriage.rack, 0.06 * m,
                                  self.node.pinion, along=(0, 0, 1))
            self.assertBlockedBeyond(self.node.carriage.rack, 0.18 * m,
                                     self.node.pinion, along=(0, 0, 1))

    def test_guides_capture_rack(self):
        m = self.node.module
        for phase in (0, 45, 90, 135, 180, 270, 360):
            self.pose(phase)
            for axis in ((1, 0, 0), (0, 1, 0)):
                self.assertFreeWithin(self.node.carriage.rack, 0.05 * m,
                                      self.node.frame, along=axis)
                self.assertBlockedBeyond(self.node.carriage.rack, 0.3 * m,
                                         self.node.frame, along=axis)

    def test_journal_and_collars_capture_pinion(self):
        m = self.node.module
        for phase in (0, 60, 120, 180, 270):
            self.pose(phase)
            for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                self.assertFreeWithin(self.node.pinion, 0.05 * m,
                                      self.node.frame, along=axis)
                self.assertBlockedBeyond(self.node.pinion, 0.3 * m,
                                         self.node.frame, along=axis)

    def test_end_stops_beyond_demonstrated_travel(self):
        m = self.node.module
        for phase, axis in ((0, (0, 0, -1)), (180, (0, 0, 1))):
            self.pose(phase)
            self.assertFreeWithin(self.node.carriage.rack, 0.5 * m,
                                  self.node.frame, along=axis, directions="forward")
            self.assertBlockedBeyond(self.node.carriage.rack, 1.5 * m,
                                     self.node.frame, along=axis, directions="forward")

    def test_hook_and_load_seating(self):
        m = self.node.module
        for phase in (0, 90, 180, 270):
            self.pose(phase)
            self.assertNotIntersecting(self.node.carriage.rack, self.node.carriage.load)
            self.assertFreeWithin(self.node.carriage.load, 0.05 * m,
                                  self.node.carriage.rack, along=(0, 0, 1))
            self.assertBlockedBeyond(self.node.carriage.load, 0.8 * m,
                                     self.node.carriage.rack, along=(0, 0, -1),
                                     directions="forward")
            self.assertAssemblySupported(self.node, ground=[self.node.frame, self.node.pinion],
                                         max_drop=0.8 * m)

    def test_reversals_controls_and_loop_closure(self):
        for phase in (0, 0.01, 90, 179.99, 180, 180.01, 270, 359.99, 360):
            self.pose(phase)
            self.check_position(phase)
            self.assertNoSolidInterference(self.node)
        for phase in (0, 90, 180, 360):
            for run in (0, 0.25, 0.5, 1):
                for time in (0, 0.125, 0.5, 0.8, 1):
                    self.node.set_state(phase=phase, run=run, time=time)
                    self.check_position(phase, run, time)
                    self.assertNoSolidInterference(self.node)
                self.node.set_state(phase=phase, run=run, time=0)
                start = self.node.carriage.load.mesh.vertices.copy()
                self.node.set_state(time=1)
                np.testing.assert_allclose(self.node.carriage.load.mesh.vertices, start, atol=1e-8)

    def test_size_and_ground(self):
        m = self.node.module
        self.pose(0)
        self.assertAlmostEqual(self.node.frame.mesh.bounds[0, 2], 0, delta=0.01)
        self.assertAlmostEqual(self.node.frame.mesh.extents[0], 64 * m, delta=0.01)
        profile = self.node.pinion.profile.mesh.vertices
        radius = np.hypot(profile[:, 0], profile[:, 2] - 80 * m).max()
        self.assertAlmostEqual(radius, 11 * m, delta=0.01)
        for value in (2.49, 3.51):
            with self.assertRaises(ValueError):
                RackAndPinion(module=value)


class RackAndPinionScenarioTest(ScenarioTest):
    node = RackAndPinion
    dt = 0.05
    meshes = True

    def test_instructions_land_and_stay_clear(self):
        sim = self.simulation()
        stages = (("Bottom", 0, 0), ("Mid-lift", 90, 0),
                  ("Top", 180, 0), ("Run", 0, 1))
        self.assertEqual(set(self.node.instructions), {s[0] for s in stages})
        for i, (name, _, _) in enumerate(stages):
            sim.at(i).trigger(name)
        sim.every(0.1, self.assertNoSolidInterference, self.node)
        for _, phase, run in stages:
            sim.run(1)
            self.assertAlmostEqual(sim.state["phase"], phase, delta=1e-5)
            self.assertAlmostEqual(sim.state["run"], run, delta=1e-5)
