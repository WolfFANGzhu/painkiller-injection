import tkinter as tk
from tkinter import messagebox
from core import Core

class PatientApp:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title("Patient Interface")

        self.request_bolus_button = tk.Button(root, text="Request Bolus", command=self.request_bolus)
        self.request_bolus_button.pack()

    def request_bolus(self):
        if self.core.request_bolus():
            messagebox.showinfo("Info", "Bolus injection successful.")
        else:
            messagebox.showerror("Error", "Bolus injection failed. Check hour and daily limits.")
