import tkinter as tk
from core import Core
from doctorAPP import DoctorApp
from patientAPP import PatientApp

def main():
    core = Core()
    
    doctor_root = tk.Tk()
    
    doctor_app = DoctorApp(doctor_root, core)
    
    patient_root = tk.Tk()
    patient_app = PatientApp(patient_root, core)
    
    # Run both windows
    doctor_root.mainloop()
    patient_root.mainloop()

if __name__ == "__main__":
    main()
    
