import os
import tkinter as tk
from tkinter import filedialog

class Path:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_base_dir(self):
        return self.base_dir

    def get_ini_file(self):
        return os.path.join(self.base_dir, 'Starfield.ini')

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select the base directory")
    if directory:
        return Path(directory)
    else:
        raise ValueError("No selected directory.")
