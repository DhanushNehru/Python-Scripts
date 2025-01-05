# Image to WebP Converter

This repository contains two Python scripts for converting images to WebP format. One script is for command-line usage, and the other provides a graphical user interface (GUI) for easier interaction.

## Files

1. `image_to_webp.py`: A command-line tool for converting images to WebP format.
2. `image_to_webp_gui.py`: A GUI tool for converting images to WebP format.

## Requirements

- Python 3.x
- Pillow library
- Tkinter library (for the GUI tool)

You can install the required libraries using pip:

```sh
pip install Pillow
```

Tkinter is included with standard Python installations. If you encounter issues, you may need to install it separately.

## Usage

### Command-Line Tool

The `image_to_webp.py` script allows you to convert images to WebP format using the command line.

#### Arguments

- `files`: Paths to the image files to convert.
- `save_directory`: Directory to save the converted WebP images.
- `quality`: Quality of the output WebP images (1-100).

#### Example

```sh
python image_to_webp.py image1.jpg image2.png /path/to/save/directory 80
```

### GUI Tool

The `image_to_webp_gui.py` script provides a graphical user interface for converting images to WebP format.

#### Steps

1. Run the script:

    ```sh
    python image_to_webp_gui.py
    ```

2. A file dialog will appear to select multiple image files.
3. Another dialog will appear to select the directory to save the converted WebP images.
4. A dialog will prompt you to enter the quality of the output WebP images (1-100).
5. The images will be converted and saved to the specified directory.

