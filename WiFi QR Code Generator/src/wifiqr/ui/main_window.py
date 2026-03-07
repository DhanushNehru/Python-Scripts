from __future__ import annotations

import json
from importlib import metadata
from dataclasses import replace
from pathlib import Path
from typing import override

from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import QModelIndex, QPoint, QSize, Qt, QTimer, Slot
from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QKeySequence,
    QPainter,
    QPalette,
    QPixmap,
    QResizeEvent,
    QShowEvent,
)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from wifiqr.constants import PREVIEW_RESIZE_THRESHOLD, SECURITY_OPTIONS
from wifiqr.services.export_service import pil_to_qpixmap
from wifiqr.services.macos_profile import (
    build_macos_mobileconfig,
    build_macos_mobileconfig_multi,
)
from wifiqr.services.qr_service import generate_qr_image, save_qr_image
from wifiqr.services.wifi_payload import WifiConfig, build_wifi_payload, is_open_security
from wifiqr.services.windows_script import (
    build_windows_connect_script,
    build_windows_connect_script_multi,
)

RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resources"


class MainWindow(QMainWindow):
    """Primary application window for building and exporting Wi-Fi QR codes."""

    STANDARD_SSID_CHARS = 32
    STANDARD_PASSWORD_CHARS = 63
    MAX_WINDOW_SIZE = 16777215
    TABLE_COLUMN_COUNT = 5
    TABLE_HEADER_LABELS = (
        "Location",
        "SSID",
        "Password",
        "Security",
        "Hidden",
    )
    INITIAL_TABLE_ROWS = 0
    NO_SEARCH_INDEX = -1
    WINDOW_MIN_WIDTH = 980
    WINDOW_MIN_HEIGHT = 620
    LAYOUT_MARGIN = 24
    LAYOUT_SPACING = 24
    LAYOUT_FORM_STRETCH = 1
    LAYOUT_TABLE_STRETCH = 2
    LAYOUT_PREVIEW_STRETCH = 1
    FORM_VERTICAL_SPACING = 14
    FORM_HORIZONTAL_SPACING = 12
    ACTION_LAYOUT_SPACING = 12
    PREVIEW_LAYOUT_SPACING = 16
    PREVIEW_MIN_SIZE = 420
    PREVIEW_TOGGLE_WIDTH = 44
    PREVIEW_TOGGLE_HEIGHT = 24
    PREVIEW_TOGGLE_SPACING = 8
    SEARCH_ROW_SPACING = 6
    TABLE_MIN_WIDTH = 520
    ACTION_BUTTON_MIN_WIDTH = 160
    ACTION_BUTTON_MIN_HEIGHT = 36
    TIMER_DELAY_MS = 0
    DEFAULT_EXPORT_INDEX = 0
    HEADER_TEXT_POINT_SIZE = 14
    HEADER_TEXT_PADDING = 16
    HEADER_TEXT_BASELINE_PADDING = 8
    TABLE_COLUMN_PADDING = 24
    TABLE_WIDTH_PADDING = 24
    PASSWORD_MASK_MIN_LENGTH = 6
    PASSWORD_TOGGLE_SIZE = 24
    DEFAULT_QR_HEADER_COLOR = "#0b1220"
    PAYLOAD_TEXT_STYLE = "color: #64748b; font-size: 11px;"
    PREVIEW_DEBOUNCE_MS = 180

    def __init__(self) -> None:
        """Initialize the main window and UI state."""
        super().__init__()
        self.setWindowTitle("WifiQR")
        self.setMinimumSize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)

        self.form_group: QGroupBox
        self.table_group: QGroupBox
        self.preview_group: QGroupBox
        self.location_input: QLineEdit
        self.ssid_input: QLineEdit
        self.password_input: QLineEdit
        self.security_input: QComboBox
        self.image_browse_button: QPushButton
        self.image_path_display: QLineEdit
        self.hidden_input: QCheckBox
        self.show_header_input: QCheckBox
        self.add_table_button: QPushButton
        self.print_button: QPushButton
        self.export_png_button: QPushButton
        self.export_pdf_button: QPushButton
        self.export_script_button: QPushButton
        self.export_macos_button: QPushButton
        self.batch_export_button: QPushButton
        self.preview_toggle: QToolButton
        self.preview_label: QLabel
        self.payload_label: QLabel
        self.search_input: QLineEdit
        self.search_up_button: QToolButton
        self.search_down_button: QToolButton
        self.network_table: QTableWidget
        self.delete_table_button: QPushButton

        self._config = WifiConfig(
            location="",
            ssid="",
            password="",
            security="WPA",
            hidden=False,
            image_data=None,
        )
        self._current_image_filename: str = ""
        self._current_pixmap: QPixmap | None = None
        self._current_payload = ""
        self._current_save_path: str | None = None
        self._sort_orders: dict[int, Qt.SortOrder] = {}
        self._search_matches: list[int] = []
        self._search_index: int = self.NO_SEARCH_INDEX
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._refresh_preview_now)
        self._last_preview_size = QSize()
        self._scaled_pixmap: QPixmap | None = None
        self._header_metrics: QFontMetrics | None = None
        self._item_metrics: QFontMetrics | None = None
        self._last_header_state = False
        self._last_location = ""
        self._last_image_data: str | None = None

        self._setup_ui()
        self._apply_style()
        self._refresh_preview()

    def _setup_ui(self) -> None:
        """Create and arrange all UI widgets."""
        self._build_menus()
        root = self._build_root_container()
        self._build_form_group()
        self._build_preview_group()
        self._build_table_group()
        self._finalize_layout(root)
        self._connect_form_signals()

    def _build_root_container(self) -> QWidget:
        """Create the root widget and horizontal layout."""
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN,
        )
        layout.setSpacing(self.LAYOUT_SPACING)
        layout.setStretch(0, self.LAYOUT_FORM_STRETCH)
        layout.setStretch(1, self.LAYOUT_TABLE_STRETCH)
        layout.setStretch(2, self.LAYOUT_PREVIEW_STRETCH)
        return root

    def _build_form_group(self) -> None:
        """Create the form group for Wi-Fi inputs and actions."""
        self.form_group = QGroupBox("Network details")
        self.form_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        form_layout = QFormLayout(self.form_group)
        form_layout.setVerticalSpacing(self.FORM_VERTICAL_SPACING)
        form_layout.setHorizontalSpacing(self.FORM_HORIZONTAL_SPACING)

        self._build_form_inputs()
        self._build_action_buttons()
        # Add spacing before bottom row
        form_layout.addRow("", QWidget())
        self._build_bottom_row(form_layout)

    def _build_form_inputs(self) -> None:
        """Create form inputs for location, SSID, and security."""
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g. HQ West")
        self.location_input.setToolTip("Location identifier for this network.")
        self.location_input.setAccessibleName("Network Location")

        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("e.g. Office-Guest")
        self.ssid_input.setToolTip("Network name (SSID). Case sensitive.")
        self.ssid_input.setAccessibleName("Network SSID")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip(
            "Network password. Disabled for open networks."
        )
        self.password_input.setAccessibleName("Network Password")

        self.security_input = QComboBox()
        self.security_input.addItems(list(SECURITY_OPTIONS))
        self.security_input.setMaxVisibleItems(3)
        view = self.security_input.view()
        palette = view.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        view.setPalette(palette)
        self.security_input.setToolTip("Select the network security type.")
        self.security_input.setAccessibleName("Security Type")

        self.image_path_display = QLineEdit()
        self.image_path_display.setPlaceholderText("No image selected (optional)")
        self.image_path_display.setReadOnly(True)
        self.image_path_display.setToolTip(
            "Selected center image (PNG, JPG, JPEG, BMP, GIF, SVG). SVG is converted to PNG."
        )

        self.image_browse_button = QPushButton("...", self.image_path_display)
        self.image_browse_button.setToolTip(
            "Select a center image for the QR code (PNG, JPG, JPEG, BMP, GIF, SVG)."
        )
        self.image_browse_button.setFixedSize(30, 24)
        self.image_browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_browse_button.clicked.connect(self._browse_image)

        # Position button inside text field on the right
        self.image_path_display.setStyleSheet("QLineEdit { padding-right: 35px; }")

        self.hidden_input = QCheckBox("Hidden network")
        self.hidden_input.setToolTip("Enable if the SSID is hidden (non-broadcast).")
        self.hidden_input.setTristate(False)
        self.hidden_input.setAccessibleName("Hidden Network Toggle")

        self.show_header_input = QCheckBox("Show location header")
        self.show_header_input.setToolTip(
            "Include location text above the QR code in preview, prints, and exports."
        )
        self.show_header_input.setTristate(False)
        self.show_header_input.setChecked(True)
        self.show_header_input.setAccessibleName("Show Header Toggle")

        # Put checkboxes side by side
        checkbox_row = QHBoxLayout()
        checkbox_row.setSpacing(20)
        checkbox_row.addWidget(self.hidden_input)
        checkbox_row.addWidget(self.show_header_input)
        checkbox_row.addStretch(1)

        form_layout = self.form_group.layout()
        assert isinstance(form_layout, QFormLayout)
        form_layout.addRow("Location", self.location_input)
        form_layout.addRow("SSID", self.ssid_input)
        form_layout.addRow("Password", self.password_input)
        form_layout.addRow("Security", self.security_input)
        form_layout.addRow("Center Image", self.image_path_display)
        form_layout.addRow(checkbox_row)

    def _build_action_buttons(self) -> None:
        """Create and place action buttons for exports and table actions."""
        self._create_action_buttons()
        self._add_action_layout()

    def _create_action_buttons(self) -> None:
        """Instantiate action buttons and assign handlers."""
        self.add_table_button = QPushButton("Add to Table")
        self.add_table_button.clicked.connect(self._add_to_table)
        self._configure_action_button(
            self.add_table_button,
            "Add to Table",
            "Add current network to the table.",
        )

        self.print_button = QPushButton("Print")
        self.print_button.clicked.connect(self._print)
        self._configure_action_button(
            self.print_button,
            "Print",
            "Print the QR code with the optional location header.",
        )

        self.export_png_button = QPushButton("Export PNG")
        self.export_png_button.clicked.connect(self._export_png)
        self._configure_action_button(
            self.export_png_button,
            "Export PNG",
            "Export the QR code as a PNG image with the optional location header.",
        )

        self.export_pdf_button = QPushButton("Export PDF")
        self.export_pdf_button.clicked.connect(self._export_pdf)
        self._configure_action_button(
            self.export_pdf_button,
            "Export PDF",
            "Export the QR code as a PDF document with the optional location header.",
        )

        self.export_script_button = QPushButton("Export Windows Script")
        self.export_script_button.clicked.connect(self._export_windows_script)
        self._configure_action_button(
            self.export_script_button,
            "Export Windows Script",
            "Export a Windows .cmd file that adds the profile and connects.",
        )

        self.export_macos_button = QPushButton("Export macOS Profile")
        self.export_macos_button.clicked.connect(self._export_macos_profile)
        self._configure_action_button(
            self.export_macos_button,
            "Export macOS Profile",
            "Export a macOS .mobileconfig profile for one-click install.",
        )

        self.batch_export_button = QPushButton("Batch Export")
        self.batch_export_button.clicked.connect(self._batch_export)
        self._configure_action_button(
            self.batch_export_button,
            "Batch Export",
            "Export selected networks in bulk (or the current network if none selected).",
        )

        self.delete_table_button = QPushButton("Delete Selected")
        self.delete_table_button.clicked.connect(self._remove_selected)
        self._configure_action_button(
            self.delete_table_button,
            "Delete Selected",
            "Delete selected network(s) from the table.",
        )

    def _add_action_layout(self) -> None:
        """Add the action buttons to the form layout."""
        action_layout = QGridLayout()
        action_layout.setHorizontalSpacing(self.ACTION_LAYOUT_SPACING)
        action_layout.setVerticalSpacing(self.ACTION_LAYOUT_SPACING)
        action_layout.setColumnStretch(0, 1)
        action_layout.setColumnStretch(1, 1)
        action_layout.setColumnStretch(2, 1)
        action_layout.addWidget(self.print_button, 0, 0)
        action_layout.addWidget(self.export_png_button, 0, 1)
        action_layout.addWidget(self.export_pdf_button, 0, 2)
        action_layout.addWidget(self.export_script_button, 1, 0)
        action_layout.addWidget(self.export_macos_button, 1, 1)
        action_layout.addWidget(self.batch_export_button, 1, 2)
        action_layout.addWidget(self.add_table_button, 2, 0)

        form_layout = self.form_group.layout()
        if isinstance(form_layout, QFormLayout):
            form_layout.addRow(action_layout)

    def _build_bottom_row(self, form_layout: QFormLayout) -> None:
        """Create bottom row with delete button and preview toggle."""
        self.preview_toggle = QToolButton()
        self.preview_toggle.setCheckable(True)
        self.preview_toggle.setChecked(True)
        self.preview_toggle.setToolTip("Show or hide the preview panel.")
        self.preview_toggle.setObjectName("PreviewToggle")
        self.preview_toggle.setFixedSize(
            self.PREVIEW_TOGGLE_WIDTH,
            self.PREVIEW_TOGGLE_HEIGHT,
        )
        self.preview_toggle.setIconSize(self.preview_toggle.size())
        self.preview_toggle.toggled.connect(self._toggle_preview_panel)
        self._update_preview_toggle_icon()

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(QLabel("Show preview"))
        bottom_row.addSpacing(self.PREVIEW_TOGGLE_SPACING)
        bottom_row.addWidget(self.preview_toggle)
        bottom_row.addStretch(1)
        bottom_row.addWidget(self.delete_table_button)
        form_layout.addRow(bottom_row)

    def _build_preview_group(self) -> None:
        """Create the preview group for QR output."""
        self.preview_group = QGroupBox("Preview")
        self.preview_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        preview_layout = QVBoxLayout(self.preview_group)
        preview_layout.setSpacing(self.PREVIEW_LAYOUT_SPACING)

        self.preview_label = QLabel("Enter network details to generate a QR code")
        self.preview_label.setObjectName("PreviewLabel")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(
            self.PREVIEW_MIN_SIZE,
            self.PREVIEW_MIN_SIZE,
        )

        self.payload_label = QLabel("")
        self.payload_label.setWordWrap(True)
        self.payload_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.payload_label.setStyleSheet(self.PAYLOAD_TEXT_STYLE)

        preview_layout.addWidget(self.preview_label, stretch=1)
        preview_layout.addWidget(self.payload_label)

    def _build_table_group(self) -> None:
        """Create the saved networks table group."""
        self.table_group = QGroupBox("Saved networks")
        self.table_group.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.table_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_layout = QVBoxLayout(self.table_group)
        table_layout.setSpacing(self.ACTION_LAYOUT_SPACING)

        search_row = self._build_table_search_row()
        self._build_network_table()

        table_layout.addLayout(search_row)
        table_layout.addWidget(self.network_table)

        self._update_button_labels()
        self._apply_table_column_widths()

    def _build_table_search_row(self) -> QHBoxLayout:
        """Create the search row with navigation controls."""
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by location or SSID")
        self.search_input.setToolTip("Filter saved networks by location or SSID.")
        self.search_input.textChanged.connect(self._apply_search_filter)

        search_row = QHBoxLayout()
        search_row.setSpacing(self.SEARCH_ROW_SPACING)

        self.search_up_button = QToolButton()
        self.search_up_button.setToolTip("Find previous")
        self.search_up_button.clicked.connect(self._find_previous)

        self.search_down_button = QToolButton()
        self.search_down_button.setToolTip("Find next")
        self.search_down_button.clicked.connect(self._find_next)

        up_icon = RESOURCE_DIR / "chevron_up.svg"
        down_icon = RESOURCE_DIR / "chevron_down.svg"
        self._set_icon_if_exists(self.search_up_button, up_icon)
        self._set_icon_if_exists(self.search_down_button, down_icon)

        search_row.addWidget(self.search_input)
        search_row.addWidget(self.search_up_button)
        search_row.addWidget(self.search_down_button)
        return search_row

    def _build_network_table(self) -> None:
        """Create the network table widget and connect events."""
        self.network_table = QTableWidget(self.INITIAL_TABLE_ROWS, self.TABLE_COLUMN_COUNT)
        self.network_table.setHorizontalHeaderLabels(list(self.TABLE_HEADER_LABELS))

        # Center all header labels
        for i in range(self.TABLE_COLUMN_COUNT):
            header_item = self.network_table.horizontalHeaderItem(i)
            if header_item:
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        header = self.network_table.horizontalHeader()

        # Calculate minimum widths based on header labels
        font_metrics = QFontMetrics(header.font())
        min_widths = {}
        for i, label in enumerate(self.TABLE_HEADER_LABELS):
            min_widths[i] = font_metrics.horizontalAdvance(label) + 30

        # Set resize modes: Interactive for resizable columns, Fixed for pinned columns
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # Location
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # SSID
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # Password
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Security (pinned)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Hidden (pinned)
        header.setStretchLastSection(False)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)  # Center all header labels

        # Set minimum widths for all columns
        for _col, min_width in min_widths.items():
            header.setMinimumSectionSize(min_width)

        # Set initial column widths
        self.network_table.setColumnWidth(0, max(150, min_widths[0]))
        self.network_table.setColumnWidth(1, max(200, min_widths[1]))
        self.network_table.setColumnWidth(2, max(200, min_widths[2]))
        self.network_table.setColumnWidth(3, 100)  # Security - uniform width
        self.network_table.setColumnWidth(4, 100)  # Hidden - uniform width

        # Connect to handle gap prevention
        header.sectionResized.connect(self._handle_column_resize)

        self.network_table.verticalHeader().setDefaultSectionSize(45)
        self.network_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.network_table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
        )
        self.network_table.setSortingEnabled(False)
        self.network_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.network_table.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.network_table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.network_table.horizontalScrollBar().setSingleStep(10)
        self.network_table.horizontalHeader().sectionClicked.connect(
            self._handle_sort
        )
        self.network_table.itemChanged.connect(self._table_item_changed)
        self.network_table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.network_table.customContextMenuRequested.connect(
            self._table_context_menu
        )
        self.network_table.doubleClicked.connect(self._table_double_clicked)

    def _finalize_layout(self, root: QWidget) -> None:
        """Attach groups to the root layout and set the central widget."""
        layout = root.layout()
        assert isinstance(layout, QHBoxLayout)
        layout.addWidget(self.form_group, self.LAYOUT_FORM_STRETCH)
        layout.addWidget(self.table_group, self.LAYOUT_TABLE_STRETCH)
        layout.addWidget(self.preview_group, self.LAYOUT_PREVIEW_STRETCH)
        self.setCentralWidget(root)

    def _connect_form_signals(self) -> None:
        """Wire input changes to preview refresh handlers."""
        self.ssid_input.textChanged.connect(self._refresh_preview)
        self.location_input.textChanged.connect(self._refresh_preview)
        self.password_input.textChanged.connect(self._refresh_preview)
        self.security_input.currentTextChanged.connect(self._on_security_changed)
        self.hidden_input.stateChanged.connect(self._refresh_preview)
        self.show_header_input.stateChanged.connect(self._refresh_preview)
        self._update_password_state()

    def _apply_style(self) -> None:
        """Apply the application stylesheet if available."""
        style_path = RESOURCE_DIR / "style.qss"
        if style_path.exists():
            self.setStyleSheet(style_path.read_text(encoding="utf-8"))

    def _configure_action_button(self, button: QPushButton, label: str, tooltip: str) -> None:
        """Standardize action button styling and tooltip text."""
        button.setToolTip(tooltip)
        button.setProperty("fullText", label)
        button.setMinimumWidth(self.ACTION_BUTTON_MIN_WIDTH)
        button.setMinimumHeight(self.ACTION_BUTTON_MIN_HEIGHT)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _set_icon_if_exists(self, widget: QPushButton | QToolButton, icon_path: Path) -> None:
        """Assign an icon when the resource exists."""
        if icon_path.exists():
            widget.setIcon(QIcon(str(icon_path)))

    def _build_menus(self) -> None:
        """Create the menu bar actions."""
        file_menu = self.menuBar().addMenu("File")

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_as)

        load_action = QAction("Load...", self)
        load_action.setShortcut(QKeySequence.StandardKey.Open)
        load_action.triggered.connect(self._load)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = self.menuBar().addMenu("Edit")

        add_action = QAction("Add to Table", self)
        add_action.setShortcut(QKeySequence("Ctrl+Return"))
        add_action.triggered.connect(self._add_to_table)

        delete_action = QAction("Delete Selected", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self._remove_selected)

        find_action = QAction("Find...", self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.triggered.connect(self._focus_search)

        edit_menu.addAction(add_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_action)

        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _browse_image(self) -> None:
        """Open file dialog to select a center image for the QR code."""
        import base64
        import io
        import os

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Center Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.svg)",
        )
        if not path:
            return

        try:
            # Read and validate image bytes
            with open(path, "rb") as f:
                image_bytes = f.read()
            _, ext = os.path.splitext(path)
            if ext.lower() == ".svg":
                import cairosvg  # type: ignore[import-untyped]

                image_bytes = cairosvg.svg2png(bytestring=image_bytes)
            if not isinstance(image_bytes, (bytes, bytearray, memoryview)):
                raise ValueError("Image data is empty or invalid.")
            image_bytes = bytes(image_bytes)
            with Image.open(io.BytesIO(image_bytes)) as image:
                image.verify()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as exc:
            QMessageBox.warning(self, "Image Load Failed", f"Could not load image: {exc}")
            return

        # Update UI and config
        self.image_path_display.setText(path)
        self._config = replace(self._config, image_data=image_base64)
        self._refresh_preview()

    def _update_config(self) -> None:
        """Sync form input values into the current config."""
        self._config = replace(
            self._config,
            location=self.location_input.text().strip(),
            ssid=self.ssid_input.text().strip(),
            password=self.password_input.text(),
            security=self.security_input.currentText(),
            hidden=self.hidden_input.isChecked(),
            # Preserve image_data from current config
        )

    @Slot()
    def _refresh_preview(self) -> None:
        """Debounce QR preview updates for smoother typing."""
        self._preview_timer.start(self.PREVIEW_DEBOUNCE_MS)

    def _refresh_preview_now(self) -> None:
        """Recompute QR preview and payload text."""
        self._update_config()

        if not self._config.ssid:
            self._current_pixmap = None
            self._current_payload = ""
            self._scaled_pixmap = None
            self._last_preview_size = QSize()
            self._last_image_data = None
            self.preview_label.clear()
            self.preview_label.setText("Enter network details to generate a QR code")
            self.payload_label.setText("")
            self._toggle_actions(False)
            return

        payload = build_wifi_payload(self._config)
        header_state = self.show_header_input.isChecked()
        current_location = self._config.location

        # Regenerate if payload, header state, or location changed
        should_regenerate = (
            payload != self._current_payload or
            header_state != self._last_header_state or
            current_location != self._last_location or
            self._config.image_data != self._last_image_data or
            self._current_pixmap is None
        )

        if should_regenerate:
            self._current_payload = payload
            self._last_header_state = header_state
            self._last_location = current_location
            self._last_image_data = self._config.image_data
            try:
                image = generate_qr_image(
                    self._current_payload, center_image_data=self._config.image_data
                )
                # Add header to preview if enabled and location exists
                if header_state and current_location:
                    image = self._compose_qr_with_header(image, current_location)
                self._current_pixmap = pil_to_qpixmap(image)
                self._scaled_pixmap = None  # Clear cache to force rescale
            except Exception as exc:
                QMessageBox.critical(self, "QR generation failed", str(exc))
                self._toggle_actions(False)
                return

        self._update_scaled_preview()
        self.preview_label.setText("")
        self.preview_label.update()
        self.payload_label.setText(self._current_payload)
        self._toggle_actions(True)

    def _toggle_actions(self, enabled: bool) -> None:
        """Enable or disable action buttons based on QR state."""
        self.print_button.setEnabled(enabled)
        self.export_png_button.setEnabled(enabled)
        self.export_pdf_button.setEnabled(enabled)
        self.export_script_button.setEnabled(enabled)
        self.export_macos_button.setEnabled(enabled)
        self.batch_export_button.setEnabled(enabled)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events for responsive preview scaling."""
        super().resizeEvent(event)
        if self._current_pixmap:
            self._update_scaled_preview()
        self._update_button_labels()
        self._position_image_button()

    @override
    def showEvent(self, event: QShowEvent) -> None:
        """Finalize layout sizing when the window is shown."""
        super().showEvent(event)
        QTimer.singleShot(self.TIMER_DELAY_MS, self._update_button_labels)
        QTimer.singleShot(self.TIMER_DELAY_MS, self._apply_panel_minimums)
        QTimer.singleShot(self.TIMER_DELAY_MS, self._lock_window_size)
        QTimer.singleShot(self.TIMER_DELAY_MS, self._position_image_button)

    def _position_image_button(self) -> None:
        """Position the browse button inside the image path text field."""
        text_field_height = self.image_path_display.height()
        button_height = self.image_browse_button.height()
        y_pos = (text_field_height - button_height) // 2
        x_pos = self.image_path_display.width() - self.image_browse_button.width() - 5
        self.image_browse_button.move(x_pos, y_pos)

    def _lock_window_size(self) -> None:
        """Lock the window size to the layout's size hint."""
        self.setMinimumSize(0, 0)
        self.setMaximumSize(self.MAX_WINDOW_SIZE, self.MAX_WINDOW_SIZE)
        central = self.centralWidget()
        layout = central.layout() if central else None
        if layout:
            layout.activate()
            layout.update()

        # Force proper size calculation
        central.adjustSize()
        self.adjustSize()

        target = self.sizeHint()
        self.resize(target)
        self.setMinimumSize(target)
        self.setMaximumSize(target)

    def _lock_window_width_only(self, height: int) -> None:
        """Lock the window width while maintaining the given height."""
        self.setMinimumSize(0, 0)
        self.setMaximumSize(self.MAX_WINDOW_SIZE, self.MAX_WINDOW_SIZE)
        central = self.centralWidget()
        layout = central.layout() if central else None
        if layout:
            layout.activate()
        target_width = central.sizeHint().width() if central else self.sizeHint().width()
        self.resize(target_width, height)
        self.setMinimumSize(target_width, height)
        self.setMaximumSize(target_width, height)

    def _update_preview_toggle_icon(self) -> None:
        """Update the preview toggle icon to match its state."""
        on_icon = RESOURCE_DIR / "toggle_on.svg"
        off_icon = RESOURCE_DIR / "toggle_off.svg"
        if self.preview_toggle.isChecked() and on_icon.exists():
            self.preview_toggle.setIcon(QIcon(str(on_icon)))
        elif not self.preview_toggle.isChecked() and off_icon.exists():
            self.preview_toggle.setIcon(QIcon(str(off_icon)))

    def _toggle_preview_panel(self, checked: bool) -> None:
        """Show or hide the preview panel."""
        # Save current window height - it should never change
        current_height = self.height()

        self.preview_group.setVisible(checked)
        self._update_preview_toggle_icon()

        # Allow layout to recalculate width, then lock it
        QTimer.singleShot(0, lambda: self._lock_window_width_only(current_height))

    def _update_scaled_preview(self) -> None:
        """Scale and apply the QR preview pixmap only when needed."""
        if not self._current_pixmap:
            self.preview_label.clear()
            return

        size = self.preview_label.size()

        # Skip rescaling if size difference is minimal (< PREVIEW_RESIZE_THRESHOLD px)
        if self._last_preview_size.isValid() and self._scaled_pixmap:
            w_diff = abs(size.width() - self._last_preview_size.width())
            h_diff = abs(size.height() - self._last_preview_size.height())
            if w_diff < PREVIEW_RESIZE_THRESHOLD and h_diff < PREVIEW_RESIZE_THRESHOLD:
                self.preview_label.setPixmap(self._scaled_pixmap)
                return

        self._last_preview_size = size
        self._scaled_pixmap = self._current_pixmap.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setPixmap(self._scaled_pixmap)

    def _on_security_changed(self, value: str) -> None:
        """Update password state and refresh preview on security changes."""
        self._update_password_state(value)
        self._refresh_preview()

    def _update_password_state(self, security_value: str | None = None) -> None:
        """Enable or disable password input based on security type."""
        security_value = security_value or self.security_input.currentText()
        is_open = is_open_security(security_value)
        self.password_input.setEnabled(not is_open)
        if is_open:
            self.password_input.setPlaceholderText("Not required for open networks")
        else:
            self.password_input.setPlaceholderText("Password")

    def _apply_panel_minimums(self) -> None:
        """Clamp group minimum sizes to their size hints."""
        # First get max height across all visible panels
        max_height = 0
        for group in (self.form_group, self.table_group, self.preview_group):
            if group.isVisible():
                max_height = max(max_height, group.sizeHint().height())

        # Now apply sizes
        for group in (self.form_group, self.table_group, self.preview_group):
            if not group.isVisible():
                group.setMinimumSize(0, 0)
                continue
            size = group.sizeHint()
            group.setMinimumSize(size.width(), max_height)
            group.setMaximumHeight(max_height)
            group.updateGeometry()
        self._update_table_group_width()

    def _update_button_labels(self) -> None:
        """Normalize action button labels and widths."""
        buttons = (
            self.print_button,
            self.export_png_button,
            self.export_pdf_button,
            self.export_script_button,
            self.export_macos_button,
            self.batch_export_button,
            self.add_table_button,
            self.delete_table_button,
        )
        for button in buttons:
            full_text = button.property("fullText") or button.text()
            base_size = button.property("basePointSize")
            if not base_size:
                base_size = button.font().pointSizeF()
                button.setProperty("basePointSize", base_size)
            font = QFont(button.font())
            font.setPointSizeF(float(base_size))
            button.setFont(font)
            button.setText(str(full_text))

        max_width = 0
        for button in buttons:
            max_width = max(max_width, button.sizeHint().width())

        for button in buttons:
            button.setMinimumWidth(max_width)

    def _render_pixmap(self, printer: QPrinter) -> None:
        """Render the current QR pixmap to a printer device."""
        if not self._current_pixmap:
            return
        painter = QPainter(printer)
        try:
            rect = painter.viewport()
            size = self._current_pixmap.size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self._current_pixmap.rect())
            painter.drawPixmap(0, 0, self._current_pixmap)
        finally:
            painter.end()

    @Slot()
    def _print(self) -> None:
        """Open the print dialog and print the QR preview."""
        if not self._current_pixmap:
            return
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self._render_pixmap(printer)

    @Slot()
    def _export_png(self) -> None:
        """Export the current QR as a PNG file."""
        if not self._current_pixmap:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PNG",
            "wifi-qr.png",
            "PNG Image (*.png)",
        )
        if not path:
            return
        try:
            self._export_png_to_path(self._config, path)
        except Exception as exc:
            QMessageBox.critical(self, "Export failed", str(exc))

    @Slot()
    def _export_pdf(self) -> None:
        """Export the current QR as a PDF file."""
        if not self._current_pixmap:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF",
            "wifi-qr.pdf",
            "PDF Document (*.pdf)",
        )
        if not path:
            return
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(path)
            self._export_pdf_to_path(self._config, printer)
        except Exception as exc:
            QMessageBox.critical(self, "Export failed", str(exc))

    @Slot()
    def _export_windows_script(self) -> None:
        """Export a Windows connect script for the current config."""
        if not self._current_payload:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Windows Script",
            "connect-wifi.cmd",
            "Command Script (*.cmd)",
        )
        if not path:
            return
        try:
            self._export_windows_script_to_path(self._config, path)
            QMessageBox.information(
                self,
                "Export complete",
                "Script exported. Run it as Administrator on Windows.",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Export failed", str(exc))

    @Slot()
    def _export_macos_profile(self) -> None:
        """Export a macOS configuration profile for the current config."""
        if not self._current_payload:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export macOS Profile",
            "wifi-profile.mobileconfig",
            "Configuration Profile (*.mobileconfig)",
        )
        if not path:
            return
        try:
            self._export_macos_profile_to_path(self._config, path)
            QMessageBox.information(
                self,
                "Export complete",
                "Profile exported. Double-click on macOS to install.",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Export failed", str(exc))

    def _export_png_to_path(self, config: WifiConfig, path: str) -> None:
        """Write a QR PNG for a config to the target path."""
        payload = build_wifi_payload(config)
        image = generate_qr_image(payload, center_image_data=config.image_data)
        if self.show_header_input.isChecked():
            image = self._compose_qr_with_header(image, config.location)
        save_qr_image(image, path)

    def _export_pdf_to_path(self, config: WifiConfig, printer: QPrinter) -> None:
        """Write a QR PDF for a config to the target printer."""
        payload = build_wifi_payload(config)
        image = generate_qr_image(payload, center_image_data=config.image_data)
        pixmap = pil_to_qpixmap(image)
        painter = QPainter(printer)
        try:
            rect = painter.viewport()
            header_text = config.location.strip() if self.show_header_input.isChecked() else ""
            header_height = 0
            if header_text:
                font = QFont(painter.font())
                font.setPointSize(self.HEADER_TEXT_POINT_SIZE)
                painter.setFont(font)
                metrics = QFontMetrics(font)
                header_height = metrics.height() + self.HEADER_TEXT_PADDING
                painter.drawText(
                    rect.x(),
                    rect.y() + metrics.ascent() + self.HEADER_TEXT_BASELINE_PADDING,
                    rect.width(),
                    metrics.height(),
                    Qt.AlignmentFlag.AlignHCenter,
                    header_text,
                )
            size = pixmap.size()
            available = rect.size()
            available.setHeight(max(1, available.height() - header_height))
            size.scale(available, Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y() + header_height, size.width(), size.height())
            painter.setWindow(pixmap.rect())
            painter.drawPixmap(0, 0, pixmap)
        finally:
            painter.end()

    def _compose_qr_with_header(self, image: Image.Image, header: str) -> Image.Image:
        """Return a new image with a location header added."""
        header = header.strip()
        if not header:
            return image

        # Use a larger font for title-sized header
        font = ImageFont.load_default(size=48)

        draw = ImageDraw.Draw(image)
        bbox = draw.textbbox((0, 0), header, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        padding = self.HEADER_TEXT_PADDING * 2
        new_width = int(image.width)
        new_height = int(image.height + text_height + padding * 2)
        new_image = Image.new("RGB", (new_width, new_height), "white")
        y_offset = int(text_height + padding * 2)
        new_image.paste(image, (0, y_offset))
        draw = ImageDraw.Draw(new_image)
        x = (new_width - text_width) // 2
        y = padding
        draw.text((x, y), header, fill=self.DEFAULT_QR_HEADER_COLOR, font=font)
        return new_image

    def _export_windows_script_to_path(self, config: WifiConfig, path: str) -> None:
        """Write a Windows connect script to disk."""
        script = build_windows_connect_script(config)
        with open(path, "w", encoding="utf-8") as file:
            file.write(script.content)

    def _export_macos_profile_to_path(self, config: WifiConfig, path: str) -> None:
        """Write a macOS profile to disk."""
        profile = build_macos_mobileconfig(config)
        with open(path, "w", encoding="utf-8") as file:
            file.write(profile.content)

    def _batch_export(self) -> None:
        """Batch export selected or all table entries."""
        configs = self._selected_or_all_configs()
        if not configs:
            if self._config.ssid:
                configs = [self._config]
            else:
                return

        export_type, ok = QInputDialog.getItem(
            self,
            "Batch Export",
            "Choose export type:",
            ["PNG", "PDF", "Windows Script", "macOS Profile"],
            self.DEFAULT_EXPORT_INDEX,
            False,
        )
        if not ok:
            return

        target_dir = QFileDialog.getExistingDirectory(self, "Select export folder")
        if not target_dir:
            return

        target_dir_path = Path(target_dir)

        if export_type == "Windows Script":
            script_path = target_dir_path / "wifi-batch.cmd"
            script = build_windows_connect_script_multi(configs)
            with open(script_path, "w", encoding="utf-8") as file:
                file.write(script.content)
            return
        if export_type == "macOS Profile":
            profile_path = target_dir_path / "wifi-batch.mobileconfig"
            profile = build_macos_mobileconfig_multi(configs)
            with open(profile_path, "w", encoding="utf-8") as file:
                file.write(profile.content)
            return

        for config in configs:
            safe_name = self._sanitize_filename(config.ssid)
            if export_type == "PNG":
                self._export_png_to_path(config, str(target_dir_path / f"{safe_name}.png"))
            elif export_type == "PDF":
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(str(target_dir_path / f"{safe_name}.pdf"))
                self._export_pdf_to_path(config, printer)

    def _add_to_table(self) -> None:
        """Add the current config to the table."""
        self._update_config()
        if not self._config.ssid:
            return
        self._add_or_update_row(self._config)

    def _remove_selected(self) -> None:
        """Remove selected rows from the table."""
        rows = sorted(self._selected_rows(), reverse=True)
        for row in rows:
            self.network_table.removeRow(row)
        self._apply_table_column_widths()

    def _add_or_update_row(self, config: WifiConfig, row: int | None = None) -> None:
        """Insert or update a table row for a config."""
        if row is None:
            row = self.network_table.rowCount()
            self.network_table.insertRow(row)

        self.network_table.blockSignals(True)
        location_item = QTableWidgetItem(config.location)
        location_item.setFlags(location_item.flags() | Qt.ItemFlag.ItemIsEditable)
        # Store image_data in the location item's UserRole
        location_item.setData(Qt.ItemDataRole.UserRole, config.image_data)

        ssid_item = QTableWidgetItem(config.ssid)
        ssid_item.setFlags(ssid_item.flags() | Qt.ItemFlag.ItemIsEditable)

        password_item = QTableWidgetItem("")
        password_item.setFlags(password_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        password_item.setData(Qt.ItemDataRole.UserRole, config.password)

        self.network_table.setItem(row, 0, location_item)
        self.network_table.setItem(row, 1, ssid_item)
        self.network_table.setItem(row, 2, password_item)

        password_widget = self._build_password_widget(row, config.password)
        self.network_table.setCellWidget(row, 2, password_widget)

        security_combo = QComboBox()
        security_combo.addItems(list(SECURITY_OPTIONS))
        security_combo.setCurrentText(config.security)
        security_combo.setMaxVisibleItems(3)
        view = security_combo.view()
        palette = view.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        view.setPalette(palette)
        security_combo.currentTextChanged.connect(
            lambda value, r=row: self._security_changed(r, value)
        )
        self.network_table.setCellWidget(row, 3, security_combo)

        hidden_checkbox = QCheckBox()
        hidden_checkbox.setChecked(config.hidden)
        hidden_checkbox.stateChanged.connect(
            lambda state, r=row: self._hidden_changed(r, state)
        )
        hidden_container = QWidget()
        hidden_layout = QHBoxLayout(hidden_container)
        hidden_layout.addWidget(hidden_checkbox)
        hidden_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hidden_layout.setContentsMargins(0, 0, 0, 0)
        self.network_table.setCellWidget(row, 4, hidden_container)

        self.network_table.blockSignals(False)
        self._apply_table_column_widths()

    def _table_item_changed(self, item: QTableWidgetItem) -> None:
        """Normalize table item values and adjust widths."""
        if item.column() == 0 and not item.text().strip():
            item.setText("Unnamed")
        if item.column() == 1 and not item.text().strip():
            item.setText("Unnamed")
        if item.column() == 3 and not item.text().strip():
            item.setText(SECURITY_OPTIONS[0])
        if item.column() in {1, 2}:
            self._apply_table_column_widths()

    def _view_password(self, row: int) -> None:
        """Prompt for a new password for a table row."""
        password_item = self.network_table.item(row, 2)
        if not password_item:
            return
        current = password_item.data(Qt.ItemDataRole.UserRole) or ""
        value, ok = QInputDialog.getText(
            self,
            "Password",
            "Edit password:",
            QLineEdit.EchoMode.Password,
            str(current),
        )
        if not ok:
            return
        password_item.setData(Qt.ItemDataRole.UserRole, value)
        self._update_password_widget(row, value, force_visible=False)

    def _obfuscate_password(self, value: str) -> str:
        """Return an obfuscated display string for a password."""
        if not value:
            return ""
        return "•" * max(self.PASSWORD_MASK_MIN_LENGTH, len(value))

    def _build_password_widget(self, row: int, password: str) -> QWidget:
        """Build a password display widget with a visibility toggle."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        label = QLabel(self._obfuscate_password(password))
        label.setProperty("isVisible", False)

        icon_path = RESOURCE_DIR / "eye.svg"
        button = QPushButton()
        self._set_icon_if_exists(button, icon_path)
        button.setToolTip("Toggle password visibility")
        button.setFixedSize(self.PASSWORD_TOGGLE_SIZE, self.PASSWORD_TOGGLE_SIZE)
        button.clicked.connect(lambda *_: self._toggle_password_visibility(row))

        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(button)
        return container

    def _update_password_widget(
        self,
        row: int,
        password: str,
        force_visible: bool | None = None,
    ) -> None:
        """Update the password widget contents for a row."""
        widget = self.network_table.cellWidget(row, 2)
        if not widget:
            return
        label = widget.findChild(QLabel)
        if not label:
            return
        is_visible = bool(label.property("isVisible"))
        if force_visible is not None:
            is_visible = force_visible
        label.setProperty("isVisible", is_visible)
        label.setText(password if is_visible else self._obfuscate_password(password))
        self._apply_table_column_widths()

    def _apply_table_column_widths(self) -> None:
        """Calculate and apply column widths for the table."""
        # Cache font metrics to avoid repeated calculations
        if not self._header_metrics:
            self._header_metrics = QFontMetrics(
                self.network_table.horizontalHeader().font()
            )
        if not self._item_metrics:
            self._item_metrics = QFontMetrics(self.network_table.font())

        standard_ssid_width = self._item_metrics.horizontalAdvance(
            "M" * self.STANDARD_SSID_CHARS
        )
        standard_pwd_width = self._item_metrics.horizontalAdvance(
            "M" * self.STANDARD_PASSWORD_CHARS
        )

        for column in range(self.network_table.columnCount()):
            if column in (3, 4):  # Skip Security, Hidden columns
                continue

            header_item = self.network_table.horizontalHeaderItem(column)
            header_text = header_item.text() if header_item else ""
            max_width = self._header_metrics.horizontalAdvance(header_text)
            max_width = max(max_width, self.network_table.sizeHintForColumn(column))

            if column == 1:
                max_width = max(max_width, standard_ssid_width)
            elif column == 2:
                max_width = max(max_width, standard_pwd_width)

            self.network_table.setColumnWidth(
                column,
                max_width + self.TABLE_COLUMN_PADDING,
            )

        self._update_table_group_width()

    def _update_table_group_width(self) -> None:
        """Update table group width based on column sizes."""
        width = 0
        for column in range(self.network_table.columnCount()):
            width += self.network_table.columnWidth(column)
        width += self.network_table.verticalHeader().width()
        width += self.network_table.frameWidth() * 2
        width += self.network_table.verticalScrollBar().sizeHint().width()
        layout = self.table_group.layout()
        if layout:
            margins = layout.contentsMargins()
            width += margins.left() + margins.right()
        width += self.TABLE_WIDTH_PADDING
        self.table_group.setMinimumWidth(width)
        self.table_group.setMaximumWidth(width)
        self.network_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _toggle_password_visibility(self, row: int) -> None:
        """Toggle visibility of a row's password widget."""
        password_item = self.network_table.item(row, 2)
        if not password_item:
            return
        password = password_item.data(Qt.ItemDataRole.UserRole) or ""
        widget = self.network_table.cellWidget(row, 2)
        if not widget:
            return
        label = widget.findChild(QLabel)
        if not label:
            return
        current = bool(label.property("isVisible"))
        self._update_password_widget(row, password, force_visible=not current)

    def _security_changed(self, row: int, value: str) -> None:
        """Update the security text for a row."""
        # Security value is stored in the combobox, no need to update item

    def _hidden_changed(self, row: int, state: int) -> None:
        """Update the hidden state for a row."""
        # Hidden value is stored in the checkbox, no need to update item

    def _table_context_menu(self, pos: QPoint) -> None:
        """Show context actions for table cells."""
        index = self.network_table.indexAt(pos)
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        menu = QMenu(self)
        if column == 1:
            edit_ssid = menu.addAction("Edit SSID")
            edit_ssid.triggered.connect(lambda *_: self._edit_ssid(row))
        if column == 2:
            edit_pwd = menu.addAction("Change Password")
            edit_pwd.triggered.connect(lambda *_: self._view_password(row))
        menu.exec(self.network_table.viewport().mapToGlobal(pos))

    def _edit_ssid(self, row: int) -> None:
        """Prompt for editing an SSID in the table."""
        ssid_item = self.network_table.item(row, 1)
        if not ssid_item:
            return
        current = ssid_item.text()
        value, ok = QInputDialog.getText(self, "SSID", "Edit SSID:", text=current)
        if ok and value.strip():
            ssid_item.setText(value.strip())

    def _apply_search_filter(self) -> None:
        """Filter table rows by the search query."""
        query = self.search_input.text().strip().lower()
        self._search_matches = []
        for row in range(self.network_table.rowCount()):
            location_item = self.network_table.item(row, 0)
            ssid_item = self.network_table.item(row, 1)
            location = location_item.text().lower() if location_item else ""
            ssid = ssid_item.text().lower() if ssid_item else ""
            match = query in location or query in ssid
            self.network_table.setRowHidden(row, not match if query else False)
            if query and match:
                self._search_matches.append(row)

        # Update placeholder text with match count
        if query and self._search_matches:
            count = len(self._search_matches)
            self.search_input.setPlaceholderText(
                f"Search by location or SSID ({count} match{'es' if count != 1 else ''})"
            )
        else:
            self.search_input.setPlaceholderText("Search by location or SSID")

        self._search_index = 0 if self._search_matches else self.NO_SEARCH_INDEX
        if self._search_matches:
            self._select_search_row(self._search_matches[0])

    def _select_search_row(self, row: int) -> None:
        """Select and scroll to a table row."""
        self.network_table.selectRow(row)
        item = self.network_table.item(row, 1)
        if item:
            self.network_table.scrollToItem(item)

    def _find_next(self) -> None:
        """Select the next search match."""
        if not self._search_matches:
            return
        self._search_index = (self._search_index + 1) % len(self._search_matches)
        self._select_search_row(self._search_matches[self._search_index])

    def _find_previous(self) -> None:
        """Select the previous search match."""
        if not self._search_matches:
            return
        self._search_index = (self._search_index - 1) % len(self._search_matches)
        self._select_search_row(self._search_matches[self._search_index])

    def _handle_column_resize(self, logical_index: int, old_size: int, new_size: int) -> None:
        """Prevent gaps by expanding Password column when needed."""
        if logical_index not in [0, 1, 2]:  # Only care about resizable columns
            return

        # Calculate available width for resizable columns
        table_width = self.network_table.viewport().width()
        security_width = self.network_table.columnWidth(3)
        hidden_width = self.network_table.columnWidth(4)
        available_width = table_width - security_width - hidden_width

        # Get current widths of resizable columns
        location_width = self.network_table.columnWidth(0)
        ssid_width = self.network_table.columnWidth(1)
        password_width = self.network_table.columnWidth(2)

        # Calculate total width of resizable columns
        total_resizable_width = location_width + ssid_width + password_width

        # If there would be a gap, expand Password column to fill it
        if total_resizable_width < available_width:
            gap = available_width - total_resizable_width
            header = self.network_table.horizontalHeader()
            header.sectionResized.disconnect(self._handle_column_resize)
            self.network_table.setColumnWidth(2, password_width + gap)
            header.sectionResized.connect(self._handle_column_resize)

    def _handle_sort(self, column: int) -> None:
        """Toggle sorting for the given column."""
        if column not in {0, 1}:
            return
        order = self._sort_orders.get(column, Qt.SortOrder.AscendingOrder)
        order = (
            Qt.SortOrder.DescendingOrder
            if order == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )
        self._sort_orders[column] = order
        self.network_table.sortItems(column, order)

    def _selected_rows(self) -> list[int]:
        """Return selected table row indices."""
        rows = {item.row() for item in self.network_table.selectedItems()}
        return sorted(rows)

    def _selected_or_all_configs(self) -> list[WifiConfig]:
        """Return configs for selected rows or all rows."""
        rows = self._selected_rows()
        if not rows:
            rows = list(range(self.network_table.rowCount()))
        configs = []
        for row in rows:
            config = self._row_to_config(row)
            if config:
                configs.append(config)
        return configs

    def _row_to_config(self, row: int) -> WifiConfig | None:
        """Convert a table row into a config if possible."""
        location_item = self.network_table.item(row, 0)
        ssid_item = self.network_table.item(row, 1)
        password_item = self.network_table.item(row, 2)
        security_combo = self.network_table.cellWidget(row, 3)
        if not location_item or not ssid_item or not password_item:
            return None
        security_value = None
        if isinstance(security_combo, QComboBox):
            security_value = security_combo.currentText()
        else:
            security_item = self.network_table.item(row, 3)
            security_value = (
                security_item.text().strip()
                if security_item
                else SECURITY_OPTIONS[0]
            )
        password = password_item.data(Qt.ItemDataRole.UserRole) or ""

        hidden_widget = self.network_table.cellWidget(row, 4)
        hidden_value = False
        if hidden_widget:
            hidden_checkbox = hidden_widget.findChild(QCheckBox)
            if hidden_checkbox:
                hidden_value = hidden_checkbox.isChecked()

        # Image data is stored in location item's UserRole
        image_data = location_item.data(Qt.ItemDataRole.UserRole)

        return WifiConfig(
            location=location_item.text().strip(),
            ssid=ssid_item.text().strip(),
            password=str(password),
            security=security_value or SECURITY_OPTIONS[0],
            hidden=hidden_value,
            image_data=image_data if isinstance(image_data, str) else None,
        )

    def _save(self) -> None:
        """Save to the last path or prompt for a new one."""
        if self._current_save_path:
            self._save_to_path(self._current_save_path)
        else:
            self._save_as()

    def _save_as(self) -> None:
        """Prompt for a save path and persist configs."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save",
            "wifi-networks.json",
            "JSON Files (*.json)",
        )
        if not path:
            return
        self._current_save_path = path
        self._save_to_path(path)

    def _save_to_path(self, path: str) -> None:
        """Write configs to a JSON path."""
        configs = self._selected_or_all_configs()
        if not configs and self._config.ssid:
            configs = [self._config]

        data = [
            {
                "location": c.location,
                "ssid": c.ssid,
                "password": c.password,
                "security": c.security,
                "hidden": c.hidden,
                "image_data": c.image_data,
            }
            for c in configs
        ]
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def _load(self) -> None:
        """Prompt for a JSON file and load configs."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load",
            "",
            "JSON Files (*.json)",
        )
        if not path:
            return
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        self._load_from_data(data)
        self._current_save_path = path

    def _load_from_data(self, data: list[dict[str, object]]) -> None:
        """Populate table and form from loaded data."""
        self.network_table.setRowCount(0)
        configs = []
        for entry in data:
            config = WifiConfig(
                location=str(entry.get("location", "")),
                ssid=str(entry.get("ssid", "")),
                password=str(entry.get("password", "")),
                security=str(entry.get("security", SECURITY_OPTIONS[0])),
                hidden=bool(entry.get("hidden", False)),
                image_data=(
                    str(img_data)
                    if (img_data := entry.get("image_data")) and isinstance(img_data, str)
                    else None
                ),
            )
            configs.append(config)
            self._add_or_update_row(config)
        if len(configs) == 1:
            self._set_form_from_config(configs[0])

    def _set_form_from_config(self, config: WifiConfig) -> None:
        """Set the form inputs based on a config."""
        self.location_input.setText(config.location)
        self.ssid_input.setText(config.ssid)
        self.password_input.setText(config.password)
        self.security_input.setCurrentText(config.security)
        self.hidden_input.setChecked(config.hidden)
        if config.image_data:
            self.image_path_display.setText("(Image loaded from saved network)")
        else:
            self.image_path_display.clear()
        self._config = config
        self._refresh_preview()

    def _table_double_clicked(self, index: QModelIndex) -> None:
        """Load the double-clicked network into the form and preview."""
        row = index.row()
        config = self._row_to_config(row)
        if config:
            self._set_form_from_config(config)

    def _show_about(self) -> None:
        """Display the About dialog."""
        try:
            version = metadata.version("wifiqr")
        except metadata.PackageNotFoundError:
            version = "dev"

        QMessageBox.information(
            self,
            "About WifiQR",
            (
                "WifiQR\n"
                "Cross-platform Wi-Fi QR code generator\n"
                f"Version: {version}\n"
                "Built with PySide6, qrcode, Pillow, CairoSVG\n"
                "Author: Randy Northrup"
            ),
        )

    @Slot()
    def _focus_search(self) -> None:
        """Focus the search input field."""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _sanitize_filename(self, value: str) -> str:
        """Return a filesystem-safe filename from a label."""
        return "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in value) or "wifi"
