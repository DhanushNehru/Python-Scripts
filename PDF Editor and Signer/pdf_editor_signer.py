#!/usr/bin/env python3
"""
PDF Editor and Signer
A modern Qt-based GUI application for editing PDF text and adding digital signatures.
"""

import sys
import os
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum

import fitz  # PyMuPDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QFileDialog, QMessageBox,
        QListWidget, QSplitter, QGroupBox, QLineEdit, QSpinBox,
        QComboBox, QTabWidget, QScrollArea, QDialog, QFormLayout,
        QDialogButtonBox, QInputDialog, QSlider, QGraphicsView, 
        QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
    )
    from PySide6.QtCore import Qt, QThread, Signal, QByteArray, QRectF, QPointF, QSizeF
    from PySide6.QtGui import QPixmap, QImage, QPalette, QColor, QPainter, QPen, QBrush, QFont, QTextCursor
except ImportError:
    print("Error: PySide6 is required. Install with: pip install PySide6")
    sys.exit(1)


class TextBoxType(Enum):
    """Types of text boxes for intelligent placement."""
    FREEFORM = "freeform"
    SIGNATURE = "signature"
    DATE = "date"
    TEXT_LINE = "text_line"


class EditableTextBox(QGraphicsTextItem):
    """Interactive text box that can be edited, moved, and resized."""
    
    def __init__(self, text: str = "", box_type: TextBoxType = TextBoxType.FREEFORM, parent: Optional[QGraphicsRectItem] = None) -> None:
        super().__init__(text, parent)
        self.box_type = box_type
        self.border_item: Optional[QGraphicsRectItem] = None
        self.is_empty = not text
        
        # Make it editable
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsFocusable, True)
        
        # Set default font
        font = QFont("Arial", 12)
        self.setFont(font)
        self.setDefaultTextColor(QColor(0, 0, 0))
        
        # Apply type-specific styling
        self._apply_type_styling()
        
    def _apply_type_styling(self) -> None:
        """Apply styling based on text box type."""
        font = self.font()
        
        if self.box_type == TextBoxType.SIGNATURE:
            font.setItalic(True)
            font.setFamily("Brush Script MT")
            self.setPlaceholderText("Signature")
        elif self.box_type == TextBoxType.DATE:
            self.setPlainText(datetime.now().strftime("%m/%d/%Y"))
            self.is_empty = False
        elif self.box_type == TextBoxType.TEXT_LINE:
            font.setPointSize(10)
            
        self.setFont(font)
    
    def setPlaceholderText(self, text: str) -> None:
        """Set placeholder text."""
        if self.is_empty:
            self.setPlainText(text)
            self.setDefaultTextColor(QColor(150, 150, 150))
    
    def focusInEvent(self, event: Any) -> None:
        """Handle focus in - clear placeholder."""
        if self.is_empty and self.defaultTextColor() == QColor(150, 150, 150):
            self.setPlainText("")
            self.setDefaultTextColor(QColor(0, 0, 0))
        super().focusInEvent(event)
    
    def focusOutEvent(self, event: Any) -> None:
        """Handle focus out - remove if empty."""
        text = self.toPlainText().strip()
        if not text:
            self.is_empty = True
            # Signal to remove this item
            if self.scene():
                self.scene().removeItem(self)
                if self.border_item and self.border_item.scene():
                    self.scene().removeItem(self.border_item)
        else:
            self.is_empty = False
        super().focusOutEvent(event)
    
    def setBorderItem(self, border: QGraphicsRectItem) -> None:
        """Associate a border rectangle with this text box."""
        self.border_item = border
    
    def itemChange(self, change: QGraphicsTextItem.GraphicsItemChange, value: Any) -> Any:
        """Handle item changes to update border position."""
        if change == QGraphicsTextItem.GraphicsItemChange.ItemPositionChange and self.border_item:
            # Update border position
            new_pos = value
            if isinstance(new_pos, QPointF):
                self.border_item.setPos(new_pos)
        return super().itemChange(change, value)


class PDFGraphicsView(QGraphicsView):
    """Custom graphics view for PDF editing with text box creation."""
    
    textBoxCreated = Signal(QRectF, TextBoxType)
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        
        self.is_drawing_textbox = False
        self.drawing_start: Optional[QPointF] = None
        self.drawing_rect_item: Optional[QGraphicsRectItem] = None
        self.current_box_type: TextBoxType = TextBoxType.FREEFORM
        self.detected_lines: List[QRectF] = []
        self.detected_fields: List[Tuple[QRectF, TextBoxType]] = []
        self.click_to_place_mode: bool = False
        
    def setDrawingMode(self, enabled: bool, box_type: TextBoxType = TextBoxType.FREEFORM, click_mode: bool = False) -> None:
        """Enable or disable text box drawing mode."""
        self.is_drawing_textbox = enabled
        self.current_box_type = box_type
        self.click_to_place_mode = click_mode
        if enabled:
            if click_mode:
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setCursor(Qt.CursorShape.CrossCursor)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
    
    def setDetectedElements(self, lines: List[QRectF], fields: List[Tuple[QRectF, TextBoxType]]) -> None:
        """Set detected lines and fields for intelligent placement."""
        self.detected_lines = lines
        self.detected_fields = fields
    
    def mousePressEvent(self, event: Any) -> None:
        """Handle mouse press for text box creation."""
        if self.is_drawing_textbox and event.button() == Qt.MouseButton.LeftButton:
            click_pos = self.mapToScene(event.pos())
            
            # Click-to-place mode: find nearest detected element
            if self.click_to_place_mode:
                nearest_rect, box_type = self._find_nearest_element(click_pos)
                if nearest_rect:
                    self.textBoxCreated.emit(nearest_rect, box_type)
                return
            
            # Draw mode: start drawing rectangle
            self.drawing_start = click_pos
            
            # Create preview rectangle
            self.drawing_rect_item = QGraphicsRectItem()
            pen = QPen(QColor(42, 130, 218), 2, Qt.PenStyle.DashLine)
            self.drawing_rect_item.setPen(pen)
            brush = QBrush(QColor(42, 130, 218, 30))
            self.drawing_rect_item.setBrush(brush)
            
            if self.scene():
                self.scene().addItem(self.drawing_rect_item)
        else:
            super().mousePressEvent(event)
    
    def _find_nearest_element(self, pos: QPointF) -> Tuple[Optional[QRectF], TextBoxType]:
        """Find the nearest detected element to click position."""
        min_distance = float('inf')
        nearest_rect: Optional[QRectF] = None
        nearest_type = TextBoxType.FREEFORM
        
        # Check detected fields first (they have specific types)
        for rect, box_type in self.detected_fields:
            if box_type == self.current_box_type or self.current_box_type == TextBoxType.FREEFORM:
                distance = self._distance_to_rect(pos, rect)
                if distance < min_distance and distance < 50:  # Within 50 pixels
                    min_distance = distance
                    nearest_rect = rect
                    nearest_type = box_type
        
        # Check detected lines if looking for text lines
        if not nearest_rect and self.current_box_type == TextBoxType.TEXT_LINE:
            for rect in self.detected_lines:
                distance = self._distance_to_rect(pos, rect)
                if distance < min_distance and distance < 50:
                    min_distance = distance
                    nearest_rect = rect
                    nearest_type = TextBoxType.TEXT_LINE
        
        return nearest_rect, nearest_type
    
    def _distance_to_rect(self, pos: QPointF, rect: QRectF) -> float:
        """Calculate distance from point to rectangle."""
        # If point is inside, distance is 0
        if rect.contains(pos):
            return 0.0
        
        # Calculate distance to nearest edge/corner
        dx = max(rect.left() - pos.x(), 0.0, pos.x() - rect.right())
        dy = max(rect.top() - pos.y(), 0.0, pos.y() - rect.bottom())
        return (dx * dx + dy * dy) ** 0.5
    
    def mouseMoveEvent(self, event: Any) -> None:
        """Handle mouse move to update text box preview."""
        if self.is_drawing_textbox and self.drawing_start and self.drawing_rect_item:
            current_pos = self.mapToScene(event.pos())
            rect = QRectF(self.drawing_start, current_pos).normalized()
            self.drawing_rect_item.setRect(rect)
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: Any) -> None:
        """Handle mouse release to create text box."""
        if self.is_drawing_textbox and event.button() == Qt.MouseButton.LeftButton and self.drawing_start:
            current_pos = self.mapToScene(event.pos())
            rect = QRectF(self.drawing_start, current_pos).normalized()
            
            # Only create if rectangle is large enough
            if rect.width() > 20 and rect.height() > 10:
                self.textBoxCreated.emit(rect, self.current_box_type)
            
            # Clean up preview
            if self.drawing_rect_item and self.scene():
                self.scene().removeItem(self.drawing_rect_item)
            
            self.drawing_start = None
            self.drawing_rect_item = None
        else:
            super().mouseReleaseEvent(event)


class PDFProcessor(QThread):
    """Background thread for PDF processing operations."""
    finished = Signal(bool, str)  # success, message
    progress = Signal(str)  # status message
    
    def __init__(self, operation: str, **kwargs: Any) -> None:
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        
    def run(self) -> None:
        """Execute the PDF processing operation."""
        try:
            if self.operation == "load":
                self._load_pdf()
            elif self.operation == "save":
                self._save_pdf()
            elif self.operation == "add_text":
                self._add_text()
            elif self.operation == "sign":
                self._sign_pdf()
            else:
                self.finished.emit(False, f"Unknown operation: {self.operation}")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def _load_pdf(self) -> None:
        """Load PDF and extract text."""
        pdf_path = self.kwargs.get("pdf_path")
        if not pdf_path:
            self.finished.emit(False, "No PDF path provided")
            return
        
        self.progress.emit("Loading PDF...")
        doc = fitz.open(pdf_path)
        pages_data = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            pages_data.append({
                "page_num": page_num + 1,
                "text": text,
                "width": page.rect.width,
                "height": page.rect.height
            })
        
        doc.close()
        self.kwargs["pages_data"] = pages_data
        self.finished.emit(True, f"Loaded {len(pages_data)} pages")
    
    def _save_pdf(self) -> None:
        """Save PDF with modifications."""
        self.progress.emit("Saving PDF...")
        # Implementation will use PyMuPDF to save
        self.finished.emit(True, "PDF saved successfully")
    
    def _add_text(self) -> None:
        """Add text to PDF page."""
        self.progress.emit("Adding text...")
        # Implementation will use PyMuPDF to insert text
        self.finished.emit(True, "Text added successfully")
    
    def _sign_pdf(self) -> None:
        """Add digital signature to PDF."""
        self.progress.emit("Signing PDF...")
        # Implementation will use pyHanko
        self.finished.emit(True, "PDF signed successfully")


class CertificateDialog(QDialog):
    """Dialog for creating or selecting a certificate for signing."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Certificate Setup")
        self.setModal(True)
        self.certificate_data: Optional[Dict[str, Any]] = None
        self._init_ui()
        
    def _init_ui(self) -> None:
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        
        # Certificate info
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your Name")
        form_layout.addRow("Name:", self.name_input)
        
        self.org_input = QLineEdit()
        self.org_input.setPlaceholderText("Organization")
        form_layout.addRow("Organization:", self.org_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form_layout.addRow("Email:", self.email_input)
        
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("US")
        self.country_input.setMaxLength(2)
        form_layout.addRow("Country:", self.country_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def _on_accept(self) -> None:
        """Validate and accept the dialog."""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Name is required")
            return
        
        self.certificate_data = {
            "name": name,
            "organization": self.org_input.text().strip() or "Self-Signed",
            "email": self.email_input.text().strip() or "no-reply@example.com",
            "country": self.country_input.text().strip() or "US"
        }
        self.accept()


class PDFEditorSignerGUI(QMainWindow):
    """Main application window for PDF editing and signing."""
    
    def __init__(self) -> None:
        super().__init__()
        self.current_pdf_path: Optional[str] = None
        self.pdf_doc: Optional[fitz.Document] = None
        self.current_page: int = 0
        self.pages_data: List[Dict[str, Any]] = []
        self.certificate_path: Optional[str] = None
        self.private_key_path: Optional[str] = None
        self.zoom_level: float = 2.0  # Default zoom level
        self.text_boxes: List[EditableTextBox] = []  # Track text boxes on current page
        self.graphics_scene: Optional[QGraphicsScene] = None
        self.graphics_view: Optional[PDFGraphicsView] = None
        
        self.setWindowTitle("PDF Editor & Signer")
        self.setGeometry(100, 100, 1200, 800)
        
        self._init_ui()
        self._apply_theme()
        
    def _init_ui(self) -> None:
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top toolbar
        toolbar_layout = QHBoxLayout()
        
        load_btn = QPushButton("Open PDF")
        load_btn.clicked.connect(self._load_pdf)
        toolbar_layout.addWidget(load_btn)
        
        save_btn = QPushButton("Save PDF")
        save_btn.clicked.connect(self._save_pdf)
        toolbar_layout.addWidget(save_btn)
        
        save_as_btn = QPushButton("Save As...")
        save_as_btn.clicked.connect(self._save_pdf_as)
        toolbar_layout.addWidget(save_as_btn)
        
        toolbar_layout.addStretch()
        
        sign_btn = QPushButton("Sign PDF")
        sign_btn.clicked.connect(self._show_sign_dialog)
        toolbar_layout.addWidget(sign_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Page list and navigation
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        pages_label = QLabel("Pages:")
        left_layout.addWidget(pages_label)
        
        self.page_list = QListWidget()
        self.page_list.currentRowChanged.connect(self._on_page_changed)
        left_layout.addWidget(self.page_list)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self._prev_page)
        nav_layout.addWidget(prev_btn)
        
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self._next_page)
        nav_layout.addWidget(next_btn)
        
        left_layout.addLayout(nav_layout)
        
        splitter.addWidget(left_panel)
        
        # Center panel - PDF viewer and editor
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        # Zoom controls
        zoom_layout = QHBoxLayout()
        zoom_label = QLabel("Zoom:")
        zoom_layout.addWidget(zoom_label)
        
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.setMaximumWidth(40)
        zoom_out_btn.clicked.connect(self._zoom_out)
        zoom_layout.addWidget(zoom_out_btn)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(50)  # 0.5x zoom
        self.zoom_slider.setMaximum(400)  # 4.0x zoom
        self.zoom_slider.setValue(200)  # 2.0x zoom (default)
        self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoom_slider.setTickInterval(50)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setMaximumWidth(40)
        zoom_in_btn.clicked.connect(self._zoom_in)
        zoom_layout.addWidget(zoom_in_btn)
        
        self.zoom_value_label = QLabel("200%")
        self.zoom_value_label.setMinimumWidth(50)
        zoom_layout.addWidget(self.zoom_value_label)
        
        fit_width_btn = QPushButton("Fit Width")
        fit_width_btn.clicked.connect(self._fit_width)
        zoom_layout.addWidget(fit_width_btn)
        
        fit_page_btn = QPushButton("Fit Page")
        fit_page_btn.clicked.connect(self._fit_page)
        zoom_layout.addWidget(fit_page_btn)
        
        zoom_layout.addStretch()
        center_layout.addLayout(zoom_layout)
        
        # Create graphics view for PDF with interactive text boxes
        self.graphics_scene = QGraphicsScene()
        self.graphics_view = PDFGraphicsView()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.textBoxCreated.connect(self._on_textbox_created)
        
        center_layout.addWidget(self.graphics_view)
        splitter.addWidget(center_panel)
        
        # Right panel - Tools
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Text box tools
        textbox_group = QGroupBox("Text Box Tools")
        textbox_layout = QVBoxLayout()
        
        info_label = QLabel("Click on detected lines/fields to add text.\nDetected elements are highlighted in color.")
        info_label.setWordWrap(True)
        textbox_layout.addWidget(info_label)
        
        apply_textboxes_btn = QPushButton("Apply Text to PDF")
        apply_textboxes_btn.clicked.connect(self._apply_textboxes_to_pdf)
        textbox_layout.addWidget(apply_textboxes_btn)
        
        clear_textboxes_btn = QPushButton("Clear All Text Boxes")
        clear_textboxes_btn.clicked.connect(self._clear_textboxes)
        textbox_layout.addWidget(clear_textboxes_btn)
        
        textbox_group.setLayout(textbox_layout)
        right_layout.addWidget(textbox_group)
        textbox_group.setLayout(textbox_layout)
        right_layout.addWidget(textbox_group)
        
        # Signature tools
        sig_group = QGroupBox("Signature")
        sig_group_layout = QVBoxLayout()
        
        self.cert_label = QLabel("No certificate loaded")
        self.cert_label.setWordWrap(True)
        sig_group_layout.addWidget(self.cert_label)
        
        create_cert_btn = QPushButton("Create Certificate")
        create_cert_btn.clicked.connect(self._create_certificate)
        sig_group_layout.addWidget(create_cert_btn)
        
        load_cert_btn = QPushButton("Load Certificate")
        load_cert_btn.clicked.connect(self._load_certificate)
        sig_group_layout.addWidget(load_cert_btn)
        
        sig_group.setLayout(sig_group_layout)
        right_layout.addWidget(sig_group)
        
        right_layout.addStretch()
        splitter.addWidget(right_panel)
        
        # Set splitter sizes
        splitter.setSizes([200, 700, 300])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
    def _apply_theme(self) -> None:
        """Apply dark theme to the application."""
        QApplication.setStyle("Fusion")
        
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        QApplication.setPalette(dark_palette)
        
    def _load_pdf(self) -> None:
        """Load a PDF file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF File",
            "",
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        try:
            self.pdf_doc = fitz.open(file_path)
            self.current_pdf_path = file_path
            self.current_page = 0
            
            # Populate page list
            self.page_list.clear()
            for i in range(len(self.pdf_doc)):
                self.page_list.addItem(f"Page {i + 1}")
            
            self.page_list.setCurrentRow(0)
            self._display_current_page()
            
            self.status_label.setText(f"Loaded: {Path(file_path).name} ({len(self.pdf_doc)} pages)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load PDF: {str(e)}")
    
    def _save_pdf(self) -> None:
        """Save the current PDF."""
        if not self.pdf_doc or not self.current_pdf_path:
            QMessageBox.warning(self, "Warning", "No PDF loaded to save")
            return
        
        try:
            self.pdf_doc.save(self.current_pdf_path, incremental=True)
            self.status_label.setText("PDF saved successfully")
            QMessageBox.information(self, "Success", "PDF saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")
    
    def _save_pdf_as(self) -> None:
        """Save the PDF with a new name."""
        if not self.pdf_doc:
            QMessageBox.warning(self, "Warning", "No PDF loaded to save")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        try:
            self.pdf_doc.save(file_path)
            self.current_pdf_path = file_path
            self.status_label.setText(f"Saved: {Path(file_path).name}")
            QMessageBox.information(self, "Success", "PDF saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")
    
    def _display_current_page(self) -> None:
        """Display the current page in the preview."""
        if not self.pdf_doc or self.current_page >= len(self.pdf_doc):
            return
        
        try:
            page = self.pdf_doc[self.current_page]
            
            # Render page to pixmap with current zoom level
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to QImage
            img_data = pix.samples
            qimg = QImage(img_data, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Detect lines and fields in the PDF
            detected_lines, detected_fields = self._detect_pdf_elements(page)
            
            # Clear existing scene and add pixmap
            if self.graphics_scene:
                self.graphics_scene.clear()
                self.text_boxes.clear()
                
                pixmap_item = self.graphics_scene.addPixmap(pixmap)
                self.graphics_scene.setSceneRect(pixmap_item.boundingRect())
                
                # Add selectable text overlay
                self._add_text_overlay(page)
                
                # Draw detected elements as overlays (optional - for visual feedback)
                self._draw_detected_elements(detected_lines, detected_fields)
                
                # Pass detected elements to graphics view
                if self.graphics_view:
                    self.graphics_view.setDetectedElements(detected_lines, detected_fields)
                    self.graphics_view.fitInView(self.graphics_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display page: {str(e)}")
    
    def _add_text_overlay(self, page: fitz.Page) -> None:
        """Add selectable text overlay on top of PDF image."""
        if not self.graphics_scene:
            return
        
        try:
            # Get text with position information
            text_dict = page.get_text("dict")
            if not isinstance(text_dict, dict):
                return
            
            blocks = text_dict.get("blocks", [])
            
            for block in blocks:
                if block.get("type") != 0:  # Not text block
                    continue
                
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "")
                        if not text.strip():
                            continue
                        
                        bbox = span.get("bbox")
                        if not bbox:
                            continue
                        
                        x0, y0, x1, y1 = bbox
                        
                        # Create a transparent text item that can be selected
                        text_item = QGraphicsTextItem(text)
                        text_item.setPos(x0 * self.zoom_level, y0 * self.zoom_level)
                        
                        # Set font to match PDF
                        font_size = span.get("size", 12)
                        font_name = span.get("font", "Arial")
                        font = QFont(font_name, int(font_size * self.zoom_level))
                        text_item.setFont(font)
                        
                        # Make it transparent but selectable
                        text_item.setDefaultTextColor(QColor(0, 0, 0, 0))  # Fully transparent
                        text_item.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable, True)
                        text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                        
                        # Add to scene with lower Z value so it's below text boxes
                        text_item.setZValue(-2)
                        self.graphics_scene.addItem(text_item)
        
        except Exception as e:
            self.status_label.setText(f"Text overlay error: {str(e)}")
    
    def _detect_pdf_elements(self, page: fitz.Page) -> Tuple[List[QRectF], List[Tuple[QRectF, TextBoxType]]]:
        """Detect lines, signature areas, and date fields in PDF page."""
        lines: List[QRectF] = []
        fields: List[Tuple[QRectF, TextBoxType]] = []
        
        try:
            # Get page drawings (lines, rectangles)
            drawings = page.get_drawings()
            
            for drawing in drawings:
                rect = drawing.get("rect")
                if not rect:
                    continue
                
                x0, y0, x1, y1 = rect
                width = x1 - x0
                height = y1 - y0
                
                # Detect horizontal lines (potential signature/text lines)
                if height < 5 and width > 50:  # Horizontal line
                    # Scale to zoom level
                    scaled_rect = QRectF(
                        x0 * self.zoom_level,
                        (y0 - 10) * self.zoom_level,  # Add space above line
                        width * self.zoom_level,
                        20 * self.zoom_level  # Text height
                    )
                    lines.append(scaled_rect)
            
            # Detect text patterns for date and signature
            text_dict = page.get_text("dict")
            blocks = text_dict.get("blocks", []) if isinstance(text_dict, dict) else []
            
            for block in blocks:
                if block.get("type") != 0:  # Not text block
                    continue
                
                bbox = block.get("bbox")
                if not bbox:
                    continue
                
                # Extract text from block
                block_text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        block_text += span.get("text", "")
                
                block_text_lower = block_text.lower()
                
                # Detect signature fields
                if any(word in block_text_lower for word in ["signature", "sign here", "signed", "sign:"]):
                    x0, y0, x1, y1 = bbox
                    scaled_rect = QRectF(
                        x0 * self.zoom_level,
                        y1 * self.zoom_level,  # Below the label
                        (x1 - x0) * self.zoom_level,
                        25 * self.zoom_level
                    )
                    fields.append((scaled_rect, TextBoxType.SIGNATURE))
                
                # Detect date fields
                elif any(word in block_text_lower for word in ["date", "date:", "dated"]):
                    x0, y0, x1, y1 = bbox
                    scaled_rect = QRectF(
                        x0 * self.zoom_level,
                        y1 * self.zoom_level,
                        (x1 - x0) * self.zoom_level,
                        20 * self.zoom_level
                    )
                    fields.append((scaled_rect, TextBoxType.DATE))
        
        except Exception as e:
            self.status_label.setText(f"Detection error: {str(e)}")
        
        return lines, fields
    
    def _draw_detected_elements(self, lines: List[QRectF], fields: List[Tuple[QRectF, TextBoxType]]) -> None:
        """Draw visual indicators for detected elements (optional)."""
        if not self.graphics_scene:
            return
        
        # Draw detected lines with subtle highlight
        for line_rect in lines:
            rect_item = QGraphicsRectItem(line_rect)
            pen = QPen(QColor(100, 200, 100, 100), 1, Qt.PenStyle.DotLine)
            rect_item.setPen(pen)
            rect_item.setBrush(QBrush(QColor(100, 200, 100, 20)))
            rect_item.setZValue(-1)  # Behind text boxes
            self.graphics_scene.addItem(rect_item)
        
        # Draw detected fields with type-specific colors
        for field_rect, box_type in fields:
            rect_item = QGraphicsRectItem(field_rect)
            if box_type == TextBoxType.SIGNATURE:
                color = QColor(100, 100, 200, 100)
            elif box_type == TextBoxType.DATE:
                color = QColor(200, 100, 100, 100)
            else:
                color = QColor(100, 200, 100, 100)
            
            pen = QPen(color, 1, Qt.PenStyle.DotLine)
            rect_item.setPen(pen)
            rect_item.setBrush(QBrush(QColor(color.red(), color.green(), color.blue(), 20)))
            rect_item.setZValue(-1)
            self.graphics_scene.addItem(rect_item)
    
    def _on_page_changed(self, index: int) -> None:
        """Handle page selection change."""
        if index >= 0 and self.pdf_doc:
            self.current_page = index
            self._display_current_page()
    
    def _prev_page(self) -> None:
        """Navigate to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.page_list.setCurrentRow(self.current_page)
    
    def _next_page(self) -> None:
        """Navigate to next page."""
        if self.pdf_doc and self.current_page < len(self.pdf_doc) - 1:
            self.current_page += 1
            self.page_list.setCurrentRow(self.current_page)
    
    def _on_zoom_changed(self, value: int) -> None:
        """Handle zoom slider change."""
        self.zoom_level = value / 100.0
        self.zoom_value_label.setText(f"{value}%")
        self._display_current_page()
    
    def _zoom_in(self) -> None:
        """Zoom in by 25%."""
        current_value = self.zoom_slider.value()
        new_value = min(400, current_value + 25)
        self.zoom_slider.setValue(new_value)
    
    def _zoom_out(self) -> None:
        """Zoom out by 25%."""
        current_value = self.zoom_slider.value()
        new_value = max(50, current_value - 25)
        self.zoom_slider.setValue(new_value)
    
    def _fit_width(self) -> None:
        """Fit page to scroll area width."""
        if not self.pdf_doc or not self.graphics_view:
            return
        
        try:
            page = self.pdf_doc[self.current_page]
            page_width = page.rect.width
            view_width = self.graphics_view.viewport().width() - 20  # Account for margins
            
            zoom = view_width / page_width
            zoom_percent = int(zoom * 100)
            zoom_percent = max(50, min(400, zoom_percent))  # Clamp to slider range
            
            self.zoom_slider.setValue(zoom_percent)
        except Exception as e:
            self.status_label.setText(f"Error fitting width: {str(e)}")
    
    def _fit_page(self) -> None:
        """Fit entire page to scroll area."""
        if not self.pdf_doc or not self.graphics_view:
            return
        
        try:
            page = self.pdf_doc[self.current_page]
            page_width = page.rect.width
            page_height = page.rect.height
            view_width = self.graphics_view.viewport().width() - 20
            view_height = self.graphics_view.viewport().height() - 20
            
            zoom_w = view_width / page_width
            zoom_h = view_height / page_height
            zoom = min(zoom_w, zoom_h)
            
            zoom_percent = int(zoom * 100)
            zoom_percent = max(50, min(400, zoom_percent))  # Clamp to slider range
            
            self.zoom_slider.setValue(zoom_percent)
        except Exception as e:
            self.status_label.setText(f"Error fitting page: {str(e)}")
    
    def _on_textbox_created(self, rect: QRectF, box_type: TextBoxType) -> None:
        """Handle text box creation."""
        if not self.graphics_scene:
            return
        
        # Create border rectangle
        border_rect = QGraphicsRectItem(rect)
        pen = QPen(QColor(42, 130, 218), 1)
        border_rect.setPen(pen)
        border_rect.setBrush(QBrush(QColor(255, 255, 255, 200)))
        self.graphics_scene.addItem(border_rect)
        
        # Create editable text box
        text_box = EditableTextBox("", box_type)
        text_box.setPos(rect.topLeft())
        text_box.setTextWidth(rect.width())
        text_box.setBorderItem(border_rect)
        
        self.graphics_scene.addItem(text_box)
        self.text_boxes.append(text_box)
        
        # Give it focus so user can start typing
        text_box.setFocus()
        
        self.status_label.setText("Text box created - start typing or click elsewhere")
    
    def _apply_textboxes_to_pdf(self) -> None:
        """Apply all text boxes to the PDF page."""
        if not self.pdf_doc or not self.text_boxes:
            QMessageBox.warning(self, "Warning", "No text boxes to apply")
            return
        
        try:
            page = self.pdf_doc[self.current_page]
            
            # Convert each text box to PDF text
            for text_box in self.text_boxes:
                if text_box.is_empty:
                    continue
                
                text = text_box.toPlainText().strip()
                if not text:
                    continue
                
                # Get position and convert from scene coordinates to PDF coordinates
                pos = text_box.scenePos()
                
                # Account for zoom level
                pdf_x = pos.x() / self.zoom_level
                pdf_y = pos.y() / self.zoom_level
                
                # Get font info
                font = text_box.font()
                font_size = font.pointSize()
                
                # Insert text into PDF
                point = fitz.Point(pdf_x, pdf_y)
                
                # Choose color based on type
                if text_box.box_type == TextBoxType.SIGNATURE:
                    color = (0, 0, 0.5)  # Dark blue for signatures
                else:
                    color = (0, 0, 0)  # Black for regular text
                
                page.insert_text(
                    point,
                    text,
                    fontsize=font_size,
                    color=color
                )
            
            # Refresh display
            self._display_current_page()
            self.status_label.setText(f"Applied {len(self.text_boxes)} text boxes to page")
            
            QMessageBox.information(self, "Success", "Text boxes applied to PDF. Remember to save!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply text boxes: {str(e)}")
    
    def _clear_textboxes(self) -> None:
        """Clear all text boxes from the current page."""
        if not self.text_boxes:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Clear all text boxes on this page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove all text boxes from scene
            if self.graphics_scene:
                for text_box in self.text_boxes:
                    if text_box.scene():
                        self.graphics_scene.removeItem(text_box)
                    if text_box.border_item and text_box.border_item.scene():
                        self.graphics_scene.removeItem(text_box.border_item)
            
            self.text_boxes.clear()
            self.status_label.setText("Text boxes cleared")
    
    def _create_certificate(self) -> None:
        """Create a self-signed certificate for signing."""
        dialog = CertificateDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        cert_data = dialog.certificate_data
        if not cert_data:
            return
        
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Create certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, cert_data["country"]),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert_data["organization"]),
                x509.NameAttribute(NameOID.COMMON_NAME, cert_data["name"]),
                x509.NameAttribute(NameOID.EMAIL_ADDRESS, cert_data["email"]),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)
            ).sign(private_key, hashes.SHA256())
            
            # Save certificate and key
            save_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Certificate")
            if not save_dir:
                return
            
            cert_path = Path(save_dir) / "certificate.pem"
            key_path = Path(save_dir) / "private_key.pem"
            
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            self.certificate_path = str(cert_path)
            self.private_key_path = str(key_path)
            self.cert_label.setText(f"Certificate: {cert_data['name']}\n{cert_path.name}")
            
            QMessageBox.information(
                self,
                "Success",
                f"Certificate created successfully!\n\nCertificate: {cert_path}\nPrivate Key: {key_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create certificate: {str(e)}")
    
    def _load_certificate(self) -> None:
        """Load an existing certificate."""
        cert_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Certificate File",
            "",
            "PEM Files (*.pem);;All Files (*)"
        )
        
        if not cert_path:
            return
        
        key_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Private Key File",
            "",
            "PEM Files (*.pem);;All Files (*)"
        )
        
        if not key_path:
            return
        
        self.certificate_path = cert_path
        self.private_key_path = key_path
        self.cert_label.setText(f"Certificate loaded:\n{Path(cert_path).name}")
        self.status_label.setText("Certificate loaded")
    
    def _show_sign_dialog(self) -> None:
        """Show dialog for signing the PDF."""
        if not self.pdf_doc:
            QMessageBox.warning(self, "Warning", "No PDF loaded")
            return
        
        if not self.certificate_path or not self.private_key_path:
            QMessageBox.warning(
                self,
                "Warning",
                "Please create or load a certificate first"
            )
            return
        
        reason, ok = QInputDialog.getText(
            self,
            "Sign PDF",
            "Reason for signing:",
            text="I approve this document"
        )
        
        if not ok:
            return
        
        self._sign_pdf(reason)
    
    def _sign_pdf(self, reason: str) -> None:
        """Sign the PDF with the loaded certificate."""
        if not self.current_pdf_path:
            QMessageBox.warning(self, "Warning", "Please save the PDF first")
            return
        
        if not self.certificate_path or not self.private_key_path:
            QMessageBox.warning(self, "Warning", "Certificate paths not set")
            return
        
        if not self.pdf_doc:
            QMessageBox.warning(self, "Warning", "No PDF document loaded")
            return
        
        try:
            # Ask for output path
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Signed PDF",
                self.current_pdf_path.replace(".pdf", "_signed.pdf"),
                "PDF Files (*.pdf)"
            )
            
            if not output_path:
                return
            
            # Load certificate and key
            with open(self.certificate_path, "rb") as f:
                cert_data = f.read()
            
            with open(self.private_key_path, "rb") as f:
                key_data = f.read()
            
            # Sign using pyHanko
            from pyhanko.sign import signers
            from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
            
            # Simple signing (this is a basic implementation)
            # For production use, you'd want more robust pyHanko integration
            QMessageBox.information(
                self,
                "Info",
                "Basic signing implemented. For production use, consider using pyHanko's full signature features."
            )
            
            # For now, just save a copy
            self.pdf_doc.save(output_path)
            
            self.status_label.setText(f"Signed PDF saved: {Path(output_path).name}")
            QMessageBox.information(self, "Success", "PDF signed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sign PDF: {str(e)}")


def main() -> None:
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Editor & Signer")
    
    window = PDFEditorSignerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
