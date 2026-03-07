import sys
import cv2
import numpy as np
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QSlider, QTabWidget, QGroupBox,
    QRadioButton, QButtonGroup, QSpinBox, QColorDialog, QComboBox,
    QMessageBox, QSplitter, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QImage, QPixmap, QPalette, QColor
from cv2.typing import MatLike
import numpy.typing as npt


class ImageProcessor(QThread):
    """Background thread for image processing operations."""
    finished = Signal(object)  # Returns processed image
    error = Signal(str)
    
    def __init__(self, image: MatLike, operation: str, params: Dict[str, Any]) -> None:
        super().__init__()
        self.image = image
        self.operation = operation
        self.params = params
    
    def run(self) -> None:
        try:
            result: Optional[MatLike] = None
            if self.operation == "remove_bg":
                result = self.remove_background()
            elif self.operation == "replace_bg":
                result = self.replace_background()
            elif self.operation == "remove_fg":
                result = self.remove_foreground()
            elif self.operation == "replace_fg":
                result = self.replace_foreground()
            else:
                result = self.image
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
    
    def remove_background(self) -> MatLike:
        """Remove background from image."""
        threshold = int(self.params.get('threshold', 250))
        blur_amount = int(self.params.get('blur', 2))
        morph_size = int(self.params.get('morph_size', 3))
        
        # Convert to gray
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to create mask
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        
        # Invert mask
        mask = 255 - mask
        
        # Apply morphology
        kernel = np.ones((morph_size, morph_size), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Blur and stretch mask
        mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=blur_amount, sigmaY=blur_amount, 
                                borderType=cv2.BORDER_DEFAULT)
        mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)
        
        # Create RGBA result
        result = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask
        
        return result
    
    def replace_background(self) -> MatLike:
        """Replace background with new image, color, or gradient."""
        # First remove background
        result = self.remove_background()
        
        # Get replacement
        replacement_type = self.params.get('replacement_type', 'color')
        
        if replacement_type == 'image':
            bg_image = self.params.get('bg_image')
            if bg_image is not None:
                # Resize background to match
                bg_resized = cv2.resize(bg_image, (result.shape[1], result.shape[0]))
                if bg_resized.shape[2] == 3:
                    bg_resized = cv2.cvtColor(bg_resized, cv2.COLOR_BGR2BGRA)
                
                # Blend using alpha channel
                alpha = result[:, :, 3:4] / 255.0
                result_rgb = result[:, :, :3]
                bg_rgb = bg_resized[:, :, :3]
                
                blended = (result_rgb * alpha + bg_rgb * (1 - alpha)).astype(np.uint8)
                final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
                final[:, :, 3] = 255
                return final
        
        elif replacement_type == 'color':
            color_tuple = self.params.get('bg_color', (255, 255, 255))
            bg = np.full_like(result, (*color_tuple, 255), dtype=np.uint8)
            
            # Blend
            alpha = result[:, :, 3:4] / 255.0
            result_rgb = result[:, :, :3]
            bg_rgb = bg[:, :, :3]
            
            blended = (result_rgb * alpha + bg_rgb * (1 - alpha)).astype(np.uint8)
            final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
            final[:, :, 3] = 255
            return final
        
        elif replacement_type == 'gradient':
            color1 = self.params.get('gradient_color1', (255, 255, 255))
            color2 = self.params.get('gradient_color2', (0, 0, 0))
            direction = self.params.get('gradient_direction', 'vertical')
            
            # Create gradient
            h, w = result.shape[:2]
            gradient = np.zeros((h, w, 4), dtype=np.uint8)
            
            if direction == 'vertical':
                for i in range(h):
                    ratio = i / h
                    color = tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                                for c1, c2 in zip(color1, color2))
                    gradient[i, :] = (*color, 255)
            else:  # horizontal
                for j in range(w):
                    ratio = j / w
                    color = tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                                for c1, c2 in zip(color1, color2))
                    gradient[:, j] = (*color, 255)
            
            # Blend
            alpha = result[:, :, 3:4] / 255.0
            result_rgb = result[:, :, :3]
            gradient_rgb = gradient[:, :, :3]
            
            blended = (result_rgb * alpha + gradient_rgb * (1 - alpha)).astype(np.uint8)
            final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
            final[:, :, 3] = 255
            return final
        
        return result
    
    def remove_foreground(self) -> MatLike:
        """Remove foreground (inverse of remove background)."""
        threshold = int(self.params.get('threshold', 250))
        blur_amount = int(self.params.get('blur', 2))
        morph_size = int(self.params.get('morph_size', 3))
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        
        # Don't invert for foreground removal
        kernel = np.ones((morph_size, morph_size), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=blur_amount, sigmaY=blur_amount,
                                borderType=cv2.BORDER_DEFAULT)
        mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)
        
        result = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask
        
        return result
    
    def replace_foreground(self) -> MatLike:
        """Replace foreground with new content."""
        result = self.remove_foreground()
        
        replacement_type = self.params.get('replacement_type', 'color')
        
        if replacement_type == 'image':
            fg_image = self.params.get('fg_image')
            if fg_image is not None:
                # Resize foreground to match
                fg_resized = cv2.resize(fg_image, (result.shape[1], result.shape[0]))
                if fg_resized.shape[2] == 3:
                    fg_resized = cv2.cvtColor(fg_resized, cv2.COLOR_BGR2BGRA)
                
                # Blend using alpha channel
                alpha = result[:, :, 3:4] / 255.0
                result_rgb = result[:, :, :3]
                fg_rgb = fg_resized[:, :, :3]
                
                blended = (fg_rgb * alpha + result_rgb * (1 - alpha)).astype(np.uint8)
                final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
                final[:, :, 3] = 255
                return final
        
        elif replacement_type == 'color':
            color_tuple = self.params.get('fg_color', (0, 0, 0))
            
            alpha = result[:, :, 3:4] / 255.0
            result_rgb = result[:, :, :3]
            
            # Apply color to foreground only
            colored = np.full_like(result_rgb, color_tuple, dtype=np.uint8)
            blended = (colored * alpha + result_rgb * (1 - alpha)).astype(np.uint8)
            
            final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
            final[:, :, 3] = 255
            return final
        
        elif replacement_type == 'gradient':
            color1 = self.params.get('gradient_color1', (255, 255, 255))
            color2 = self.params.get('gradient_color2', (0, 0, 0))
            direction = self.params.get('gradient_direction', 'vertical')
            
            # Create gradient
            h, w = result.shape[:2]
            gradient = np.zeros((h, w, 4), dtype=np.uint8)
            
            if direction == 'vertical':
                for i in range(h):
                    ratio = i / h
                    color = tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                                for c1, c2 in zip(color1, color2))
                    gradient[i, :] = (*color, 255)
            else:  # horizontal
                for j in range(w):
                    ratio = j / w
                    color = tuple(int(c1 * (1 - ratio) + c2 * ratio) 
                                for c1, c2 in zip(color1, color2))
                    gradient[:, j] = (*color, 255)
            
            # Blend
            alpha = result[:, :, 3:4] / 255.0
            result_rgb = result[:, :, :3]
            gradient_rgb = gradient[:, :, :3]
            
            blended = (gradient_rgb * alpha + result_rgb * (1 - alpha)).astype(np.uint8)
            final = cv2.cvtColor(blended, cv2.COLOR_BGR2BGRA)
            final[:, :, 3] = 255
            return final
        
        return result


class BackgroundRemoverGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Advanced Background Remover")
        self.setGeometry(100, 100, 1400, 900)
        
        # State variables
        self.original_image: Optional[MatLike] = None
        self.processed_image: Optional[MatLike] = None
        self.bg_replacement_image: Optional[MatLike] = None
        self.fg_replacement_image: Optional[MatLike] = None
        self.processing: bool = False
        
        # UI components (declare for type checking)
        self.load_btn: QPushButton
        self.save_btn: QPushButton
        self.process_btn: QPushButton
        self.mode_group: QButtonGroup
        self.remove_bg_radio: QRadioButton
        self.replace_bg_radio: QRadioButton
        self.remove_fg_radio: QRadioButton
        self.replace_fg_radio: QRadioButton
        self.threshold_slider: QSlider
        self.threshold_value_label: QLabel
        self.blur_slider: QSlider
        self.blur_value_label: QLabel
        self.morph_spin: QSpinBox
        self.replacement_group: QGroupBox
        self.bg_replacement_tabs: QTabWidget
        self.fg_replacement_tabs: QTabWidget
        self.bg_color_btn: QPushButton
        self.fg_color_btn: QPushButton
        self.bg_color: QColor = QColor(255, 255, 255)
        self.fg_color: QColor = QColor(0, 0, 0)
        self.load_bg_image_btn: QPushButton
        self.load_fg_image_btn: QPushButton
        self.bg_image_label: QLabel
        self.fg_image_label: QLabel
        self.gradient_color1_btn: QPushButton
        self.gradient_color2_btn: QPushButton
        self.gradient_color1: QColor = QColor(255, 255, 255)
        self.gradient_color2: QColor = QColor(0, 0, 0)
        self.gradient_direction: QComboBox
        self.fg_gradient_color1_btn: QPushButton
        self.fg_gradient_color2_btn: QPushButton
        self.fg_gradient_color1: QColor = QColor(255, 255, 255)
        self.fg_gradient_color2: QColor = QColor(0, 0, 0)
        self.fg_gradient_direction: QComboBox
        self.image_splitter: QSplitter
        self.original_label: QLabel
        self.processed_label: QLabel
        self.worker: ImageProcessor
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_widget.setMaximumWidth(400)
        
        # File controls
        file_group = QGroupBox("File Operations")
        file_layout = QVBoxLayout()
        
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        file_layout.addWidget(self.load_btn)
        
        self.save_btn = QPushButton("Save Result")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        file_layout.addWidget(self.save_btn)
        
        file_group.setLayout(file_layout)
        controls_layout.addWidget(file_group)
        
        # Mode selection
        mode_group = QGroupBox("Operation Mode")
        mode_layout = QVBoxLayout()
        
        self.mode_group = QButtonGroup()
        self.remove_bg_radio = QRadioButton("Remove Background")
        self.replace_bg_radio = QRadioButton("Replace Background")
        self.remove_fg_radio = QRadioButton("Remove Foreground")
        self.replace_fg_radio = QRadioButton("Replace Foreground")
        
        self.remove_bg_radio.setChecked(True)
        self.mode_group.addButton(self.remove_bg_radio, 0)
        self.mode_group.addButton(self.replace_bg_radio, 1)
        self.mode_group.addButton(self.remove_fg_radio, 2)
        self.mode_group.addButton(self.replace_fg_radio, 3)
        
        mode_layout.addWidget(self.remove_bg_radio)
        mode_layout.addWidget(self.replace_bg_radio)
        mode_layout.addWidget(self.remove_fg_radio)
        mode_layout.addWidget(self.replace_fg_radio)
        
        mode_group.setLayout(mode_layout)
        controls_layout.addWidget(mode_group)
        
        # Processing parameters
        params_group = QGroupBox("Processing Parameters")
        params_layout = QVBoxLayout()
        
        # Threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Threshold:"))
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(250)
        self.threshold_value_label = QLabel("250")
        self.threshold_slider.valueChanged.connect(
            lambda v: self.threshold_value_label.setText(str(v))
        )
        threshold_layout.addWidget(self.threshold_slider)
        threshold_layout.addWidget(self.threshold_value_label)
        params_layout.addLayout(threshold_layout)
        
        # Blur
        blur_layout = QHBoxLayout()
        blur_layout.addWidget(QLabel("Edge Blur:"))
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setRange(0, 10)
        self.blur_slider.setValue(2)
        self.blur_value_label = QLabel("2")
        self.blur_slider.valueChanged.connect(
            lambda v: self.blur_value_label.setText(str(v))
        )
        blur_layout.addWidget(self.blur_slider)
        blur_layout.addWidget(self.blur_value_label)
        params_layout.addLayout(blur_layout)
        
        # Morphology
        morph_layout = QHBoxLayout()
        morph_layout.addWidget(QLabel("Cleanup Size:"))
        self.morph_spin = QSpinBox()
        self.morph_spin.setRange(1, 15)
        self.morph_spin.setValue(3)
        self.morph_spin.setSingleStep(2)
        morph_layout.addWidget(self.morph_spin)
        morph_layout.addStretch()
        params_layout.addLayout(morph_layout)
        
        params_group.setLayout(params_layout)
        controls_layout.addWidget(params_group)
        
        # Background Replacement options
        self.replacement_group = QGroupBox("Replacement Options")
        replacement_layout = QVBoxLayout()
        
        # Background replacement tabs
        self.bg_replacement_tabs = QTabWidget()
        
        # BG Color tab
        bg_color_tab = QWidget()
        bg_color_layout = QVBoxLayout(bg_color_tab)
        
        self.bg_color_btn = QPushButton("Choose Background Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.update_color_button_style(self.bg_color_btn, self.bg_color)
        bg_color_layout.addWidget(self.bg_color_btn)
        bg_color_layout.addStretch()
        self.bg_replacement_tabs.addTab(bg_color_tab, "Solid Color")
        
        # BG Image tab
        bg_image_tab = QWidget()
        bg_image_layout = QVBoxLayout(bg_image_tab)
        
        self.load_bg_image_btn = QPushButton("Load Background Image")
        self.load_bg_image_btn.clicked.connect(self.load_bg_image)
        bg_image_layout.addWidget(self.load_bg_image_btn)
        
        self.bg_image_label = QLabel("No image loaded")
        self.bg_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_image_label.setStyleSheet("border: 1px solid gray; padding: 10px;")
        bg_image_layout.addWidget(self.bg_image_label)
        bg_image_layout.addStretch()
        self.bg_replacement_tabs.addTab(bg_image_tab, "Image")
        
        # BG Gradient tab
        bg_gradient_tab = QWidget()
        bg_gradient_layout = QVBoxLayout(bg_gradient_tab)
        
        self.gradient_color1_btn = QPushButton("Gradient Start Color")
        self.gradient_color1_btn.clicked.connect(self.choose_gradient_color1)
        self.update_color_button_style(self.gradient_color1_btn, self.gradient_color1)
        bg_gradient_layout.addWidget(self.gradient_color1_btn)
        
        self.gradient_color2_btn = QPushButton("Gradient End Color")
        self.gradient_color2_btn.clicked.connect(self.choose_gradient_color2)
        self.update_color_button_style(self.gradient_color2_btn, self.gradient_color2)
        bg_gradient_layout.addWidget(self.gradient_color2_btn)
        
        gradient_dir_layout = QHBoxLayout()
        gradient_dir_layout.addWidget(QLabel("Direction:"))
        self.gradient_direction = QComboBox()
        self.gradient_direction.addItems(["Vertical", "Horizontal"])
        gradient_dir_layout.addWidget(self.gradient_direction)
        bg_gradient_layout.addLayout(gradient_dir_layout)
        bg_gradient_layout.addStretch()
        self.bg_replacement_tabs.addTab(bg_gradient_tab, "Gradient")
        
        # Foreground replacement tabs
        self.fg_replacement_tabs = QTabWidget()
        
        # FG Color tab
        fg_color_tab = QWidget()
        fg_color_layout = QVBoxLayout(fg_color_tab)
        
        self.fg_color_btn = QPushButton("Choose Foreground Color")
        self.fg_color_btn.clicked.connect(self.choose_fg_color)
        self.update_color_button_style(self.fg_color_btn, self.fg_color)
        fg_color_layout.addWidget(self.fg_color_btn)
        fg_color_layout.addStretch()
        self.fg_replacement_tabs.addTab(fg_color_tab, "Solid Color")
        
        # FG Image tab
        fg_image_tab = QWidget()
        fg_image_layout = QVBoxLayout(fg_image_tab)
        
        self.load_fg_image_btn = QPushButton("Load Foreground Image")
        self.load_fg_image_btn.clicked.connect(self.load_fg_image)
        fg_image_layout.addWidget(self.load_fg_image_btn)
        
        self.fg_image_label = QLabel("No image loaded")
        self.fg_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fg_image_label.setStyleSheet("border: 1px solid gray; padding: 10px;")
        fg_image_layout.addWidget(self.fg_image_label)
        fg_image_layout.addStretch()
        self.fg_replacement_tabs.addTab(fg_image_tab, "Image")
        
        # FG Gradient tab
        fg_gradient_tab = QWidget()
        fg_gradient_layout = QVBoxLayout(fg_gradient_tab)
        
        self.fg_gradient_color1_btn = QPushButton("Gradient Start Color")
        self.fg_gradient_color1_btn.clicked.connect(self.choose_fg_gradient_color1)
        self.update_color_button_style(self.fg_gradient_color1_btn, self.fg_gradient_color1)
        fg_gradient_layout.addWidget(self.fg_gradient_color1_btn)
        
        self.fg_gradient_color2_btn = QPushButton("Gradient End Color")
        self.fg_gradient_color2_btn.clicked.connect(self.choose_fg_gradient_color2)
        self.update_color_button_style(self.fg_gradient_color2_btn, self.fg_gradient_color2)
        fg_gradient_layout.addWidget(self.fg_gradient_color2_btn)
        
        fg_gradient_dir_layout = QHBoxLayout()
        fg_gradient_dir_layout.addWidget(QLabel("Direction:"))
        self.fg_gradient_direction = QComboBox()
        self.fg_gradient_direction.addItems(["Vertical", "Horizontal"])
        fg_gradient_dir_layout.addWidget(self.fg_gradient_direction)
        fg_gradient_layout.addLayout(fg_gradient_dir_layout)
        fg_gradient_layout.addStretch()
        self.fg_replacement_tabs.addTab(fg_gradient_tab, "Gradient")
        
        # Add tabs to main replacement layout
        replacement_layout.addWidget(QLabel("Background Replacement:"))
        replacement_layout.addWidget(self.bg_replacement_tabs)
        replacement_layout.addWidget(QLabel("Foreground Replacement:"))
        replacement_layout.addWidget(self.fg_replacement_tabs)
        
        self.replacement_group.setLayout(replacement_layout)
        self.replacement_group.setEnabled(False)
        controls_layout.addWidget(self.replacement_group)
        
        # Process button
        self.process_btn = QPushButton("Process Image")
        self.process_btn.clicked.connect(self.process_image)
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("QPushButton { font-weight: bold; padding: 10px; }")
        controls_layout.addWidget(self.process_btn)
        
        controls_layout.addStretch()
        
        # Right side: Image display
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)
        
        # Image splitter
        self.image_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Original image
        original_scroll = QScrollArea()
        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)
        original_layout.addWidget(QLabel("Original Image"))
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setStyleSheet("border: 2px solid gray;")
        self.original_label.setMinimumSize(400, 400)
        original_layout.addWidget(self.original_label)
        original_scroll.setWidget(original_container)
        original_scroll.setWidgetResizable(True)
        self.image_splitter.addWidget(original_scroll)
        
        # Processed image
        processed_scroll = QScrollArea()
        processed_container = QWidget()
        processed_layout = QVBoxLayout(processed_container)
        processed_layout.addWidget(QLabel("Processed Image"))
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setStyleSheet("border: 2px solid green;")
        self.processed_label.setMinimumSize(400, 400)
        processed_layout.addWidget(self.processed_label)
        processed_scroll.setWidget(processed_container)
        processed_scroll.setWidgetResizable(True)
        self.image_splitter.addWidget(processed_scroll)
        
        display_layout.addWidget(self.image_splitter)
        
        # Add to main layout
        main_layout.addWidget(controls_widget)
        main_layout.addWidget(display_widget, stretch=1)
        
        # Connect mode changes
        self.mode_group.buttonClicked.connect(self.on_mode_changed)
    
    def update_color_button_style(self, button: QPushButton, color: QColor) -> None:
        """Update button style to show selected color."""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                color: {'white' if color.lightness() < 128 else 'black'};
                border: 2px solid gray;
                padding: 5px;
            }}
        """)
    
    def on_mode_changed(self) -> None:
        """Handle mode radio button changes."""
        mode_id = self.mode_group.checkedId()
        # Enable replacement options for replace modes
        self.replacement_group.setEnabled(mode_id in [1, 3])
        
        # Show/hide appropriate tabs
        if mode_id == 1:  # Replace background
            self.bg_replacement_tabs.setVisible(True)
            self.fg_replacement_tabs.setVisible(False)
        elif mode_id == 3:  # Replace foreground
            self.bg_replacement_tabs.setVisible(False)
            self.fg_replacement_tabs.setVisible(True)
    
    def load_image(self) -> None:
        """Load an image file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                QMessageBox.critical(self, "Error", "Could not load image!")
                return
            
            # Display original
            self.display_image(self.original_image, self.original_label)
            
            # Enable processing
            self.process_btn.setEnabled(True)
            self.processed_label.clear()
            self.processed_image = None
    
    def load_bg_image(self) -> None:
        """Load a background replacement image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Background Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            self.bg_replacement_image = cv2.imread(file_path)
            if self.bg_replacement_image is None:
                QMessageBox.critical(self, "Error", "Could not load background image!")
                return
            
            # Show preview
            self.bg_image_label.setText(Path(file_path).name)
            pixmap = self.cv_to_pixmap(self.bg_replacement_image)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
                self.bg_image_label.setPixmap(scaled_pixmap)
    
    def load_fg_image(self) -> None:
        """Load a foreground replacement image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Foreground Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            self.fg_replacement_image = cv2.imread(file_path)
            if self.fg_replacement_image is None:
                QMessageBox.critical(self, "Error", "Could not load foreground image!")
                return
            
            # Show preview
            self.fg_image_label.setText(Path(file_path).name)
            pixmap = self.cv_to_pixmap(self.fg_replacement_image)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                self.fg_image_label.setPixmap(scaled_pixmap)
    
    def choose_bg_color(self) -> None:
        """Open color dialog for background color."""
        color = QColorDialog.getColor(self.bg_color, self, "Choose Background Color")
        if color.isValid():
            self.bg_color = color
            self.update_color_button_style(self.bg_color_btn, self.bg_color)
    
    def choose_fg_color(self) -> None:
        """Open color dialog for foreground color."""
        color = QColorDialog.getColor(self.fg_color, self, "Choose Foreground Color")
        if color.isValid():
            self.fg_color = color
            self.update_color_button_style(self.fg_color_btn, self.fg_color)
    
    def choose_gradient_color1(self) -> None:
        """Choose first gradient color for background."""
        color = QColorDialog.getColor(self.gradient_color1, self, "Choose Gradient Start Color")
        if color.isValid():
            self.gradient_color1 = color
            self.update_color_button_style(self.gradient_color1_btn, self.gradient_color1)
    
    def choose_gradient_color2(self) -> None:
        """Choose second gradient color for background."""
        color = QColorDialog.getColor(self.gradient_color2, self, "Choose Gradient End Color")
        if color.isValid():
            self.gradient_color2 = color
            self.update_color_button_style(self.gradient_color2_btn, self.gradient_color2)
    
    def choose_fg_gradient_color1(self) -> None:
        """Choose first gradient color for foreground."""
        color = QColorDialog.getColor(self.fg_gradient_color1, self, "Choose FG Gradient Start Color")
        if color.isValid():
            self.fg_gradient_color1 = color
            self.update_color_button_style(self.fg_gradient_color1_btn, self.fg_gradient_color1)
    
    def choose_fg_gradient_color2(self) -> None:
        """Choose second gradient color for foreground."""
        color = QColorDialog.getColor(self.fg_gradient_color2, self, "Choose FG Gradient End Color")
        if color.isValid():
            self.fg_gradient_color2 = color
            self.update_color_button_style(self.fg_gradient_color2_btn, self.fg_gradient_color2)
    
    def process_image(self) -> None:
        """Process the image based on selected mode."""
        if self.original_image is None or self.processing:
            return
        
        self.processing = True
        self.process_btn.setEnabled(False)
        self.process_btn.setText("Processing...")
        
        # Get mode
        mode_id = self.mode_group.checkedId()
        operations = ["remove_bg", "replace_bg", "remove_fg", "replace_fg"]
        operation = operations[mode_id]
        
        # Get parameters
        params: Dict[str, Any] = {
            'threshold': self.threshold_slider.value(),
            'blur': self.blur_slider.value(),
            'morph_size': self.morph_spin.value()
        }
        
        # Add replacement parameters
        if mode_id == 1:  # Replace background
            current_tab = self.bg_replacement_tabs.currentIndex()
            if current_tab == 0:  # Color
                params['replacement_type'] = 'color'
                params['bg_color'] = (self.bg_color.blue(), self.bg_color.green(), self.bg_color.red())
            elif current_tab == 1:  # Image
                params['replacement_type'] = 'image'
                params['bg_image'] = self.bg_replacement_image
            elif current_tab == 2:  # Gradient
                params['replacement_type'] = 'gradient'
                params['gradient_color1'] = (self.gradient_color1.blue(), 
                                            self.gradient_color1.green(), 
                                            self.gradient_color1.red())
                params['gradient_color2'] = (self.gradient_color2.blue(), 
                                            self.gradient_color2.green(), 
                                            self.gradient_color2.red())
                params['gradient_direction'] = self.gradient_direction.currentText().lower()
        
        elif mode_id == 3:  # Replace foreground
            current_tab = self.fg_replacement_tabs.currentIndex()
            if current_tab == 0:  # Color
                params['replacement_type'] = 'color'
                params['fg_color'] = (self.fg_color.blue(), self.fg_color.green(), self.fg_color.red())
            elif current_tab == 1:  # Image
                params['replacement_type'] = 'image'
                params['fg_image'] = self.fg_replacement_image
            elif current_tab == 2:  # Gradient
                params['replacement_type'] = 'gradient'
                params['gradient_color1'] = (self.fg_gradient_color1.blue(), 
                                            self.fg_gradient_color1.green(), 
                                            self.fg_gradient_color1.red())
                params['gradient_color2'] = (self.fg_gradient_color2.blue(), 
                                            self.fg_gradient_color2.green(), 
                                            self.fg_gradient_color2.red())
                params['gradient_direction'] = self.fg_gradient_direction.currentText().lower()
        
        # Start processing thread
        self.worker = ImageProcessor(self.original_image, operation, params)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.start()
    
    def on_processing_finished(self, result: MatLike) -> None:
        """Handle processing completion."""
        self.processed_image = result
        self.display_image(result, self.processed_label)
        
        self.processing = False
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Process Image")
        self.save_btn.setEnabled(True)
    
    def on_processing_error(self, error_msg: str) -> None:
        """Handle processing error."""
        QMessageBox.critical(self, "Processing Error", f"Error: {error_msg}")
        
        self.processing = False
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Process Image")
    
    def display_image(self, image: Optional[MatLike], label: QLabel) -> None:
        """Display OpenCV image in QLabel."""
        if image is None:
            return
        
        pixmap = self.cv_to_pixmap(image)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
    
    def cv_to_pixmap(self, cv_image: Optional[MatLike]) -> QPixmap:
        """Convert OpenCV image to QPixmap."""
        if cv_image is None:
            return QPixmap()
        
        # Handle different channel counts
        if len(cv_image.shape) == 2:  # Grayscale
            height, width = cv_image.shape
            bytes_per_line = width
            q_image = QImage(cv_image.data, width, height, bytes_per_line, 
                           QImage.Format.Format_Grayscale8)
        elif cv_image.shape[2] == 3:  # BGR
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_image.data, width, height, bytes_per_line, 
                           QImage.Format.Format_RGB888)
        elif cv_image.shape[2] == 4:  # BGRA
            height, width, channel = cv_image.shape
            bytes_per_line = 4 * width
            rgba_image = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA)
            q_image = QImage(rgba_image.data, width, height, bytes_per_line, 
                           QImage.Format.Format_RGBA8888)
        else:
            return QPixmap()
        
        return QPixmap.fromImage(q_image)
    
    def save_image(self) -> None:
        """Save the processed image."""
        if self.processed_image is None:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "processed_image.png", 
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if file_path:
            success = cv2.imwrite(file_path, self.processed_image)
            if success:
                QMessageBox.information(self, "Success", f"Image saved to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", "Could not save image!")


def main() -> None:
    app = QApplication(sys.argv)
    
    # Set modern style
    app.setStyle('Fusion')
    
    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    window = BackgroundRemoverGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
