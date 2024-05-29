import unittest
from unittest.mock import patch
import tkinter as tk
from project.src.core import Core
from project.src.doctorAPP import DoctorApp

class TestDoctorApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.core = Core()
        cls.app = DoctorApp(cls.root, cls.core)
    
    # 你的测试代码...

if __name__ == '__main__':
    unittest.main()
