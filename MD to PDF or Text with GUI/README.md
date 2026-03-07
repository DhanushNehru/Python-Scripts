# Markdown Converter (PySide6)

A simple Python GUI tool built with **PySide6** that converts Markdown (`.md`) files into **PDF** or **Text** files.  
It provides a clean interface to select the input file, choose the output format, and save it wherever you want.  

---

## Features
- 🖱️ **User-friendly GUI** built with PySide6
- 📂 **File selection dialogs** for choosing input and output files
- 📝 **Markdown → Text** conversion
- 📄 **Markdown → PDF** conversion with **Unicode** support (Chinese, Japanese, Korean, emoji, etc.)
- ❌ Error handling with pop-up dialogs
- ⚡ Option to run **with or without Pandoc**

---

## Requirements

Make sure you have **Python 3.8+** installed.  

Install the required Python packages:
```bash
pip install PySide6 reportlab pypandoc
```

---

## Installing Pandoc (Required for Default Conversion)

This tool uses **pypandoc**, which depends on the Pandoc binary.  
Pandoc must be installed separately on your system.  

### 1. Official Installation Instructions
- Pandoc Official Installation Guide: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

### 2. Windows
- Download the **Windows Installer (.msi)** from the [Pandoc Releases Page](https://github.com/jgm/pandoc/releases)
- Run the installer and let it add Pandoc to your PATH automatically.

### 3. macOS
Using **Homebrew** (recommended):
```bash
brew install pandoc
```
Or download the **macOS package** from the [Pandoc Releases Page](https://github.com/jgm/pandoc/releases)

### 4. Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install pandoc
```
For other Linux distros, check the [Pandoc Install Guide](https://pandoc.org/installing.html) for commands.

---

## Verify Pandoc Installation
After installation, open a terminal or command prompt and run:
```bash
pandoc --version
```
You should see version information for Pandoc.

---

## How to Run

1. Save the script as `markdown_converter.py`.
2. Run the program:
```bash
python markdown_converter.py
```

---

## Usage

1. Click **"Select Markdown File"** in the app window.
2. Choose a `.md` file from your system.
3. Select output type: **PDF** or **Text**.
4. Choose the save location and file name.
5. Done! 🎉  

---

## Unicode Support

- The PDF generation uses **HeiseiMin-W3** font to support a wide range of Unicode characters.
- This ensures **Chinese, Japanese, Korean, and emoji** render correctly in the final PDF.

---

## Running Without Pandoc (Pure Python Option)

If you don’t want to install Pandoc,  
the code can be modified to use Python libraries like **markdown2** or **mistune** for parsing Markdown  
and **ReportLab** for PDF generation.  

This removes the external dependency but keeps full functionality.  

---

## Example Screenshots & GIF Demo (Optional)

You can add screenshots or a short screen recording here to make the README more user-friendly.

---

## License
MIT License – free to use, modify, and share.

---

## Author

Randy Northrup
