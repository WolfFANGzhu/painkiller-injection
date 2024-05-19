import tkinter as tk
from tkinter import messagebox
from core import Core

class DoctorApp:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title("Doctor Interface")

        self.baseline_label = tk.Label(root, text="Set Baseline (0.01-0.1 mL/min):")
        self.baseline_label.pack()
        self.baseline_entry = tk.Entry(root)
        self.baseline_entry.pack()

        self.bolus_label = tk.Label(root, text="Set Bolus (0.2-0.5 mL):")
        self.bolus_label.pack()
        self.bolus_entry = tk.Entry(root)
        self.bolus_entry.pack()

        self.set_baseline_button = tk.Button(root, text="Set Baseline", command=self.set_baseline)
        self.set_baseline_button.pack()

        self.set_bolus_button = tk.Button(root, text="Set Bolus", command=self.set_bolus)
        self.set_bolus_button.pack()

        self.baseline_on_button = tk.Button(root, text="Baseline On", command=self.baseline_on)
        self.baseline_on_button.pack()

        self.baseline_off_button = tk.Button(root, text="Baseline Off", command=self.baseline_off)
        self.baseline_off_button.pack()

        self.status_button = tk.Button(root, text="Show Status", command=self.show_status)
        self.status_button.pack()

    def set_baseline(self):
        try:
            baseline = float(self.baseline_entry.get())
            message = self.core.set_baseline(baseline)
            messagebox.showinfo("Info", message)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please provide a number between 0.01 and 0.1.")

    def set_bolus(self):
        try:
            bolus = float(self.bolus_entry.get())
            message = self.core.set_bolus(bolus)
            messagebox.showinfo("Info", message)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please provide a number between 0.2 and 0.5.")

    def baseline_on(self):
        self.core.baseline_on()
        messagebox.showinfo("Info", "Baseline injection turned on.")

    def baseline_off(self):
        self.core.baseline_off()
        messagebox.showinfo("Info", "Baseline injection turned off.")

    def show_status(self):
        status = self.core.status()
        status_message = "\n".join(f"{key}: {value}" for key, value in status.items())
        messagebox.showinfo("Status", status_message)
