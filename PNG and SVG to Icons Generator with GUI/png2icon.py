import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QCheckBox, QLabel, QHBoxLayout, QGroupBox
from PIL import Image
import io

# Pillow 10+ uses Image.Resampling.LANCZOS, fallback for older versions
try:
    LANCZOS_RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS_RESAMPLE = 1  # 1 is the value for LANCZOS in older Pillow

class IconConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNG/SVG to Icon Converter")
        self.setGeometry(200, 200, 400, 250)

        self.sizes = [16, 24, 32, 48, 64, 128, 256, 512]
        self.checkboxes = []

        # Check SVG support
        try:
            import cairosvg
            self.svg_support = True
        except ImportError:
            self.svg_support = False

        layout = QVBoxLayout()
        self.button = QPushButton("Select Image and Convert")
        self.button.clicked.connect(self.convert_icon)
        layout.addWidget(self.button)

        # Add checkboxes for sizes
        size_group = QGroupBox("Select icon sizes to output")
        size_layout = QHBoxLayout()
        for size in self.sizes:
            cb = QCheckBox(f"{size}x{size}")
            cb.setChecked(True)
            self.checkboxes.append(cb)
            size_layout.addWidget(cb)
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        self.setLayout(layout)

    def convert_icon(self):
        # Step 1: Select PNG or SVG file
        file_filter = "Image Files (*.png *.svg)" if self.svg_support else "PNG Files (*.png)"
        img_file, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", file_filter)
        if not img_file:
            return

        # Step 2: Ask where to save icons
        save_dir = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if not save_dir:
            return

        try:
            # Load image (handle SVG if needed)
            if img_file.lower().endswith('.svg'):
                import cairosvg  # Ensure cairosvg is in local scope
                if not self.svg_support:
                    QMessageBox.critical(self, "Error", "SVG support requires cairosvg. Please install it.")
                    return
                # Convert SVG to PNG in memory
                png_bytes = cairosvg.svg2png(url=img_file)
                if png_bytes is None:
                    raise ValueError("SVG conversion failed.")
                img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            else:
                img = Image.open(img_file).convert("RGBA")

            # Get selected sizes
            selected_sizes = [self.sizes[i] for i, cb in enumerate(self.checkboxes) if cb.isChecked()]
            if not selected_sizes:
                QMessageBox.warning(self, "No Sizes Selected", "Please select at least one icon size.")
                return

            # Windows ICO
            ico_path = os.path.join(save_dir, "icon.ico")
            ico_sizes = [(s, s) for s in selected_sizes if s in [16, 32, 48, 256]]
            if ico_sizes:
                img.save(ico_path, format="ICO", sizes=ico_sizes)

            # macOS ICNS
            icns_path = os.path.join(save_dir, "icon.icns")
            if any(s in [16, 32, 128, 256, 512] for s in selected_sizes):
                img.save(icns_path, format="ICNS")

            # Linux PNG sizes
            linux_dir = os.path.join(save_dir, "linux_icons")
            os.makedirs(linux_dir, exist_ok=True)
            for size in selected_sizes:
                resized = img.resize((size, size), LANCZOS_RESAMPLE)
                resized.save(os.path.join(linux_dir, f"icon_{size}x{size}.png"))

            QMessageBox.information(self, "Success", f"Icons saved in:\n{save_dir}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconConverterApp()
    window.show()
    sys.exit(app.exec())
