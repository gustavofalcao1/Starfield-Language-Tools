import tkinter as tk
from tkinter import ttk
from .path import select_directory
from .core import Core

class App:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title('Select Language')

        self.root.geometry('400x300')
        self.root.resizable(False, False)

        self.root.configure(bg='#f5f5f7')

        self.button_frame = tk.Frame(root, bg='#f5f5f7')
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.button_style = ttk.Style()
        self.button_style.configure('TButton',
            background='#007AFF',
            foreground='#FFFFFF',
            borderwidth=1,
            relief='flat',
            padding=(10, 5)
        )
        self.button_style.map('TButton',
            background=[('active', '#0051A8')],
            foreground=[('active', '#FFFFFF')]
        )

        self.button_apply = ttk.Button(self.button_frame, text='Apply', command=self.apply_language)
        self.button_apply.pack(side=tk.LEFT, padx=5)

        self.button_update = ttk.Button(self.button_frame, text='Refresh', command=self.update_language_list)
        self.button_update.pack(side=tk.LEFT, padx=5)

        self.button_reselect = ttk.Button(self.button_frame, text='Select folder', command=self.reselect_directory)
        self.button_reselect.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(root, text='Select a language:', bg='#f5f5f7', font=('Arial', 12))
        self.label.pack(pady=10)

        self.combobox = ttk.Combobox(root, font=('Arial', 12), state='readonly')
        self.combobox.pack(pady=10, fill=tk.X, padx=20)
        self.update_language_list()

        self.style = ttk.Style()
        self.style.configure('TCombobox',
            fieldbackground='#ffffff',
            background='#ffffff',
            bordercolor='#d1d5da',
            borderwidth=1,
            arrowcolor='#007AFF'
        )
        self.style.map('TCombobox',
            fieldbackground=[('readonly', '#ffffff')],
            background=[('readonly', '#ffffff')],
            bordercolor=[('readonly', '#d1d5da')]
        )

        self.message_label = tk.Label(root, text='', fg='green', bg='#f5f5f7', font=('Arial', 12))
        self.message_label.pack(pady=5)

    def apply_language(self):
        selected_language = self.combobox.get()
        if selected_language:
            message = self.core.update_ini_file(selected_language)
            self.show_message(message)
        else:
            self.show_message('No selected language.')

    def update_language_list(self):
        self.combobox['values'] = [] 
        language_files = self.core.list_language_files()
        language_list = [file[len('Starfield_'):-len('.ini')] for file in language_files]
        self.combobox['values'] = language_list

    def reselect_directory(self):
        try:
            new_path = select_directory() 
            self.core = Core(new_path)
            self.update_language_list()
            self.show_message(f'New Select Directoryo: {new_path}')
        except ValueError as e:
            self.show_message(f'Error when selecting directory: {e}')

    def show_message(self, message):
        self.message_label.config(text=message)
