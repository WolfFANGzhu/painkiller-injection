import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import sys
import os
from matplotlib.figure import Figure
from decimal import Decimal
# find correct path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.core import Core
from src.doctorAPP import DoctorApp
from src.patientAPP import PatientApp

class TestDoctorApp_UI(unittest.TestCase):

    def setUp(self):
        self.root1 = tk.Tk()
        self.root2 = tk.Tk()
        self.core = Core()
        self.app = DoctorApp(self.root1, self.core)
        self.patient = PatientApp(self.root2, self.core)

    def tearDown(self):
        self.root1.destroy()
        self.root2.destroy()

    def button_click(self, button): # simulate button click
        button.invoke()

    @patch.object(DoctorApp, 'show_message')
    def test_set_baseline(self, mock_show_message): # set_baseline_button + set_button
        
        self.button_click(self.app.set_baseline_button)
        self.app.baseline_scale.set(0.03)
        self.button_click(self.app.set_button)
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.03'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')
        mock_show_message.assert_called_with("Success set baseline to " + "0.03" + " ml.")

    @patch.object(DoctorApp, 'show_message')
    def test_set_bolus(self, mock_show_message): # set_bolus_button + set_button

        self.button_click(self.app.set_bolus_button)
        self.app.bolus_scale.set(0.32)
        self.button_click(self.app.set_button)
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.32'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')
        mock_show_message.assert_called_with("Success set bolus to " + "0.32" + " ml.")

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_on(self, mock_show_message): # baseline_on_button

        self.button_click(self.app.baseline_on_button)
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'on')
        mock_show_message.assert_called_with("Baseline injection turned on.") 

    @patch.object(DoctorApp, 'show_message')
    def test_baseline_off(self, mock_show_message): # baseline_off_button

        self.button_click(self.app.baseline_off_button)
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')
        mock_show_message.assert_called_with("Baseline injection turned off.") 

    def test_graph(self): # graph_button
        
        self.button_click(self.app.graph_button)
        self.assertEqual(self.app.showing_graph, 'on')
        self.assertTrue(self.app.stop_graph_button['state'] == tk.NORMAL)    
        self.assertTrue(self.app.graph_button['state'] == tk.DISABLED)     

    @patch.object(DoctorApp, 'show_message')
    def test_stop_graph(self, mock_show_message): # graph_button + stop_graph_button

        self.button_click(self.app.graph_button)
        self.button_click(self.app.stop_graph_button)
        mock_show_message.assert_called_with("Graph stopped.")
        self.assertEqual(self.app.showing_graph, 'off')
        self.assertTrue(self.app.stop_graph_button['state'] == tk.DISABLED)    
        self.assertTrue(self.app.graph_button['state'] == tk.NORMAL)        

    @patch.object(DoctorApp, 'show_message')
    def test_start(self, mock_show_message): # start_button

        self.button_click(self.app.start_button)
        status = self.core.status()
        self.assertTrue(self.app.start_button['state'] == tk.DISABLED)
        self.assertTrue(self.app.start)
        mock_show_message.assert_called_with("Simulation started.")

        ## start will update once
        self.assertEqual(status['Time'], Decimal('1'))

    @patch.object(DoctorApp, 'show_message')
    def test_simulate_speed(self, mock_show_message): # set_simulate_speed_button + set button
        
        self.button_click(self.app.set_simulate_speed_button)
        self.app.speed_scale.set(3)
        self.button_click(self.app.set_button)
        self.assertEqual(self.app.simulate_speed, int(1000/3))
        mock_show_message.assert_called_with("Simulation speed set to 3x.")
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')

    def test_pause_not_show(self): # pause_button

        self.button_click(self.app.pause_button)
        expected_text = "Simulation is paused. Press the \"Resume\" button to restart the system."
        self.assertEqual(self.app.pause_label.cget("text"), expected_text)
        self.assertEqual(self.app.showing_graph, 'off')

    def test_pause_show(self): # pause_button + graph_button

        self.button_click(self.app.graph_button)
        self.button_click(self.app.pause_button)
        expected_text = "Simulation is paused. Press the \"Resume\" button to restart the system."
        self.assertEqual(self.app.pause_label.cget("text"), expected_text)
        self.assertEqual(self.app.showing_graph, 'pause')

    @patch.object(DoctorApp, 'show_message')
    def test_reset_not_show(self, mock_show_message) : # reset_button

        self.button_click(self.app.reset_button)
        mock_show_message.assert_called_with("System reset.")
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')
        self.assertFalse(self.app.start)
        self.assertFalse(self.app.paused)
        self.assertTrue(self.app.showing_graph == 'off')
        self.assertTrue(self.app.start_button['state'] == tk.NORMAL) 

    @patch.object(DoctorApp, 'show_message')
    def test_reset_show(self, mock_show_message) : # reset_button + graph_button
        
        self.button_click(self.app.graph_button)
        self.button_click(self.app.reset_button)
        mock_show_message.assert_called_with("System reset.")
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('0'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')
        self.assertTrue(self.app.start_button['state'] == tk.NORMAL) 
        self.assertFalse(self.app.start)
        self.assertFalse(self.app.paused)
        self.assertTrue(self.app.showing_graph == 'off')
        self.assertTrue(self.app.stop_graph_button['state'] == tk.DISABLED)    
        self.assertTrue(self.app.graph_button['state'] == tk.NORMAL)  

    @patch.object(DoctorApp, 'show_message')
    def test_resume_pause_show(self, mock_show_message): # graph_button + pause_button + resume_button

        self.button_click(self.app.graph_button)
        self.button_click(self.app.pause_button)
        self.button_click(self.app.resume_button)
        self.assertFalse(self.app.paused)
        mock_show_message.assert_called_with("Simulation resumed.")
        self.assertTrue(self.app.showing_graph == 'on')
        self.assertTrue(self.app.graph_button['state'] == tk.DISABLED)    

    @patch.object(DoctorApp, 'show_message')
    def test_resume_pause_not_show(self, mock_show_message): # start_button + pause_button + resume_button

        self.button_click(self.app.start_button)
        self.button_click(self.app.pause_button)
        self.button_click(self.app.resume_button)
        self.assertFalse(self.app.paused)
        mock_show_message.assert_called_with("Simulation resumed.")
        self.assertTrue(self.app.showing_graph == 'off')
        self.assertTrue(self.app.stop_graph_button['state'] == tk.DISABLED)    
        self.assertTrue(self.app.start_button['state'] == tk.DISABLED)   

    def test_combine_1(self): # simulate the all day condition 1 start can go truely
        
        self.button_click(self.app.start_button)
        for _ in range(599):
            self.core.update_by_minute()
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('600'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')

    def test_combine_2(self): # simulate the all day condition 2 start can go correctly with set baseline
        
        self.button_click(self.app.set_baseline_button)
        self.app.baseline_scale.set(0.05)
        self.button_click(self.app.set_button)
        self.button_click(self.app.baseline_on_button)
        self.button_click(self.app.start_button)
        for _ in range(69):
            self.core.update_by_minute()
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('70'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.05'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.2'))
        self.assertEqual(status['Hourly Amount'], Decimal('1.0'))
        self.assertEqual(status['Daily Amount'], Decimal('1.0'))
        self.assertEqual(status['Baseline Status'], 'on')

    def test_combine_3(self): # simulate the all day condition 2 start can go correctly with set bolus
        
        self.button_click(self.app.set_bolus_button)
        self.app.bolus_scale.set(0.35)
        self.button_click(self.app.set_button)
        self.button_click(self.app.start_button)
        for _ in range(69):
            self.core.update_by_minute()
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('70'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.01'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.35'))
        self.assertEqual(status['Hourly Amount'], Decimal('0.0'))
        self.assertEqual(status['Daily Amount'], Decimal('0.0'))
        self.assertEqual(status['Baseline Status'], 'off')

    def test_combine_4(self): # simulate the all day condition 2 start can go correctly with set bolus + baseline
        
        self.button_click(self.app.set_baseline_button)
        self.app.baseline_scale.set(0.05)
        self.button_click(self.app.set_button)
        self.button_click(self.app.set_bolus_button)
        self.app.bolus_scale.set(0.30)
        self.button_click(self.app.set_button)
        self.button_click(self.app.start_button)
        self.button_click(self.app.baseline_on_button)
        for i in range(59):
            self.core.update_by_minute()
            status = self.core.status()
            print(status['Time'])
            if i == 4:
                self.button_click(self.patient.request_bolus_button)
            if i == 5:
                self.assertEqual(status['Time'], Decimal('7'))
                self.assertEqual(status['Baseline Rate'], Decimal('0.05'))
                self.assertEqual(status['Bolus Amount'], Decimal('0.30'))
                self.assertEqual(status['Hourly Amount'], Decimal('0.60'))
                self.assertEqual(status['Daily Amount'], Decimal('0.60'))
                self.assertEqual(status['Baseline Status'], 'on')
        status = self.core.status()
        # print(status)
        self.assertEqual(status['Time'], Decimal('60'))
        self.assertEqual(status['Baseline Rate'], Decimal('0.05'))
        self.assertEqual(status['Bolus Amount'], Decimal('0.30'))
        self.assertEqual(status['Hourly Amount'], Decimal('1.00'))
        self.assertEqual(status['Daily Amount'], Decimal('1.00'))
        self.assertEqual(status['Baseline Status'], 'on')

if __name__ == "__main__":
    unittest.main()
