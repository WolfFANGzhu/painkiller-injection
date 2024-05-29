import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from decimal import Decimal
from core import Core
from doctorAPP import DoctorApp

class TestDoctorApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the root window during tests

    def setUp(self):
        """Initialization of each test case"""
        self.core = Core()
        self.app = DoctorApp(self.root, self.core)
        self.app.root.update_idletasks()
        self.app.root.update()
        self.app.root.after(1000)  # Wait for 1000 milliseconds to observe the interface change

    def tearDown(self):
        """Cleanup after each test case"""
        self.app.root.update_idletasks()
        self.app.root.update()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed"""
        cls.root.quit()
        cls.root.update_idletasks()
        cls.root.update()

    @patch.object(DoctorApp, 'show_message')
    def test_set_baseline(self, mock_show_message):
        """Test setting baseline value"""
        self.app.show_baseline_scale()
        self.app.baseline_scale.set(0.05)
        self.app.set_baseline()
        self.app.root.update_idletasks()
        self.app.root.update()
        self.app.root.after(1000)  # Wait for 1000 milliseconds to observe the interface change

        # Check if the baseline was set correctly
        self.assertEqual(self.core.status()['Baseline Rate'], Decimal('0.05'))
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Success set baseline to 0.05 ml")

    @patch.object(DoctorApp, 'show_message')
    def test_set_bolus(self, mock_show_message):
        """Test setting bolus value"""
        self.app.show_bolus_scale()
        self.app.bolus_scale.set(0.3)
        self.app.set_bolus()
        self.app.root.update_idletasks()
        self.app.root.update()
        self.app.root.after(1000)  # Wait for 1000 milliseconds to observe the interface change

        # Check if the bolus was set correctly
        self.assertEqual(self.core.status()['Bolus Amount'], Decimal('0.3'))
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Success set bolus to 0.3 ml")

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_on(self, mock_show_message):
        """Test turning baseline on"""
        self.app.baseline_on()
        self.app.root.update_idletasks()
        self.app.root.update()
        self.app.root.after(1000)  # Wait for 1000 milliseconds to observe the interface change

        # Check if the baseline status was set correctly
        self.assertEqual(self.core.status()['Baseline Status'], 'on')
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Baseline injection turned on.")

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_off(self, mock_show_message):
        """Test turning baseline off"""
        self.app.baseline_off()
        self.app.root.update_idletasks()
        self.app.root.update()
        self.app.root.after(1000)  # Wait for 1000 milliseconds to observe the interface change

        # Check if the baseline status was set correctly
        self.assertEqual(self.core.status()['Baseline Status'], 'off')
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Baseline injection turned off.")

if __name__ == "__main__":
    unittest.main()
