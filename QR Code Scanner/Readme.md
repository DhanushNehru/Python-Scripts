# QR Code Scanner Script

This script enables users to scan and decode QR codes from image files (PNG and JPG formats). It uses OpenCV and Pyzbar for decoding QR codes and provides a simple file dialog for selecting images on your local machine.

## Requirements

To run this script, you'll need Python 3.x installed on your machine. The required libraries are listed in `requirements.txt`, including:

- **opencv-python**: For image processing.
- **pyzbar**: For decoding QR codes.
- **Pillow**: Required for handling image formats.
- **tk**: Provides a file dialog for image selection.

## Installation

1. **Clone the repository** (or download the script and `requirements.txt` directly):
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. **Install dependencies:**(Run the following command to install the necessary libraries from `requirements.txt`:)

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the script** (Execute the QR code scanner script using:)
   ```bash
   python qr_code_scanner.py
   ```
2. **Select an Image**
   - A file dialog will open, allowing you to select a PNG or JPG image containing a QR code.
   - Once an image is selected, the script will attempt to decode any QR code present in the image.
3. **View the Output**
   - If a QR code is detected, its contents will be displayed in the terminal.

## Requirements.txt File

The `requirements.txt` file lists all dependencies for the QR code scanner script. This file ensures that the correct versions of each library are installed to avoid compatibility issues. Libraries in `requirements.txt` include:

```bash
opencv-python
pyzbar
Pillow
tk
```

Make sure to install these libraries by running pip install -r `requirements.txt` before using the script.

## License
