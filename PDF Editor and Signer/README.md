# PDF Editor and Signer

A sophisticated PDF editor with intelligent element detection, click-to-place text insertion, and digital signature capabilities built with PySide6 and PyMuPDF.

## Features

### Intelligent Element Detection
- **Automatic Detection**: The application automatically detects interactive elements in your PDF:
  - **Horizontal Lines**: Text fields and underlines (green highlight)
  - **Signature Fields**: Areas with "signature" keywords (blue highlight)
  - **Date Fields**: Areas with "date" keywords (red highlight)
- **Visual Feedback**: Detected elements are highlighted when you hover nearby
- **No Manual Controls**: Detection is always active - no buttons needed

### Click-to-Place Text Insertion
- **Smart Placement**: Click near any detected element (within 50 pixels) to add text
- **Type-Aware Formatting**:
  - Signature fields: Italic script font style
  - Date fields: Auto-filled with current date (MM/DD/YYYY)
  - Text lines: Standard font
  - Freeform: Standard font anywhere on the page
- **Auto-Focus**: Text boxes automatically receive focus when created
- **Auto-Remove**: Empty text boxes disappear when you click away
- **Intuitive UX**: Just click where you want to type - the app handles the rest

### Selectable Text Overlay
- **Native Selection**: Select and copy text directly from the PDF view
- **Transparent Layer**: Text overlay doesn't interfere with visual appearance
- **Preserved Layout**: Text positioned exactly as it appears in the PDF

### Zoom Controls
- **Zoom Slider**: 50% to 400% zoom range
- **Zoom Buttons**: +/- buttons for incremental zoom (10% steps)
- **Fit Width**: Automatically fit PDF to window width
- **Fit Page**: Automatically fit entire page in view
- **Zoom-Aware Coordinates**: Text placement accounts for current zoom level

### Digital Signatures
- **Certificate Management**:
  - Create new certificates with RSA 2048-bit keys
  - Load existing certificate and key files
  - X.509 format with SHA-256 hashing
- **PDF Signing**: Apply digital signatures to edited PDFs
- **Signature Validation**: Digitally signed documents maintain integrity

## Installation

### Requirements
- Python 3.7+
- PySide6 (Qt6 GUI framework)
- PyMuPDF (PDF rendering and manipulation)
- pyHanko (digital signatures)
- cryptography (certificate generation)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PySide6>=6.0.0 PyMuPDF>=1.23.0 pyHanko>=0.20.0 cryptography>=41.0.0
```

## Usage

### Run the Application

```bash
python pdf_editor_signer.py
```

### Workflow

1. **Open PDF**: Click "Open PDF" to load a document
2. **Navigate**: Use page navigation controls or enter page number directly
3. **Add Text**:
   - Click near a detected line, signature field, or date field
   - The text box appears automatically at the correct location
   - Type your text (dates auto-fill)
   - Click elsewhere when done (empty boxes disappear)
4. **Zoom**: Use zoom controls to adjust view as needed
5. **Select Text**: Select and copy text directly from the PDF
6. **Save**: Click "Save PDF" to save your edits
7. **Sign** (optional):
   - Create or load a certificate
   - Click "Sign PDF" to apply digital signature

### Text Box Types

The application automatically determines the text box type based on what you click:

- **Text Line**: Click near a horizontal line (green highlight)
- **Signature**: Click near a signature keyword (blue highlight)
- **Date**: Click near a date keyword (red highlight)
- **Freeform**: Click anywhere else on the page

### Certificate Management

**Create Certificate**:
1. Click "Create Certificate"
2. Enter details (Country, Organization, Common Name, etc.)
3. Certificate and key files saved in current directory

**Load Certificate**:
1. Click "Load Certificate"
2. Select certificate file (.pem)
3. Select key file (.pem)
4. Certificate loaded for signing

## Architecture

### Graphics System
- **Z-Layering**:
  - Z-Level -2: Selectable text overlay (transparent)
  - Z-Level -1: Element detection highlights
  - Z-Level 0: User-created text boxes
- **Coordinate Conversion**: Automatic conversion between Qt scene coordinates and PDF coordinates

### Detection Algorithm
- **Line Detection**: Analyzes PDF drawings for horizontal rectangles (<5px height, >50px width)
- **Text Pattern Matching**: Searches text blocks for "signature" and "date" keywords
- **Distance Calculation**: Finds nearest detected element within 50-pixel threshold

### Type Safety
- Full type annotations throughout codebase
- Strict mypy compliance
- Qt type hints for all widgets and events

## File Structure

```
PDF Editor and Signer/
├── pdf_editor_signer.py    # Main application (~1200 lines)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technical Details

### Text Box Styling
- **Signature**: `font-style: italic; font-family: 'Brush Script MT', cursive;`
- **Date**: Auto-filled with current date on creation
- **Standard**: Default font, adjustable size
- **Border**: Yellow border for all editable boxes

### PDF Manipulation
- **Rendering**: PyMuPDF (fitz) converts pages to QPixmap
- **Text Extraction**: `page.get_text("dict")` provides text with bounding boxes
- **Drawing Detection**: `page.get_drawings()` provides vector graphics data
- **Text Insertion**: Applied to PDF with zoom-aware coordinate conversion

### Digital Signatures
- **Key Algorithm**: RSA 2048-bit
- **Certificate Format**: X.509
- **Hash Algorithm**: SHA-256
- **Signing Backend**: pyHanko with cryptography library

## Known Limitations

- Element detection works best with text-based PDFs (may not detect elements in scanned/image PDFs)
- Signature detection requires text containing "signature" keyword
- Date detection requires text containing "date" keyword
- Custom detection patterns not currently configurable

## Contributing

Contributions welcome! Areas for enhancement:
- OCR integration for scanned PDFs
- Configurable detection patterns
- Custom text box styles
- Annotation tools (highlighting, shapes)
- Form field recognition

## License

[Add your license here]

## Credits

Built with:
- [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt6 Python bindings
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing
- [pyHanko](https://github.com/MatthiasValvekens/pyHanko) - PDF signing
- [cryptography](https://cryptography.io/) - Cryptographic operations
