from shutil import move
import os
import json

# Load folder-extension mappings from config.json
def load_config(file='config.json'):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file {file} not found! Using default settings.")
        return {}

# Create folders based on config.json
def create_folders(directory):
    for dir_ in directory:
        try:
            os.mkdir(dir_)
            print(f'{dir_:20} Created')
        except OSError:
            print(f'{dir_:20} Already Exists')

# Determine which folder a file belongs to
def get_folder(ext, directory):
    for folder, extensions in directory.items():
        if ext in extensions:
            return folder
    return 'Other'

# Start moving files based on their extensions
def start(directory):
    for filename in os.listdir():
        if filename != __file__ and filename[0] != '.' and '.' in filename:
            ext = os.path.basename(filename).split('.')[-1]
            folder = get_folder(ext, directory)
            if not os.path.isfile(os.path.join(folder, filename)):
                move(filename, folder)

if __name__ == '__main__':
    config = load_config()  # Load configuration
    create_folders(config)  # Create necessary folders
    start(config)           # Start organizing files
