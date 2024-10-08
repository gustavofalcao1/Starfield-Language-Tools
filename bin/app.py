import tkinter as tk
from tkinter import ttk
from .path import select_directory
from .core import Core
import os

class App:
    def __init__(self, root, core):
        self.core = core
        self.root = root
        self.root.title('Select Language')

        self.root.geometry('400x350')
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

        self.language_map = {
            'de': 'Deutsch',
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'it': 'Italiano',
            'jp': '日本語',
            'pl': 'Polski',
            'ptbr': 'Português-Brasil',
            'zhhans': '简体中文'
        }

        self.update_language_list()
        self.preselect_language()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def apply_language(self):
        selected_language_display = self.combobox.get()
        selected_language_code = self.get_language_code(selected_language_display)
        if selected_language_code:
            if selected_language_code == 'en':
                message = self.core.remove_language_entry()
            else:
                message = self.core.update_ini_file(selected_language_code)
            self.show_message(message)
        else:
            self.show_message('No selected language.')

    def update_language_list(self):
        self.combobox['values'] = []

        language_files = self.core.list_language_files()
        existing_languages = [file[len('Starfield_'):-len('.ini')] for file in language_files]

        all_languages = list(self.language_map.keys())
        for code in all_languages:
            if code != 'en':
                file_name = f'Starfield_{code}.ini'
                file_path = os.path.join(self.core.base_dir, file_name)
                if not os.path.exists(file_path):
                    self.create_language_file(code)
        
        all_languages_display = [self.language_map.get(lang, lang) for lang in all_languages]
        self.combobox['values'] = all_languages_display

    def preselect_language(self):
        current_language_code = self.core.get_current_language()
        display_name = self.language_map.get(current_language_code, 'English')
        self.combobox.set(display_name)

    def create_language_file(self, language_code):
        file_name = f'Starfield_{language_code}.ini'
        file_path = os.path.join(self.core.base_dir, file_name)
        with open(file_path, 'w') as file:
            if language_code == 'en':
                file.write(f"[General]\n\n[Archive]\n")
            else:
                file.write(f"[General]\nsLanguage={language_code}\n\n[Archive]\nsResourceLocaleVoiceList=Starfield - Voices_{language_code}01.ba2, Starfield - Voices_{language_code}02.ba2, Starfield - Voices_{language_code}_Patch.ba2")

    def get_language_code(self, display_name):
        for code, name in self.language_map.items():
            if name == display_name:
                return code
        return display_name

    def reselect_directory(self):
        try:
            new_path = select_directory()
            self.core = Core(new_path)
            self.update_language_list()
            self.show_message(f'New Select Directory: {new_path}')
        except ValueError as e:
            self.show_message(f'Error when selecting directory: {e}')

    def show_message(self, message):
        self.message_label.config(text=message)

    def on_closing(self):
        self.root.quit()
        self.root.destroy()
