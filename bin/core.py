import os
from .path import Path

class Core:
    def __init__(self, path: Path):
        self.path = path
        self.base_dir = self.path.get_base_dir()
        self.ini_file = self.path.get_ini_file()

    def list_language_files(self):
        return [f for f in os.listdir(self.base_dir) if f.startswith('Starfield_') and f.endswith('.ini')]

    def update_ini_file(self, selected_language):
        with open(self.ini_file, 'r') as file:
            lines = file.readlines()

        with open(self.ini_file, 'w') as file:
            in_general_section = False
            language_updated = False

            for line in lines:
                if line.strip() == '[General]':
                    in_general_section = True
                    file.write(line)
                    if not language_updated:
                        file.write(f'sLanguage={selected_language}\n')
                        language_updated = True
                elif line.startswith('['):
                    if in_general_section:
                        in_general_section = False
                    file.write(line)
                elif line.startswith('sLanguage='):
                    if not language_updated:
                        file.write(f'sLanguage={selected_language}\n')
                        language_updated = True
                else:
                    file.write(line)

            if not language_updated and in_general_section:
                file.write(f'sLanguage={selected_language}\n')
        
        return f'Altered language to {selected_language.upper()}.'

    def remove_language_entry(self):
        with open(self.ini_file, 'r') as file:
            lines = file.readlines()

        with open(self.ini_file, 'w') as file:
            in_general_section = False

            for line in lines:
                if line.strip() == '[General]':
                    in_general_section = True
                    file.write(line)
                elif line.startswith('['):
                    if in_general_section:
                        in_general_section = False
                    if line.startswith('sLanguage='):
                        continue
                    file.write(line)
                else:
                    if in_general_section and line.startswith('sLanguage='):
                        continue
                    file.write(line)
        
        return 'Altered language to EN.'

    def validate_language_file(self, file_name):
        return file_name.startswith('Starfield_') and file_name.endswith('.ini')

    def get_current_language(self):
        with open(self.ini_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.strip().startswith('sLanguage='):
                return line.strip().split('=')[1]
        return 'en'
