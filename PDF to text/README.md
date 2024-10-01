# PDF to Text Converter

This project is a Python tool designed to convert PDF files into clean and readable text. It is built to extract text from both local and remote PDFs, perform post-processing to improve readability, and save the formatted content into `.txt` files. The project also includes features for downloading PDFs from URLs and cleaning up the extracted text to prevent issues with line breaks and disorganized spacing.

---

## Features
1. **Text Extraction from Local and Remote PDFs**:
   - Supports PDF files stored locally and PDFs available via URL.
2. **Text Cleaning and Formatting**:
   - Removes unwanted line breaks and excessive spacing.
   - Preserves paragraphs and maintains the original structure.
3. **Saving Extracted Text as `.txt` Files**:
   - The extracted text can be saved as a `.txt` file with the same name as the original PDF.
4. **Automatic Output Folder Creation**:
   - Organizes generated text files into an `output_texts` folder for easy navigation and future use.

## Requirements

Make sure to have the following libraries installed:

- `requests`
- `PyPDF2`

If you do not have them yet, install them using:

```bash
pip install requests PyPDF2
