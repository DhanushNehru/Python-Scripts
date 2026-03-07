"""QR image generation helpers."""

from __future__ import annotations

import base64
import binascii
import io

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.pil import PilImage

from wifiqr.constants import (
    DEFAULT_QR_BACKGROUND_COLOR,
    DEFAULT_QR_BORDER,
    DEFAULT_QR_BOX_SIZE,
    DEFAULT_QR_FILL_COLOR,
    DEFAULT_QR_SIZE,
)

CENTER_IMAGE_SIZE = 100  # Optimal size for center image in QR codes


def generate_qr_image(
    payload: str, size: int = DEFAULT_QR_SIZE, center_image_data: str | None = None
) -> Image.Image:
    """Generate a QR image for the provided payload with optional center image."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,  # High error correction for center images
        box_size=DEFAULT_QR_BOX_SIZE,
        border=DEFAULT_QR_BORDER,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    image_factory = qr.make_image(
        image_factory=PilImage,
        fill_color=DEFAULT_QR_FILL_COLOR,
        back_color=DEFAULT_QR_BACKGROUND_COLOR,
    )
    image: Image.Image = image_factory.get_image().convert("RGB")

    if size and image.size != (size, size):
        image = image.resize((size, size), Image.Resampling.LANCZOS)

    # Add center image if provided
    if center_image_data:
        try:
            image_bytes = base64.b64decode(center_image_data, validate=True)
        except binascii.Error as exc:
            raise ValueError("Center image data is not valid base64.") from exc

        try:
            center_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        except Exception as exc:
            raise ValueError("Center image data is not a valid image.") from exc

        # Resize center image to fixed size
        center_img = center_img.resize(
            (CENTER_IMAGE_SIZE, CENTER_IMAGE_SIZE), Image.Resampling.LANCZOS
        )

        # Calculate position to center the image
        qr_width, qr_height = image.size
        pos_x = (qr_width - CENTER_IMAGE_SIZE) // 2
        pos_y = (qr_height - CENTER_IMAGE_SIZE) // 2

        # Convert QR to RGBA for compositing
        image = image.convert("RGBA")

        # Paste center image
        image.paste(center_img, (pos_x, pos_y), center_img)

        # Convert back to RGB
        image = image.convert("RGB")

    return image


def save_qr_image(image: Image.Image, file_path: str) -> None:
    """Persist a QR image to disk."""
    image.save(file_path)
