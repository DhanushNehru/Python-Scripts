import os
import shutil

# Prompt the user for the directory path to organize files
path = input("Enter path: ")

# Check if the directory exists
if not os.path.exists(path):
    print("Error: The specified directory does not exist.")
else:
    # List all items in the specified directory
    files = os.listdir(path)

# Iterate through each file in the directory
    for file in files:
        file_path = os.path.join(path, file)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Split the filename and extension
        filename, extension = os.path.splitext(file)
        extension = extension[1:] if extension else "NoExtension"  # Handle files without extensions

        # Destination folder for the extension
        dest_folder = os.path.join(path, extension)

        # Create the directory if it does not exist
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Handle duplicate files by renaming them
        dest_file_path = os.path.join(dest_folder, file)
        counter = 1
        while os.path.exists(dest_file_path):
            newfilename = f"{filename}{counter}.{extension}" if extension != "NoExtension" else f"{filename}_{counter}"
            dest_file_path = os.path.join(dest_folder, new_filename)
            counter += 1

        # Move the file
        shutil.move(file_path, dest_file_path)
        print(f"Moved: {file} → {dest_file_path}")