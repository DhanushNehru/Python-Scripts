import os
import uuid

# Initialize a list to store files containing the keyword
contains = []

# Generate a unique identifier for this search session (not currently used)
id_ = uuid.uuid4()

# List of file extensions to search within
extensions = [".txt", ".docx", ".pdf"]

def change_direct():
    # Prompt the user to enter the directory path
    path = input("Enter path: ")
    # Prompt the user to enter the keyword or phrase to search for
    keyword = input("Keyword/Phrase: ")
    # Start searching the specified folder
    search_folder(path, keyword)

def search_folder(path, keyword):
    global contains  # Declare the global variable to store found files
    # Check if the given path is a directory
    if os.path.isdir(path):
        # List all files and directories in the specified path
        files = os.listdir(path)
        # Iterate over each file in the directory
        for file in files:
            # Construct the full path to the file or directory
            full_path = os.path.join(path, file)

            # If the current path is a directory, recursively search inside it
            if os.path.isdir(full_path):
                search_folder(full_path, keyword)
            else:
                # Get the file extension and convert it to lowercase
                filetype = os.path.splitext(file)[-1].lower()
                # Check if the file type is in the allowed extensions
                if filetype in extensions:
                    try:
                        # Open the file and read its content
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as file_:
                            # Check if the keyword is found in the file content
                            if keyword in file_.read():
                                contains.append(file)  # Add the file to the list of found files
                                print(keyword, "found in", file)  # Print the result
                    except Exception as e:
                        # Print any errors encountered while reading the file
                        print(f"Error reading {full_path}: {e}")
    else:
        # Print an error message if the provided path is not a directory
        print(f"{path} is not a directory.")

# Start the process by calling the change_direct function
change_direct()
