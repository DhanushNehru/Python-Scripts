"""
Main GUI application for Advanced Search
"""
import sys
import os
import re
import json
import string
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem, QTextEdit, QLineEdit,
    QSplitter, QLabel, QCheckBox, QSpinBox,
    QProgressBar, QStatusBar, QMessageBox, QMenu, QComboBox,
    QDialog, QFormLayout, QDialogButtonBox, QTabWidget, QGridLayout
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor, QAction, QIcon
from .search_engine import SearchEngine, SearchMatch


class PreferencesDialog(QDialog):
    """Preferences dialog window"""
    
    def __init__(self, parent, preferences):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.preferences = preferences.copy()
        
        # Create layout
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # Max results
        self.max_results_input = QSpinBox()
        self.max_results_input.setRange(0, 1000000)
        self.max_results_input.setValue(preferences['max_results'])
        self.max_results_input.setSpecialValueText("Unlimited")
        self.max_results_input.setToolTip("Maximum search results to return (0 = unlimited)")
        form.addRow("Max Search Results:", self.max_results_input)
        
        # Max preview file size
        self.max_preview_size_input = QSpinBox()
        self.max_preview_size_input.setRange(1, 1000)
        self.max_preview_size_input.setValue(preferences['max_preview_file_size_mb'])
        self.max_preview_size_input.setSuffix(" MB")
        self.max_preview_size_input.setToolTip("Maximum file size to display in preview")
        form.addRow("Max Preview File Size:", self.max_preview_size_input)
        
        # Max search file size
        self.max_search_size_input = QSpinBox()
        self.max_search_size_input.setRange(1, 1000)
        self.max_search_size_input.setValue(preferences['max_search_file_size_mb'])
        self.max_search_size_input.setSuffix(" MB")
        self.max_search_size_input.setToolTip("Maximum file size to search through")
        form.addRow("Max Search File Size:", self.max_search_size_input)
        
        # Max cache size
        self.max_cache_input = QSpinBox()
        self.max_cache_input.setRange(0, 500)
        self.max_cache_input.setValue(preferences['max_cache_size'])
        self.max_cache_input.setSpecialValueText("Disabled")
        self.max_cache_input.setToolTip("Maximum number of files to cache in memory")
        form.addRow("File Cache Size:", self.max_cache_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.resize(400, 250)
    
    def get_preferences(self):
        """Get updated preferences from dialog"""
        return {
            'max_results': self.max_results_input.value(),
            'max_preview_file_size_mb': self.max_preview_size_input.value(),
            'max_search_file_size_mb': self.max_search_size_input.value(),
            'max_cache_size': self.max_cache_input.value()
        }


class HelpDialog(QDialog):
    """Comprehensive help dialog window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Help - Advanced Search Tool")
        self.setModal(False)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create tab widget for different help sections
        tabs = QTabWidget()
        
        # Overview tab
        overview_text = QTextEdit()
        overview_text.setReadOnly(True)
        overview_text.setHtml("""
        <h2>Advanced Search Tool - Overview</h2>
        <p>A powerful grep-style search application for Windows with advanced features including regex patterns, 
        metadata search, and result sorting.</p>
        
        <h3>Quick Start</h3>
        <ol>
            <li>Select a directory or file in the <b>File Explorer</b> (left panel)</li>
            <li>Enter your search pattern in the search box</li>
            <li>Configure search options (case sensitive, regex, whole word, etc.)</li>
            <li>Click <b>Search</b> or press <b>Enter</b></li>
            <li>View results in the middle panel, preview on the right</li>
        </ol>
        
        <h3>Three-Panel Layout</h3>
        <ul>
            <li><b>Left Panel:</b> File Explorer - Navigate directories and select search locations</li>
            <li><b>Middle Panel:</b> Results Tree - Shows files with matches and match counts</li>
            <li><b>Right Panel:</b> Preview Pane - Displays file content with highlighted matches</li>
        </ul>
        """)
        tabs.addTab(overview_text, "Overview")
        
        # Search Options tab
        options_text = QTextEdit()
        options_text.setReadOnly(True)
        options_text.setHtml("""
        <h2>Search Options</h2>
        
        <h3>Basic Options</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Option</th><th>Description</th></tr>
            <tr><td><b>Case Sensitive</b></td><td>Match exact letter case (A ≠ a)</td></tr>
            <tr><td><b>Use Regex</b></td><td>Enable regular expression pattern matching</td></tr>
            <tr><td><b>Whole Word</b></td><td>Only match complete words, not partial matches</td></tr>
            <tr><td><b>Context Lines</b></td><td>Show 0-10 lines before/after each match</td></tr>
            <tr><td><b>File Extensions</b></td><td>Filter by file types (e.g., .py,.txt,.js)</td></tr>
        </table>
        
        <h3>Metadata Search</h3>
        <p><b>Search Image Metadata:</b> Search EXIF, GPS, and PNG metadata in JPG, PNG, TIFF, GIF, BMP, WebP files</p>
        <p><b>Search File Metadata:</b> Search properties in documents, audio, video, archives, and structured data:</p>
        <ul>
            <li><b>Documents:</b> PDF, Word, Excel, PowerPoint, OpenDocument, eBooks, RTF</li>
            <li><b>Screenwriting:</b> Final Draft (.fdx), Fountain (.fountain), Celtx (.celtx)</li>
            <li><b>Archives:</b> ZIP, EPUB</li>
            <li><b>Structured Data:</b> CSV, JSON, XML</li>
            <li><b>Databases:</b> SQLite (.db, .sqlite, .sqlite3) - schema and table info</li>
            <li><b>Media:</b> Audio (MP3, FLAC, M4A, OGG, WMA) and Video (MP4, AVI, MKV, MOV, WMV)</li>
        </ul>
        <p><b>Note:</b> When metadata search is enabled, ONLY metadata is searched, not file contents.</p>
        
        <h3>Advanced Search Modes</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Mode</th><th>Description</th></tr>
            <tr><td><b>Search in Archives</b></td><td>Search inside ZIP and EPUB files without extraction. Results show as "archive.zip/internal/path.txt"</td></tr>
            <tr><td><b>Binary/Hex Search</b></td><td>Search binary files for hex patterns. Results show byte offsets and hex dumps</td></tr>
        </table>
        
        <h3>Result Sorting</h3>
        <p>Use the Sort dropdown to organize results by:</p>
        <ul>
            <li>Path (A-Z or Z-A)</li>
            <li>Match Count (High-Low or Low-High)</li>
            <li>File Size (Large-Small or Small-Large)</li>
            <li>Date Modified (Newest or Oldest)</li>
        </ul>
        """)
        tabs.addTab(options_text, "Search Options")
        
        # Regex Patterns tab
        regex_text = QTextEdit()
        regex_text.setReadOnly(True)
        regex_text.setHtml("""
        <h2>Regex Patterns</h2>
        
        <h3>Using the Regex Patterns Menu</h3>
        <p>Click the <b>"Regex Patterns ▼"</b> button to access common regex patterns:</p>
        <ol>
            <li>Click the button to open the patterns menu</li>
            <li>Check one or more patterns to enable them</li>
            <li>The search box will update with the combined pattern</li>
            <li>Uncheck patterns or click "Clear All" to reset</li>
        </ol>
        
        <h3>Available Patterns</h3>
        <table border="1" cellpadding="5" cellspacing="0" width="100%">
            <tr><th>Pattern</th><th>Description</th><th>Example Matches</th></tr>
            <tr><td><b>Email Addresses</b></td><td>Standard email format</td><td>user@example.com</td></tr>
            <tr><td><b>URLs</b></td><td>HTTP/HTTPS web addresses</td><td>https://example.com</td></tr>
            <tr><td><b>IPv4 Addresses</b></td><td>IP addresses</td><td>192.168.1.1</td></tr>
            <tr><td><b>Phone Numbers</b></td><td>Various phone formats</td><td>(555) 123-4567</td></tr>
            <tr><td><b>Dates</b></td><td>Various date formats</td><td>2024-01-15, 01/15/2024</td></tr>
            <tr><td><b>Numbers</b></td><td>Integer numbers</td><td>123, 4567</td></tr>
            <tr><td><b>Hex Values</b></td><td>Hexadecimal notation</td><td>0xFF, #A3B5C7</td></tr>
            <tr><td><b>Words/Identifiers</b></td><td>Programming identifiers</td><td>variable_name, camelCase</td></tr>
        </table>
        
        <h3>Custom Regex</h3>
        <p>Enable <b>"Use Regex"</b> checkbox and enter your own regular expression patterns.</p>
        <p><b>Common Regex Syntax:</b></p>
        <ul>
            <li><b>.</b> - Any character</li>
            <li><b>*</b> - Zero or more of previous</li>
            <li><b>+</b> - One or more of previous</li>
            <li><b>?</b> - Zero or one of previous</li>
            <li><b>[abc]</b> - Any of a, b, or c</li>
            <li><b>[a-z]</b> - Any lowercase letter</li>
            <li><b>\\d</b> - Any digit</li>
            <li><b>\\w</b> - Any word character</li>
            <li><b>^</b> - Start of line</li>
            <li><b>$</b> - End of line</li>
        </ul>
        """)
        tabs.addTab(regex_text, "Regex Patterns")
        
        # Keyboard Shortcuts tab
        shortcuts_text = QTextEdit()
        shortcuts_text.setReadOnly(True)
        shortcuts_text.setHtml("""
        <h2>Keyboard Shortcuts</h2>
        
        <h3>Search & Navigation</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Shortcut</th><th>Action</th></tr>
            <tr><td><b>Enter</b></td><td>Start search (when in search box)</td></tr>
            <tr><td><b>Ctrl+Up</b></td><td>Go to previous match in preview</td></tr>
            <tr><td><b>Ctrl+Down</b></td><td>Go to next match in preview</td></tr>
        </table>
        
        <h3>Application</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Shortcut</th><th>Action</th></tr>
            <tr><td><b>Ctrl+Q</b></td><td>Quit application</td></tr>
        </table>
        
        <h3>Mouse Actions</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Action</th><th>Result</th></tr>
            <tr><td><b>Single Click</b> on result</td><td>Show preview in right panel</td></tr>
            <tr><td><b>Double Click</b> on result</td><td>Open file in default application</td></tr>
            <tr><td><b>Right Click</b> on result</td><td>Show context menu with options</td></tr>
            <tr><td><b>Right Click</b> on directory</td><td>Show directory context menu</td></tr>
        </table>
        """)
        tabs.addTab(shortcuts_text, "Shortcuts")
        
        # Context Menu tab
        context_text = QTextEdit()
        context_text.setReadOnly(True)
        context_text.setHtml("""
        <h2>Context Menus</h2>
        
        <h3>Results Tree Context Menu</h3>
        <p>Right-click on any result to access:</p>
        <ul>
            <li><b>Open File</b> - Open in default application</li>
            <li><b>Open in VS Code</b> - Open in Visual Studio Code (if installed)</li>
            <li><b>Copy Full Path</b> - Copy file path to clipboard</li>
            <li><b>Copy File Name</b> - Copy just the file name</li>
            <li><b>Open Containing Folder</b> - Open folder in Windows Explorer</li>
        </ul>
        
        <h3>Directory Tree Context Menu</h3>
        <p>Right-click on a directory to:</p>
        <ul>
            <li><b>Search in Directory</b> - Set as search location</li>
            <li><b>Open in Explorer</b> - Open in Windows Explorer</li>
            <li><b>Copy Path</b> - Copy directory path to clipboard</li>
            <li><b>Refresh</b> - Reload directory contents</li>
        </ul>
        """)
        tabs.addTab(context_text, "Context Menus")
        
        # Tips & Tricks tab
        tips_text = QTextEdit()
        tips_text.setReadOnly(True)
        tips_text.setHtml("""
        <h2>Tips & Tricks</h2>
        
        <h3>Performance Tips</h3>
        <ul>
            <li><b>Use file extensions filter</b> to limit search scope (.py,.txt,.js)</li>
            <li><b>Adjust max file size</b> in Preferences for faster searches</li>
            <li><b>Enable metadata search only when needed</b> - it adds processing time</li>
            <li><b>Use specific patterns</b> instead of broad searches</li>
            <li><b>Sort by match count</b> to find files with most occurrences first</li>
        </ul>
        
        <h3>Search Strategies</h3>
        <ul>
            <li><b>Start broad, then refine</b> - Do a general search, then add filters</li>
            <li><b>Use whole word</b> to avoid partial matches in variable names</li>
            <li><b>Combine regex patterns</b> to find multiple items at once</li>
            <li><b>Search metadata</b> to find files by author, date, or properties</li>
            <li><b>Use context lines</b> to see surrounding code/text</li>
        </ul>
        
        <h3>Metadata Search Examples</h3>
        <ul>
            <li><b>Find photos by camera:</b> Enable image metadata, search "Canon" or "Nikon"</li>
            <li><b>Find documents by author:</b> Enable file metadata, search author name</li>
            <li><b>Find geotagged images:</b> Enable image metadata, search "GPS"</li>
            <li><b>Find audio by artist:</b> Enable file metadata, search artist name</li>
            <li><b>Find screenplays by title:</b> Enable file metadata, search in .fdx or .fountain files</li>
        </ul>
        
        <h3>Working with Results</h3>
        <ul>
            <li><b>Use Previous/Next buttons</b> to navigate between matches in preview</li>
            <li><b>Match counter shows</b> current position (e.g., "3 / 15")</li>
            <li><b>Matches are highlighted</b> - yellow for all, orange for current</li>
            <li><b>Search history</b> provides autocomplete from previous searches</li>
            <li><b>Results persist</b> until next search - you can explore freely</li>
        </ul>
        
        <h3>File Browser Tips</h3>
        <ul>
            <li><b>Directories load on demand</b> - expand folders to see contents</li>
            <li><b>Search in specific file</b> - click a file instead of a folder</li>
            <li><b>Refresh directory</b> - right-click for latest contents</li>
            <li><b>Drive letters shown</b> - start from any drive on Windows</li>
        </ul>
        """)
        tabs.addTab(tips_text, "Tips & Tricks")
        
        # Troubleshooting tab
        trouble_text = QTextEdit()
        trouble_text.setReadOnly(True)
        trouble_text.setHtml("""
        <h2>Troubleshooting</h2>
        
        <h3>Common Issues</h3>
        
        <h4>Q: Search is slow or hangs</h4>
        <ul>
            <li>Reduce <b>Max Search File Size</b> in Preferences</li>
            <li>Add file extension filters to limit scope</li>
            <li>Disable metadata search if not needed</li>
            <li>Search in smaller directories first</li>
            <li>Click <b>Stop</b> to cancel long-running searches</li>
        </ul>
        
        <h4>Q: No results found</h4>
        <ul>
            <li>Check <b>Case Sensitive</b> option - try disabling it</li>
            <li>Verify file extension filter isn't excluding target files</li>
            <li>Make sure you're searching in the right directory</li>
            <li>If using regex, verify pattern syntax is correct</li>
            <li>Check if metadata search is enabled when searching content</li>
        </ul>
        
        <h4>Q: Preview shows garbled text</h4>
        <ul>
            <li>File may have different encoding (UTF-8, ASCII, etc.)</li>
            <li>Binary files won't display properly in text preview</li>
            <li>Very large files may be truncated</li>
            <li>Increase <b>Max Preview File Size</b> in Preferences if needed</li>
        </ul>
        
        <h4>Q: Metadata search not working</h4>
        <ul>
            <li>Ensure the file type is supported (see Search Options tab)</li>
            <li>Not all files contain metadata - depends on creation method</li>
            <li>Required library must be installed (Pillow, PyPDF2, etc.)</li>
            <li>Some formats require specific libraries</li>
        </ul>
        
        <h4>Q: Can't open file in VS Code</h4>
        <ul>
            <li>Visual Studio Code must be installed</li>
            <li>VS Code must be in system PATH</li>
            <li>Try "Open File" to use default application instead</li>
        </ul>
        
        <h3>Performance Notes</h3>
        <ul>
            <li><b>File cache</b> speeds up repeated access to same files</li>
            <li><b>Background threading</b> prevents UI freezing during search</li>
            <li><b>Max results limit</b> can be set in Preferences (0 = unlimited)</li>
            <li><b>Excluded patterns</b> skip .git, node_modules, __pycache__, etc.</li>
        </ul>
        
        <h3>Getting Help</h3>
        <p>For additional support:</p>
        <ul>
            <li>Check the README.md file in the installation directory</li>
            <li>Visit the project repository for issues and updates</li>
            <li>Review CONTRIBUTING.md for development information</li>
        </ul>
        """)
        tabs.addTab(trouble_text, "Troubleshooting")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.resize(800, 600)


class CustomPatternManagerDialog(QDialog):
    """Dialog for managing custom regex patterns"""
    
    def __init__(self, parent, custom_patterns):
        super().__init__(parent)
        self.setWindowTitle("Manage Custom Regex Patterns")
        self.setModal(True)
        self.custom_patterns = custom_patterns.copy()
        
        # Create layout
        layout = QVBoxLayout()
        
        # Instructions
        inst_label = QLabel("Add, edit, or remove your custom regex patterns:")
        layout.addWidget(inst_label)
        
        # List of patterns
        self.pattern_list = QTreeWidget()
        self.pattern_list.setHeaderLabels(["Label", "Pattern"])
        self.pattern_list.setColumnWidth(0, 200)
        self.pattern_list.setColumnWidth(1, 400)
        self.refresh_pattern_list()
        layout.addWidget(self.pattern_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Pattern")
        add_btn.clicked.connect(self.add_pattern)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_pattern)
        button_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_pattern)
        button_layout.addWidget(remove_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Dialog buttons
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout.addWidget(dialog_buttons)
        
        self.setLayout(layout)
        self.resize(700, 400)
    
    def refresh_pattern_list(self):
        """Refresh the pattern list widget"""
        self.pattern_list.clear()
        for name, info in self.custom_patterns.items():
            item = QTreeWidgetItem(self.pattern_list)
            item.setText(0, info['label'])
            item.setText(1, info['pattern'])
            item.setData(0, Qt.UserRole, name)
    
    def add_pattern(self):
        """Add a new custom pattern"""
        dialog = CustomPatternEditDialog(self, "", "", "")
        if dialog.exec() == QDialog.Accepted:
            name, label, pattern = dialog.get_pattern()
            if name and label and pattern:
                # Generate unique name
                base_name = name.lower().replace(' ', '_')
                unique_name = base_name
                counter = 1
                while unique_name in self.custom_patterns:
                    unique_name = f"{base_name}_{counter}"
                    counter += 1
                
                self.custom_patterns[unique_name] = {
                    'pattern': pattern,
                    'enabled': False,
                    'label': label
                }
                self.refresh_pattern_list()
    
    def edit_pattern(self):
        """Edit the selected pattern"""
        selected_items = self.pattern_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a pattern to edit")
            return
        
        item = selected_items[0]
        name = item.data(0, Qt.UserRole)
        info = self.custom_patterns[name]
        
        dialog = CustomPatternEditDialog(self, name, info['label'], info['pattern'])
        if dialog.exec() == QDialog.Accepted:
            _, label, pattern = dialog.get_pattern()
            if label and pattern:
                self.custom_patterns[name]['label'] = label
                self.custom_patterns[name]['pattern'] = pattern
                self.refresh_pattern_list()
    
    def remove_pattern(self):
        """Remove the selected pattern"""
        selected_items = self.pattern_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a pattern to remove")
            return
        
        item = selected_items[0]
        name = item.data(0, Qt.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Remove pattern '{self.custom_patterns[name]['label']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.custom_patterns[name]
            self.refresh_pattern_list()
    
    def get_custom_patterns(self):
        """Return the updated custom patterns"""
        return self.custom_patterns


class CustomPatternEditDialog(QDialog):
    """Dialog for editing a single custom pattern"""
    
    def __init__(self, parent, name, label, pattern):
        super().__init__(parent)
        self.setWindowTitle("Edit Custom Pattern" if name else "Add Custom Pattern")
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # Name field (only for new patterns)
        if not name:
            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("e.g., my_pattern")
            form.addRow("Name:", self.name_input)
        else:
            self.name_input = None
        
        # Label field
        self.label_input = QLineEdit()
        self.label_input.setText(label)
        self.label_input.setPlaceholderText("e.g., My Custom Pattern")
        form.addRow("Label:", self.label_input)
        
        # Pattern field
        self.pattern_input = QLineEdit()
        self.pattern_input.setText(pattern)
        self.pattern_input.setPlaceholderText(r"e.g., \\b[A-Z]{3}-\\d{4}\\b")
        form.addRow("Regex Pattern:", self.pattern_input)
        
        layout.addLayout(form)
        
        # Example/help text
        help_label = QLabel(
            "<small>Examples:<br>" +
            "• <b>\\\\b[A-Z]{3}-\\\\d{4}\\\\b</b> - Match ABC-1234 format<br>" +
            "• <b>TODO:|FIXME:</b> - Find code comments<br>" +
            "• <b>\\\\$\\\\d+\\\\.\\\\d{2}</b> - Match currency amounts<br>" +
            "</small>"
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.resize(500, 250)
    
    def get_pattern(self):
        """Return the pattern data (name, label, pattern)"""
        name = self.name_input.text().strip() if self.name_input else ""
        label = self.label_input.text().strip()
        pattern = self.pattern_input.text().strip()
        return name, label, pattern


class SearchWorker(QThread):
    """Worker thread for performing searches"""
    finished = Signal(list)  # all results
    
    def __init__(self, search_engine, root_path, pattern):
        super().__init__()
        self.search_engine = search_engine
        self.root_path = root_path
        self.pattern = pattern
        self._is_running = True
    
    def run(self):
        """Run the search in background thread"""
        results = self.search_engine.search(self.root_path, self.pattern)
        if self._is_running:
            self.finished.emit(results)
    
    def stop(self):
        """Stop the search"""
        self._is_running = False


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Class constants for file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.gif', '.bmp', '.webp'}
    FILE_METADATA_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.pptx', '.mp3', '.flac', '.m4a', '.mp4', '.avi', '.mkv'}
    
    def __init__(self):
        super().__init__()
        self.search_engine = SearchEngine()
        self.search_worker = None
        self.current_results = []
        self.current_directory = os.path.expanduser("~")
        self.current_search_pattern = ""
        self.current_file_matches = []
        self.current_match_index = 0
        self.search_history = []
        self.history_file = os.path.join(os.path.expanduser("~"), ".advanced_search_history.json")
        self.preferences_file = os.path.join(os.path.expanduser("~"), ".advanced_search_preferences.json")
        self.custom_patterns_file = os.path.join(os.path.expanduser("~"), ".advanced_search_custom_patterns.json")
        
        # Default preferences
        self.preferences = {
            'max_results': 0,  # 0 = unlimited
            'max_preview_file_size_mb': 10,
            'max_search_file_size_mb': 50,
            'max_cache_size': 50
        }
        self.load_preferences()
        
        # Performance caches
        self.file_cache = {}  # Cache file contents {path: (size, content_lines)}
        self.max_cache_size = self.preferences['max_cache_size']
        self.max_file_size = self.preferences['max_preview_file_size_mb'] * 1024 * 1024
        self.parsed_extensions = []  # Cached parsed extensions
        
        # Regex pattern options
        self.regex_patterns = {
            'emails': {'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'enabled': False, 'label': 'Email addresses'},
            'urls': {'pattern': r'https?://[^\s]+', 'enabled': False, 'label': 'URLs (http/https)'},
            'ipv4': {'pattern': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', 'enabled': False, 'label': 'IPv4 addresses'},
            'phone': {'pattern': r'\b(?:\+?1[-.]?)?(?:\(?[0-9]{3}\)?[-.]?)?[0-9]{3}[-.]?[0-9]{4}\b', 'enabled': False, 'label': 'Phone numbers'},
            'dates': {'pattern': r'\b\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}\b', 'enabled': False, 'label': 'Dates (various formats)'},
            'numbers': {'pattern': r'\b\d+\b', 'enabled': False, 'label': 'Numbers'},
            'hex': {'pattern': r'\b0x[0-9A-Fa-f]+\b|#[0-9A-Fa-f]{6}\b', 'enabled': False, 'label': 'Hex values'},
            'words': {'pattern': r'\b[A-Za-z_]\w*\b', 'enabled': False, 'label': 'Words/identifiers'},
        }
        self.regex_menu = None  # Track the menu instance
        self.regex_menu_open = False  # Track menu state
        
        # Custom user-defined patterns
        self.custom_patterns = {}  # {name: {'pattern': str, 'enabled': bool, 'label': str}}
        self.load_custom_patterns()
        
        # Apply preferences to search engine
        self.search_engine.max_results = self.preferences['max_results']
        self.search_engine.max_search_file_size = self.preferences['max_search_file_size_mb'] * 1024 * 1024
        
        self.load_search_history()
        
        self.init_ui()
        self.create_menu_bar()
        self.setWindowTitle("Advanced Search Tool")
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.resize(1400, 900)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Combined search and options bar
        search_options_layout = self.create_search_and_options()
        main_layout.addLayout(search_options_layout)
        
        # Main content area with three panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Directory tree
        dir_widget = QWidget()
        dir_layout = QVBoxLayout(dir_widget)
        dir_layout.setContentsMargins(0, 0, 0, 0)
        
        dir_label = QLabel("File Explorer:")
        dir_label.setStyleSheet("font-weight: bold; padding: 5px;")
        dir_label.setToolTip("Select a directory or file to search")
        dir_layout.addWidget(dir_label)
        
        self.dir_tree = QTreeWidget()
        self.dir_tree.setHeaderLabels(["Name"])
        self.dir_tree.setToolTip("Click a folder to search recursively or a file to search in that file\nRight-click for options")
        self.dir_tree.itemClicked.connect(self.on_dir_selected)
        self.dir_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dir_tree.customContextMenuRequested.connect(self.show_dir_context_menu)
        self.dir_tree.itemExpanded.connect(self.on_dir_expanded)
        self.populate_directory_tree()
        dir_layout.addWidget(self.dir_tree)
        
        splitter.addWidget(dir_widget)
        
        # Middle panel - Results tree
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(0, 0, 0, 0)
        
        # Results header with sort controls
        results_header = QHBoxLayout()
        results_label = QLabel("Search Results:")
        results_label.setStyleSheet("font-weight: bold; padding: 5px;")
        results_label.setToolTip("Files and matches found in search")
        results_header.addWidget(results_label)
        
        results_header.addStretch()
        
        # Sort dropdown
        sort_label = QLabel("Sort:")
        results_header.addWidget(sort_label)
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Path (A-Z)",
            "Path (Z-A)",
            "Match Count (High-Low)",
            "Match Count (Low-High)",
            "File Size (Large-Small)",
            "File Size (Small-Large)",
            "Date Modified (Newest)",
            "Date Modified (Oldest)"
        ])
        self.sort_combo.setToolTip("Sort search results")
        self.sort_combo.currentIndexChanged.connect(self.apply_sort)
        results_header.addWidget(self.sort_combo)
        
        results_layout.addLayout(results_header)
        
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["File", "Matches"])
        self.results_tree.setColumnWidth(0, 400)
        self.results_tree.setToolTip("Click to preview, double-click to open file, right-click for options")
        self.results_tree.itemClicked.connect(self.on_tree_item_clicked)
        self.results_tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.results_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_tree.customContextMenuRequested.connect(self.show_context_menu)
        results_layout.addWidget(self.results_tree)
        
        splitter.addWidget(results_widget)
        
        # Right panel - Content preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview header with navigation
        preview_header = QHBoxLayout()
        preview_label = QLabel("Preview:")
        preview_label.setStyleSheet("font-weight: bold; padding: 5px;")
        preview_label.setToolTip("File content preview with matched lines highlighted")
        preview_header.addWidget(preview_label)
        
        preview_header.addStretch()
        
        # Match navigation controls
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        prev_icon_path = os.path.join(assets_dir, "chevron_up.svg")
        self.prev_match_btn = QPushButton()
        if os.path.exists(prev_icon_path):
            self.prev_match_btn.setIcon(QIcon(prev_icon_path))
        else:
            self.prev_match_btn.setText("◄")
        self.prev_match_btn.setMaximumWidth(30)
        self.prev_match_btn.setToolTip("Go to previous match (Ctrl+Up)")
        self.prev_match_btn.clicked.connect(self.go_to_previous_match)
        self.prev_match_btn.setEnabled(False)
        preview_header.addWidget(self.prev_match_btn)
        
        self.match_counter_label = QLabel("0/0")
        self.match_counter_label.setStyleSheet("padding: 0 10px;")
        self.match_counter_label.setToolTip("Current match / Total matches")
        preview_header.addWidget(self.match_counter_label)
        
        next_icon_path = os.path.join(assets_dir, "chevron_down.svg")
        self.next_match_btn = QPushButton()
        if os.path.exists(next_icon_path):
            self.next_match_btn.setIcon(QIcon(next_icon_path))
        else:
            self.next_match_btn.setText("►")
        self.next_match_btn.setMaximumWidth(30)
        self.next_match_btn.setToolTip("Go to next match (Ctrl+Down)")
        self.next_match_btn.clicked.connect(self.go_to_next_match)
        self.next_match_btn.setEnabled(False)
        preview_header.addWidget(self.next_match_btn)
        
        preview_layout.addLayout(preview_header)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        self.preview_text.setToolTip("File preview - search terms are highlighted in yellow")
        preview_layout.addWidget(self.preview_text)
        
        splitter.addWidget(preview_widget)
        splitter.setSizes([300, 400, 700])
        
        main_layout.addWidget(splitter)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("&Settings")
        
        preferences_action = QAction("Preferences...", self)
        preferences_action.triggered.connect(self.show_preferences)
        settings_menu.addAction(preferences_action)
        
        settings_menu.addSeparator()
        
        clear_history_action = QAction("Clear Search History", self)
        clear_history_action.triggered.connect(self.clear_search_history)
        settings_menu.addAction(clear_history_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        help_action = QAction("Help...", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_search_and_options(self):
        """Create combined search and options controls"""
        layout = QHBoxLayout()
        
        # Search for label and input
        search_label = QLabel("Search for:")
        search_label.setToolTip("Enter text or regular expression pattern to search for")
        layout.addWidget(search_label)
        
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setInsertPolicy(QComboBox.NoInsert)
        self.search_input.lineEdit().setPlaceholderText("Enter search pattern...")
        self.search_input.setToolTip("Text or regex pattern to find in files\nPress Enter to start search\nUse Up/Down arrows to cycle through history")
        self.search_input.lineEdit().returnPressed.connect(self.start_search)
        self.search_input.setMinimumWidth(250)
        self.search_input.setMaxVisibleItems(10)
        # Enable auto-completion
        self.search_input.setCompleter(self.search_input.completer())
        self.update_search_history_dropdown()
        layout.addWidget(self.search_input)
        
        # Multi-modal Search/Stop button
        self.search_stop_btn = QPushButton("Search")
        self.search_stop_btn.setToolTip("Start searching in the selected directory (Enter)")
        self.search_stop_btn.clicked.connect(self.toggle_search)
        self.search_stop_btn.setDefault(True)
        self.is_searching = False
        layout.addWidget(self.search_stop_btn)
        
        # Separator
        layout.addSpacing(10)
        
        # Compact grid layout for all controls
        controls_grid = QGridLayout()
        controls_grid.setSpacing(8)
        controls_grid.setContentsMargins(0, 0, 0, 0)
        
        # Row 0: Context, Regex, Case sensitive, Whole word, Image metadata
        context_label = QLabel("Context:")
        context_label.setToolTip("Number of lines to show before and after each match")
        controls_grid.addWidget(context_label, 0, 0)
        
        self.context_combo = QComboBox()
        for i in range(11):  # 0 to 10
            self.context_combo.addItem(str(i))
        self.context_combo.setCurrentIndex(2)  # Default to 2
        self.context_combo.setToolTip("Lines of context to show around matches (0-10)")
        self.context_combo.currentIndexChanged.connect(
            lambda index: self.search_engine.set_context_lines(index)
        )
        self.context_combo.setMinimumWidth(50)
        self.context_combo.setMaximumWidth(70)
        controls_grid.addWidget(self.context_combo, 0, 1)
        
        # Regex pattern selector button
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        chevron_icon_path = os.path.join(assets_dir, "chevron_down.svg")
        self.regex_btn = QPushButton("Regex")
        if os.path.exists(chevron_icon_path):
            self.regex_btn.setIcon(QIcon(chevron_icon_path))
            self.regex_btn.setLayoutDirection(Qt.RightToLeft)  # Icon on the right
        self.regex_btn.setToolTip("Select common regex patterns to search for")
        self.regex_btn.setMaximumWidth(100)
        self.regex_btn.clicked.connect(self.show_regex_patterns_menu)
        controls_grid.addWidget(self.regex_btn, 0, 2)
        
        self.case_sensitive_cb = QCheckBox("Case sensitive")
        self.case_sensitive_cb.setToolTip("Match exact case when searching")
        self.case_sensitive_cb.stateChanged.connect(
            lambda state: self.search_engine.set_case_sensitive(state == Qt.Checked)
        )
        controls_grid.addWidget(self.case_sensitive_cb, 0, 3)
        
        self.whole_word_cb = QCheckBox("Whole word")
        self.whole_word_cb.setToolTip("Only match complete words (not partial matches)")
        self.whole_word_cb.stateChanged.connect(
            lambda state: self.search_engine.set_whole_word(state == Qt.Checked)
        )
        controls_grid.addWidget(self.whole_word_cb, 0, 4)
        
        self.metadata_cb = QCheckBox("Image metadata")
        self.metadata_cb.setToolTip("Search image metadata (EXIF, GPS, etc.) for JPG, PNG, TIFF files")
        self.metadata_cb.stateChanged.connect(
            lambda state: self.search_engine.set_search_metadata(state == 2)
        )
        controls_grid.addWidget(self.metadata_cb, 0, 5)
        
        # Row 1: Extensions label/input, File metadata, Archive search, Binary/hex
        ext_label = QLabel("Extensions:")
        ext_label.setToolTip("Filter files by extension (leave empty to search all files)")
        controls_grid.addWidget(ext_label, 1, 0)
        
        self.extensions_input = QLineEdit()
        self.extensions_input.setPlaceholderText(".py,.txt,.js")
        self.extensions_input.setToolTip("Comma-separated file extensions to search\nExample: .py,.txt,.js\nLeave empty to search all files")
        self.extensions_input.setMaximumWidth(150)
        controls_grid.addWidget(self.extensions_input, 1, 1, 1, 2)
        
        self.file_metadata_cb = QCheckBox("File metadata")
        self.file_metadata_cb.setToolTip("Search file properties (PDF, Office docs, audio/video files): author, title, dates, etc.")
        self.file_metadata_cb.stateChanged.connect(
            lambda state: self.search_engine.set_search_file_metadata(state == 2)
        )
        controls_grid.addWidget(self.file_metadata_cb, 1, 3)
        
        self.archive_search_cb = QCheckBox("Archive search")
        self.archive_search_cb.setToolTip("Search inside ZIP and EPUB files without extraction")
        self.archive_search_cb.stateChanged.connect(
            lambda state: self.search_engine.set_search_in_archives(state == 2)
        )
        controls_grid.addWidget(self.archive_search_cb, 1, 4)
        
        self.hex_search_cb = QCheckBox("Binary/hex")
        self.hex_search_cb.setToolTip("Search binary files using hex patterns")
        self.hex_search_cb.stateChanged.connect(
            lambda state: self.search_engine.set_hex_search(state == 2)
        )
        controls_grid.addWidget(self.hex_search_cb, 1, 5)
        
        layout.addLayout(controls_grid)
        
        layout.addStretch()
        return layout
    
    def populate_directory_tree(self):
        """Populate directory tree with common locations"""
        self.dir_tree.setUpdatesEnabled(False)  # Batch updates for performance
        self.dir_tree.clear()
        
        # Add common locations
        home_path = os.path.expanduser("~")
        username = os.path.basename(home_path)
        home_item = QTreeWidgetItem(self.dir_tree)
        home_item.setText(0, f"Home ({username})")
        home_item.setData(0, Qt.UserRole, {"path": home_path, "is_file": False})
        home_item.setExpanded(True)
        
        # Add subdirectories and files of home
        self._populate_tree_item(home_item, home_path)
        
        # Add drives (Windows)
        if os.name == 'nt':
            import ctypes
            for drive in string.ascii_uppercase:
                drive_path = f"{drive}:\\\\"
                if os.path.exists(drive_path):
                    # Get volume label
                    try:
                        volume_name = ctypes.create_unicode_buffer(256)
                        ctypes.windll.kernel32.GetVolumeInformationW(
                            ctypes.c_wchar_p(drive_path),
                            volume_name, ctypes.sizeof(volume_name),
                            None, None, None, None, 0
                        )
                        label = volume_name.value
                        display_text = f"{drive}: ({label})" if label else f"{drive}:"
                    except Exception:
                        display_text = f"{drive}:"
                    
                    drive_item = QTreeWidgetItem(self.dir_tree)
                    drive_item.setText(0, display_text)
                    drive_item.setData(0, Qt.UserRole, {"path": drive_path, "is_file": False})
                    # Add placeholder for lazy loading
                    placeholder = QTreeWidgetItem(drive_item)
                    placeholder.setText(0, "Loading...")
        
        self.dir_tree.setUpdatesEnabled(True)  # Re-enable updates
    
    def _populate_tree_item(self, parent_item, path, max_items=100):
        """Populate a tree item with directories and files"""
        try:
            entries = []
            for entry in os.scandir(path):
                if not entry.name.startswith('.'):
                    entries.append(entry)
            
            # Sort: directories first, then files
            entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))
            
            # Limit to prevent UI freeze
            for entry in entries[:max_items]:
                child_item = QTreeWidgetItem(parent_item)
                if entry.is_dir():
                    child_item.setText(0, entry.name)
                    child_item.setData(0, Qt.UserRole, {"path": entry.path, "is_file": False})
                    # Add placeholder for lazy loading
                    placeholder = QTreeWidgetItem(child_item)
                    placeholder.setText(0, "Loading...")
                else:
                    child_item.setText(0, entry.name)
                    child_item.setData(0, Qt.UserRole, {"path": entry.path, "is_file": True})
        except PermissionError:
            pass
    
    def on_dir_expanded(self, item):
        """Handle directory expansion - lazy load contents"""
        data = item.data(0, Qt.UserRole)
        if data and not data.get("is_file", False):
            # Check if we have a placeholder
            if item.childCount() == 1 and item.child(0).text(0) == "Loading...":
                # Remove placeholder
                item.removeChild(item.child(0))
                # Load actual contents
                self._populate_tree_item(item, data["path"])
    
    def on_dir_selected(self, item, column):
        """Handle directory or file selection"""
        data = item.data(0, Qt.UserRole)
        if data:
            path = data["path"]
            is_file = data.get("is_file", False)
            self.current_directory = path
            if is_file:
                self.status_bar.showMessage(f"Selected file: {path}")
            else:
                self.status_bar.showMessage(f"Selected directory: {path}")
    
    def show_regex_patterns_menu(self):
        """Show or hide popup menu with regex pattern options"""
        # If menu exists and is visible, close it and prevent reopening
        if self.regex_menu is not None and self.regex_menu.isVisible():
            self.regex_menu.close()
            self.regex_menu_open = False
            return
        
        # If we just closed the menu, don't reopen immediately
        if self.regex_menu_open:
            return
        
        # Mark menu as opening
        self.regex_menu_open = True
        
        # Create new menu
        self.regex_menu = QMenu(self)
        self.regex_menu.setToolTipsVisible(True)
        
        # Add header
        header_action = self.regex_menu.addAction("Select Regex Patterns:")
        header_action.setEnabled(False)
        self.regex_menu.addSeparator()
        
        # Add checkbox for each pattern
        for pattern_key, pattern_info in self.regex_patterns.items():
            action = self.regex_menu.addAction(pattern_info['label'])
            action.setCheckable(True)
            action.setChecked(pattern_info['enabled'])
            action.setToolTip(f"Pattern: {pattern_info['pattern']}")
            action.triggered.connect(lambda checked, key=pattern_key: self.toggle_regex_pattern(key, checked))
        
        # Add custom patterns section if any exist
        if self.custom_patterns:
            self.regex_menu.addSeparator()
            custom_header = self.regex_menu.addAction("Custom Patterns:")
            custom_header.setEnabled(False)
            
            for pattern_key, pattern_info in self.custom_patterns.items():
                action = self.regex_menu.addAction(pattern_info['label'])
                action.setCheckable(True)
                action.setChecked(pattern_info['enabled'])
                action.setToolTip(f"Pattern: {pattern_info['pattern']}")
                action.triggered.connect(lambda checked, key=pattern_key: self.toggle_custom_pattern(key, checked))
        
        self.regex_menu.addSeparator()
        
        # Add manage custom patterns option
        manage_action = self.regex_menu.addAction("Manage Custom Patterns...")
        manage_action.triggered.connect(self.show_custom_pattern_manager)
        
        self.regex_menu.addSeparator()
        
        # Add clear all option
        clear_action = self.regex_menu.addAction("Clear All")
        clear_action.triggered.connect(self.clear_all_regex_patterns)
        
        # Clean up when menu is hidden/closed
        def on_menu_hidden():
            # Use a timer to delay the flag reset to avoid immediate reopening
            from PySide6.QtCore import QTimer
            QTimer.singleShot(200, lambda: setattr(self, 'regex_menu_open', False))
        
        self.regex_menu.aboutToHide.connect(on_menu_hidden)
        
        # Show menu below button using popup (non-blocking)
        self.regex_menu.popup(self.regex_btn.mapToGlobal(self.regex_btn.rect().bottomLeft()))
    
    def toggle_regex_pattern(self, pattern_key, enabled):
        """Toggle a regex pattern on/off"""
        self.regex_patterns[pattern_key]['enabled'] = enabled
        self.update_search_with_regex_patterns()
        
        # Update button text to show active patterns count
        active_count = sum(1 for p in self.regex_patterns.values() if p['enabled'])
        active_count += sum(1 for p in self.custom_patterns.values() if p['enabled'])
        if active_count > 0:
            self.regex_btn.setText(f"Regex Patterns ({active_count})")
            self.regex_btn.setStyleSheet("font-weight: bold;")
        else:
            self.regex_btn.setText("Regex Patterns")
            self.regex_btn.setStyleSheet("")
    
    def toggle_custom_pattern(self, pattern_key, enabled):
        """Toggle a custom regex pattern on/off"""
        self.custom_patterns[pattern_key]['enabled'] = enabled
        self.save_custom_patterns()
        self.update_search_with_regex_patterns()
        
        # Update button text to show active patterns count
        active_count = sum(1 for p in self.regex_patterns.values() if p['enabled'])
        active_count += sum(1 for p in self.custom_patterns.values() if p['enabled'])
        if active_count > 0:
            self.regex_btn.setText(f"Regex Patterns ({active_count})")
            self.regex_btn.setStyleSheet("font-weight: bold;")
        else:
            self.regex_btn.setText("Regex Patterns")
            self.regex_btn.setStyleSheet("")
    
    def clear_all_regex_patterns(self):
        """Clear all selected regex patterns"""
        for pattern_info in self.regex_patterns.values():
            pattern_info['enabled'] = False
        for pattern_info in self.custom_patterns.values():
            pattern_info['enabled'] = False
        self.save_custom_patterns()
        self.update_search_with_regex_patterns()
        self.regex_btn.setText("Regex Patterns")
        self.regex_btn.setStyleSheet("")
    
    def update_search_with_regex_patterns(self):
        """Update search input with combined regex patterns"""
        enabled_patterns = [info['pattern'] for info in self.regex_patterns.values() if info['enabled']]
        enabled_patterns += [info['pattern'] for info in self.custom_patterns.values() if info['enabled']]
        
        if enabled_patterns:
            # Combine patterns with OR operator
            combined_pattern = '|'.join(f'({pattern})' for pattern in enabled_patterns)
            self.search_input.lineEdit().setText(combined_pattern)
            # Enable regex mode in search engine
            self.search_engine.set_regex(True)
        else:
            # If no patterns selected, keep current search text
            # and disable regex mode
            self.search_engine.set_regex(False)
    
    def load_custom_patterns(self):
        """Load custom user-defined regex patterns from file"""
        try:
            if os.path.exists(self.custom_patterns_file):
                with open(self.custom_patterns_file, 'r', encoding='utf-8') as f:
                    self.custom_patterns = json.load(f)
        except Exception as e:
            print(f"Error loading custom patterns: {e}")
            self.custom_patterns = {}
    
    def save_custom_patterns(self):
        """Save custom patterns to file"""
        try:
            with open(self.custom_patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving custom patterns: {e}")
    
    def add_custom_pattern(self, name, pattern, label):
        """Add a new custom regex pattern"""
        self.custom_patterns[name] = {
            'pattern': pattern,
            'enabled': False,
            'label': label
        }
        self.save_custom_patterns()
    
    def remove_custom_pattern(self, name):
        """Remove a custom regex pattern"""
        if name in self.custom_patterns:
            del self.custom_patterns[name]
            self.save_custom_patterns()
    
    def show_custom_pattern_manager(self):
        """Show dialog to manage custom regex patterns"""
        dialog = CustomPatternManagerDialog(self, self.custom_patterns)
        if dialog.exec() == QDialog.Accepted:
            self.custom_patterns = dialog.get_custom_patterns()
            self.save_custom_patterns()
            self.status_bar.showMessage("Custom patterns updated", 3000)
    
    def show_dir_context_menu(self, position):
        """Show context menu for directory tree items"""
        item = self.dir_tree.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.UserRole)
        if not data or data.get("path") is None:
            return
        
        menu = QMenu()
        path = data["path"]
        is_file = data.get("is_file", False)
        
        if is_file:
            # File menu
            open_file_action = menu.addAction("Open File")
            open_file_action.triggered.connect(lambda: self.open_file(path))
            
            open_parent_action = menu.addAction("Open Parent Directory")
            open_parent_action.triggered.connect(lambda: self.open_file_directory(path))
        else:
            # Directory menu
            open_dir_action = menu.addAction("Open Directory")
            open_dir_action.triggered.connect(lambda: self.open_directory(path))
            
            parent_path = os.path.dirname(path)
            if parent_path and parent_path != path:
                open_parent_action = menu.addAction("Open Parent Directory")
                open_parent_action.triggered.connect(lambda: self.open_directory(parent_path))
        
        menu.exec(self.dir_tree.viewport().mapToGlobal(position))
    
    def open_directory(self, directory_path):
        """Open a directory in file explorer"""
        try:
            os.startfile(directory_path)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open directory: {str(e)}")
    
    def load_preferences(self):
        """Load preferences from file"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    saved_prefs = json.load(f)
                    self.preferences.update(saved_prefs)
        except Exception as e:
            print(f"Error loading preferences: {e}")
    
    def save_preferences(self):
        """Save preferences to file"""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def show_preferences(self):
        """Show preferences dialog"""
        dialog = PreferencesDialog(self, self.preferences)
        if dialog.exec() == QDialog.Accepted:
            # Update preferences
            self.preferences = dialog.get_preferences()
            self.save_preferences()
            
            # Apply new preferences
            self.max_cache_size = self.preferences['max_cache_size']
            self.max_file_size = self.preferences['max_preview_file_size_mb'] * 1024 * 1024
            self.search_engine.max_results = self.preferences['max_results']
            self.search_engine.max_search_file_size = self.preferences['max_search_file_size_mb'] * 1024 * 1024
            
            # Clear cache if size reduced
            if len(self.file_cache) > self.max_cache_size:
                # Keep only the last max_cache_size items
                keys = list(self.file_cache.keys())
                for key in keys[:-self.max_cache_size]:
                    del self.file_cache[key]
            
            self.status_bar.showMessage("Preferences updated", 3000)
    
    def apply_sort(self):
        """Apply sorting to current search results"""
        if not self.current_results:
            return
        
        # Group results by file
        files_dict = {}
        for match in self.current_results:
            if match.file_path not in files_dict:
                files_dict[match.file_path] = []
            files_dict[match.file_path].append(match)
        
        # Apply sorting
        sort_option = self.sort_combo.currentText()
        
        if sort_option == "Path (A-Z)":
            sorted_files = sorted(files_dict.items(), key=lambda x: x[0].lower())
        elif sort_option == "Path (Z-A)":
            sorted_files = sorted(files_dict.items(), key=lambda x: x[0].lower(), reverse=True)
        elif sort_option == "Match Count (High-Low)":
            sorted_files = sorted(files_dict.items(), key=lambda x: len(x[1]), reverse=True)
        elif sort_option == "Match Count (Low-High)":
            sorted_files = sorted(files_dict.items(), key=lambda x: len(x[1]))
        elif sort_option == "File Size (Large-Small)":
            sorted_files = sorted(files_dict.items(), 
                                key=lambda x: os.path.getsize(x[0]) if os.path.exists(x[0]) else 0, 
                                reverse=True)
        elif sort_option == "File Size (Small-Large)":
            sorted_files = sorted(files_dict.items(), 
                                key=lambda x: os.path.getsize(x[0]) if os.path.exists(x[0]) else 0)
        elif sort_option == "Date Modified (Newest)":
            sorted_files = sorted(files_dict.items(), 
                                key=lambda x: os.path.getmtime(x[0]) if os.path.exists(x[0]) else 0, 
                                reverse=True)
        elif sort_option == "Date Modified (Oldest)":
            sorted_files = sorted(files_dict.items(), 
                                key=lambda x: os.path.getmtime(x[0]) if os.path.exists(x[0]) else 0)
        else:
            sorted_files = sorted(files_dict.items(), key=lambda x: x[0].lower())
        
        # Update the results tree
        self.results_tree.clear()
        
        for file_path, matches in sorted_files:
            file_item = QTreeWidgetItem(self.results_tree)
            file_item.setText(0, file_path)
            file_item.setText(1, str(len(matches)))
            file_item.setData(0, Qt.UserRole, matches)
            
            # Add match items
            for match in matches:
                match_item = QTreeWidgetItem(file_item)
                match_item.setText(0, f"  Line {match.line_number}: {match.line_content[:80]}")
                match_item.setData(0, Qt.UserRole, match)
        
        # Update status
        total_matches = sum(len(matches) for _, matches in sorted_files)
        total_files = len(sorted_files)
        
        self.status_bar.showMessage(
            f"Found {total_matches} matches in {total_files} files"
        )
    
    def toggle_search(self):
        """Toggle between starting and stopping search"""
        if self.is_searching:
            self.stop_search()
        else:
            self.start_search()
    
    def start_search(self):
        """Start a new search"""
        pattern = self.search_input.currentText()
        root_path = self.current_directory
        
        if not pattern:
            QMessageBox.warning(self, "Warning", "Please enter a search pattern")
            return
        
        # Add to search history
        self.add_to_search_history(pattern)
        
        if not os.path.isdir(root_path):
            QMessageBox.warning(self, "Warning", "Please select a valid directory from the tree")
            return
        
        self.current_search_pattern = pattern
        
        # Update file extensions filter
        extensions_text = self.extensions_input.text().strip()
        if extensions_text:
            extensions = [ext.strip() for ext in extensions_text.split(',')]
            self.search_engine.set_file_extensions(extensions)
        else:
            self.search_engine.set_file_extensions([])
        
        # Clear previous results
        self.results_tree.clear()
        self.preview_text.clear()
        self.current_results = []
        
        # Update UI state
        self.is_searching = True
        self.search_stop_btn.setText("Stop")
        self.search_stop_btn.setToolTip("Stop the current search operation")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_bar.showMessage(f"Searching for '{pattern}'...")
        
        # Start search in background thread
        self.search_worker = SearchWorker(self.search_engine, root_path, pattern)
        self.search_worker.finished.connect(self.on_search_finished)
        self.search_worker.start()
    
    def stop_search(self):
        """Stop the current search"""
        if self.search_worker:
            self.search_worker.stop()
            self.search_worker.wait()
        self.on_search_finished([])
    
    def on_search_finished(self, results):
        """Handle search completion"""
        self.current_results = results
        
        # Apply sorting to display results
        self.apply_sort()
        
        # Update UI state
        self.is_searching = False
        self.search_stop_btn.setText("Search")
        self.search_stop_btn.setToolTip("Start searching in the selected directory (Enter)")
        self.progress_bar.setVisible(False)
    
    def on_tree_item_clicked(self, item, column):
        """Handle tree item click"""
        data = item.data(0, Qt.UserRole)
        
        if isinstance(data, SearchMatch):
            # Single match - show full file with all matches
            matches = [data]
            # Try to find all matches for this file from results
            for result in self.current_results:
                if result.file_path == data.file_path and result != data:
                    matches.append(result)
            self.show_file_contents_with_matches(matches)
        elif isinstance(data, list):
            # File with multiple matches - show file contents with highlights
            self.show_file_contents_with_matches(data)
    
    def on_item_double_clicked(self, item, column):
        """Handle double-click to open file"""
        data = item.data(0, Qt.UserRole)
        
        if isinstance(data, SearchMatch):
            self.open_file(data.file_path, data.line_number)
        elif isinstance(data, list) and len(data) > 0:
            self.open_file(data[0].file_path)
    
    def show_file_contents_with_matches(self, matches):
        """Show full file contents with matched lines highlighted"""
        if not matches:
            self.current_file_matches = []
            self.current_match_index = 0
            self.update_match_navigation()
            return
        
        file_path = matches[0].file_path
        self.current_file_matches = matches
        self.current_match_index = 0
        self.preview_text.clear()
        
        try:
            # Check if this is an image file
            file_ext = os.path.splitext(file_path)[1].lower()
            image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.gif', '.bmp', '.webp'}
            file_metadata_extensions = {'.pdf', '.docx', '.xlsx', '.pptx', '.mp3', '.flac', '.m4a', '.mp4', '.avi', '.mkv'}
            is_image = file_ext in image_extensions
            is_file_with_metadata = file_ext in file_metadata_extensions
            
            # If metadata search is enabled and this is an image, show image metadata
            if is_image and self.search_engine.search_metadata:
                self._display_image_metadata_preview(file_path, matches)
                return
            
            # If file metadata search is enabled and this has metadata, show file metadata
            if is_file_with_metadata and self.search_engine.search_file_metadata:
                self._display_file_metadata_preview(file_path, matches)
                return
            
            # Check file size first
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                self.preview_text.setPlainText(f"File too large to display ({file_size / 1024 / 1024:.1f}MB).\nMaximum size: {self.max_file_size / 1024 / 1024:.1f}MB")
                self.current_file_matches = []
                self.current_match_index = 0
                self.update_match_navigation()
                return
            
            # Check cache first
            if file_path in self.file_cache:
                cached_size, lines = self.file_cache[file_path]
                if cached_size == file_size:
                    # Use cached content
                    pass
                else:
                    # File changed, re-read
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    self._cache_file(file_path, file_size, lines)
            else:
                # Read entire file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                self._cache_file(file_path, file_size, lines)
            
            # Build match line numbers set for quick lookup
            match_lines = {match.line_number for match in matches}
            
            # Display file with highlights (optimized with list comprehension)
            display_lines = [
                f"File: {file_path}",
                f"Total matches: {len(matches)}",
                "=" * 80,
                ""
            ]
            
            # Show all lines (optimized loop)
            display_lines.extend(
                f"{'>>> ' if i in match_lines else '    '}{i:5d} | {line.rstrip()}"
                for i, line in enumerate(lines, 1)
            )
            
            self.preview_text.setPlainText("\n".join(display_lines))
            
            # Highlight all matches
            self.highlight_all_matches()
            
            # Update navigation and go to first match
            self.update_match_navigation()
            if matches:
                self.jump_to_current_match()
                
        except Exception as e:
            self.preview_text.setPlainText(f"Error reading file: {str(e)}")
            self.current_file_matches = []
            self.current_match_index = 0
            self.update_match_navigation()
    
    def _display_image_metadata_preview(self, file_path, matches):
        """Display image metadata in preview pane"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS
            import os
            from datetime import datetime
            
            metadata = {}
            
            # Extract and display metadata
            with Image.open(file_path) as img:
                # File system info
                stat_info = os.stat(file_path)
                metadata['File_Size'] = f"{stat_info.st_size / 1024:.2f} KB"
                metadata['File_Created'] = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                metadata['File_Modified'] = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                # Basic image info
                metadata['Format'] = img.format or 'Unknown'
                metadata['Mode'] = img.mode
                metadata['Size'] = f"{img.width}x{img.height}"
                
                # Try to get EXIF data using getexif() (newer API)
                try:
                    exif = img.getexif()
                    if exif:
                        for tag_id, value in exif.items():
                            tag_name = TAGS.get(tag_id, f"Tag_{tag_id}")
                            
                            # Handle GPS data specially
                            if tag_name == "GPSInfo":
                                try:
                                    gps_data = {GPSTAGS.get(gps_tag_id, f"GPS_{gps_tag_id}"): str(value[gps_tag_id]) 
                                               for gps_tag_id in value}
                                    metadata['GPS_Info'] = str(gps_data)
                                except Exception:
                                    metadata['GPS_Info'] = str(value)
                            else:
                                # Convert value to string, handle bytes
                                if isinstance(value, bytes):
                                    try:
                                        value = value.decode('utf-8', errors='ignore')
                                    except Exception:
                                        value = str(value)[:100]
                                elif isinstance(value, (tuple, list)) and len(str(value)) > 100:
                                    value = str(value)[:100] + "..."
                                metadata[tag_name] = str(value)
                except (AttributeError, KeyError, TypeError):
                    pass
                
                # PNG info
                if hasattr(img, 'info') and img.info:
                    for key, value in img.info.items():
                        if key not in metadata:
                            metadata[f"PNG_{key}"] = str(value)[:200]
            
            # Display using common metadata display method
            note = "This image has no EXIF metadata (typical for screenshots)" if len(metadata) <= 6 else None
            self._display_metadata_common(file_path, matches, metadata, "Image Metadata", note)
                
        except Exception as e:
            self.preview_text.setPlainText(f"Error reading image metadata: {str(e)}")
            self.current_file_matches = []
            self.current_match_index = 0
            self.update_match_navigation()
    
    def _display_file_metadata_preview(self, file_path, matches):
        """Display file metadata in preview pane (PDF, Office, audio, etc.)"""
        try:
            import os
            from datetime import datetime
            
            # Extract file metadata
            metadata = self.search_engine._extract_file_metadata(file_path)
            
            # Add file system info
            stat_info = os.stat(file_path)
            metadata['File_Size'] = f"{stat_info.st_size / 1024:.2f} KB"
            metadata['File_Created'] = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            metadata['File_Modified'] = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Display using common metadata display method
            note = "No extractable metadata found for this file type" if len(metadata) <= 3 else None
            self._display_metadata_common(file_path, matches, metadata, "File Metadata", note)
                
        except Exception as e:
            self.preview_text.setPlainText(f"Error reading file metadata: {str(e)}")
            self.current_file_matches = []
            self.current_match_index = 0
            self.update_match_navigation()
    
    def _display_metadata_common(self, file_path, matches, metadata, header_text, note=None):
        """Common method to display metadata in preview pane"""
        display_lines = [
            f"{header_text}: {file_path}",
            f"Total matches: {len(matches)}",
            "=" * 80,
            ""
        ]
        
        if note:
            display_lines.append(f"    Note: {note}")
            display_lines.append("")
        
        # Build match line numbers set for quick lookup
        match_lines = {match.line_number for match in matches}
        
        # Display metadata with match indicators
        for line_num, (key, value) in enumerate(metadata.items(), start=1):
            line_text = f"{key}: {value}"
            prefix = '>>> ' if line_num in match_lines else '    '
            display_lines.append(f"{prefix}{line_num:5d} | {line_text}")
        
        self.preview_text.setPlainText("\n".join(display_lines))
        
        # Highlight all matches
        self.highlight_all_matches()
        
        # Update navigation and go to first match
        self.update_match_navigation()
        if matches:
            self.jump_to_current_match()
    
    def _cache_file(self, file_path, file_size, lines):
        """Cache file contents with LRU eviction"""
        # If cache is full, remove oldest entry
        if len(self.file_cache) >= self.max_cache_size:
            # Remove first (oldest) item
            first_key = next(iter(self.file_cache))
            del self.file_cache[first_key]
        
        self.file_cache[file_path] = (file_size, lines)
    
    def highlight_all_matches(self):
        """Highlight all search matches in the preview text (optimized)"""
        if not self.current_file_matches or not self.current_search_pattern:
            return
        
        # Get the search pattern for highlighting
        pattern = self.current_search_pattern
        
        # Build regex for highlighting
        try:
            if self.search_engine.use_regex:
                flags = 0 if self.search_engine.case_sensitive else re.IGNORECASE
                regex = re.compile(pattern, flags)
            else:
                escaped_pattern = re.escape(pattern)
                if self.search_engine.whole_word:
                    escaped_pattern = r'\b' + escaped_pattern + r'\b'
                flags = 0 if self.search_engine.case_sensitive else re.IGNORECASE
                regex = re.compile(escaped_pattern, flags)
        except re.error:
            return
        
        # Yellow highlight format
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor(255, 255, 0))
        
        # Get text once (optimization)
        text = self.preview_text.toPlainText()
        
        # Skip header (4 lines)
        header_lines = text.split('\n', 4)
        if len(header_lines) < 5:
            return
        header_length = sum(len(line) + 1 for line in header_lines[:4])
        
        # Batch highlight all matches (optimized)
        cursor = self.preview_text.textCursor()
        cursor.beginEditBlock()  # Batch operations
        
        for match in regex.finditer(text[header_length:]):
            cursor.setPosition(header_length + match.start())
            cursor.setPosition(header_length + match.end(), QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(highlight_format)
        
        cursor.endEditBlock()  # Complete batch
    
    def jump_to_current_match(self):
        """Jump to the current match in preview"""
        if not self.current_file_matches or self.current_match_index >= len(self.current_file_matches):
            return
        
        match = self.current_file_matches[self.current_match_index]
        
        # Re-highlight all matches first (to reset orange highlight)
        self.highlight_all_matches()
        
        # Find header position (skip first 4 lines)
        header_cursor = QTextCursor(self.preview_text.document())
        header_cursor.movePosition(QTextCursor.Start)
        for _ in range(4):
            header_cursor.movePosition(QTextCursor.Down)
        header_pos = header_cursor.position()
        
        # Find all matches in the preview text (after header)
        text = self.preview_text.toPlainText()
        
        # Build regex for finding matches
        try:
            pattern = self.current_search_pattern
            if self.search_engine.use_regex:
                flags = 0 if self.search_engine.case_sensitive else re.IGNORECASE
                regex = re.compile(pattern, flags)
            else:
                escaped_pattern = re.escape(pattern)
                if self.search_engine.whole_word:
                    escaped_pattern = r'\b' + escaped_pattern + r'\b'
                flags = 0 if self.search_engine.case_sensitive else re.IGNORECASE
                regex = re.compile(escaped_pattern, flags)
            
            # Find all matches after header only
            all_matches = [m for m in regex.finditer(text) if m.start() >= header_pos]
            
            if self.current_match_index < len(all_matches):
                match_obj = all_matches[self.current_match_index]
                
                # Create cursor and select the match
                cursor = QTextCursor(self.preview_text.document())
                cursor.setPosition(match_obj.start())
                cursor.setPosition(match_obj.end(), QTextCursor.KeepAnchor)
                
                # Apply orange highlight to current match
                current_format = QTextCharFormat()
                current_format.setBackground(QColor(255, 165, 0))  # Orange
                cursor.mergeCharFormat(current_format)
                
                # Move cursor to this position and ensure visible
                cursor.setPosition(match_obj.start())
                self.preview_text.setTextCursor(cursor)
                self.preview_text.ensureCursorVisible()
                
        except re.error:
            pass
    
    def update_match_navigation(self):
        """Update match counter and navigation button states"""
        if not self.current_file_matches:
            self.match_counter_label.setText("0/0")
            self.prev_match_btn.setEnabled(False)
            self.next_match_btn.setEnabled(False)
        else:
            total = len(self.current_file_matches)
            current = self.current_match_index + 1
            self.match_counter_label.setText(f"{current}/{total}")
            # Always enable buttons if there are matches (cycling enabled)
            self.prev_match_btn.setEnabled(True)
            self.next_match_btn.setEnabled(True)
    
    def go_to_previous_match(self):
        """Navigate to previous match (wraps to last)"""
        if not self.current_file_matches:
            return
        
        if self.current_match_index > 0:
            self.current_match_index -= 1
        else:
            # Wrap to last match
            self.current_match_index = len(self.current_file_matches) - 1
        
        self.highlight_all_matches()  # Re-highlight all
        self.jump_to_current_match()
        self.update_match_navigation()
    
    def go_to_next_match(self):
        """Navigate to next match (wraps to first)"""
        if not self.current_file_matches:
            return
        
        if self.current_match_index < len(self.current_file_matches) - 1:
            self.current_match_index += 1
        else:
            # Wrap to first match
            self.current_match_index = 0
        
        self.highlight_all_matches()  # Re-highlight all
        self.jump_to_current_match()
        self.update_match_navigation()
    
    def show_context_menu(self, position):
        """Show context menu for tree items"""
        item = self.results_tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu()
        
        # Get data from item
        data = item.data(0, Qt.UserRole)
        
        if isinstance(data, SearchMatch):
            # Single match
            open_action = menu.addAction("Open")
            open_action.triggered.connect(lambda: self.open_file(data.file_path, data.line_number))
            
            open_dir_action = menu.addAction("Open File Directory")
            open_dir_action.triggered.connect(lambda: self.open_file_directory(data.file_path))
            
            menu.addSeparator()
            
            copy_path_action = menu.addAction("Copy File Path")
            copy_path_action.triggered.connect(lambda: QApplication.clipboard().setText(data.file_path))
            
            copy_line_action = menu.addAction("Copy Line Content")
            copy_line_action.triggered.connect(lambda: QApplication.clipboard().setText(data.line_content))
            
        elif isinstance(data, list) and len(data) > 0:
            # File with multiple matches
            open_action = menu.addAction("Open")
            open_action.triggered.connect(lambda: self.open_file(data[0].file_path))
            
            open_dir_action = menu.addAction("Open Folder Directory")
            open_dir_action.triggered.connect(lambda: self.open_file_directory(data[0].file_path))
            
            menu.addSeparator()
            
            copy_path_action = menu.addAction("Copy File Path")
            copy_path_action.triggered.connect(lambda: QApplication.clipboard().setText(data[0].file_path))
            
            menu.addSeparator()
            
            expand_action = menu.addAction("Expand All")
            expand_action.triggered.connect(lambda: item.setExpanded(True))
            
            collapse_action = menu.addAction("Collapse All")
            collapse_action.triggered.connect(lambda: item.setExpanded(False))
        
        menu.exec(self.results_tree.viewport().mapToGlobal(position))
    
    def open_file(self, file_path, line_number=None):
        """Open file in default editor"""
        try:
            if line_number:
                # Try to open with VS Code if available
                try:
                    subprocess.Popen(['code', '-g', f'{file_path}:{line_number}'])
                except FileNotFoundError:
                    # VS Code not available, just open the file
                    os.startfile(file_path)
            else:
                # Use default application
                os.startfile(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open file: {str(e)}")
    
    def open_file_directory(self, file_path):
        """Open the directory containing the file"""
        try:
            directory = os.path.dirname(file_path)
            os.startfile(directory)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open directory: {str(e)}")
    
    def show_help(self):
        """Show comprehensive help dialog"""
        dialog = HelpDialog(self)
        dialog.exec()
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Advanced Search Tool",
            "<h3>Advanced Search Tool</h3>"
            "<p>Version 0.5.1</p>"
            "<p>Author: Randy Northrup</p>"
            "<p>A Windows GUI application for grep-style searching with advanced regex patterns and metadata search.</p>"
            "<p><b>Key Features:</b></p>"
            "<ul>"
            "<li>Grep-style pattern search with full regex support</li>"
            "<li>8 common regex patterns in quick-access menu</li>"
            "<li>Image metadata search (EXIF, GPS) for JPG, PNG, TIFF, etc.</li>"
            "<li>File metadata search (PDF, Office docs, audio/video)</li>"
            "<li>File browser with organized results tree</li>"
            "<li>Context display and syntax highlighting</li>"
            "<li>Performance optimizations and caching</li>"
            "</ul>"
            "<p>Built with Python, PySide6, Pillow, PyPDF2, and more</p>"
        )
    
    def load_search_history(self):
        """Load search history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.search_history = json.load(f)
                    # Limit to last 50 entries
                    self.search_history = self.search_history[-50:]
        except Exception as e:
            print(f"Failed to load search history: {e}")
            self.search_history = []
    
    def save_search_history(self):
        """Save search history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save search history: {e}")
    
    def add_to_search_history(self, pattern):
        """Add a search pattern to history"""
        if not pattern or pattern.strip() == "":
            return
        
        # Remove if already exists (to move to end)
        if pattern in self.search_history:
            self.search_history.remove(pattern)
        
        # Add to end
        self.search_history.append(pattern)
        
        # Limit to 50 entries
        if len(self.search_history) > 50:
            self.search_history = self.search_history[-50:]
        
        # Update dropdown and save
        self.update_search_history_dropdown()
        self.save_search_history()
    
    def update_search_history_dropdown(self):
        """Update the search input dropdown with history"""
        self.search_input.clear()
        # Add history in reverse order (most recent first)
        for pattern in reversed(self.search_history):
            self.search_input.addItem(pattern)
    
    def clear_search_history(self):
        """Clear all search history"""
        reply = QMessageBox.question(
            self,
            "Clear Search History",
            "Are you sure you want to clear all search history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.search_history = []
            self.update_search_history_dropdown()
            self.save_search_history()
            QMessageBox.information(self, "Success", "Search history has been cleared.")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
