import numpy as np
from solid_node.test import TestCase, testing_steps
from solid_node.simulation import ScenarioTest
from .Automatic_weaving_loom import AutomaticWeavingLoom


class AutomaticWeavingLoomTest(TestCase):

    node = AutomaticWeavingLoom

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @testing_steps(17)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_frame_stands_on_ground(self):
        bounds = self.node.frame.mesh.bounds
        self.assertAlmostEqual(bounds[0, 2], 0.0, delta=0.01)
        self.assertGreater(bounds[1, 2], 240)

    @testing_steps(9)
    def test_machine_has_a_support_path(self):
        self.assertAssemblySupported(self.node, ground=self.node.frame, max_drop=0.8)

    def test_opposite_heddles(self):
        lift = self.node.shed_lift
        for angle, expected in [(0, 0), (90, lift), (180, 0), (270, -lift)]:
            self.node.set_state(phase=angle, run=0, time=0)
            for heddle, sign in [(self.node.heddle_a, 1), (self.node.heddle_b, -1)]:
                z = heddle.cage.mesh.bounds[:, 2].mean()
                self.assertAlmostEqual(z, 180 + sign * expected, delta=0.01)

    def test_yarn_reaches_its_heddle_eye(self):
        lift = self.node.shed_lift
        for angle, direction in [(90, 1), (270, -1)]:
            self.node.set_state(phase=angle, run=0, time=0)
            for yarn, y, sign in [(self.node.warp_a[0], 20, 1),
                                   (self.node.warp_b[0], 40, -1)]:
                vertices = yarn.front.mesh.vertices
                rim = vertices[abs(vertices[:, 1] - y) < 0.15]
                self.assertGreater(len(rim), 0)
                self.assertAlmostEqual(rim[:, 2].mean(), 180 + sign * direction * lift, delta=0.01)

    def test_shed_envelope_is_guarded(self):
        for lift in (15.9, 20.1):
            with self.assertRaises(ValueError):
                AutomaticWeavingLoom(shed_lift=lift)

    @testing_steps(9)
    def test_eccentric_is_captured_with_bounded_play(self):
        for heddle, pin in [(self.node.heddle_a, self.node.crank.pin_a),
                            (self.node.heddle_b, self.node.crank.pin_b)]:
            self.assertNotIntersecting(heddle.yoke, pin)
            self.assertFreeWithin(heddle.yoke, 0.2, pin, along=(0, 0, 1))
            self.assertBlockedBeyond(heddle.yoke, 0.8, pin, along=(0, 0, 1))

    def test_shuttle_travel_and_handoff(self):
        for angle, x in [(0, -130), (90, 0), (180, 130), (270, 0), (360, -130)]:
            self.node.set_state(phase=angle, run=0, time=0)
            self.assertAlmostEqual(self.node.carrier.spool.mesh.bounds[:, 0].mean(), x, delta=0.01)
            if x == 0:
                lv = self.node.carrier.left.mesh.vertices
                rv = self.node.carrier.right.mesh.vertices
                left = lv[lv[:, 2] > 180, 0].max()
                right = rv[rv[:, 2] > 180, 0].min()
                self.assertAlmostEqual(left, -12.5, delta=0.02)
                self.assertAlmostEqual(right, 12.5, delta=0.02)

    def test_reed_arrives_after_carrier_clears(self):
        for angle, expected_y in [(0, -102), (90, -65), (180, -102), (270, -65)]:
            self.node.set_state(phase=angle, run=0, time=0)
            y = self.node.reed.mesh.bounds[:, 1].mean()
            self.assertAlmostEqual(y, expected_y, delta=0.01)
            if expected_y == -102:
                self.assertGreater(abs(self.node.carrier.spool.mesh.bounds[:, 0].mean()), 90)

    def test_warp_paths_leave_space_for_spool(self):
        # Check actual yarn surfaces at the spool's fore/aft envelope,
        # against drawing inputs, independently of the motion formulas.
        for angle in range(45, 136, 15):
            for phase in (angle, angle + 180):
                self.node.set_state(phase=phase, run=0, time=0)
                for thread in (self.node.warp_a[0], self.node.warp_b[0]):
                    vertices = thread.front.mesh.vertices
                    region = vertices[(vertices[:, 1] >= -43) & (vertices[:, 1] <= -27)]
                    self.assertGreater(len(region), 0)
                    self.assertGreater(np.min(abs(region[:, 2] - 180)), 4.0)


class LoomScenarioTest(ScenarioTest):
    node = AutomaticWeavingLoom
    dt = 0.05
    meshes = True

    def test_every_instruction_lands_and_stays_clear(self):
        sim = self.simulation()
        stages = [("Beat left", 0, 0), ("Open shed", 60, 0),
                  ("Handoff", 90, 0), ("Beat right", 180, 0),
                  ("Return pick", 270, 0), ("Run", 0, 1)]
        self.assertEqual(set(self.node.instructions), {stage[0] for stage in stages})
        for index, (name, _, _) in enumerate(stages):
            start = index * 1.0
            sim.at(start).trigger(name)
        sim.every(0.5, self.assertNoSolidInterference, self.node)
        for name, phase, run in stages:
            sim.run(1.0)
            self.assertAlmostEqual(sim.state["phase"], phase, delta=0.00001)
            self.assertAlmostEqual(sim.state["run"], run, delta=0.00001)
