"""Independent contracts for the fixed frame's carpentry."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from machinome.test import TestCase
import numpy as np
from .frame import Frame, FrameCarpentry


def leaves(node):
    if node.rigid:
        yield node
    else:
        for child in node.children:
            yield from leaves(child)


class FrameTest(TestCase):
    node = Frame

    def test_fixed_frame_is_individual_cut_timbers(self):
        stand = self.node.timber_structure
        self.assertFalse(stand.bed.rigid, 'The bed must be individual fitted timbers')
        self.assertFalse(stand.saw_tower.rigid, 'The tower must be individual fitted timbers')
        expected = {f'{prefix}{i}' for prefix, count in
                    (('L',4),('B',2),('S',2),('C',4),('R',2),('F',2),('T',6),('A',2))
                    for i in range(1,count+1)}
        expected.update(f'P{i:02}' for i in range(1,35))
        self.assertEqual(set(self.members()), expected)

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)

    def members(self):
        return {n.name.split(' · ')[0]: n for n in leaves(self.node.timber_structure)}

    def test_offset_lower_tenons_keep_two_complete_necks(self):
        parts = self.members()
        rail, cross, leg = parts['S1'], parts['C2'], parts['L2']
        self.assertAlmostEqual(rail.mesh.extents[0], 680, delta=0.01)
        self.assertTrue(rail.mesh.contains([[338, -99, 76]])[0])
        self.assertTrue(cross.mesh.contains([[335, -97, 67]])[0])
        self.assertFalse(leg.mesh.contains([[338, -99, 76], [335, -97, 67]]).any())
        self.assertTrue(leg.mesh.contains([[338, -99, 71.5]])[0], 'Keep wood between the two mortises')
        self.assertFreeWithin(rail, 0.05, leg, along=(0, 1, 0))
        self.assertBlockedBeyond(rail, 0.4, leg, along=(0, 1, 0))

    def test_pegs_capture_both_members_of_every_joint(self):
        from .carpentry import PEGS
        parts = self.members()
        for spec in PEGS:
            peg = parts[spec.code]
            # A displacement across the bore must engage EACH timber.
            direction = (0, 0, 1) if spec.axis != 'z' else (1, 0, 0)
            for code in spec.members:
                with self.subTest(peg=spec.code, timber=code):
                    self.assertFreeWithin(peg, 0.03, parts[code], along=direction)
                    self.assertBlockedBeyond(peg, 0.35, parts[code], along=direction)

    def test_frame_has_a_load_path_to_the_display_plinth(self):
        parts = self.members()
        # These short cantilevers are held by pegged tenons. Their moment
        # reactions are outside the drop solver's vertical contact model;
        # peg engagement is measured separately, never presumed from a flag.
        self.assertAssemblySupported(self.node, ground=self.node.foundation, max_drop=0.3,
                                     supports=[(parts['F1'], parts['B2']),
                                               (parts['F2'], parts['B2'])])

    def test_pivot_bearer_tenons_resist_tipping(self):
        parts = self.members()
        for code, x, z in (('F1', 235, 324), ('F2', 37, 333)):
            bearer = parts[code]
            for angle in (-2, 2):
                bearer.save_checkpoint()
                try:
                    bearer.translate([-x, -106, -z]).rotate(angle, [1,0,0]).translate([x,106,z])
                    self.assertIntersecting(bearer, parts['B2'])
                finally:
                    bearer.restore_checkpoint()

    def test_running_surface_has_recessed_pin_heads(self):
        from .carpentry import PEGS
        parts = self.members()
        for peg in PEGS:
            if any(code in ('R1','R2') for code in peg.members):
                self.assertLess(parts[peg.code].mesh.bounds[1,2], 345)
                self.assertGreater(parts[peg.code].mesh.bounds[1,2], 344.5)


class FrameCarpentryTest(TestCase):
    node = FrameCarpentry

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_assembly_integrity(self):
        # Sample every extraction and the neighborhoods of changes of direction.
        for stage in sorted(set(np.linspace(0, 11, 89)) | {
                i+d for i in range(1, 11) for d in (-0.001, 0.001)}):
            self.node.set_state(disassembly=float(stage))
            try:
                self.assertNoSolidInterference(self.node)
            except AssertionError as error:
                self.fail(f'Assembly stage {stage:g}: {error}')

    def test_reassembly_restores_the_actual_frame(self):
        self.node.set_state(disassembly=0)
        before = {n.name: n.mesh.bounds.copy() for n in leaves(self.node)}
        self.node.set_state(disassembly=11)
        after = {n.name: n.mesh.bounds.copy() for n in leaves(self.node)}
        self.assertGreater(after['R1 · Continuous carriage running rail'][0,2], 400)
        self.node.set_state(disassembly=0)
        for n in leaves(self.node):
            np.testing.assert_allclose(n.mesh.bounds, before[n.name], atol=1e-7)
