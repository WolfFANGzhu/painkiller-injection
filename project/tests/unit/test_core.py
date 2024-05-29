import unittest
from decimal import Decimal
from project.src.core import Core

class TestCore(unittest.TestCase):

    def setUp(self):
        self.core = Core()

    def test_set_baseline(self):
        self.core.set_baseline(0.05)
        self.assertEqual(self.core.status()['Baseline Rate'], Decimal('0.05'))

    def test_set_bolus(self):
        self.core.set_bolus(0.3)
        self.assertEqual(self.core.status()['Bolus Amount'], Decimal('0.3'))

    def test_baseline_on(self):
        self.core.baseline_on()
        self.assertEqual(self.core.status()['Baseline Status'], 'on')

    def test_baseline_off(self):
        self.core.baseline_off()
        self.assertEqual(self.core.status()['Baseline Status'], 'off')

    def test_reset(self):
        self.core.set_baseline(0.05)
        self.core.set_bolus(0.3)
        self.core.reset()
        self.assertEqual(self.core.status()['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(self.core.status()['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(self.core.status()['Baseline Status'], 'off')
        self.assertEqual(self.core.status()['Daily Amount'], Decimal('0.0'))
        self.assertEqual(self.core.status()['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(self.core.status()['Time'], 0)
        

if __name__ == "__main__":
    unittest.main()
