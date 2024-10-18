import os
import re

# Prompt the user for the directory path where files need to be renamed
directory = input("Enter path: ")

# Provide instructions on how to use regex for searching specific files
print("To look for specific files, enter what you know, using .* for any characters you don't know.")
print("For example: IMG.* will filter files that start with IMG")

# Get the regex pattern to match files and the new base name for renaming
pattern = input("Enter pattern: ")
new_name = input("Enter the new name: ")

def rename_files(directory, pattern, new_name):
    # List all files in the specified directory
    files = os.listdir(directory)
    counter = 0  # Initialize a counter for unique naming

    # Iterate over each file in the directory
    for file in files:
        # Check if the file matches the given pattern
        if re.match(pattern, file):
            # Get the file extension
            filetype = file.split('.')[-1]
            # Rename the file with the new base name and counter
            os.rename(directory + '/' + file, directory + '/' + new_name + str(counter) + '.' + filetype)
            counter += 1  # Increment the counter for the next file

# Call the function to rename files
rename_files(directory, pattern, new_name)
