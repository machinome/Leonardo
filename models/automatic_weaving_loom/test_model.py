# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import numpy as np
from machinome.test import TestCase
from .checks import sampled_poses, rigid_parts
from machinome.simulation import ScenarioTest
from .model import AutomaticWeavingLoom


class AutomaticWeavingLoomTest(TestCase):

    node = AutomaticWeavingLoom

    def test_00_declared_time_is_sixty_seconds(self):
        self.assertEqual(getattr(AutomaticWeavingLoom.time, "loop", None), 60)
        for seconds, angle in ((0, 0), (15, 360), (30, 720), (45, 1080), (60, 1440)):
            self.node.set_state(phase=0, run=1, time=seconds)
            self.assertAlmostEqual(self.node.cycle.value, angle)

    def test_00_historical_timing_train_is_present(self):
        self.assertTrue(
            hasattr(self.node, "timing"),
            "The one-tooth / six-tooth / twelve-tooth transmission is missing",
        )

    def test_01_weaving_outputs_have_physical_actuators(self):
        self.assertTrue(
            hasattr(self.node, "head_drive"),
            "Arms, reed and gripping jaws still lack physical transmissions",
        )

    def test_01_reed_crosses_the_carrier_and_returns_behind_it(self):
        n = self.node
        for phase, expected_y in (
            (0, 48),
            (45, 148),
            (90, 148),
            (135, 148),
            (180, 48),
            (225, 148),
            (270, 148),
            (315, 148),
            (360, 48),
        ):
            n.set_state(phase=phase, run=0, time=0)
            self.assertAlmostEqual(
                n.reed.mesh.bounds[:, 1].mean(), expected_y, delta=0.01
            )
        crossings = []
        for phase in range(361):
            n.set_state(phase=phase, run=0, time=0)
            bounds = n.reed.mesh.bounds
            if bounds[0, 1] < 123 and bounds[1, 1] > 107:
                crossings.append(phase)
                self.assertLess(n.carrier.left.body.mesh.bounds[1, 0], -98)
                self.assertGreater(n.carrier.right.body.mesh.bounds[0, 0], 98)
                for _, part in rigid_parts(n.carrier):
                    self.assertNotIntersecting(n.reed, part)
        self.assertGreaterEqual(len(crossings), 4, "Reed never crosses the hands")

    def test_01_reed_tracks_carry_the_entire_working_stroke(self):
        n = self.node
        for phase in (0, 10, 20, 45, 90, 160, 170, 180):
            n.set_state(phase=phase, run=0, time=0)
            feet = n.reed.mesh.vertices
            feet = feet[feet[:, 2] < 445]
            track = n.reed_tracks.mesh.bounds
            self.assertGreater(feet[:, 1].min(), track[0, 1])
            self.assertLess(feet[:, 1].max(), track[1, 1])
            self.assertNotIntersecting(n.reed, n.reed_tracks)
            self.assertFreeWithin(n.reed, 0.1, n.reed_tracks, along=(1, 0, 0))
            self.assertBlockedBeyond(n.reed, 0.7, n.reed_tracks, along=(1, 0, 0))

    def test_reed_cam_captures_the_roller_on_the_beat_flanks(self):
        # The former 45-degree head sampling saw only this cam's dwells.
        # Probe the steep motion sectors themselves, in both directions.
        for beat in (0, 180):
            for offset in range(-26, 27, 2):
                phase = (beat + offset) % 360
                self.node.set_state(phase=phase, run=0, time=0)
                roller, cam = self.node.head_drive.reed, self.node.timing.input
                try:
                    self.assertNotIntersecting(roller, cam)
                    self.assertFreeWithin(roller, 0.1, cam, along=(0, 0, 1))
                    self.assertBlockedBeyond(roller, 1.5, cam, along=(0, 0, 1))
                except AssertionError as error:
                    raise AssertionError(f"reed cam at {phase}°: {error}") from error

    def test_01_reed_presses_the_visible_red_weft_toward_the_fell(self):
        from .test_cord_bench import centerline

        n = self.node
        for phase in (0, 180, 360):
            n.set_state(phase=phase, run=0, time=0)
            yarn = centerline(n.weft)
            ribbon = yarn[np.abs(yarn[:, 0]) < 60]
            self.assertGreater(len(ribbon), 0)
            self.assertLessEqual(ribbon[:, 1].max(), 46.55)
            self.assertGreaterEqual(ribbon[:, 1].min(), 45)
            np.testing.assert_allclose(
                yarn[-1],
                (n.carrier.spool.mesh.bounds[:, 0].mean(), 115, 520),
                atol=0.002,
            )

    def test_02_operating_flexible_routes_clear_the_machine(self):
        import trimesh
        from .test_cord_bench import centerline

        n = self.node
        routes = []
        for side in ("left", "right"):
            group = getattr(n.cords, side)
            arm = getattr(n.carrier, side)
            mechanism = getattr(n.head_drive, side)
            routes.extend(
                (
                    (
                        side + " haul",
                        group.haul.cord,
                        8,
                        {id(mechanism.output): 0, id(arm.body): -1},
                    ),
                    (
                        side + " return",
                        group.returning.cord,
                        8,
                        {id(arm.body): 0, id(group.weight): -1},
                    ),
                    (
                        side + " spring",
                        arm.spring,
                        4,
                        {id(arm.body): 0, id(arm.jaw): -1},
                    ),
                )
            )
        routes.extend(
            (
                (
                    "reed haul",
                    n.cords.reed.haul.cord,
                    8,
                    {id(n.head_drive.reed): 0, id(n.reed): -1},
                ),
                (
                    "reed return",
                    n.cords.reed.returning.cord,
                    8,
                    {id(n.reed): 0, id(n.cords.reed.weight): -1},
                ),
            )
        )
        rigid = list(rigid_parts(n))
        for phase in range(0, 361, 15):
            n.set_state(phase=phase, run=0, time=0)
            meshes = [(path, part, part.mesh) for path, part in rigid]
            for name, flexible, profile, terminations in routes:
                mesh = flexible.mesh
                a = mesh.bounds
                ends = centerline(flexible, profile)
                for path, part, other in meshes:
                    b = other.bounds
                    if not (np.all(a[0] < b[1]) and np.all(b[0] < a[1])):
                        continue
                    try:
                        if id(part) not in terminations:
                            self.assertNotIntersecting(flexible, part)
                        else:
                            # A cord is tied into a 3 mm terminal zone; a
                            # spring is clamped/bearing at its ends. Admit
                            # those local attachments, never an entire mate.
                            overlap = trimesh.boolean.intersection(
                                [mesh, other], engine="manifold"
                            )
                            if len(overlap.vertices):
                                endpoint = ends[terminations[id(part)]]
                                self.assertLessEqual(
                                    np.linalg.norm(
                                        overlap.vertices - endpoint, axis=1
                                    ).max(),
                                    3,
                                )
                    except AssertionError as error:
                        raise AssertionError(
                            f"{name}, {phase}°, {path}: {error}"
                        ) from error

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    @sampled_poses(289, end=60)
    def test_assembly_integrity(self):
        try:
            self.assertNoSolidInterference(self.node)
        except AssertionError as error:
            raise AssertionError(
                f"four-turn sample {self.node.time}: {error}"
            ) from error

    def test_transition_neighborhoods_and_combined_controls(self):
        for angle in (
            0,
            10,
            50,
            60,
            85,
            90,
            95,
            120,
            130,
            170,
            180,
            190,
            230,
            240,
            265,
            270,
            275,
            300,
            310,
            350,
            360,
            480,
            600,
            720,
            1080,
            1440,
        ):
            for delta in (-0.1, 0, 0.1):
                effective = min(1440, max(0, angle + delta))
                self.node.set_state(phase=0, run=1, time=effective / 24)
                self.assertNoSolidInterference(self.node)
        # Two mixed controls representing the same imposed shaft coordinate
        # must put actual geometry in the same place, including winding.
        for phase, run, time in ((73, 0, 0), (13, 0.5, 5), (0, 1, 73 / 24)):
            self.node.set_state(phase=phase, run=run, time=time)
            if phase == 73:
                spool = self.node.carrier.spool.mesh.vertices.copy()
                rack = self.node.winding.rack.mesh.vertices.copy()
            else:
                np.testing.assert_allclose(
                    self.node.carrier.spool.mesh.vertices, spool, atol=0.002
                )
                np.testing.assert_allclose(
                    self.node.winding.rack.mesh.vertices, rack, atol=0.002
                )
        self.node.set_state(phase=0, run=1, time=60)
        end = self.node.winding.rack.mesh.bounds.copy()
        self.node.set_state(phase=360, run=1, time=60)
        np.testing.assert_allclose(self.node.winding.rack.mesh.bounds, end, atol=0.002)

    def test_frame_stands_on_ground(self):
        bounds = self.node.frame.mesh.bounds
        self.assertAlmostEqual(bounds[0, 2], 0.0, delta=0.01)
        self.assertGreater(bounds[1, 2], 590)

    @sampled_poses(9, end=15)
    def test_machine_has_a_support_path(self):
        # The three weights are suspended by the independently checked taut
        # cords. The rigid-only static checker cannot supply a rope tension.
        weights = (
            self.node.cords.left.weight,
            self.node.cords.right.weight,
            self.node.cords.reed.weight,
        )
        # Largest vertical cam play is 2.5-1.5=1.0 mm. A 1.2 mm drop
        # exceeds it, but stays below the 1 mm finger plus its 0.3 mm gap.
        self.assertAssemblySupported(
            self.node,
            ground=self.node.frame,
            max_drop=1.2,
            supports=[(weight, self.node.frame) for weight in weights],
        )

    def test_arm_and_jaw_guides_are_physically_closed(self):
        for phase in range(0, 361, 15):
            self.node.set_state(phase=phase, run=0, time=0)
            for arm in (self.node.carrier.left, self.node.carrier.right):
                for along in ((0, 1, 0), (0, 0, 1)):
                    self.assertFreeWithin(arm.body, 0.1, self.node.frame, along=along)
                    self.assertBlockedBeyond(
                        arm.body, 0.7, self.node.frame, along=along
                    )
                for along in ((1, 0, 0), (0, 0, 1)):
                    self.assertFreeWithin(arm.jaw, 0.1, arm.body, along=along)
                    self.assertBlockedBeyond(arm.jaw, 0.7, arm.body, along=along)
                from .test_cord_bench import centerline

                spring = centerline(arm.spring, 4)
                bounds = arm.body.mesh.bounds
                outer = bounds[0, 0] if arm.side < 0 else bounds[1, 0]
                origin_x = outer - arm.side * 192.5
                np.testing.assert_allclose(
                    spring[0],
                    (origin_x + arm.side * 185, 140 if arm.side < 0 else 70, 522),
                    atol=0.002,
                )
                # The tip bears on top of the jaw's actuation bar to close it.
                tip_x = origin_x + arm.side * 185
                top = arm.jaw.mesh.bounds[1, 2]
                opening = arm.jaw.mesh.bounds[1, 1] - (139 if arm.side < 0 else 153)
                np.testing.assert_allclose(
                    spring[-1], (tip_x, 99 + opening, top), atol=0.002
                )

    def test_opposite_heddles(self):
        lift = self.node.shed_lift
        for angle, expected in [(0, 0), (90, lift), (180, 0), (270, -lift)]:
            self.node.set_state(phase=angle, run=0, time=0)
            for heddle, sign in [
                (self.node.head_drive.heddle_a, 1),
                (self.node.head_drive.heddle_b, -1),
            ]:
                z = heddle.cage.mesh.bounds[:, 2].mean()
                self.assertAlmostEqual(z, 520 + sign * expected, delta=0.01)

    def test_yarn_reaches_its_heddle_eye(self):
        lift = self.node.shed_lift
        for angle, direction in [(90, 1), (270, -1)]:
            self.node.set_state(phase=angle, run=0, time=0)
            for yarn, y, sign in [
                (self.node.warp_a[0], 170, 1),
                (self.node.warp_b[0], 190, -1),
            ]:
                vertices = yarn.front.fiber.mesh.vertices
                rim = vertices[abs(vertices[:, 1] - y) < 0.15]
                self.assertGreater(len(rim), 0)
                self.assertAlmostEqual(
                    rim[:, 2].mean(), 520 + sign * direction * lift, delta=0.01
                )

    def test_shed_envelope_is_guarded(self):
        for lift in (15.9, 20.1):
            with self.assertRaises(ValueError):
                AutomaticWeavingLoom(shed_lift=lift)

    @sampled_poses(9, end=15)
    def test_head_followers_are_captured_by_the_common_shaft(self):
        h = self.node.head_drive
        for name, follower in (
            ("heddle A", h.heddle_a.follower),
            ("heddle B", h.heddle_b.follower),
            ("left arm", h.left.follower),
            ("right arm", h.right.follower),
            ("reed", h.reed),
            ("selector A", h.selector_a),
            ("selector B", h.selector_b),
        ):
            try:
                self.assertNotIntersecting(follower, self.node.timing.input)
                self.assertFreeWithin(
                    follower, 0.1, self.node.timing.input, along=(0, 0, 1)
                )
                self.assertBlockedBeyond(
                    follower, 1.5, self.node.timing.input, along=(0, 0, 1)
                )
            except AssertionError as error:
                raise AssertionError(f"{name}: {error}") from error

    @sampled_poses(17, end=15)
    def test_rocking_levers_close_both_slots(self):
        for arm in (self.node.head_drive.left, self.node.head_drive.right):
            for slider in (arm.follower, arm.output):
                self.assertFreeWithin(slider, 0.1, arm.lever, along=(0, 0, 1))
                self.assertBlockedBeyond(slider, 0.7, arm.lever, along=(0, 0, 1))

    def test_shuttle_travel_and_handoff(self):
        for angle, x in [(0, -130), (90, 0), (180, 130), (270, 0), (360, -130)]:
            self.node.set_state(phase=angle, run=0, time=0)
            self.assertAlmostEqual(
                self.node.carrier.spool.mesh.bounds[:, 0].mean(), x, delta=0.01
            )
            if x == 0:
                lv = self.node.carrier.left.body.mesh.vertices
                rv = self.node.carrier.right.body.mesh.vertices
                # Measure the central outer stops, not the newly added
                # side cheeks that deliberately extend along the boat.
                left = lv[(lv[:, 2] > 520) & (abs(lv[:, 1] - 115) < 4.01), 0].max()
                right = rv[(rv[:, 2] > 520) & (abs(rv[:, 1] - 115) < 4.01), 0].min()
                self.assertAlmostEqual(left, -12.5, delta=0.02)
                self.assertAlmostEqual(right, 12.5, delta=0.02)

    def test_reed_arrives_after_carrier_clears(self):
        for angle, expected_y in [(0, 48), (90, 148), (180, 48), (270, 148)]:
            self.node.set_state(phase=angle, run=0, time=0)
            y = self.node.reed.mesh.bounds[:, 1].mean()
            self.assertAlmostEqual(y, expected_y, delta=0.01)
            if expected_y == 48:
                self.assertGreater(
                    abs(self.node.carrier.spool.mesh.bounds[:, 0].mean()), 90
                )

    def test_warp_paths_leave_space_for_spool(self):
        # Check actual yarn surfaces at the spool's fore/aft envelope,
        # against drawing inputs, independently of the motion formulas.
        for angle in range(45, 136, 15):
            for phase in (angle, angle + 180):
                self.node.set_state(phase=phase, run=0, time=0)
                for thread in (self.node.warp_a[0], self.node.warp_b[0]):
                    vertices = thread.front.fiber.mesh.vertices
                    region = vertices[(vertices[:, 1] >= 107) & (vertices[:, 1] <= 123)]
                    self.assertGreater(len(region), 0)
                    self.assertGreater(np.min(abs(region[:, 2] - 520)), 4.0)

    def test_actual_warp_does_not_touch_the_hands_or_spool(self):
        # Rigid integrity cannot see yarn. Check both shed signs, including
        # entry and exit rather than only the centre handoff.
        parts = (
            self.node.carrier.spool,
            self.node.carrier.left.body,
            self.node.carrier.left.jaw,
            self.node.carrier.right.body,
            self.node.carrier.right.jaw,
            self.node.carrier.left.spring,
            self.node.carrier.right.spring,
            self.node.reed,
        )
        yarns = [end.front.fiber for end in (*self.node.warp_a, *self.node.warp_b)]
        for phase in range(0, 361, 5):
            self.node.set_state(phase=phase, run=0, time=0)
            bounds = {id(part): part.mesh.bounds for part in parts}
            for yarn in yarns:
                a = yarn.mesh.bounds
                for part in parts:
                    b = bounds[id(part)]
                    if np.all(a[0] < b[1]) and np.all(b[0] < a[1]):
                        try:
                            self.assertNotIntersecting(yarn, part)
                        except AssertionError as error:
                            raise AssertionError(
                                f"warp entry/exit at {phase}°: {error}"
                            ) from error

    def test_integrated_grips_retain_the_spool(self):
        for phase in (
            0,
            30,
            60,
            84,
            85,
            89,
            90,
            91,
            95,
            96,
            120,
            180,
            240,
            264,
            265,
            269,
            270,
            271,
            275,
            276,
            300,
            360,
        ):
            self.node.set_state(phase=phase, run=0, time=0)
            arm = (
                self.node.carrier.left
                if phase < 90 or phase >= 270
                else self.node.carrier.right
            )
            for part, along in (
                (arm.body, (arm.side, 0, 0)),
                (arm.jaw, (-arm.side, 0, 0)),
                (arm.jaw, (0, -arm.side, 0)),
                (arm.body, (0, arm.side, 0)),
                (arm.jaw, (0, 0, 1)),
                (arm.body, (0, 0, -1)),
            ):
                self.assertFreeWithin(self.node.carrier.spool, 0.1, part, along=along)
                self.assertBlockedBeyond(
                    self.node.carrier.spool,
                    0.8,
                    part,
                    along=along,
                    directions="forward",
                )

    def test_cords_meet_the_real_arm_and_reed_attachments(self):
        from .test_cord_bench import centerline

        for phase in range(0, 361, 15):
            self.node.set_state(phase=phase, run=0, time=0)
            for mechanism, arm, cords in (
                (
                    self.node.head_drive.left,
                    self.node.carrier.left,
                    self.node.cords.left,
                ),
                (
                    self.node.head_drive.right,
                    self.node.carrier.right,
                    self.node.cords.right,
                ),
            ):
                haul = centerline(cords.haul.cord)
                output = mechanism.output.mesh.bounds
                np.testing.assert_allclose(
                    haul[0], (output[:, 0].mean(), 240, output[0, 2] + 200), atol=0.002
                )
                bounds = arm.body.mesh.bounds
                attach_x = bounds[0, 0] + 7.5 if arm.side < 0 else bounds[1, 0] - 7.5
                np.testing.assert_allclose(haul[-1], (attach_x, 240, 520), atol=0.002)
                self.assertAlmostEqual(
                    haul[0, 2] + cords.weight.mesh.bounds[1, 2], 848, delta=0.002
                )
            reed = self.node.reed.mesh.bounds
            np.testing.assert_allclose(
                centerline(self.node.cords.reed.haul.cord)[-1],
                (-357, reed[:, 1].mean(), 570),
                atol=0.002,
            )
            np.testing.assert_allclose(
                centerline(self.node.cords.reed.haul.cord)[0],
                (-357, 180, self.node.head_drive.reed.mesh.bounds[1, 2]),
                atol=0.002,
            )
            np.testing.assert_allclose(
                centerline(self.node.cords.reed.returning.cord)[0],
                (-331, reed[:, 1].mean(), 570),
                atol=0.002,
            )
            self.assertAlmostEqual(
                centerline(self.node.cords.reed.haul.cord)[0, 2]
                + self.node.cords.reed.weight.mesh.bounds[1, 2],
                1027.5,
                delta=0.002,
            )


class LoomScenarioTest(ScenarioTest):
    node = AutomaticWeavingLoom
    dt = 0.05
    meshes = True

    def test_every_instruction_lands_and_stays_clear(self):
        sim = self.simulation()
        stages = [
            ("Beat left", 0, 0),
            ("Open shed", 60, 0),
            ("Handoff", 90, 0),
            ("Beat right", 180, 0),
            ("Return pick", 270, 0),
            ("Run", 0, 1),
        ]
        self.assertEqual(set(self.node.instructions), {stage[0] for stage in stages})
        for index, (name, _, _) in enumerate(stages):
            start = index * 1.0
            sim.at(start).trigger(name)
        sim.every(0.5, self.assertNoSolidInterference, self.node)
        for name, phase, run in stages:
            sim.run(1.0)
            self.assertAlmostEqual(sim.state["phase"], phase, delta=0.00001)
            self.assertAlmostEqual(sim.state["run"], run, delta=0.00001)
