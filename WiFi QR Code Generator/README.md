# WifiQR

WifiQR is a cross-platform desktop app for generating Wi‑Fi QR codes and exporting Wi‑Fi profiles. Built with PySide6, it provides a modern Qt interface for fast, consistent onboarding across Windows, macOS, and mobile devices.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

## Table of contents
- [Highlights](#highlights)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Run the app](#run-the-app)
- [Usage](#usage)
- [Exports](#exports)
- [Security modes](#security-modes)
- [Saved Networks Table](#saved-networks-table)
- [Save File Format](#save-file-format)
- [Packaging](#packaging)
- [Development](#development)
- [Project layout](#project-layout)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Highlights
- Modern Qt UI with consistent QSS-based styling
- Live QR preview with optional center image embedding
- High error correction QR codes (30% error correction level H)
- Saved networks table with smooth scrolling, search, sorting, and batch export
- Smart column resizing with gap prevention
- Double-click table rows to load networks into the preview
- Windows .cmd export (netsh) and macOS .mobileconfig export
- PNG and PDF export with optional location header
- Portable save format with base64-encoded images
- Full test suite with 100% coverage gate

## Features
- **Network configuration**: SSID, password, security mode, hidden network, and location fields
- **Center image**: Optional image embedding in the QR code center (automatically resized to 100x100px)
- **Live preview**: Real-time QR code generation with payload preview (matches exports and print output)
- **Print support**: Print dialog with proper scaling and layout
- **Export formats**:
  - PNG/PDF with optional location header
  - Windows .cmd scripts for automated deployment
  - macOS .mobileconfig profiles for one-click setup
- **Table management**:
  - In-table editing with combo boxes (Security) and checkboxes (Hidden)
  - Double-click rows to load into preview
  - Password obfuscation with show/hide toggle
  - Centered column headers
  - Uniform sizing for Security and Hidden columns (100px each)
- **Search**: Incremental search with next/previous match navigation
- **Menu bar**: Save, Save As, Load, About, Print, and Export options
- **Portable storage**: All data including images stored in a single JSON file

## Requirements
- Python 3.10+
- PySide6 6.6+
- qrcode 7.4+
- Pillow 10.0+
- CairoSVG 2.7+ (for SVG center images)

## Installation
1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the app and dependencies:

```bash
pip install -e .
```

## Run the app

```bash
wifiqr
```

Or run directly via module:

```bash
python -m wifiqr.app
```

## Usage

### Basic Workflow
1. Enter **Location**, **SSID**, **Password**, and select **Security** type and **Hidden** status.
2. (Optional) Click the **...** button next to Center Image to select an image file (PNG, JPG, JPEG, BMP, GIF, SVG).
3. Use the preview panel to verify the QR code in real-time.
4. Click **Add to Table** to save the network to the Saved Networks table.
5. **Double-click** any row in the table to load that network back into the preview.
6. Export individual networks or use batch export.

### Center Image Feature
- Click the ellipsis (**...**) button to browse for an image
- Supported formats: PNG, JPG, JPEG, BMP, GIF, SVG
- Images are automatically resized to 100x100 pixels
- Images are base64-encoded and stored in the save file for portability
- QR codes use high error correction (Level H - 30%) to ensure scannability with center images
- Center images appear in both preview and all exports (PNG, PDF)
- SVG files are converted to PNG on import for consistent rendering

### Table Interactions
- **Double-click** any row to load that network into the details form and preview
- **Edit in-place**: Click cells to edit Location, SSID; use dropdowns for Security
- **Toggle Hidden**: Click checkbox directly in the Hidden column
- **Password visibility**: Click the eye icon to view/hide passwords
- **Search**: Use Ctrl+F or Edit → Find to search networks
- **Sort**: Click column headers to sort (Location and SSID only)
- **Delete**: Select rows and press Delete key or right-click → Delete

### Export Options
- **PNG/PDF** for printed handouts, signage, or digital sharing
- **Windows .cmd** for scripted profile deployment across Windows machines
- **macOS .mobileconfig** for one-click installation on macOS/iOS devices
- **Batch Export**: Select multiple rows or export all networks at once

## Exports

### QR (PNG/PDF)
- Exports optionally include a location header above the QR code for easy identification.
- Toggle "Show location header" checkbox to enable/disable header (preview matches exports and print).
- PNG is ideal for digital sharing or signage; PDF is optimized for printing.
- QR codes use error correction Level H (30%) for reliable scanning even with center images.
- Center images (if selected) are embedded at 100x100 pixels in the QR code center.

### Windows Script (.cmd)
- Uses Windows netsh command to add Wi-Fi profiles and auto-connect.
- For batch export, a single script is generated containing all saved networks.
- Run the script as Administrator for proper execution.
- Compatible with Windows 7 and later.

### macOS Profile (.mobileconfig)
- Creates a managed Wi‑Fi configuration profile for macOS and iOS.
- For batch export, one profile file is generated containing all networks.
- Install by double-clicking the .mobileconfig file and following system prompts.
- Works on macOS 10.7+ and iOS 5+.

## Security modes
WifiQR accepts several security labels and normalizes them for each export format:
- **WPA/WPA2/WPA3** (encoded as "WPA" for QR payloads, expanded for system profiles)
- **WEP** (legacy encryption, not recommended)
- **None / Open / No Password** (treated as open network)

## Saved Networks Table
- **Centered Headers**: All column headers are centered for visual consistency
- **Smart Column Resizing**: Location, SSID, and Password columns resize independently from the left edge
- **Gap Prevention**: Password column automatically expands to prevent blank space
- **Pinned Columns**: Security and Hidden columns (100px each) stay fixed on the right side
- **Smooth Scrolling**: Horizontal scrolling uses 10-pixel increments for smooth navigation
- **Minimum Widths**: All columns enforce minimum width based on header label size
- **Double-Click Loading**: Double-click any row to load that network into the form and preview

## Save File Format
- Networks are saved as JSON files (.json extension)
- Each network includes: location, SSID, password, security, hidden status, and optional image data
- Images are stored as base64-encoded strings for complete portability
- Single file contains all networks and their images - no external dependencies
- Compatible with Save (Ctrl+S), Save As, and Load (Ctrl+O) operations

## Packaging
WifiQR includes a GitHub Actions workflow that builds:
- Linux executable and .deb package
- Windows executable
- macOS Intel executable

### CI workflow
The workflow is defined in [.github/workflows/build-packages.yml](.github/workflows/build-packages.yml). It runs on tags that start with v and on manual dispatch.

### Local packaging (optional)
You can build a local executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --name wifiqr --onefile --windowed -m wifiqr.app \
  --add-data "src/wifiqr/resources:wifiqr/resources"
```

On Windows, use a semicolon separator:

```bash
pyinstaller --name wifiqr --onefile --windowed -m wifiqr.app \
  --add-data "src/wifiqr/resources;wifiqr/resources"
```

## Development

### Tests
Install test dependencies and run the full test suite:

```bash
pip install -e .[test]
python -m pytest
```

Coverage is enforced at 100%. Tests include:
- UI flow and interaction tests
- QR payload generation and validation
- Export service tests for all formats
- Table widget behavior and editing
- Registry/configuration tests

### Typing and linting
Strict typing and linting are enforced with mypy and ruff:

```bash
pip install -e .[dev]
python -m mypy src tests
python -m ruff check .
```

Configuration uses Python 3.12 target with strict mypy checks enabled.

## Project layout
```
src/wifiqr/
  app.py                  # Application entry point
  constants.py            # Application constants
  ui/
    main_window.py        # Main window UI and logic
  services/
    qr_service.py         # QR code generation
    export_service.py     # Export orchestration
    wifi_payload.py       # QR payload formatting
    windows_script.py     # Windows .cmd generation
    macos_profile.py      # macOS .mobileconfig generation
    wifi_profiles.py      # Profile save/load logic
    xml_utils.py          # XML utilities for macOS profiles
  resources/
    style.qss             # Application stylesheet
tests/
  test_app_ui_flow.py     # UI interaction tests
  test_payload.py         # Payload generation tests
  test_services.py        # Export service tests
  test_ui.py              # UI component tests
  test_registry.py        # Configuration tests
  test_table_save_batch.py # Table and batch tests
  test_preview_updates.py  # Preview update tests
```

## Troubleshooting
- **Preview disabled**: Verify that SSID field is not empty.
- **Export disabled**: Ensure at least one network is in the Saved Networks table.
- **Windows script fails**: Run the .cmd file as Administrator; verify netsh is available.
- **macOS profile not installing**: Open from System Settings → Profiles; check for valid XML format.
- **QR code not scanning**: Ensure adequate contrast and size when printing; test with multiple QR readers. Center images may reduce scannability if too large or complex.
- **QR code with image not scanning**: Try using a simpler image with high contrast, or remove the center image. Error correction Level H supports up to 30% damage/obscuration.
- **Table columns not resizing**: Check that you're dragging from the left edge of column separators.
- **Center image button not visible**: The ellipsis (...) button is embedded inside the Center Image text field on the right side.
- **Image not showing in preview**: Verify the image file format is supported (PNG, JPG, JPEG, BMP, GIF, SVG) and the file is accessible.
- **Saved file won't load**: Ensure the JSON file is valid and hasn't been manually edited with syntax errors.
- **Double-click doesn't load network**: Make sure you're double-clicking on the row, not just selecting it.

## License
MIT
