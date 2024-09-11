# Emoji PDF Generator

This script generates a PDF with an emoji using a custom TrueType font.

## Requirements

- Python 3.x
- `reportlab` library

## Installation

1. Install the `reportlab` library if you haven't already:

    ```sh
    pip install reportlab
    ```

2. Download a valid `.ttf` font file that supports emojis and place it in the specified directory. For example, you can use the "Noto Emoji" font from [Google Fonts](https://fonts.google.com/).

## Usage

1. Update the `font_path` variable in the script to point to your downloaded `.ttf` file.

    ```python
    font_path = "/path/to/your/valid/Emoji.ttf"  # Replace with the path to your emoji font
    ```

2. Run the script:

    ```sh
    python emoji.py
    ```

## Disclaimer

Always backup your data before using scripts that modify files. The author is not responsible for any data loss.


<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->