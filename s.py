import unittest
from unittest.mock import MagicMock
from engine.plant1 import Plant1

class TestPlant1(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.plant1 = Plant1(self.env_mock)

    def test_induce_reclaimed_structure(self):
        reclaimed_structure = self.plant1.induce_reclaimed_structure()
        self.assertIn(reclaimed_structure, self.plant1.reclaimed_structures)

    def test_fabrication_process(self):
        product_mock = MagicMock()
        self.plant1.fabrication_process(product_mock)
        self.assertTrue(self.plant1.fab_in_process)

    def test_transfer_to_completed(self):
        structure_mock = MagicMock()
        structure_mock.id = 'hull.test'
        self.plant1.hulls.append(structure_mock)
        self.plant1.transfer_to_completed(structure_mock)
        self.assertIn(structure_mock, self.plant1.completed_hulls)

if __name__ == '__main__':
    unittest.main()


import unittest
from unittest.mock import MagicMock
from model.assembly import Assembly

class TestAssembly(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.operations = [(1, 'Operation1', 'Dept1')]
        self.department_dict_mock = {'Dept1': MagicMock()}
        self.assembly = Assembly(self.env_mock, 'id1', 'num1', 'name1', 1, 'make', 'station1', self.operations, self.department_dict_mock)

    def test_add_child(self):
        part_mock = MagicMock()
        self.assembly.add_child(part_mock)
        self.assertIn(part_mock, self.assembly.children)

    def test_process(self):
        product_mock = MagicMock()
        self.assembly.process(product_mock)
        # Since process is a generator, you need to advance it to test effects
        try:
            next(self.assembly.process(product_mock))
        except StopIteration:
            pass
        self.assertTrue(self.assembly.in_process)

if __name__ == '__main__':
    unittest.main()
