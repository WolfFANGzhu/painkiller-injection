import tkinter as tk
from tkinter import messagebox
from core import Core

class DoctorApp:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title("Doctor Interface")

        self.root.geometry('600x450+500+200')

        # Create title bar for dragging with larger height
        self.title_bar = tk.Frame(root, bg="lightgrey", relief="raised", bd=2, height=40)
        self.title_bar.pack(fill=tk.X)
        self.title_bar_label = tk.Label(self.title_bar, text="Doctor Interface", bg="lightgrey")
        self.title_bar_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.make_window_draggable(self.title_bar)

        button_width = 20  # Set a uniform button width

        # Set Baseline button
        self.set_baseline_button = tk.Button(root, text="Set Baseline", command=self.show_baseline_scale, width=button_width)
        self.set_baseline_button.pack(pady=5)

        # Set Bolus button
        self.set_bolus_button = tk.Button(root, text="Set Bolus", command=self.show_bolus_scale, width=button_width)
        self.set_bolus_button.pack(pady=5)

        # Baseline On button
        self.baseline_on_button = tk.Button(root, text="Baseline On", command=self.baseline_on, width=button_width)
        self.baseline_on_button.pack(pady=5)

        # Baseline Off button
        self.baseline_off_button = tk.Button(root, text="Baseline Off", command=self.baseline_off, width=button_width)
        self.baseline_off_button.pack(pady=5)

        # Show Status button
        self.status_button = tk.Button(root, text="Show Status", command=self.show_status, width=button_width)
        self.status_button.pack(pady=5)

        # Frame for the dynamic part of the interface
        self.dynamic_frame = tk.Frame(root)
        self.dynamic_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_baseline_scale(self):
        self.clear_dynamic_frame()
        baseline_label = tk.Label(self.dynamic_frame, text="Set Baseline (0.01-0.1 mL/min):")
        baseline_label.pack(pady=5, anchor=tk.CENTER)
        self.baseline_scale = tk.Scale(self.dynamic_frame, from_=0.01, to=0.1, resolution=0.01, orient=tk.HORIZONTAL, length=300)
        self.baseline_scale.pack(pady=5, anchor=tk.CENTER)

        set_button = tk.Button(self.dynamic_frame, text="Set Baseline", command=self.set_baseline)
        set_button.pack(pady=5, anchor=tk.CENTER)

    def show_bolus_scale(self):
        self.clear_dynamic_frame()
        bolus_label = tk.Label(self.dynamic_frame, text="Set Bolus (0.2-0.5 mL):")
        bolus_label.pack(pady=5, anchor=tk.CENTER)
        self.bolus_scale = tk.Scale(self.dynamic_frame, from_=0.2, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, length=300)
        self.bolus_scale.pack(pady=5, anchor=tk.CENTER)

        set_button = tk.Button(self.dynamic_frame, text="Set Bolus", command=self.set_bolus)
        set_button.pack(pady=5, anchor=tk.CENTER)

    def clear_dynamic_frame(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def set_baseline(self):
        baseline = self.baseline_scale.get()
        message = self.core.set_baseline(baseline)
        messagebox.showinfo("Info", message)
        self.clear_dynamic_frame()

    def set_bolus(self):
        bolus = self.bolus_scale.get()
        message = self.core.set_bolus(bolus)
        messagebox.showinfo("Info", message)
        self.clear_dynamic_frame()

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

        def on_mouse_down(event):
            self.offset_x = event.x
            self.offset_y = event.y

        def on_mouse_move(event):
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f'+{x}+{y}')

        widget.bind('<Button-1>', on_mouse_down)
        widget.bind('<B1-Motion>', on_mouse_move)


