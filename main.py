import sys
import os
import tkinter as tk
from bin.path import select_directory
from bin.core import Core
from bin.app import App

def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bin_dir = os.path.join(script_dir, 'bin')
        sys.path.insert(0, bin_dir)

        path = select_directory()
        core = Core(path)

        root = tk.Tk()
        app = App(root, core)
        root.mainloop()

    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    main()
