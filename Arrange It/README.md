# Arrange It

With the help of this script, files can be moved automatically to the folder that corresponds to their extension (for example, .jpg or .png files go to the /Pictures folder, and .mp4 files go to /Videos).

## New Feature: Custom Folder Configuration

Now, you can customize how files are arranged by defining your own folder structure and file extensions using a config.json file. This allows for more flexibility without needing to modify the Python code itself.
`python arrangeit.py`

# How To Use the config.json File

1. The config.json file contains the mappings of file extensions to folder names.
2. You can modify, add, or remove folder categories and file extensions as per your needs.

Example config.json:

```bash
{
  "Programming Files": ["ipynb", "py", "java", "cs", "js"],
  "Music": ["mp3", "wav", "aac"],
  "Videos": ["mp4", "mkv", "avi"],
  "Pictures": ["jpeg", "png", "gif"],
  "Documents": ["pdf", "docx", "xlsx"]
}
```

# How To Run

Put the script and the config.json file in the folder where you want to automatically move the files.

Run the following command from the terminal:

```bash
python arrangeit.py
```

The script will create folders and move files based on the folder-extension mappings in the config.json file.


# Benefits

**Customizable:** Easily modify the config.json file to tailor the organization to your preferences.

**User-Friendly:** No need to modify Python code—just update the config.json file.

**Scalable:** Works with different folder structures for different use cases.
