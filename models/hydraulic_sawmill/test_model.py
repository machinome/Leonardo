# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
from pathlib import Path

import numpy as np
import trimesh

from machinome.test import TestCase, testing_steps
from machinome.node import CadQueryNode

from .model import LeonardoHydraulicSawmill
from .rope_drive import PASS_SECONDS, PASS_TURNS
from .layout import TURN_SECONDS


class BearingJournalProbe(CadQueryNode):
    """Local shaft section tests each wooden seat in the complete
    fixture."""

    def render(self):
        from .parts import cylinder_y

        return cylinder_y(6, 14)


class LeonardoHydraulicSawmillTest(TestCase):
    node = LeonardoHydraulicSawmill

    def test_python_sources_follow_pep8(self):
        from test_style import check_python_style

        check_python_style(Path(__file__).resolve().parent)

    @staticmethod
    def fixture_parts(fixture):
        if fixture.rigid:
            yield fixture
        else:
            for child in fixture.children:
                yield from LeonardoHydraulicSawmillTest.fixture_parts(child)

    def assertFixtureFree(self, moving, amount, fixture, **kwargs):
        # The fixture is now actual parts, with no fused fixture STL.
        for part in self.fixture_parts(fixture):
            self.assertFreeWithin(moving, amount, part, **kwargs)

    def fixture_mesh(self, fixture):
        return trimesh.util.concatenate(
            [part.mesh for part in self.fixture_parts(fixture)]
        )

    def assertFixtureBlocked(self, moving, amount, fixture, **kwargs):
        # Preserve whole-fixture semantics: each direction must meet at
        # least
        # one real part; opposed stops need not be the same member.
        directions = kwargs.pop("directions", "both")
        for sign in ((1,) if directions == "forward" else (1, -1)):
            options = dict(kwargs, directions="forward")
            key = "along" if "along" in options else "axis"
            options[key] = tuple(sign * v for v in options.get(key, (0, 0, 1)))
            for part in self.fixture_parts(fixture):
                try:
                    self.assertBlockedBeyond(moving, amount, part, **options)
                except AssertionError:
                    continue
                break
            else:
                self.fail(
                    f"{moving.name} is not blocked by {fixture.name}, "
                    f"direction {sign}"
                )

    def test_photographed_handedness(self):
        self.node.set_keyframe(0)
        blade = self.node.saw.sash.blade.mesh.bounds
        self.assertAlmostEqual(blade[1, 0], 10, delta=0.01)
        self.assertAlmostEqual(blade[0, 0], -5, delta=0.01)
        self.assertGreater(
            self.node.feed.feed_drum.mesh.bounds[:, 0].mean(), 100
        )
        self.assertGreater(
            self.node.carriage.timber.log_left.mesh.bounds[0, 0], 10
        )
        self.assertLess(self.node.feed.upper_roller.mesh.bounds[1, 0], -350)
        gear = self.node.feed.feed_drum.mesh.vertices
        rim = gear[np.linalg.norm(gear[:, [0, 2]] - [115, 330], axis=1) > 41]
        timber_max = max(
            n.mesh.bounds[1, 1]
            for n in (
                self.node.carriage.timber.log_left,
                self.node.carriage.timber.log_right,
            )
        )
        self.assertGreater(rim[:, 1].min(), timber_max)
        self.assertLess(
            self.node.water_drive.waterwheel.mesh.bounds[1, 1], -100
        )

    def test_iron_links_are_adjacent_inside_the_frame(self):
        nodes = (
            self.node.saw.connecting_rod,
            self.node.feed.feed_tie,
            self.node.feed.rocker,
            self.node.feed.pawl,
        )
        centres = [n.mesh.bounds[:, 1].mean() for n in nodes]
        self.assertLess(max(centres) - min(centres), 60)
        self.assertAlmostEqual(centres[0], 0, delta=0.01)
        self.assertTrue(
            all(a < b for a, b in zip(centres, centres[1:])), centres
        )
        self.assertLess(max(centres), 60)

    def test_shaft_reaches_a_separate_square_bored_crank(self):
        self.assertTrue(
            hasattr(self.node.water_drive, "crank"),
            "The round shaft and square-bored crank must be "
            "separate fitted solids",
        )
        end = self.node.water_drive.crankshaft.mesh.bounds[1, 1]
        self.assertGreater(end, -12)
        self.assertLess(
            end,
            0,
            "The shaft must end at the central crank, not cross "
            "the saw and return",
        )
        self.assertFreeWithin(
            self.node.water_drive.crank,
            1,
            self.node.water_drive.crankshaft,
            axis=(0, 1, 0),
        )
        self.assertBlockedBeyond(
            self.node.water_drive.crank,
            8,
            self.node.water_drive.crankshaft,
            axis=(0, 1, 0),
        )

    def test_haul_force_is_on_the_carriage_centreline(self):
        for seconds in (0, PASS_SECONDS / 2, PASS_SECONDS):
            self.node.set_keyframe(seconds)
            free = self.rope_centres(self.node.feed.haul.rope)
            np.testing.assert_allclose(free[:73, 1], 0, atol=0.001)
            self.assertAlmostEqual(free[0, 2], 370, delta=0.001)
            self.assertAlmostEqual(
                self.node.carriage.anchor.mesh.bounds[:, 1].mean(),
                0,
                delta=0.01,
            )
            self.assertLessEqual(
                self.node.carriage.anchor.mesh.extents[2],
                12.1,
                "No hanging strap: haul through the upper crossmember",
            )
            self.assertGreater(
                free[0, 0], self.node.carriage.bed.mesh.bounds[0, 0]
            )
            self.assertLess(
                free[0, 0], self.node.carriage.bed.mesh.bounds[0, 0] + 20
            )

    def test_frame_has_no_duplicate_rail_above_the_gear(self):
        wood = self.fixture_mesh(self.node.frame.timber_structure.bed)
        hits, _, _ = wood.ray.intersects_location(
            [[150, 115, 400]], [[0, 0, -1]]
        )
        self.assertGreater(len(hits), 0)
        self.assertAlmostEqual(hits[:, 2].max(), 339, delta=0.01)

    def test_rectangular_frame_has_no_pulley_outrigger_or_rope_notch(self):
        wood = self.fixture_mesh(self.node.frame.timber_structure.bed)
        self.assertAlmostEqual(
            wood.bounds[0, 0],
            -wood.bounds[1, 0],
            delta=0.01,
            msg="The end pulley must not require a wooden outrigger",
        )
        for x in (-335, 335):
            hits, _, _ = wood.ray.intersects_location(
                [[x, 0, 400]], [[0, 0, -1]]
            )
            self.assertGreater(len(hits), 0)
            self.assertAlmostEqual(
                hits[:, 2].max(),
                338,
                delta=0.01,
                msg="Keep the end crossmember continuous through the centre",
            )

    def test_photographed_upper_roller_is_present(self):
        self.assertTrue(
            hasattr(self.node.feed, "upper_roller"),
            "The carriage rope passes over a separate roller at the rail ends",
        )
        roller = self.node.feed.upper_roller.mesh
        self.assertGreater(roller.extents[1], 60)
        self.assertGreater(roller.bounds[:, 2].mean(), 330)

    def test_compound_reduction_is_not_a_direct_carriage_drive(self):
        self.assertTrue(hasattr(self.node.feed, "reduction_shaft"))
        self.node.set_keyframe(0)
        start = self.node.carriage.bed.mesh.bounds[:, 0].mean()
        self.node.set_keyframe(4)
        travel = start - self.node.carriage.bed.mesh.bounds[:, 0].mean()
        self.assertGreater(travel, 0.3)
        self.assertLess(
            travel,
            0.4,
            "Bare input axle and thin take-up must both reduce the feed",
        )
        from machinome.motion.ports import declared_time

        self.assertGreater(declared_time(type(self.node)).loop, 1200)

    def test_ratchet_rope_builds_radially_beside_the_gear(self):
        self.node.set_keyframe(0)
        gear = self.node.feed.feed_drum.mesh.vertices
        inward = gear[(gear[:, 1] > -60) & (gear[:, 1] < 54)]
        self.assertGreater(len(inward), 0)
        radius = np.linalg.norm(inward[:, [0, 2]] - [115, 330], axis=1)
        self.assertLessEqual(
            radius.max(), 5.01, "No large drum on the ratchet axle"
        )
        initial = self.rope_centres(self.node.feed.winding.rope)
        self.assertGreater(
            initial[:, 1].min(), 49, "Keep the winding close to the gear"
        )
        self.assertLess(
            initial[:, 1].max(), 55, "Winding belongs inward of the ratchet"
        )
        self.node.set_keyframe(PASS_SECONDS)
        final = self.rope_centres(self.node.feed.winding.rope)
        self.assertLess(
            np.ptp(final[:, 1]), 0.001, "No axial traversing into the rocker"
        )
        self.assertAlmostEqual(
            final[:, 1].mean(), initial[:, 1].mean(), delta=0.001
        )
        r0 = np.linalg.norm(initial[:, [0, 2]] - [115, 330], axis=1)
        r1 = np.linalg.norm(final[:, [0, 2]] - [115, 330], axis=1)
        self.assertGreater(
            r1.max(), r0.max() + 10, "Rope builds over its previous turns"
        )
        self.assertLess(
            r1.max(), 42, "The coil remains below the ratchet tooth roots"
        )

    def test_drive_rope_clears_the_moving_feed_links(self):
        for seconds in np.linspace(0, PASS_SECONDS, 25):
            self.node.set_keyframe(float(seconds))
            for rope in (
                self.node.feed.winding.rope,
                self.node.feed.drive_line.rope,
            ):
                for link in (
                    self.node.feed.rocker,
                    self.node.feed.feed_tie,
                    self.node.feed.pawl,
                    self.node.feed.holding_pawl,
                ):
                    self.assertNotIntersecting(rope, link)

    def test_lower_pulley_is_inward_of_the_opposite_saw_upright(self):
        bounds = self.node.feed.drive_idler.mesh.bounds
        self.assertAlmostEqual(bounds[:, 0].mean(), 0, delta=0.01)
        self.assertGreater(bounds[0, 1], 25)
        self.assertLess(bounds[1, 1], 68)
        self.assertAlmostEqual(bounds[:, 2].mean(), 120, delta=0.01)
        shaft = self.node.feed.reduction_shaft.mesh.vertices
        working = shaft[
            np.linalg.norm(shaft[:, [0, 2]] - [-335, 285], axis=1) > 10
        ]
        self.assertGreater(working[:, 1].min(), -88)
        self.assertLess(
            working[:, 1].max(),
            104,
            "Compound winding sections stay within end legs",
        )

    def test_fixed_saw_tower_is_identifiable(self):
        self.assertTrue(hasattr(self.node.frame.timber_structure, "saw_tower"))
        self.assertFalse(
            self.node.frame.timber_structure.rigid,
            "Bed and fixed saw tower must not be one fused display solid",
        )

    def test_running_rails_are_continuous_at_the_saw_tower(self):
        bed = self.fixture_mesh(self.node.frame.timber_structure.bed)
        for y in (-42, 42):
            hits, _, _ = bed.ray.intersects_location(
                [[0, y, 350]], [[0, 0, -1]]
            )
            self.assertGreater(
                len(hits), 0, "No unsupported gap in a running rail"
            )
            self.assertAlmostEqual(hits[:, 2].max(), 345, delta=0.01)

    def test_timber_carriage_is_a_closed_rectangle(self):
        self.node.set_keyframe(0)
        bed = self.node.carriage.bed.mesh
        centre = bed.bounds[:, 0].mean()
        for x in (centre - 188, centre + 188):
            # Across both ends, except the small intentional rope tie
            # bore.
            points = [[x, y, 370] for y in (-28, -18, -8, 8, 18, 28)]
            self.assertTrue(
                bed.contains(points).all(),
                "Both end members must bridge and join the side timbers",
            )

    def test_rope_train_journals_are_supported_and_retained(self):
        wood = self.node.frame.timber_structure.bed
        tower = self.node.frame.timber_structure.saw_tower
        for seconds in (0, 1, 2, PASS_SECONDS):
            self.node.set_keyframe(seconds)
            for shaft, fixture in (
                (self.node.feed.feed_drum, wood),
                (self.node.feed.reduction_shaft, wood),
                (self.node.feed.idler_pin, tower),
            ):
                self.assertFixtureFree(shaft, 0.3, fixture, along=(1, 0, 0))
                self.assertFixtureBlocked(shaft, 1.3, fixture, along=(1, 0, 0))
            self.assertFixtureFree(
                self.node.feed.reduction_shaft, 2, wood, along=(0, 1, 0)
            )
            self.assertFixtureBlocked(
                self.node.feed.reduction_shaft, 3.2, wood, along=(0, 1, 0)
            )
            self.assertFixtureFree(
                self.node.feed.feed_drum, 0.2, wood, along=(0, 1, 0)
            )
            self.assertFixtureBlocked(
                self.node.feed.feed_drum, 1, wood, along=(0, 1, 0)
            )
            for direction in ((1, 0, 0), (0, 1, 0)):
                self.assertFreeWithin(
                    self.node.feed.drive_idler,
                    0.2,
                    self.node.feed.idler_pin,
                    along=direction,
                )
                self.assertBlockedBeyond(
                    self.node.feed.drive_idler,
                    1.3,
                    self.node.feed.idler_pin,
                    along=direction,
                )

    def test_round_shaft_is_seated_in_timber(self):
        self.assertTrue(
            hasattr(
                self.node.frame.timber_structure.saw_tower, "inner_bearing"
            )
        )
        probes = []
        for y in (-207, -32):
            probe = BearingJournalProbe()
            probe.assemble()
            probe.translate([0, y, 120])
            probe.build_stls()
            probes.append(probe)
        for phase in (0, 45, 90, 180, 270):
            self.node.set_keyframe(phase / 90)
            shaft = self.node.water_drive.crankshaft
            wood = self.node.frame.timber_structure.saw_tower
            self.assertFixtureFree(shaft, 0.3, wood, along=(1, 0, 0))
            self.assertFixtureBlocked(shaft, 1.3, wood, along=(1, 0, 0))
            self.assertFixtureBlocked(shaft, 1.3, wood, along=(0, 0, 1))
            for probe in probes:
                self.assertFixtureFree(probe, 0.3, wood, along=(1, 0, 0))
                self.assertFixtureBlocked(probe, 1.3, wood, along=(1, 0, 0))
                self.assertFixtureBlocked(probe, 1.3, wood, along=(0, 0, 1))

    def test_driving_hook_transmits_a_pull(self):
        pawl = self.node.feed.pawl
        local = trimesh.load_mesh(pawl.stl_file)
        bore = np.isclose(
            np.linalg.norm(local.vertices[:, [0, 2]], axis=1), 3.6, atol=0.0001
        )
        toe = np.isclose(local.vertices[:, 2], 75) & (
            local.vertices[:, 0] >= -1.01
        )
        face = np.isclose(local.triangles[:, :, 2], 75).all(axis=1) & (
            local.face_normals[:, 2] < -0.99
        )
        self.assertTrue(bore.any() and toe.any() and face.any())
        first = None
        for phase in (0, 45, 90, 135, 180):
            self.node.set_keyframe(phase / 90)
            mesh = pawl.mesh
            pivot = mesh.vertices[bore].mean(axis=0)
            tip = mesh.vertices[toe].mean(axis=0)
            # Reaction on the hook is opposite its material's outward
            # normal.
            reaction = -mesh.face_normals[face].mean(axis=0)
            shank = tip - pivot
            self.assertGreater(
                np.dot(reaction, shank) / np.linalg.norm(shank), 0.99
            )
            if first is None:
                first = (pivot, shank)
            else:
                self.assertLess(
                    np.dot(pivot - first[0], first[1]),
                    0,
                    "The rocker must retreat from the caught tooth, "
                    "pulling the hook",
                )

    def test_holding_tooth_reaction_seats_the_free_pawl(self):
        for phase in (0, 180, 270, 360, 26550):
            self.node.set_keyframe(phase / 90)
            pawl = self.node.feed.holding_pawl.mesh
            wheel = self.node.feed.feed_drum.mesh
            pivot = self.node.feed.holding_pin.mesh.bounds.mean(axis=0)
            pivot[1] = pawl.bounds[:, 1].mean()
            centre = wheel.bounds.mean(axis=0)
            centre[1] = pivot[1]
            # Innermost tip vertex is measured from the real pawl, not
            # its law.
            radii = np.linalg.norm((pawl.vertices - centre)[:, [0, 2]], axis=1)
            tip = pawl.vertices[np.argmin(radii)].copy()
            tip[1] = pivot[1]
            # Find first locking contact within the existing 5-degree
            # limit,
            # not an assumed 2.5-degree pose which can already penetrate
            # it.
            # This independently measures the real wheel and pawl
            # surfaces.
            for rollback_angle in np.arange(0, 5.001, 0.025):
                moved = wheel.copy()
                moved.apply_transform(
                    trimesh.transformations.rotation_matrix(
                        math.radians(-rollback_angle), (0, 1, 0), centre
                    )
                )
                closest, distance, triangles = trimesh.proximity.closest_point(
                    moved, [tip]
                )
                if distance[0] < 0.025:
                    break
            self.assertLess(
                distance[0],
                0.025,
                "No locking contact within the allowed play",
            )
            normal = moved.face_normals[triangles[0]]
            rollback = np.cross((0, -1, 0), closest[0] - centre)
            self.assertGreater(np.dot(normal, rollback), 0)
            reaction_moment = np.cross(tip - pivot, normal)[1]
            radial_motion = np.dot(
                np.cross((0, 1, 0), tip - pivot), tip - centre
            )
            self.assertLess(
                reaction_moment * radial_motion,
                0,
                "Rollback must seat the hinged pawl, not lift it out",
            )

    def test_holding_pawl_stays_seated_through_every_recovery(self):
        from .kinematics import holding_angle, ratchet_angle

        # A stationary ratchet cannot lift its seated holding pawl.
        # Sample
        # every tooth boundary: floating-point wrap errors vary by turn.
        for turn in range(PASS_TURNS):
            angles = [
                holding_angle(ratchet_angle(turn * 360 + phase))
                for phase in range(180, 360, 3)
            ]
            self.assertLess(
                np.ptp(angles),
                0.000001,
                f"Holding pawl chatters during recovery {turn}",
            )
        for turn in (0, 16, 64, 182, PASS_TURNS - 1):
            first = None
            for phase in range(180, 360, 3):
                self.node.set_keyframe((turn * 360 + phase) / 90)
                vertices = self.node.feed.holding_pawl.mesh.vertices.copy()
                if first is None:
                    first = vertices
                np.testing.assert_allclose(
                    vertices,
                    first,
                    atol=0.000001,
                    err_msg="The actual seated pawl must not oscillate",
                )

    def test_complete_timber_course(self):
        self.node.set_keyframe(0)
        blade = self.node.saw.sash.blade.mesh.bounds
        timber = self.node.carriage.timber.log_left.mesh.bounds
        self.assertGreater(timber[0, 0], blade[1, 0] + 0.2)
        self.assertLess(timber[0, 0] - blade[1, 0], 2)
        self.node.set_keyframe(PASS_SECONDS)
        timber = self.node.carriage.timber.log_left.mesh.bounds
        self.assertLess(timber[1, 0], blade[0, 0] - 2)
        self.assertLess(blade[0, 0] - timber[1, 0], 6)

    def test_timeline_is_the_only_control(self):
        from machinome.simulation import (
            qualified_drivers,
            qualified_instructions,
        )
        from machinome.motion.ports import declared_time

        self.assertFalse(qualified_drivers(self.node))
        self.assertFalse(qualified_instructions(self.node))
        self.assertEqual(
            declared_time(type(self.node)).loop, PASS_TURNS * TURN_SECONDS
        )
        self.assertGreater(declared_time(type(self.node)).loop, 800)

    def test_uncut_kerf_insert_recedes_at_the_teeth(self):
        for seconds in (
            0,
            8,
            64,
            PASS_SECONDS / 2,
            PASS_SECONDS - 16,
            PASS_SECONDS - 4,
            PASS_SECONDS,
        ):
            self.node.set_keyframe(seconds)
            filler = self.node.carriage.timber.uncut
            mesh = filler.mesh
            timber = self.node.carriage.timber.log_left.mesh.bounds
            expected = max(0, min(320, timber[1, 0] - 10.2))
            self.assertTrue(np.isfinite(mesh.vertices).all())
            self.assertAlmostEqual(mesh.extents[0], expected, delta=0.001)
            if expected > 0.1:
                self.assertAlmostEqual(
                    mesh.volume, expected * 56 * self.node.kerf, delta=0.01
                )
                self.assertAlmostEqual(
                    mesh.bounds[1, 0], timber[1, 0], delta=0.001
                )
                for rigid in (
                    self.node.saw.sash.blade,
                    self.node.carriage.bed,
                    self.node.carriage.timber.log_left,
                    self.node.carriage.timber.log_right,
                ):
                    self.assertNotIntersecting(filler, rigid)
            elif expected == 0:
                self.assertEqual(mesh.volume, 0)
                self.assertEqual(mesh.area, 0)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_historical_feed_linkage_has_captured_joints(self):
        self.node.set_keyframe((270) / 90)
        self.assertFreeWithin(
            self.node.feed.feed_tie,
            0.2,
            self.node.saw.sash.pin,
            along=(1, 0, 0),
        )
        self.assertBlockedBeyond(
            self.node.feed.feed_tie,
            1.5,
            self.node.saw.sash.pin,
            along=(1, 0, 0),
        )

    def test_end_pulley_and_holding_pawl_are_present_and_engaged(self):
        self.node.set_keyframe((0) / 90)
        self.assertGreater(self.node.feed.upper_roller.mesh.volume, 0)
        self.assertGreater(self.node.feed.reduction_shaft.mesh.volume, 0)
        self.assertBlockedBeyond(
            self.node.feed.feed_drum,
            5,
            self.node.feed.holding_pawl,
            axis=(0, 1, 0),
            directions="forward",
        )

    def test_blade_is_mechanically_attached(self):
        for clamp in (
            self.node.saw.sash.clamps.lower,
            self.node.saw.sash.clamps.upper,
        ):
            self.assertFreeWithin(
                self.node.saw.sash.blade, 0.2, clamp, along=(0, 0, 1)
            )
            self.assertBlockedBeyond(
                self.node.saw.sash.blade, 2, clamp, along=(0, 0, 1)
            )

    @testing_steps(149, end=PASS_SECONDS)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_saw_has_full_stroke(self):
        self.node.set_keyframe((0) / 90)
        upper = self.node.saw.sash.frame.mesh.bounds[:, 2].mean()
        self.node.set_keyframe((180) / 90)
        lower = self.node.saw.sash.frame.mesh.bounds[:, 2].mean()
        self.assertAlmostEqual(upper - lower, 48.0, delta=0.01)

    @testing_steps(13, end=4)
    def test_blade_clears_both_log_halves(self):
        self.assertNotIntersecting(
            self.node.saw.sash.blade, self.node.carriage.timber.log_left
        )
        self.assertNotIntersecting(
            self.node.saw.sash.blade, self.node.carriage.timber.log_right
        )

    def test_feed_pulls_down_then_holds_on_recovery(self):
        positions = []
        for phase in (0, 90, 180, 270, 360):
            self.node.set_keyframe((phase) / 90)
            positions.append(self.node.carriage.bed.mesh.bounds[:, 0].mean())
        self.assertLess(positions[1], positions[0])
        self.assertAlmostEqual(positions[2], positions[4], delta=0.01)
        self.assertGreater(positions[0] - positions[4], 0.32)
        self.assertLess(positions[0] - positions[4], 0.34)

    def test_linkage_closure_and_pawl_journals_through_cycle(self):
        for phase in range(0, 361, 15):
            self.node.set_keyframe((phase) / 90)
            for moving, pin in (
                (self.node.feed.feed_tie, self.node.saw.sash.pin),
                (self.node.feed.feed_tie, self.node.feed.rocker),
                (self.node.feed.rocker, self.node.feed.rocker_pin),
                (self.node.feed.pawl, self.node.feed.rocker),
                (self.node.feed.holding_pawl, self.node.feed.holding_pin),
            ):
                self.assertFreeWithin(moving, 0.2, pin, along=(1, 0, 0))
                self.assertBlockedBeyond(moving, 1.5, pin, along=(1, 0, 0))

    def test_tooth_transitions_and_pass_endpoints(self):
        for phase in sorted(
            set(
                list(range(0, 361, 2))
                + [0.01, 179.99, 180.01, 359.99, 360.01, 1439.99, 1440]
            )
        ):
            self.node.set_keyframe((phase) / 90)
            self.assertNoSolidInterference(self.node)
        for seconds in (
            0,
            0.001,
            PASS_SECONDS / 2,
            PASS_SECONDS - 0.001,
            PASS_SECONDS,
        ):
            self.node.set_keyframe(seconds)
            self.assertNoSolidInterference(self.node)
            advance = 171 - self.node.carriage.bed.mesh.bounds[:, 0].mean()
            self.assertGreaterEqual(advance, -0.01)
            self.assertLessEqual(advance, 342)

    def test_undershot_water_channel_and_wheel_direction(self):
        self.node.set_keyframe((0) / 90)
        water = self.node.water_drive.water.mesh.vertices
        below = water[np.abs(water[:, 0]) < 100]
        self.assertGreater(len(below), 0)
        self.assertLess(below[:, 2].max(), 28)
        self.assertLess(water[:, 2].max(), 120)
        self.assertLess(self.node.water_drive.channel.mesh.bounds[1, 2], 150)
        self.assertAlmostEqual(
            self.fixture_mesh(
                self.node.frame.timber_structure.saw_tower
            ).bounds[1, 2],
            645,
            delta=0.01,
        )
        first = self.node.water_drive.waterwheel.mesh.vertices.copy()
        low = int(np.argmin(first[:, 2]))
        self.node.set_keyframe((1) / 90)
        self.assertLess(
            self.node.water_drive.waterwheel.mesh.vertices[low, 0],
            first[low, 0],
        )

    def rope_centres(self, node):
        return (
            np.asarray(node.mesh.vertices)[:-2].reshape(-1, 12, 3).mean(axis=1)
        )

    def test_continuous_rope_length_winding_and_attachment(self):
        initial = None
        for seconds in (
            0,
            1,
            2,
            2.3,
            3,
            4,
            16,
            PASS_SECONDS / 4,
            PASS_SECONDS / 2,
            3 * PASS_SECONDS / 4,
            PASS_SECONDS - 4,
            PASS_SECONDS - 0.001,
            PASS_SECONDS,
        ):
            self.node.set_keyframe(seconds)
            free = self.node.feed.haul.rope
            lower = self.node.feed.haul_span
            drive = self.node.feed.drive_line.rope
            windings = (
                self.node.feed.winding.rope,
                self.node.feed.reserve.rope,
                self.node.feed.takeup.rope,
            )
            points = self.rope_centres(free)
            span = self.rope_centres(lower)
            driven = self.rope_centres(drive)
            coils = [self.rope_centres(w) for w in windings]
            self.assertEqual(points.shape, (145, 3))
            self.assertEqual(span.shape, (2, 3))
            self.assertEqual(driven.shape, (109, 3))
            np.testing.assert_allclose(points[-1], span[0], atol=0.001)
            np.testing.assert_allclose(span[-1], coils[2][0], atol=0.001)
            np.testing.assert_allclose(driven[0], coils[0][-1], atol=0.001)
            np.testing.assert_allclose(driven[-1], coils[1][0], atol=0.001)
            advance = 171 - self.node.carriage.bed.mesh.bounds[:, 0].mean()
            np.testing.assert_allclose(
                points[0], [-23 - advance, 0, 370], atol=0.001
            )
            # Independent Archimedean-spiral length from measured radii,
            # not the quadrature or the winding coordinate driving the
            # CAD.
            spiral = coils[0]
            self.assertEqual(spiral.shape, (2049, 3))
            radial = spiral[:, [0, 2]] - [115, 330]
            radii = np.linalg.norm(radial, axis=1)
            angles = np.unwrap(np.arctan2(radial[:, 0], radial[:, 1]))
            lead = 1.82 / (2 * math.pi)
            np.testing.assert_allclose(
                radii, 6.2 + lead * np.abs(angles - angles[0]), atol=0.002
            )
            np.testing.assert_allclose(spiral[:, 1], 52, atol=0.001)

            def primitive(r):
                return (
                    r * math.hypot(r, lead)
                    + lead * lead * math.asinh(r / lead)
                ) / (2 * lead)

            lengths = [primitive(radii[-1]) - primitive(radii[0])]
            distance = trimesh.proximity.closest_point(
                self.node.feed.gear_tie.mesh, [spiral[0]]
            )[1][0]
            self.assertLess(distance, 0.001)
            # The rope departs along the growing spiral's tangent, not
            # the
            # tangent of a fictitious fixed-radius input pulley.
            a = angles[-1]
            tangent = np.array(
                [
                    lead * math.sin(a) - radii[-1] * math.cos(a),
                    lead * math.cos(a) + radii[-1] * math.sin(a),
                ]
            )
            direction = (driven[6] - driven[0])[[0, 2]]
            self.assertGreater(
                np.dot(tangent, direction)
                / np.linalg.norm(tangent)
                / np.linalg.norm(direction),
                0.999999,
            )
            for coil, r, centre, pitch, tie in zip(
                coils[1:],
                (26.4, 7.2),
                ((-335, 285), (-335, 285)),
                (3.2, 3.2),
                (self.node.feed.input_tie, self.node.feed.haul_tie),
            ):
                self.assertEqual(coil.shape, (721, 3))
                radial = coil[:, [0, 2]] - centre
                np.testing.assert_allclose(
                    np.linalg.norm(radial, axis=1), r, atol=0.001
                )
                angles = np.unwrap(np.arctan2(radial[:, 0], radial[:, 1]))
                wrap = abs(angles[-1] - angles[0])
                dy = abs(coil[-1, 1] - coil[0, 1])
                self.assertAlmostEqual(
                    dy, pitch * wrap / (2 * math.pi), delta=0.001
                )
                self.assertGreater(pitch, 1.8)
                lengths.append(math.hypot(r * wrap, dy))
                distance = trimesh.proximity.closest_point(
                    tie.mesh, [coil[-1]]
                )[1][0]
                self.assertLess(
                    distance,
                    0.001,
                    "The rope must end on its rotating through-bore tie",
                )
            upper_radial = points[72:, [0, 2]] - [-370, 340]
            np.testing.assert_allclose(
                np.linalg.norm(upper_radial, axis=1), 7.4, atol=0.001
            )
            upper_angles = np.unwrap(
                np.arctan2(upper_radial[:, 0], upper_radial[:, 1])
            )
            upper_arc = 7.4 * abs(upper_angles[-1] - upper_angles[0])
            idler_radial = driven[6:103, [0, 2]] - [0, 120]
            np.testing.assert_allclose(
                np.linalg.norm(idler_radial, axis=1), 11.4, atol=0.001
            )
            idler_angles = np.unwrap(
                np.arctan2(idler_radial[:, 0], idler_radial[:, 1])
            )
            idler_arc = 11.4 * abs(idler_angles[-1] - idler_angles[0])
            self.assertAlmostEqual(
                np.linalg.norm(np.diff(driven[6:103], axis=0), axis=1).sum(),
                idler_arc,
                delta=0.001,
            )
            total = np.array(
                [
                    lengths[0]
                    + np.linalg.norm(driven[6] - driven[0])
                    + idler_arc
                    + np.linalg.norm(driven[-1] - driven[102])
                    + lengths[1],
                    np.linalg.norm(points[72] - points[0])
                    + upper_arc
                    + np.linalg.norm(span[1] - span[0])
                    + lengths[2],
                ]
            )
            if initial is None:
                initial = total
            np.testing.assert_allclose(total, initial, atol=0.001)
            for rope in (free, lower, drive, *windings):
                for rigid in (
                    *self.fixture_parts(self.node.frame.timber_structure),
                    self.node.feed.upper_roller,
                    self.node.feed.feed_drum,
                    self.node.feed.reduction_shaft,
                    self.node.feed.drive_idler,
                    self.node.carriage.bed,
                    self.node.saw.sash.frame,
                    self.node.saw.sash.blade,
                ):
                    self.assertNotIntersecting(rope, rigid)
            for tie, rigid in (
                (self.node.feed.gear_tie, self.node.feed.feed_drum),
                (self.node.feed.input_tie, self.node.feed.reduction_shaft),
                (self.node.feed.haul_tie, self.node.feed.reduction_shaft),
                (self.node.carriage.anchor, self.node.carriage.bed),
            ):
                self.assertFreeWithin(tie, 0.15, rigid, along=(0, 1, 0))
                self.assertBlockedBeyond(tie, 0.8, rigid, along=(0, 1, 0))

    def test_wheel_and_carriage_retention(self):
        self.node.set_keyframe((0) / 90)
        self.assertFreeWithin(
            self.node.water_drive.waterwheel,
            0.3,
            self.node.water_drive.crankshaft,
            along=(0, 1, 0),
        )
        self.assertBlockedBeyond(
            self.node.water_drive.waterwheel,
            2,
            self.node.water_drive.crankshaft,
            along=(0, 1, 0),
        )
        for wheel in (
            *self.node.carriage.running_gear.outer_wheels,
            *self.node.carriage.running_gear.inner_wheels,
        ):
            self.assertFixtureFree(
                wheel,
                0.2,
                self.node.frame.timber_structure.bed,
                along=(0, 1, 0),
            )
        self.assertFreeWithin(
            self.node.feed.upper_roller,
            0.2,
            self.node.feed.upper_pin,
            along=(1, 0, 0),
        )
        self.assertBlockedBeyond(
            self.node.feed.upper_roller,
            1.2,
            self.node.feed.upper_pin,
            along=(1, 0, 0),
        )

    def test_reposing_is_reproducible(self):
        self.node.set_keyframe((73) / 90)
        first = self.node.saw.sash.frame.mesh.bounds.copy()
        self.node.set_keyframe((1100) / 90)
        self.node.set_keyframe((73) / 90)
        np.testing.assert_allclose(
            self.node.saw.sash.frame.mesh.bounds, first, atol=1e-6
        )

    @testing_steps(9, end=4)
    def test_crank_pin_captures_rod(self):
        self.assertFreeWithin(
            self.node.saw.connecting_rod,
            0.3,
            self.node.water_drive.crank,
            along=(1, 0, 0),
        )
        self.assertBlockedBeyond(
            self.node.saw.connecting_rod,
            1.5,
            self.node.water_drive.crank,
            along=(1, 0, 0),
        )

    @testing_steps(9, end=4)
    def test_sash_stays_in_guide_slots(self):
        self.assertFixtureFree(
            self.node.saw.sash.frame,
            0.3,
            self.node.frame.timber_structure.saw_tower,
            along=(1, 0, 0),
        )
        self.assertFixtureBlocked(
            self.node.saw.sash.frame,
            1.3,
            self.node.frame.timber_structure.saw_tower,
            along=(1, 0, 0),
        )

    def test_waterwheel_is_keyed_to_shaft(self):
        self.assertFreeWithin(
            self.node.water_drive.waterwheel,
            1,
            self.node.water_drive.crankshaft,
            axis=(0, 1, 0),
        )
        self.assertBlockedBeyond(
            self.node.water_drive.waterwheel,
            10,
            self.node.water_drive.crankshaft,
            axis=(0, 1, 0),
        )

    def test_seated_pawl_engages_ratchet(self):
        for phase in (0, 30, 60, 90, 120, 150, 180, 360, 720, 1080, 1440):
            self.node.set_keyframe((phase) / 90)
            self.assertFreeWithin(
                self.node.feed.feed_drum,
                0.3,
                self.node.feed.pawl,
                axis=(0, 1, 0),
            )
            self.assertBlockedBeyond(
                self.node.feed.feed_drum,
                5,
                self.node.feed.pawl,
                axis=(0, 1, 0),
                directions="forward",
            )

    def test_tree_groups_are_useful(self):
        self.assertEqual(
            [child.name for child in self.node.children],
            [
                "Frame and guides",
                "Water drive",
                "Saw mechanism",
                "Timber carriage",
                "Feed mechanism",
            ],
        )
        self.assertEqual(
            [child.name for child in self.node.carriage.children],
            [
                "Bed and slotted log cradles",
                "Carriage rope knot",
                "Timber",
                "Rollers and axles",
            ],
        )

    def test_timber_fit_and_support_through_pass(self):
        for seconds in np.linspace(0, PASS_SECONDS, 10):
            self.node.set_keyframe(float(seconds))
            for timber in (
                self.node.carriage.timber.log_left,
                self.node.carriage.timber.log_right,
            ):
                bounds = timber.mesh.bounds
                self.assertAlmostEqual(
                    bounds[1, 0] - bounds[0, 0], 320, delta=0.01
                )
                self.assertFreeWithin(
                    timber, 0.1, self.node.carriage.bed, along=(0, 0, -1)
                )
                self.assertBlockedBeyond(
                    timber,
                    2,
                    self.node.carriage.bed,
                    along=(0, 0, -1),
                    directions="forward",
                )
            for wheel in (
                *self.node.carriage.running_gear.outer_wheels,
                *self.node.carriage.running_gear.inner_wheels,
            ):
                self.assertGreater(wheel.mesh.bounds[0, 0], -380)
                self.assertLess(wheel.mesh.bounds[1, 0], 380)
                travel = 171 - self.node.carriage.bed.mesh.bounds[:, 0].mean()
                theta = travel / 12
                self.assertFixtureBlocked(
                    wheel,
                    0.5,
                    self.node.frame.timber_structure.bed,
                    along=(math.sin(theta), 0, -math.cos(theta)),
                    directions="forward",
                )
            self.assertNotIntersecting(
                self.node.saw.sash.blade, self.node.carriage.bed
            )
