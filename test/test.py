import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from src.core import Core
from src.doctorAPP import DoctorApp

class TestDoctorApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.core = Core()
        self.app = DoctorApp(self.root, self.core)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_set_baseline(self, mock_showinfo):
        # Simulate setting baseline value
        self.app.show_baseline_scale()
        self.app.baseline_scale.set(0.05)
        self.app.set_baseline()
        
        # Check if the baseline was set correctly
        self.assertEqual(self.core.status()['Baseline Rate'], 0.05)
        # Check if the messagebox was called with the correct message
        mock_showinfo.assert_called_with("Info", "Success Set Baseline to 0.05")

    @patch('tkinter.messagebox.showinfo')
    def test_set_bolus(self, mock_showinfo):
        # Simulate setting bolus value
        self.app.show_bolus_scale()
        self.app.bolus_scale.set(0.3)
        self.app.set_bolus()
        
        # Check if the bolus was set correctly
        self.assertEqual(self.core.status()['Bolus Amount'], 0.3)
        # Check if the messagebox was called with the correct message
        mock_showinfo.assert_called_with("Info", "Success Set Bolus to 0.3")

    @patch('tkinter.messagebox.showinfo')
    def test_baseline_on(self, mock_showinfo):
        # Simulate turning baseline on
        self.app.baseline_on()
        
        # Check if the baseline status was set correctly
        self.assertTrue(self.core.status()['Baseline Status'])
        # Check if the messagebox was called with the correct message
        mock_showinfo.assert_called_with("Info", "Baseline injection turned on.")

    @patch('tkinter.messagebox.showinfo')
    def test_baseline_off(self, mock_showinfo):
        # Simulate turning baseline off
        self.app.baseline_off()
        
        # Check if the baseline status was set correctly
        self.assertFalse(self.core.status()['Baseline Status'])
        # Check if the messagebox was called with the correct message
        mock_showinfo.assert_called_with("Info", "Baseline injection turned off.")

if __name__ == "__main__":
    unittest.main()
