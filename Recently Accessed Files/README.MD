# recently_accessed_files

## Introduction

This Python script that extracts the path of recently accessed files in the specified directory.

## Usage

### Prerequisites

Before using this script, ensure you have the following:

- Python installed on your system.
- Required libraries: `os`, `datetime`

### Running the Script

1. Run this script in your terminal.

```python
$ python recently_accessed_files.py
```
2. After running the python script we have to provide the desired directory from which we want to extract the paths.
   
```python
$ Enter the directory path to search:
```
3. Example Output

![Alt text](image-1.png)

### Information about  .py file

1. `get_file_access_time` function
   
- This function provides the time, in seconds since the Unix epoch, when the file was last accessed.
- Args :
    - **file_path**: provided directory path
- Returns:
    - access time

1. `get_recently_accessed_files` function
   
- This function returns a list of recently accessed files in the given directory and its subdirectories, sorted by their access time in descending order.
  
- Args :
    - **directory_path**: The path to the directory to search.
    - **time_threshold**: The time threshold in seconds since the Unix epoch. Only files accessed   after the time threshold will be returned. If `None`, all files will be returned.

- Returns:
    - A list of file paths, sorted by their access time in descending order.

### Output

The script will create a list of recently accessed files.

### Example

  - file1.txt
  - file2.txt
  - file3.txt
  - file4.txt
  - file5.txt
  - file6.txt
<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->