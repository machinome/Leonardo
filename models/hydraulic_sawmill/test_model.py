# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import math
import numpy as np

from machinome.test import TestCase, testing_steps
from machinome.simulation import ScenarioTest
from .model import LeonardoHydraulicSawmill


class LeonardoHydraulicSawmillTest(TestCase):
    node = LeonardoHydraulicSawmill

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_historical_feed_linkage_has_captured_joints(self):
        self.node.set_state(time=0, phase=270, playback=0)
        self.assertFreeWithin(self.node.feed_tie, 0.2, self.node.sash.pin, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.feed_tie, 1.5, self.node.sash.pin, along=(1, 0, 0))

    def test_end_pulley_and_holding_pawl_are_present_and_engaged(self):
        self.node.set_state(time=0,phase=0,playback=0)
        self.assertGreater(self.node.return_pulley.mesh.volume, 0)
        self.assertBlockedBeyond(self.node.feed_drum, 5, self.node.holding_pawl,
                                axis=(0, -1, 0), directions='forward')

    def test_blade_is_mechanically_attached(self):
        for clamp in (self.node.sash.clamps.lower,self.node.sash.clamps.upper):
            self.assertFreeWithin(self.node.sash.blade, 0.2, clamp, along=(0,0,1))
            self.assertBlockedBeyond(self.node.sash.blade, 2, clamp, along=(0,0,1))

    @testing_steps(33)
    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def test_saw_has_full_stroke(self):
        self.node.set_state(time=0, phase=0, playback=0)
        upper = self.node.sash.frame.mesh.bounds[:, 2].mean()
        self.node.set_state(phase=180)
        lower = self.node.sash.frame.mesh.bounds[:, 2].mean()
        self.assertAlmostEqual(upper - lower, 48.0, delta=0.01)

    @testing_steps(13, end=0.25)
    def test_blade_clears_both_log_halves(self):
        self.assertNotIntersecting(self.node.sash.blade, self.node.carriage.log_left)
        self.assertNotIntersecting(self.node.sash.blade, self.node.carriage.log_right)

    def test_feed_dwells_then_advances(self):
        positions = []
        for phase in (0, 90, 180, 270, 360):
            self.node.set_state(time=0, phase=phase, playback=0)
            positions.append(self.node.carriage.bed.mesh.bounds[:, 0].mean())
        self.assertAlmostEqual(positions[0], positions[2], delta=0.01)
        self.assertGreater(positions[3], positions[2])
        self.assertAlmostEqual(positions[4]-positions[0], 2*math.pi*23.4/32, delta=0.01)

    def test_linkage_closure_and_pawl_journals_through_cycle(self):
        for phase in range(0,361,15):
            self.node.set_state(phase=phase,time=0,playback=0)
            for moving,pin in ((self.node.feed_tie,self.node.sash.pin),
                               (self.node.feed_tie,self.node.rocker),
                               (self.node.rocker,self.node.rocker_pin),
                               (self.node.pawl,self.node.rocker),
                               (self.node.holding_pawl,self.node.holding_pin)):
                self.assertFreeWithin(moving,0.2,pin,along=(1,0,0))
                self.assertBlockedBeyond(moving,1.5,pin,along=(1,0,0))

    def test_tooth_transitions_and_combined_controls(self):
        for phase in sorted(set(list(range(0,361,2))+[0.01,179.99,180.01,359.99,360.01,1439.99,1440])):
            self.node.set_state(phase=phase,time=0,playback=0)
            self.assertNoSolidInterference(self.node)
        for phase,time,playback in ((0,0,1),(720,0.75,1),(1440,1,1),(250,0.4,0.5)):
            self.node.set_state(phase=phase,time=time,playback=playback)
            self.assertNoSolidInterference(self.node)
            advance=self.node.carriage.bed.mesh.bounds[:,0].mean()-(-69.5)
            self.assertGreaterEqual(advance,-0.01)
            self.assertLessEqual(advance,4*2*math.pi*23.4/32+0.01)

    def test_undershot_water_channel_and_wheel_direction(self):
        self.node.set_state(phase=0,time=0,playback=0)
        water=self.node.water.mesh.vertices
        below=water[np.abs(water[:,0])<100]
        self.assertGreater(len(below),0)
        self.assertLess(below[:,2].max(),28)
        self.assertLess(water[:,2].max(),120)
        self.assertLess(self.node.channel.mesh.bounds[1,2],150)
        self.assertAlmostEqual(self.node.timber_structure.mesh.bounds[1,2],645,delta=0.01)
        first=self.node.waterwheel.mesh.vertices.copy()
        low=int(np.argmin(first[:,2]))
        self.node.set_state(phase=1)
        self.assertLess(self.node.waterwheel.mesh.vertices[low,0],first[low,0])

    def rope_centres(self):
        return np.asarray(self.node.rope.mesh.vertices)[:-2].reshape(-1,12,3).mean(axis=1)

    def test_continuous_rope_length_winding_and_attachment(self):
        initial=None
        for phase in (0,90,180,210,270,330,360,450,720,1080,1439.99,1440):
            self.node.set_state(phase=phase,time=0,playback=0)
            points=self.rope_centres()
            self.assertEqual(points.shape,(289,3))
            ends=points[::72]
            advance=self.node.carriage.bed.mesh.bounds[1,0]-111
            np.testing.assert_allclose(ends[0],[104+advance,98,353.4],atol=0.001)
            np.testing.assert_allclose(ends[1:4],[[325,98,353.4],[325,98,306.6],[-115,98,306.6]],atol=0.001)
            total=float(np.linalg.norm(ends[1]-ends[0])+np.linalg.norm(ends[3]-ends[2]))
            for start,centre in ((72,np.array([325,98,330])),(216,np.array([-115,98,330]))):
                arc=points[start:start+73]-centre
                radii=np.linalg.norm(arc,axis=1)
                np.testing.assert_allclose(radii,23.4,atol=0.001)
                unit=arc/radii[:,None]
                angle=np.arccos(np.clip(np.sum(unit[1:]*unit[:-1],axis=1),-1,1)).sum()
                if start==72:
                    self.assertAlmostEqual(angle,math.pi,delta=0.001)
                    self.assertGreater(points[108,0],348)
                else:
                    self.assertAlmostEqual(23.4*(angle-1.5*math.pi),advance,delta=0.001)
                total+=float(radii.mean()*angle)
            if initial is None:
                initial=total
            self.assertAlmostEqual(total,661+2.5*math.pi*23.4,delta=0.001)
            self.assertAlmostEqual(total,initial,delta=0.001)
            # The origin lies in the carriage's bored lug; the other cap is
            # in the rotating cleat, verified by the actual surrounding solid.
            for rigid in (self.node.timber_structure,self.node.return_pulley,
                          self.node.feed_drum,self.node.carriage.bed,self.node.sash.frame):
                self.assertNotIntersecting(self.node.rope,rigid)
            self.assertFreeWithin(self.node.rope,0.15,self.node.carriage.bed,along=(0,1,0))
            self.assertBlockedBeyond(self.node.rope,0.8,self.node.carriage.bed,along=(0,1,0))
            self.assertFreeWithin(self.node.rope,0.15,self.node.feed_drum,along=(0,1,0))
            self.assertBlockedBeyond(self.node.rope,0.8,self.node.feed_drum,along=(0,1,0))

    def test_wheel_and_carriage_retention(self):
        self.node.set_state(phase=0,time=0,playback=0)
        self.assertFreeWithin(self.node.waterwheel,0.3,self.node.crankshaft,along=(0,1,0))
        self.assertBlockedBeyond(self.node.waterwheel,2,self.node.crankshaft,along=(0,1,0))
        for wheel in (*self.node.carriage.outer_wheels,*self.node.carriage.inner_wheels):
            self.assertFreeWithin(wheel,0.2,self.node.timber_structure,along=(0,1,0))
        self.assertFreeWithin(self.node.return_pulley,0.2,self.node.pulley_pin,along=(1,0,0))
        self.assertBlockedBeyond(self.node.return_pulley,1.2,self.node.pulley_pin,along=(1,0,0))

    def test_reposing_is_reproducible(self):
        self.node.set_state(time=0, phase=73, playback=0)
        first = self.node.sash.frame.mesh.bounds.copy()
        self.node.set_state(phase=1100)
        self.node.set_state(phase=73)
        np.testing.assert_allclose(self.node.sash.frame.mesh.bounds, first, atol=1e-6)

    @testing_steps(9, end=0.25)
    def test_crank_pin_captures_rod(self):
        self.assertFreeWithin(self.node.connecting_rod, 0.3, self.node.crankshaft, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.connecting_rod, 1.5, self.node.crankshaft, along=(1, 0, 0))

    @testing_steps(9, end=0.25)
    def test_sash_stays_in_guide_slots(self):
        self.assertFreeWithin(self.node.sash.frame, 0.3, self.node.timber_structure, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.sash.frame, 1.3, self.node.timber_structure, along=(1, 0, 0))

    def test_waterwheel_is_keyed_to_shaft(self):
        self.assertFreeWithin(self.node.waterwheel, 1, self.node.crankshaft, axis=(0, 1, 0))
        self.assertBlockedBeyond(self.node.waterwheel, 10, self.node.crankshaft, axis=(0, 1, 0))

    def test_seated_pawl_engages_ratchet(self):
        for phase in (0,180,210,240,270,300,330,360,720,1080,1440):
            self.node.set_state(time=0, phase=phase, playback=0)
            self.assertFreeWithin(self.node.feed_drum, 0.3, self.node.pawl, axis=(0, 1, 0))
            self.assertBlockedBeyond(self.node.feed_drum, 5, self.node.pawl, axis=(0, -1, 0), directions='forward')


class SawmillInstructionsTest(ScenarioTest):
    node=LeonardoHydraulicSawmill
    dt=0.05
    meshes=True

    def test_named_pass_stays_clear_and_finishes_at_four_teeth(self):
        sim=self.simulation()
        sim.at(0).trigger('Start of pass')
        sim.at(0.7).trigger('Run four cycles')
        sim.every(0.2,self.assertNoSolidInterference,self.node)
        sim.run(16.8)
        self.assertAlmostEqual(self.node.carriage.bed.mesh.bounds[1,0]-111,
                               4*2*math.pi*23.4/32,delta=0.01)
