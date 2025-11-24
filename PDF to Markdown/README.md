# PDF to Markdown Converter

A Python script that intelligently converts PDF files to Markdown format. The script automatically detects whether a PDF is text-based or image-based and applies the appropriate conversion method.

## Features

- **Smart Detection**: Automatically identifies if a PDF contains text or images
- **Text PDF Conversion**: Extracts text directly from text-based PDFs
- **Image PDF Conversion**: Uses OCR (Optical Character Recognition) to extract text from image-based PDFs
- **Batch Processing**: Converts multiple PDF files at once
- **Vietnamese Language Support**: Includes Vietnamese OCR support

## Requirements

- Python 3.x
- pytesseract
- Pillow (PIL)
- markitdown
- pdf2image
- Tesseract OCR (installed separately)
- Poppler (installed separately)

## Installation

1. Install Python dependencies:
```bash
pip install pytesseract Pillow markitdown pdf2image
```

2. Install Tesseract OCR from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

3. Install Poppler from [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)

4. Update the paths in the script:
   - `tesseract_cmd`: Path to your Tesseract executable
   - `poppler_path`: Path to your Poppler bin folder
   - `data_folder`: Folder containing your PDF files
   - `output_folder`: Folder where Markdown files will be saved

## Usage

1. Place your PDF files in the data folder
2. Run the script:
```bash
python PDFtoMD.py
```

3. Find converted Markdown files in the output folder

## How It Works

1. The script scans the data folder for PDF files
2. For each PDF, it detects whether it's text-based or image-based
3. Text PDFs are converted directly using MarkItDown
4. Image PDFs are converted using OCR with pytesseract
5. Output is saved as `.md` files with the same name as the input PDF

## License

This project is open source and available under the MIT License.
