"""Independent geometry measurements of the complete rope and rigid tackle."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math

import numpy as np
from scipy.spatial.distance import cdist
from solid_node.test import TestCase, testing_steps
from solid_node.simulation import ScenarioTest

from .model import PulleyBlock


class PulleyBlockTest(TestCase):
    node = PulleyBlock

    def pose(self, phase):
        self.node.set_state(phase=phase, run=0, time=0)

    def rope_centres(self):
        # Molejo's public layout is ring-major, 16 profile vertices/ring,
        # followed by two cap centres. Read the actual world mesh, not ports.
        vertices = np.asarray(self.node.rope.mesh.vertices)
        return vertices[:-2].reshape(-1, 16, 3).mean(axis=1)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(25)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def check_travel(self, phase, run=0, time=0):
        static = (1 - math.cos(math.radians(phase))) / 2
        animated = (1 - math.cos(math.radians(phase) + 2*math.pi*time)) / 2
        rise = 40*((1-run)*static + run*animated)
        load_bottom = self.node.block.load.mesh.bounds[0, 2]
        effort_top = self.node.effort.mesh.bounds[1, 2]
        self.assertAlmostEqual(load_bottom, 24 + rise, delta=0.01)
        self.assertAlmostEqual(effort_top, 208 - 3*rise, delta=0.01)
        self.assertAlmostEqual((208-effort_top), 3*(load_bottom-24), delta=0.01)
        return rise

    def check_route(self, rise):
        centres = self.rope_centres()
        # Nine elements, each 48 intervals, with shared seam rings.
        self.assertEqual(centres.shape, (433, 3))
        joints = centres[::48]
        expected = [(-62, 0, 112+rise), (-62, 0, 106+rise),
                    (-54, 0, 106+rise), (-54, 0, 230), (-18, 0, 230),
                    (-18, 0, 90+rise), (18, 0, 90+rise),
                    (18, 0, 230), (54, 0, 230), (54, 0, 200-3*rise)]
        total = 0.0
        arc_centres = {1: (-58, 0, 106+rise), 3: (-36, 0, 230),
                       5: (0, 0, 90+rise), 7: (36, 0, 230)}
        for index in range(9):
            points = centres[index*48:(index+1)*48+1]
            if index in arc_centres:
                centre = np.asarray(arc_centres[index])
                radii = np.linalg.norm(points-centre, axis=1)
                np.testing.assert_allclose(radii, 4 if index == 1 else 18, atol=0.001)
                # Actual swept angle and measured radius, not a copied arc length.
                vectors = (points-centre)/radii[:, None]
                angles = np.arccos(np.clip(np.sum(vectors[1:]*vectors[:-1], axis=1), -1, 1))
                self.assertAlmostEqual(float(angles.sum()), math.pi, delta=0.001)
                total += float(radii.mean()*angles.sum())
                sign = -1 if index in (1, 5) else 1
                self.assertGreater(sign*(points[24, 2]-centre[2]), 3.9 if index == 1 else 17.9)
            else:
                length = np.linalg.norm(points[-1]-points[0])
                total += float(length)
                np.testing.assert_allclose(points[:, 0], points[0, 0], atol=0.001)
        self.assertAlmostEqual(total, 440+58*math.pi, delta=0.01)
        np.testing.assert_allclose(joints, expected, atol=0.001)
        # Mesh volume is independent evidence of the full tube, including caps.
        polygon_area = 8*1.25**2*math.sin(2*math.pi/16)
        self.assertAlmostEqual(self.node.rope.mesh.volume/polygon_area, total, delta=0.16)
        return centres

    def test_displacement_route_and_constant_length(self):
        for phase in (0, 0.01, 30, 60, 90, 120, 150, 179.99, 180,
                      180.01, 210, 270, 330, 359.99, 360):
            self.pose(phase)
            self.check_route(self.check_travel(phase))

    def test_rope_clearance_and_self_separation(self):
        for phase in (0, 45, 90, 135, 180, 225, 270, 315, 360):
            self.pose(phase)
            for rigid in (self.node.frame, self.node.first, self.node.second,
                          self.node.block.carrier, self.node.block.wheel,
                          self.node.block.load, self.node.effort):
                self.assertNotIntersecting(self.node.rope, rigid)
            centres = self.rope_centres()
            chain = np.r_[0, np.cumsum(np.linalg.norm(np.diff(centres, axis=0), axis=1))]
            separation = cdist(centres, centres)
            remote = np.abs(chain[:, None]-chain[None, :]) > 6
            self.assertGreater(float(separation[remote].min()), 2*1.25+0.5)
            self.assertTrue(self.node.rope.mesh.is_watertight)
            self.assertEqual(len(self.node.rope.mesh.split(only_watertight=False)), 1)

    def test_sheave_journals_and_cheeks_capture(self):
        for phase in (0, 60, 120, 180, 270):
            self.pose(phase)
            for wheel, carrier in ((self.node.first, self.node.frame),
                                   (self.node.second, self.node.frame),
                                   (self.node.block.wheel, self.node.block.carrier)):
                for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                    self.assertFreeWithin(wheel, 0.12, carrier, along=axis)
                    self.assertBlockedBeyond(wheel, 0.65, carrier, along=axis)

    def test_rope_groove_capture_and_terminals(self):
        for phase in (0, 90, 180, 270):
            self.pose(phase)
            # All four wraps must remain clear in their lanes and be
            # caught by the flange / anchor cheeks beyond their axial play.
            for wheel in (self.node.first, self.node.second, self.node.block.wheel):
                self.assertFreeWithin(self.node.rope, 0.12, wheel, along=(0, 1, 0))
                self.assertBlockedBeyond(self.node.rope, 2.1, wheel, along=(0, 1, 0))
            centres = self.rope_centres()
            # Endpoints stay inside deep blind sockets. Independent measured
            # carrier/effort bounds tie them to the actual attached solids.
            carrier = self.node.block.carrier.mesh.bounds
            effort = self.node.effort.mesh.bounds
            self.assertAlmostEqual(centres[0, 2], carrier[1, 2]-2, delta=0.01)
            self.assertAlmostEqual(centres[-1, 2], effort[1, 2]-8, delta=0.01)
            self.assertFreeWithin(self.node.rope, 0.10, self.node.effort, along=(1, 0, 0))
            self.assertBlockedBeyond(self.node.rope, 0.65, self.node.effort, along=(1, 0, 0))
            self.assertFreeWithin(self.node.rope, 0.10, self.node.block.carrier, along=(0, 0, 1))
            self.assertBlockedBeyond(self.node.rope, 0.65, self.node.block.carrier,
                                     along=(0, 0, 1), directions="forward")

    def test_load_eye_and_declared_suspension_support(self):
        for phase in (0, 90, 180, 270):
            self.pose(phase)
            self.assertFreeWithin(self.node.block.load, 0.1, self.node.block.carrier, along=(0, 0, 1))
            self.assertBlockedBeyond(self.node.block.load, 0.7, self.node.block.carrier,
                                     along=(0, 0, -1), directions="forward")
            # Ideal rope suspension and held effort are explicit fixtures.
            # The solver proves the remaining rigid journal/eye support.
            self.assertAssemblySupported(self.node,
                ground=[self.node.frame, self.node.block.carrier, self.node.effort], max_drop=0.7)

    def test_control_combinations_and_loop_return(self):
        for phase in (0, 90, 180, 360):
            for run in (0, 0.25, 0.5, 1):
                for time in (0, 0.125, 0.5, 0.8, 1):
                    self.node.set_state(phase=phase, run=run, time=time)
                    self.check_route(self.check_travel(phase, run, time))
                    self.assertNoSolidInterference(self.node)
                self.node.set_state(time=0)
                start = self.node.rope.mesh.vertices.copy()
                self.node.set_state(time=1)
                np.testing.assert_allclose(self.node.rope.mesh.vertices, start, atol=1e-8)

    def test_sheave_rotation_from_actual_vertices(self):
        self.pose(0)
        wheels = (self.node.first, self.node.block.wheel, self.node.second)
        initial = [w.mesh.vertices.copy() for w in wheels]
        for phase in (45, 90, 135, 180, 270):
            self.pose(phase)
            rise = 20*(1-math.cos(math.radians(phase)))
            for w, start, factor, centre in zip(wheels, initial, (1, -2, 3),
                                               ((-36, 0, 230), (0, 0, 90), (36, 0, 230))):
                angle = factor*rise/18
                c, s = math.cos(angle), math.sin(angle)
                rotation = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
                expected = (start-centre) @ rotation.T + centre
                if factor == -2:
                    expected[:, 2] += rise
                np.testing.assert_allclose(w.mesh.vertices, expected, atol=0.001)


class PulleyBlockScenarioTest(ScenarioTest):
    node = PulleyBlock
    dt = 0.05
    meshes = True

    def test_instruction_ramps_are_clear(self):
        sim = self.simulation()
        stages = (("Low", 0, 0), ("Mid", 90, 0), ("High", 180, 0), ("Run", 0, 1))
        self.assertEqual(set(self.node.instructions), {s[0] for s in stages})
        for i, (name, _, _) in enumerate(stages):
            sim.at(i).trigger(name)
        sim.every(0.2, self.assertNoSolidInterference, self.node)
        for _, phase, run in stages:
            sim.run(1)
            self.assertAlmostEqual(sim.state["phase"], phase, delta=1e-5)
            self.assertAlmostEqual(sim.state["run"], run, delta=1e-5)
