import os
import shutil

# Prompt the user for the directory path to organize files
path = input("Enter path: ")

# List all files in the specified directory
files = os.listdir(path)

# Iterate through each file in the directory
for file in files:
    # Split the filename and extension
    filename, extension = os.path.splitext(file)
    
    # Remove the leading dot from the extension for folder naming
    extension = extension[1:]

    # Check if a directory for the file extension already exists
    if os.path.exists(path + '/' + extension):
        # Move the file to the corresponding extension folder
        shutil.move(path + '/' + file, path + '/' + extension + '/' + file)
    else:
        # If the directory does not exist, create it
        os.makedirs(path + '/' + extension)
        # Move the file to the newly created extension folder
        shutil.move(path + '/' + file, path + '/' + extension + '/' + file)
