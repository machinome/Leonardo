# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import numpy as np

from machinome.test import TestCase, testing_steps
from .model import LeonardoHydraulicSawmill


class LeonardoHydraulicSawmillTest(TestCase):
    node = LeonardoHydraulicSawmill

    def test_complete_timber_course(self):
        self.node.set_keyframe(0)
        blade = self.node.saw.sash.blade.mesh.bounds
        timber = self.node.carriage.timber.log_left.mesh.bounds
        self.assertLess(timber[1, 0], blade[0, 0] - 0.2)
        self.assertLess(blade[0, 0]-timber[1, 0],2)
        self.node.set_keyframe(296)
        timber = self.node.carriage.timber.log_left.mesh.bounds
        self.assertGreater(timber[0, 0], blade[1, 0] + 2)
        self.assertLess(timber[0, 0]-blade[1, 0],5)

    def test_timeline_is_the_only_control(self):
        from machinome.simulation import qualified_drivers, qualified_instructions
        from machinome.motion.ports import declared_time
        self.assertFalse(qualified_drivers(self.node))
        self.assertFalse(qualified_instructions(self.node))
        self.assertEqual(declared_time(type(self.node)).loop, 296)

    def test_uncut_kerf_insert_recedes_at_the_teeth(self):
        for seconds in (0, 8, 64, 148, 240, 280, 296):
            self.node.set_keyframe(seconds)
            filler=self.node.carriage.timber.uncut
            mesh=filler.mesh
            timber=self.node.carriage.timber.log_left.mesh.bounds
            expected=max(0,min(320,-10.2-timber[0,0]))
            self.assertTrue(np.isfinite(mesh.vertices).all())
            self.assertAlmostEqual(mesh.extents[0],expected,delta=0.001)
            if expected > 0.1:
                self.assertAlmostEqual(mesh.volume,expected*56*self.node.kerf,delta=0.01)
                self.assertAlmostEqual(mesh.bounds[0,0],timber[0,0],delta=0.001)
                for rigid in (self.node.saw.sash.blade,self.node.carriage.bed,
                              self.node.carriage.timber.log_left,self.node.carriage.timber.log_right):
                    self.assertNotIntersecting(filler,rigid)
            elif expected == 0:
                self.assertEqual(mesh.volume,0)
                self.assertEqual(mesh.area,0)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_historical_feed_linkage_has_captured_joints(self):
        self.node.set_keyframe((270) / 90)
        self.assertFreeWithin(self.node.feed.feed_tie, 0.2, self.node.saw.sash.pin, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.feed.feed_tie, 1.5, self.node.saw.sash.pin, along=(1, 0, 0))

    def test_end_pulley_and_holding_pawl_are_present_and_engaged(self):
        self.node.set_keyframe((0) / 90)
        self.assertGreater(self.node.feed.return_pulley.mesh.volume, 0)
        self.assertBlockedBeyond(self.node.feed.feed_drum, 5, self.node.feed.holding_pawl,
                                axis=(0, -1, 0), directions='forward')

    def test_blade_is_mechanically_attached(self):
        for clamp in (self.node.saw.sash.clamps.lower,self.node.saw.sash.clamps.upper):
            self.assertFreeWithin(self.node.saw.sash.blade, 0.2, clamp, along=(0,0,1))
            self.assertBlockedBeyond(self.node.saw.sash.blade, 2, clamp, along=(0,0,1))

    @testing_steps(149, end=296)
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
        self.assertNotIntersecting(self.node.saw.sash.blade, self.node.carriage.timber.log_left)
        self.assertNotIntersecting(self.node.saw.sash.blade, self.node.carriage.timber.log_right)

    def test_feed_dwells_then_advances(self):
        positions = []
        for phase in (0, 90, 180, 270, 360):
            self.node.set_keyframe((phase) / 90)
            positions.append(self.node.carriage.bed.mesh.bounds[:, 0].mean())
        self.assertAlmostEqual(positions[0], positions[2], delta=0.01)
        self.assertGreater(positions[3], positions[2])
        self.assertAlmostEqual(positions[4]-positions[0], 2*math.pi*23.4/32, delta=0.01)

    def test_linkage_closure_and_pawl_journals_through_cycle(self):
        for phase in range(0,361,15):
            self.node.set_keyframe((phase) / 90)
            for moving,pin in ((self.node.feed.feed_tie,self.node.saw.sash.pin),
                               (self.node.feed.feed_tie,self.node.feed.rocker),
                               (self.node.feed.rocker,self.node.feed.rocker_pin),
                               (self.node.feed.pawl,self.node.feed.rocker),
                               (self.node.feed.holding_pawl,self.node.feed.holding_pin)):
                self.assertFreeWithin(moving,0.2,pin,along=(1,0,0))
                self.assertBlockedBeyond(moving,1.5,pin,along=(1,0,0))

    def test_tooth_transitions_and_pass_endpoints(self):
        for phase in sorted(set(list(range(0,361,2))+[0.01,179.99,180.01,359.99,360.01,1439.99,1440])):
            self.node.set_keyframe((phase) / 90)
            self.assertNoSolidInterference(self.node)
        for seconds in (0, 0.001, 148, 295.999, 296):
            self.node.set_keyframe(seconds)
            self.assertNoSolidInterference(self.node)
            advance=self.node.carriage.bed.mesh.bounds[:,0].mean()-(-170.5)
            self.assertGreaterEqual(advance,-0.01)
            self.assertLessEqual(advance,340.2)

    def test_undershot_water_channel_and_wheel_direction(self):
        self.node.set_keyframe((0) / 90)
        water=self.node.water_drive.water.mesh.vertices
        below=water[np.abs(water[:,0])<100]
        self.assertGreater(len(below),0)
        self.assertLess(below[:,2].max(),28)
        self.assertLess(water[:,2].max(),120)
        self.assertLess(self.node.water_drive.channel.mesh.bounds[1,2],150)
        self.assertAlmostEqual(self.node.frame.timber_structure.mesh.bounds[1,2],645,delta=0.01)
        first=self.node.water_drive.waterwheel.mesh.vertices.copy()
        low=int(np.argmin(first[:,2]))
        self.node.set_keyframe((1) / 90)
        self.assertLess(self.node.water_drive.waterwheel.mesh.vertices[low,0],first[low,0])

    def rope_centres(self, node):
        return np.asarray(node.mesh.vertices)[:-2].reshape(-1,12,3).mean(axis=1)

    def test_continuous_rope_length_winding_and_attachment(self):
        initial=None
        for seconds in (0,1,2,2.3,3,4,16,64,128,192,256,295.999,296):
            self.node.set_keyframe(seconds)
            free=self.node.feed.rope
            wound=self.node.feed.winding.rope
            lower=self.node.feed.return_span
            points=self.rope_centres(free)
            span=self.rope_centres(lower)
            coil=self.rope_centres(wound)
            self.assertEqual(points.shape,(145,3))
            self.assertEqual(span.shape,(2,3))
            self.assertEqual(coil.shape,(241,3))
            ends=np.vstack([points[::72],span[-1]])
            np.testing.assert_allclose(points[-1],span[0],atol=0.001)
            advance=self.node.carriage.bed.mesh.bounds[:,0].mean()+170.5
            np.testing.assert_allclose(ends[0],[33+advance,98,353.4],atol=0.001)
            np.testing.assert_allclose(ends[1:3],[[400,98,353.4],[400,98,306.6]],atol=0.001)
            np.testing.assert_allclose(ends[3],coil[0],atol=0.001)
            radial=coil[:,[0,2]]-[-115,330]
            np.testing.assert_allclose(np.linalg.norm(radial,axis=1),23.4,atol=0.001)
            angle=np.unwrap(np.arctan2(-radial[:,0],-radial[:,1]))
            wrap=angle[-1]-angle[0]
            self.assertAlmostEqual(coil[-1,1],93,delta=0.001)
            self.assertAlmostEqual(coil[0,1]-coil[-1,1],3.2*wrap/(2*math.pi),delta=0.001)
            # Every whole turn separates adjacent windings by 3.2 mm,
            # greater than the 1.8 mm rope diameter.
            self.assertLessEqual(wrap,math.radians(847.5)+0.001)
            total=(np.linalg.norm(ends[1]-ends[0])+math.pi*23.4+
                   np.linalg.norm(ends[3]-ends[2])+
                   math.hypot(23.4*wrap,coil[-1,1]-coil[0,1]))
            if initial is None:
                initial=total
            self.assertAlmostEqual(total,initial,delta=0.001)
            for rope in (free,lower,wound):
                for rigid in (self.node.frame.timber_structure,self.node.feed.return_pulley,
                              self.node.feed.feed_drum,self.node.carriage.bed,self.node.saw.sash.frame):
                    self.assertNotIntersecting(rope,rigid)
            self.assertFreeWithin(free,0.15,self.node.carriage.bed,along=(0,1,0))
            self.assertBlockedBeyond(free,0.8,self.node.carriage.bed,along=(0,1,0))
            self.assertFreeWithin(wound,0.15,self.node.feed.feed_drum,along=(0,0,1))
            self.assertBlockedBeyond(wound,0.8,self.node.feed.feed_drum,along=(0,0,1))

    def test_wheel_and_carriage_retention(self):
        self.node.set_keyframe((0) / 90)
        self.assertFreeWithin(self.node.water_drive.waterwheel,0.3,self.node.water_drive.crankshaft,along=(0,1,0))
        self.assertBlockedBeyond(self.node.water_drive.waterwheel,2,self.node.water_drive.crankshaft,along=(0,1,0))
        for wheel in (*self.node.carriage.running_gear.outer_wheels,*self.node.carriage.running_gear.inner_wheels):
            self.assertFreeWithin(wheel,0.2,self.node.frame.timber_structure,along=(0,1,0))
        self.assertFreeWithin(self.node.feed.return_pulley,0.2,self.node.feed.pulley_pin,along=(1,0,0))
        self.assertBlockedBeyond(self.node.feed.return_pulley,1.2,self.node.feed.pulley_pin,along=(1,0,0))

    def test_reposing_is_reproducible(self):
        self.node.set_keyframe((73) / 90)
        first = self.node.saw.sash.frame.mesh.bounds.copy()
        self.node.set_keyframe((1100) / 90)
        self.node.set_keyframe((73) / 90)
        np.testing.assert_allclose(self.node.saw.sash.frame.mesh.bounds, first, atol=1e-6)

    @testing_steps(9, end=4)
    def test_crank_pin_captures_rod(self):
        self.assertFreeWithin(self.node.saw.connecting_rod, 0.3, self.node.water_drive.crankshaft, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.saw.connecting_rod, 1.5, self.node.water_drive.crankshaft, along=(1, 0, 0))

    @testing_steps(9, end=4)
    def test_sash_stays_in_guide_slots(self):
        self.assertFreeWithin(self.node.saw.sash.frame, 0.3, self.node.frame.timber_structure, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.saw.sash.frame, 1.3, self.node.frame.timber_structure, along=(1, 0, 0))

    def test_waterwheel_is_keyed_to_shaft(self):
        self.assertFreeWithin(self.node.water_drive.waterwheel, 1, self.node.water_drive.crankshaft, axis=(0, 1, 0))
        self.assertBlockedBeyond(self.node.water_drive.waterwheel, 10, self.node.water_drive.crankshaft, axis=(0, 1, 0))

    def test_seated_pawl_engages_ratchet(self):
        for phase in (0,180,210,240,270,300,330,360,720,1080,1440):
            self.node.set_keyframe((phase) / 90)
            self.assertFreeWithin(self.node.feed.feed_drum, 0.3, self.node.feed.pawl, axis=(0, 1, 0))
            self.assertBlockedBeyond(self.node.feed.feed_drum, 5, self.node.feed.pawl, axis=(0, -1, 0), directions='forward')

    def test_tree_groups_are_useful(self):
        self.assertEqual([child.name for child in self.node.children],
                         ['Frame and guides', 'Water drive', 'Saw mechanism',
                          'Timber carriage', 'Feed mechanism'])
        self.assertEqual([child.name for child in self.node.carriage.children],
                         ['Bed and slotted log cradles', 'Timber', 'Rollers and axles'])

    def test_timber_fit_and_support_through_pass(self):
        for seconds in (0, 32, 64, 96, 128, 160, 192, 224, 256, 296):
            self.node.set_keyframe(seconds)
            for timber in (self.node.carriage.timber.log_left,
                           self.node.carriage.timber.log_right):
                bounds=timber.mesh.bounds
                self.assertAlmostEqual(bounds[1,0]-bounds[0,0],320,delta=0.01)
                self.assertFreeWithin(timber,0.1,self.node.carriage.bed,along=(0,0,-1))
                self.assertBlockedBeyond(timber,2,self.node.carriage.bed,
                                        along=(0,0,-1),directions='forward')
            for wheel in (*self.node.carriage.running_gear.outer_wheels,
                          *self.node.carriage.running_gear.inner_wheels):
                self.assertGreater(wheel.mesh.bounds[0,0],-380)
                self.assertLess(wheel.mesh.bounds[1,0],380)
                travel=self.node.carriage.bed.mesh.bounds[:,0].mean()+170.5
                theta=travel/12
                self.assertBlockedBeyond(wheel,0.5,self.node.frame.timber_structure,
                                         along=(math.sin(theta),0,-math.cos(theta)),
                                         directions='forward')
            self.assertNotIntersecting(self.node.saw.sash.blade,self.node.carriage.bed)
