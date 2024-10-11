# OCR Text Extractor

## Overview
**OCR Text Extractor** is a Python application that allows users to extract text from images using Optical Character Recognition (OCR) via the Tesseract engine. The application provides a simple and user-friendly graphical interface for uploading images, capturing full-screen screenshots, or pasting images from the clipboard to extract text.

## Features
- **Select Image File**: Choose an image from your computer to extract text from. Supported formats include `.png`, `.jpg`, `.jpeg`, and `.bmp`.
- **Paste Image from Clipboard**: Take a partial screenshot (e.g., using Windows + Shift + S) and extract text from the image saved in the clipboard.
- **Capture Full Screen Screenshot**: Capture a screenshot of your entire screen and extract text from it.

## Requirements
To run this application, you need to have the following installed:

- Python 3.x
- The following Python packages:
  - `pytesseract` (Download Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki and Add to Environment Path) 
  - `Pillow` (Python Imaging Library, a fork of PIL)
  - `Tkinter` (comes pre-installed with Python on most systems)

### Installation of Required Packages
You can install the required packages using pip:

```bash
pip install pytesseract Pillow
```

### How to Run
```bash
python main.py
```
