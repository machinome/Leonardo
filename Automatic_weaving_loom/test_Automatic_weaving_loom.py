from solid_node.test import TestCase


class AutomaticWeavingLoomTest(TestCase):

    def test_solid_integrity(self):
        self.assertNoDisconnectedSolids(self.node)

    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)
