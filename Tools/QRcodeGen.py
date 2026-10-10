import qrcode
from qrcode.constants import ERROR_CORRECT_L

def generate_qrcode(data: str, file_path: str = "qrcode.png", fill_color: str = "black", back_color: str = "white"):
    """
    Generates a QR code from the provided data and saves it as an image file.
    
    Parameters:
    - data (str): The content the QR code should contain (URL, text, etc.).
    - file_path (str): The path to save the QR code image file (default: "qrcode.png").
    - fill_color (str): Color of the QR code (default: "black").
    - back_color (str): Background color of the QR code (default: "white").
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate the image with specified colors
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(file_path)
    print(f"QR code saved as {file_path}")

# Usage example
generate_qrcode("https://example.com", "my_qrcode.png")
