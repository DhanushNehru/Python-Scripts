# PNG/SVG to Icon Converter (GUI)

A simple Python GUI tool to convert PNG and SVG images into icon formats for Windows (.ico), macOS (.icns), and Linux (multiple PNG sizes). Built with PySide6, Pillow, and CairoSVG.

---


## Features
- 🖼️ Select a PNG or SVG file and convert it to:
  - Windows .ico (user-selectable sizes)
  - macOS .icns
  - Linux PNG icons (user-selectable sizes)
- ☑️ Checkboxes to select which icon sizes to output
- 📂 Choose output directory
- ⚡ Fast, one-click conversion
- ❌ Error handling with pop-up dialogs

---

## Requirements


- Python 3.8+
- PySide6
- Pillow
- CairoSVG (for SVG support)

Install dependencies:
```bash
pip install PySide6 Pillow cairosvg
```

---

## How to Use

1. Run the script:
   ```bash
   python png2icon.py
   ```
2. Click **"Select PNG and Convert"**
3. Choose a PNG or SVG file
4. Select a directory to save the icons
5. Icons for Windows, macOS, and Linux will be created in the chosen folder, in the sizes you selected

---

## Author

Randy Northrup

---

## License
MIT License – free to use, modify, and share.
