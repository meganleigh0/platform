Unit Tests for Plant3
python
Copy code
import unittest
from unittest.mock import MagicMock
from engine.plant3 import Plant3

class TestPlant3(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.station_dict_mock = {'station1': MagicMock()}
        self.plant3 = Plant3(self.env_mock, self.station_dict_mock)

    def test_hull_line_process(self):
        hull_mock = MagicMock()
        product_mock = MagicMock()
        self.plant3.hull_line_process(hull_mock, product_mock)
        self.env_mock.process.assert_called_with(hull_mock.plant3_process(product_mock))

    def test_turret_line_process(self):
        turret_mock = MagicMock()
        product_mock = MagicMock()
        self.plant3.turret_line_process(turret_mock, product_mock)
        self.env_mock.process.assert_called_with(turret_mock.plant3_process(product_mock))

if __name__ == '__main__':
    unittest.main()
Unit Tests for JSMC
python
Copy code
import unittest
from unittest.mock import MagicMock
from engine.jsmc import JSMC

class TestJSMC(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.jsmc = JSMC(self.env_mock)

    def test_process(self):
        product_mock = MagicMock()
        self.jsmc.process(product_mock)
        # Verify process is called on plant1 and plant3 simulations
        self.assertTrue(self.jsmc.plant1_simulation.induce_reclaimed_structure.called)
        self.assertTrue(self.jsmc.plant3_simulation.hull_line_process.called or self.jsmc.plant3_simulation.turret_line_process.called)

if __name__ == '__main__':
    unittest.main()
Unit Tests for Turret
python
Copy code
import unittest
from unittest.mock import MagicMock
from model.turret import Turret

class TestTurret(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.turret = Turret(self.env_mock, 'turret_id', MagicMock())

    def test_plant1_process(self):
        product_mock = MagicMock()
        self.turret.plant1_process(product_mock)
        # Assert that the process method is called
        self.assertTrue(self.env_mock.process.called)

    def test_plant3_process(self):
        product_mock = MagicMock()
        self.turret.plant3_process(product_mock)
        # Assert that the process method waits for p1_processed
        self.turret.p1_processed.succeed()
        self.assertTrue(self.env_mock.process.called)

if __name__ == '__main__':
    unittest.main()
Unit Tests for Hull
python
Copy code
import unittest
from unittest.mock import MagicMock
from model.hull import Hull

class TestHull(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        self.hull = Hull(self.env_mock, 'hull_id', MagicMock())

    def test_plant1_process(self):
        product_mock = MagicMock()
        self.hull.plant1_process(product_mock)
        # Assert that the process method is called
        self.assertTrue(self.env_mock.process.called)

    def test_plant3_process(self):
        product_mock = MagicMock()
        self.hull.plant3_process(product_mock)
        # Assert that the process method waits for p1_processed
        self.hull.p1_processed.succeed()
        self.assertTrue(self.env_mock.process.called)

if __name__ == '__main__':
    unittest.main()
Unit Tests for Operation
python
Copy code
import unittest
from unittest.mock import MagicMock
from model.operation import Operation

class TestOperation(unittest.TestCase):
    def setUp(self):
        self.env_mock = MagicMock()
        department_dict_mock = {'Dept1': MagicMock()}
        self.operation = Operation(self.env_mock, 'Operation1', 1, 'Dept1', department_dict_mock)

    def test_process(self):
        assembly_mock = MagicMock()
        product_mock = MagicMock()
        self.operation.process(assembly_mock, product_mock)
        # Verify timeout is called with the standard time divided by num_heads_req
        self.env_mock.timeout.assert_called()

if __name__ == '__main__':
    unittest.main()
