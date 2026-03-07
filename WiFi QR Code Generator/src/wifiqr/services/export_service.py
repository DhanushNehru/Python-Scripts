"""Qt conversion helpers for PIL images."""

from __future__ import annotations

from PIL import Image
from PySide6.QtGui import QImage, QPixmap


def pil_to_qimage(image: Image.Image) -> QImage:
    """Convert a PIL image into a Qt QImage."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    width, height = image.size
    data = image.tobytes("raw", "RGB")
    qimage = QImage(data, width, height, QImage.Format.Format_RGB888)
    return qimage.copy()


def pil_to_qpixmap(image: Image.Image) -> QPixmap:
    """Convert a PIL image into a Qt QPixmap."""
    return QPixmap.fromImage(pil_to_qimage(image))
