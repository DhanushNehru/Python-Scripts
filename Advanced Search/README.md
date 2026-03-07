# Advanced Search Tool

<div align="center">

![Version](https://img.shields.io/badge/version-0.5.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

**A powerful Windows GUI application for grep-style searching with advanced regex patterns and metadata search capabilities**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Metadata Search](#metadata-search) • [Contributing](#contributing)

</div>

---

## 📋 Overview

Advanced Search Tool is a modern, high-performance desktop application that brings the power of grep-style pattern searching to Windows users with a beautiful, easy-to-use graphical interface. Search through file contents, image metadata (EXIF/GPS), and document properties (PDF, Office, audio/video files) with powerful regex pattern matching.

## ✨ Features

### Core Functionality
- 🔍 **Powerful Search Engine** - Fast grep-style pattern matching across files and directories
- 📊 **Smart Sorting** - Sort results by path, match count, file size, or modification date (8 sorting options)
- 🎯 **Smart Highlighting** - Yellow highlights for all matches, orange for current match
- 📁 **File Browser** - Integrated file explorer with lazy loading for smooth navigation
- 📊 **Results Tree** - Organized results grouped by file with match counts and line numbers

### Regex & Pattern Matching
- 🔄 **Full Regex Support** - Complete regular expression pattern matching
- 📋 **Regex Pattern Library** - Quick-access popover menu with 8 built-in common regex patterns:
  - Email addresses (`user@domain.com`)
  - URLs (http/https)
  - IPv4 addresses
  - Phone numbers (multiple formats)
  - Dates (various formats)
  - Numbers
  - Hex values (0x... and #...)
  - Words/identifiers
- ✏️ **Custom Pattern Library** - Create, save, and manage your own regex patterns with persistent storage
- ✅ **Pattern Auto-Apply** - Check patterns in menu to instantly apply to your search
- 🔀 **Pattern Combination** - Enable multiple patterns simultaneously

### Metadata Search
- 🖼️ **Image Metadata Search** - Extract and search EXIF, GPS, and PNG metadata from:
  - JPG/JPEG files (EXIF tags, GPS coordinates, camera info)
  - PNG files (text chunks, creation time)
  - TIFF files (comprehensive EXIF data)
  - Other formats: GIF, BMP, WebP
- 📄 **File Metadata Search** - Extract and search properties from:
  - **PDF files**: Title, author, subject, keywords, creator, creation/modification dates
  - **Microsoft Office** (.docx, .xlsx, .pptx): Author, title, subject, keywords, creation/modification dates, document statistics
  - **OpenDocument** (.odt, .ods, .odp): LibreOffice/OpenOffice metadata and properties
  - **Screenwriting** (.fdx, .fountain, .celtx): Final Draft, Fountain format, Celtx projects - title, author, scenes
  - **eBooks** (.epub): Title, author, publisher, language, ISBN from EPUB metadata
  - **Archives** (.zip): File lists, compressed size, contents preview
  - **Structured Data** (.csv, .json, .xml): Headers, keys, schema information
  - **Databases** (.db, .sqlite, .sqlite3): SQLite database schema, table names, column info, row counts
  - **RTF files** (.rtf): Rich Text Format documents - title, author, subject, RTF version
  - **Audio files** (.mp3, .flac, .m4a, .ogg, .wma): Artist, album, title, duration, bitrate
  - **Video files** (.mp4, .avi, .mkv, .mov, .wmv): Video metadata, codec info, duration

### Advanced Search Modes
- 📦 **Archive Content Search** - Search inside ZIP and EPUB files without manual extraction
  - Results displayed as `archive.zip/internal/path/file.txt:line`
  - Supports nested directory structures within archives
  - Automatic text encoding detection
- 🔢 **Binary/Hex Search** - Search binary files using hex patterns
  - Results show byte offsets and hex dumps
  - 32-byte context window (16 bytes before/after match)
  - Useful for firmware, executables, and binary data analysis

### Performance Optimizations
- ⚡ **Multi-threaded Search** - Background search operations don't freeze the UI
- 💾 **File Content Caching** - LRU cache for frequently accessed files
- 📦 **Batch UI Updates** - Efficient result rendering
- 🎚️ **Configurable Limits** - File size limits, max results, cache size
- 🚀 **Smart File Filtering** - Automatic exclusion of binary files and common build directories
- 🌐 **Network Drive Optimization** - Automatic UNC path detection with timeout handling and accessibility caching

### User Interface
- 🎨 **Three-Panel Layout** - File Explorer | Results Tree | Preview Pane
- 🎭 **Modern Design** - Clean, responsive interface with SVG icons
- 📊 **Progress Indicators** - Real-time search progress with file count and status
- 🔽 **Context Dropdown** - Select 0-10 lines of context around matches
- ⌨️ **Keyboard Shortcuts** - Quick navigation and actions

### Persistence & Configuration
- 💾 **Search History** - Auto-complete from previous searches
- ⚙️ **User Preferences** - Customizable settings saved between sessions
- 📁 **Session State** - Remembers last directory and search options
- 🔧 **Flexible Options** - Case sensitivity, whole word, file extensions, context lines

## 🚀 Installation

### Prerequisites
- **Python 3.8 or higher**
- **Windows OS** (tested on Windows 10/11)
- **Git** (for cloning the repository)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/RandyNorthrup/Python-Scripts.git
cd Python-Scripts/Advanced\ Search

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

The following libraries will be installed:

| Library | Version | Purpose |
|---------|---------|---------|
| PySide6 | ≥6.6.0 | Qt6 GUI framework |
| Pillow | ≥10.0.0 | Image metadata (EXIF, GPS) |
| PyPDF2 | ≥3.0.0 | PDF metadata extraction |
| python-docx | ≥1.0.0 | Word document metadata |
| openpyxl | ≥3.1.0 | Excel metadata |
| mutagen | ≥1.47.0 | Audio/video file tags |

**Note:** XML, JSON, CSV, and ZIP support use Python standard library (no extra dependencies)

## 📖 Usage

### Basic Search

1. **Select Directory** - Click on a folder in the left panel (File Explorer)
2. **Enter Pattern** - Type your search term in the search box at the top
3. **Configure Options** - Enable case sensitivity, regex mode, whole word, etc.
4. **Set Context** - Use dropdown to select 0-10 lines of context around matches
5. **Search** - Click "Search" button or press Enter
6. **Browse Results** - Click results in middle panel to preview, double-click to open

### Using Regex Patterns

Click the **"Regex Patterns ▼"** button to open a menu with common regex patterns:

- ✓ **Check patterns** to enable them in your search
- ✅ **Combine multiple patterns** by checking several boxes
- 🗑️ **Clear all patterns** using the "Clear All" option at the bottom
- 🔄 The menu toggles open/close on each click

**Example**: Enable "Email addresses" to find all email addresses in your files without writing regex manually.

### Custom Patterns

Create and save your own regex patterns:

1. Click **"Regex Patterns ▼"** to open the menu
2. Click **"Manage Custom Patterns..."** at the bottom
3. Click **"Add Pattern"** to create a new pattern
4. Enter a name and regex pattern, then click **"Save"**
5. Your custom patterns appear in the menu alongside built-in patterns
6. Check your custom pattern to apply it to searches

### Search Options

| Option | Description | Default |
|--------|-------------|---------|
| **Case Sensitive** | Match exact letter case | Off |
| **Use Regex** | Enable regular expression patterns | Off |
| **Whole Word** | Match complete words only (not partial) | Off |
| **Context** | Lines of context to show around matches | 2 |
| **Extensions** | Filter by file types (e.g., `.py,.txt,.js`) | All files |
| **Search image metadata** | Search EXIF/GPS in JPG, PNG, TIFF, etc. | Off |
| **Search file metadata** | Search properties in PDF, Office, audio/video | Off |
| **Search archive contents** | Search inside ZIP and EPUB files | Off |
| **Binary/hex search** | Search binary files using hex patterns | Off |

### Metadata Search

#### Image Metadata Search

Enable **"Search image metadata"** checkbox to search within image files:

**What it searches:**
- EXIF tags (camera model, settings, software)
- GPS coordinates (latitude, longitude, altitude)
- PNG text chunks (creation time, software)
- File system metadata (creation date, modified date, size)

**Supported formats:** JPG, JPEG, PNG, TIFF, TIF, GIF, BMP, WebP

**Example searches:**
- Camera model: Search for "Canon" to find all Canon photos
- Location: Search for "GPS" to find geotagged images
- Date: Search for "2024" in DateTime tags

#### File Metadata Search

Enable **"Search file metadata"** checkbox to search document properties:

**PDF Files:**
- Title, Author, Subject, Keywords, Creator, Producer
- Creation date, Modification date, Page count

**Microsoft Office (.docx, .xlsx, .pptx):**
- Creator, Title, Subject, Keywords, Category
- Creation date, Modified date
- Document statistics (paragraphs, sheets, etc.)

**OpenDocument (.odt, .ods, .odp):**
- Title, Creator, Subject, Keywords
- LibreOffice/OpenOffice metadata

**Screenwriting Files:**
- **Final Draft (.fdx)**: Title, author, scene count, script metadata
- **Fountain (.fountain)**: Title page metadata, scene headings count
- **Celtx (.celtx)**: Project type, file count

**eBooks (.epub):**
- Title, Author, Publisher, Language, ISBN

**Archives (.zip):**
- File count, compressed size, contents listing

**Structured Data:**
- **CSV**: Column headers, row count
- **JSON**: Keys, structure type, item count
- **XML**: Root tag, namespaces, attributes

**SQLite Databases (.db, .sqlite, .sqlite3):**
- Database schema, table names
- Column names and types
- Row counts per table

**RTF Files (.rtf):**
- Title, Author, Subject
- RTF version, creation date

**Audio Files (.mp3, .flac, .m4a, .ogg, .wma):**
- Artist, Album, Title, Genre, Year
- Duration, Bitrate, Sample rate

**Video Files (.mp4, .avi, .mkv, .mov, .wmv):**
- Title, Artist, Album, Genre
- Duration, Bitrate, Video codec

**Note:** When metadata search is enabled, the tool searches ONLY metadata, not file contents. Disable to search file text content.

### Archive Content Search

Enable **"Search archive contents"** to search inside ZIP and EPUB files:

- Searches text files within archives without extracting
- Results show the full path: `archive.zip/folder/file.txt:line_number`
- Supports nested directory structures
- Works with both .zip and .epub formats

### Binary/Hex Search

Enable **"Binary/hex search"** to search binary files using hexadecimal patterns:

- Enter hex patterns like `48656C6C6F` to search for "Hello" in binary files
- Results display byte offsets and hex dumps
- Shows 16 bytes before and after each match (32-byte context window)
- Useful for firmware analysis, executables, and binary data inspection

### Navigation & Workflow

| Action | Method |
|--------|--------|
| **Sort results** | Use Sort dropdown: Path, Match Count, File Size, Date Modified |
| **Navigate matches** | Use Previous/Next buttons or `Ctrl+Up`/`Ctrl+Down` |
| **Open file** | Double-click result in results tree |
| **Open in VS Code** | Right-click → "Open in VS Code" (if installed) |
| **Copy file path** | Right-click → "Copy Full Path" |
| **View in explorer** | Right-click → "Open Containing Folder" |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Start search |
| `Ctrl+Up` | Previous match |
| `Ctrl+Down` | Next match |
| `Ctrl+Q` | Quit application |
| `F1` | Open help window |

### Preferences

Access preferences via **Menu → Preferences** to configure:

| Setting | Description | Default |
|---------|-------------|---------|
| **Max Search Results** | Limit total results (0 = unlimited) | 0 (unlimited) |
| **Max Preview File Size** | Maximum file size to display in preview pane (MB) | 10 MB |
| **Max Search File Size** | Maximum file size to search through (MB) | 50 MB |
| **File Cache Size** | Number of files to keep in memory cache | 50 files |

**Note:** All preferences are saved automatically and persist between sessions.

## 🏗️ Architecture

```
advanced_search/
├── assets/              # Icons and images
│   ├── icon.ico        # Application icon (Windows)
│   ├── icon.svg        # SVG version of icon
│   ├── chevron_up.svg  # Up arrow icon
│   └── chevron_down.svg # Down arrow icon
├── src/                 # Source code
│   ├── main.py         # Main application & GUI (2,057 lines)
│   ├── search_engine.py # Core search functionality (827 lines)
│   └── __pycache__/    # Python bytecode cache
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT License
└── CONTRIBUTING.md    # Contribution guidelines
```

### Technology Stack
- **GUI Framework:** PySide6 (Qt6) - Modern, cross-platform UI
- **Search Engine:** Python `re` module with multi-threading
- **Image Processing:** Pillow (PIL) for EXIF/GPS extraction
- **Document Parsing:** PyPDF2, python-docx, openpyxl for metadata
- **Media Tags:** Mutagen for audio/video file metadata
- **Threading:** QThread for non-blocking background operations
- **Persistence:** JSON for settings and search history

### Key Components

**MainWindow Class** (`src/main.py`)
- Three-panel UI layout with compact controls
- File browser with lazy loading and drive labels
- Results tree with match grouping and sorting
- Preview pane with syntax highlighting
- Regex pattern menu system with custom pattern editor
- Metadata preview formatting
- Search history management
- Preferences dialog
- Multi-modal Search/Stop button

**SearchEngine Class** (`src/search_engine.py`)
- Multi-threaded file scanning
- Regex pattern compilation and caching
- Image metadata extraction (EXIF, GPS, PNG)
- File metadata extraction (PDF, Office, audio/video, SQLite, RTF)
- Archive content search (ZIP, EPUB)
- Binary/hex pattern search
- Context line extraction
- File filtering and exclusion patterns
- Network drive optimization with timeout handling
- Performance optimizations (file size limits, caching)

## 🛠️ Development

### Running from Source

```bash
# Ensure you're in the project directory
cd advanced_search

# Run the application
python main.py
```

### Code Structure

The application uses a clean separation of concerns:

1. **main.py (entry point)** - Launches the application
2. **src/main.py** - All GUI code and user interactions
3. **src/search_engine.py** - Pure search logic, no GUI dependencies

### Key Design Patterns

- **MVC Pattern** - Separation of search logic from UI
- **Observer Pattern** - Qt signals/slots for event handling
- **Worker Thread Pattern** - QThread for background search operations
- **Lazy Loading** - File browser loads directories on-demand
- **LRU Cache** - File content caching with size limits
- **Multi-modal UI** - Single button for Search/Stop with state tracking

### Adding New Features

To add new metadata sources:

1. Add library import with try/except in `search_engine.py`
2. Add file extensions to `FILE_METADATA_EXTENSIONS` class constant
3. Add extraction logic to `_extract_file_metadata()` method
4. Update README with supported formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Randy Northrup**

## 🙏 Acknowledgments

- SVG Icons created for this project (chevron_up.svg, chevron_down.svg, icon.svg)
- Built with [PySide6](https://wiki.qt.io/Qt_for_Python) - Qt for Python
- Image processing by [Pillow](https://python-pillow.org/)
- PDF parsing by [PyPDF2](https://pypdf2.readthedocs.io/)
- Office document handling by [python-docx](https://python-docx.readthedocs.io/) and [openpyxl](https://openpyxl.readthedocs.io/)
- Audio/video metadata by [Mutagen](https://mutagen.readthedocs.io/)

## 📮 Support

If you encounter any issues or have suggestions, please [open an issue](../../issues).

## ⚠️ Known Limitations

- **Windows only** - Currently designed for Windows (paths, file handling, drive labels)
- **Text encoding** - Files must be text-readable or supported binary formats (images, PDFs, Office docs)
- **Large files** - Very large files (>50MB default) are skipped to prevent slowdown
- **Metadata availability** - Not all files contain metadata; results vary by file type and creation method
- **Network drives** - Network path timeout set to 5 seconds; inaccessible drives are cached

## 📊 Performance Tips

1. **Use file extension filters** - Limit search to specific file types (`.py,.js,.txt`)
2. **Adjust file size limits** - Reduce max file size in preferences for faster searches
3. **Enable metadata search selectively** - Only when needed, as it adds processing overhead
4. **Clear cache periodically** - If experiencing memory issues with large file sets
5. **Use specific regex patterns** - More specific patterns search faster than broad ones
6. **Network drives** - First access may be slow due to accessibility checks; subsequent searches use caching

---

<div align="center">
Made with ❤️ by Randy Northrup
</div>
