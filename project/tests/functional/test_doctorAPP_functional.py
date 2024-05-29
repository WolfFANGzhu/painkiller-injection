import time
import unittest
from unittest.mock import patch
import tkinter as tk
from decimal import Decimal
from project.src.core import Core
from project.src.doctorAPP import DoctorApp

class TestDoctorApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.root = tk.Tk()
        cls.core = Core()
        cls.app = DoctorApp(cls.root, cls.core)
        cls.app.root.update_idletasks()
        cls.app.root.update()

    def setUp(self):
        """Reset the application state before each test case"""
        self.core.reset()  

    def tearDown(self):
        """Update the UI after each test case to ensure it is cleaned up"""
        self.app.root.update_idletasks()
        self.app.root.update()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed"""
        cls.app.root.quit()
        cls.app.root.update_idletasks()
        cls.app.root.update()

    @patch.object(DoctorApp, 'show_message')
    def test_set_baseline(self, mock_show_message):
        """Test setting baseline value"""
        time.sleep(1)
        self.app.show_baseline_scale()
        self.app.baseline_scale.set(0.06)
        self.app.set_baseline()
        # Check if the baseline was set correctly
        self.assertEqual(self.core.status()['Baseline Rate'], Decimal('0.06'))
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Success set baseline to 0.06 ml.")
        time.sleep(1)

    @patch.object(DoctorApp, 'show_message')
    def test_set_bolus(self, mock_show_message):
        """Test setting bolus value"""
        time.sleep(1) 
        self.app.show_bolus_scale()
        self.app.bolus_scale.set(0.5)
        self.app.set_bolus()
        

        # Check if the bolus was set correctly
        self.assertEqual(self.core.status()['Bolus Amount'], Decimal('0.5'))
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Success set bolus to 0.5 ml.")
        time.sleep(1) 

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_on(self, mock_show_message):
        """Test turning baseline on"""
        time.sleep(1)  
        self.app.baseline_on()
       

        # Check if the baseline status was set correctly
        self.assertEqual(self.core.status()['Baseline Status'], 'on')
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Baseline injection turned on.")
        time.sleep(1)  

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_off(self, mock_show_message):
        """Test turning baseline off"""
        time.sleep(1)
        self.app.baseline_off()
        # Check if the baseline status was set correctly
        self.assertEqual(self.core.status()['Baseline Status'], 'off')
        # Check if the message method was called with the correct message
        mock_show_message.assert_called_with("Baseline injection turned off.")
        time.sleep(1)

if __name__ == "__main__":
    unittest.main()
