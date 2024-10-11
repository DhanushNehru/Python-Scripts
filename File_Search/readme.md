Automated File Explorer:
This Python script searches a specified folder for all files, regardless of file type, within its directory and subdirectories. It outputs the paths of all files found and also lists all unique file extensions present in the folder. The script uses Python's pathlib module, which is cross-platform and simplifies working with file paths.

Features:
File Path Finder: The script scans a folder and lists the file paths of all files it finds within the specified directory and its subdirectories.
Unique File Extension Lister: The script identifies all unique file extensions present in the folder, displaying them in lowercase format.

Requirements: Python 3.x

Set the Folder Path:

Replace 'Place the folder path here under quotes' in the script with the path to the folder you want to scan:
all_files_path = pathlib.Path('path/to/your/folder')

Run the Script:

Save the script as file_finder.py (or another name of your choice).
Open your terminal or command prompt.
Navigate to the folder containing the script and run it with:
python file_finder.py

Output:
The script will output two lists:
The first list contains the paths of all files found within the specified folder and its subdirectories.
The second list contains all unique file extensions in the folder, displayed in lowercase.


Example output:

[  "path/to/folder/document.txt",  "path/to/folder/image.jpg",  "path/to/folder/subfolder/script.py"]
[  ".txt",  ".jpg",  ".py"]
