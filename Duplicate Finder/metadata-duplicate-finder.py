import os
import hashlib
from collections import defaultdict

def find_duplicates(folder_path):
    file_metadata = defaultdict(list)
    
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            metadata = get_file_metadata(file_path)
            if metadata:
                file_metadata[metadata].append(file_path)
    
    duplicates = [files for files in file_metadata.values() if len(files) > 1]
    
    if not duplicates:
        print("No duplicates found.")
    else:
        for index, files in enumerate(duplicates, start=1):
            print(f"\nDuplicate Group {index}:")
            for file in files:
                print(f"  {file}")

def get_file_metadata(file_path):
    try:
        file_size = os.path.getsize(file_path)
        mod_time = os.path.getmtime(file_path)
        file_hash = calculate_file_hash(file_path)
        return (file_size, mod_time, file_hash)
    except (OSError, IOError) as e:
        print(f"Error accessing file {file_path}: {e}")
        return None

def calculate_file_hash(file_path, hash_algo=hashlib.md5):
    try:
        hash_obj = hash_algo()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except (OSError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None



if __name__ == "__main__":
    folder_path = input("Enter the path to the folder to scan for duplicates: ").strip()
    if os.path.isdir(folder_path):
        find_duplicates(folder_path)
    else:
        print("The specified path is not a valid directory.")

