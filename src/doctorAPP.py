import tkinter as tk
from tkinter import messagebox
from core import Core

class DoctorApp:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title("Doctor Interface")

        # Create title bar for dragging
        self.title_bar = tk.Frame(root, bg="lightgrey", relief="raised", bd=2)
        self.title_bar.pack(fill=tk.X)
        self.title_bar_label = tk.Label(self.title_bar, text="Doctor Interface", bg="lightgrey")
        self.title_bar_label.pack(side=tk.LEFT, padx=10)

        self.make_window_draggable(self.title_bar)

        self.baseline_label = tk.Label(root, text="Set Baseline (0.01-0.1 mL/min):")
        self.baseline_label.pack()
        self.baseline_scale = tk.Scale(root, from_=0.01, to=0.1, resolution=0.01, orient=tk.HORIZONTAL)
        self.baseline_scale.pack()

        self.bolus_label = tk.Label(root, text="Set Bolus (0.2-0.5 mL):")
        self.bolus_label.pack()
        self.bolus_scale = tk.Scale(root, from_=0.2, to=0.5, resolution=0.01, orient=tk.HORIZONTAL)
        self.bolus_scale.pack()

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
        baseline = self.baseline_scale.get()
        message = self.core.set_baseline(baseline)
        messagebox.showinfo("Info", message)

    def set_bolus(self):
        bolus = self.bolus_scale.get()
        message = self.core.set_bolus(bolus)
        messagebox.showinfo("Info", message)

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

    def make_window_draggable(self, widget):
        self.offset_x = 0
        self.offset_y = 0
        self.root.geometry('+600+300')
        def on_mouse_down(event):
            self.offset_x = event.x
            self.offset_y = event.y

        def on_mouse_move(event):
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f'+{x}+{y}')

        widget.bind('<Button-1>', on_mouse_down)
        widget.bind('<B1-Motion>', on_mouse_move)
