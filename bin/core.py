import shutil
from datetime import datetime
import os
from .path import Path

class Core:
    def __init__(self, path: Path):
        self.path = path
        self.base_dir = self.path.get_base_dir()
        self.ini_file = self.path.get_ini_file()
        self.backup_dir = self.path.get_backup_dir()

    def list_language_files(self):
        return [f for f in os.listdir(self.base_dir) if f.startswith('Starfield_') and f.endswith('.ini')]

    def update_ini_file(self, selected_language):
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'Starfield_{date_str}.ini')

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        shutil.copy(self.ini_file, backup_file)

        with open(self.ini_file, 'r') as file:
            lines = file.readlines()

        with open(self.ini_file, 'w') as file:
            in_general_section = False
            language_updated = False

            for line in lines:
                if line.strip() == '[General]':
                    in_general_section = True
                    file.write(line)
                    if selected_language != 'en':
                        file.write(f'sLanguage={selected_language}\n')
                        language_updated = True
                elif line.startswith('['):
                    if in_general_section and not language_updated and selected_language != 'en':
                        file.write(f'sLanguage={selected_language}\n')
                        language_updated = True
                    in_general_section = False
                    file.write(line)
                elif in_general_section and line.startswith('sLanguage='):
                    if selected_language == 'en':
                        continue
                    elif not language_updated:
                        file.write(f'sLanguage={selected_language}\n')
                        language_updated = True
                else:
                    file.write(line)

            if in_general_section and not language_updated and selected_language != 'en':
                file.write(f'sLanguage={selected_language}\n')

        return f'Altered language to {selected_language if selected_language != "en" else "English"} and Backup created.'

    def validate_language_file(self, file_name):
        return file_name.startswith('Starfield_') and file_name.endswith('.ini')
    
    def get_current_language(self):
        with open(self.ini_file, 'r') as file:
            for line in file:
                if line.startswith('sLanguage='):
                    return line.strip().split('=')[1].lower()
        return 'en'