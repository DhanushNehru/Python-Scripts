import cv2
from pyzbar.pyzbar import decode
from tkinter import filedialog
from tkinter import Tk
from PIL import Image

def scan_qrcode(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Decode the QR code in the image
    decoded_objects = decode(img)

    # Check if any QR code is found
    if decoded_objects:
        for obj in decoded_objects:
            print(f"QR Code Detected: {obj.data.decode('utf-8')}")
    else:
        print("No QR code detected in the image.")

def open_file():
    # Open a file dialog to allow the user to select an image file (PNG or JPG)
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        scan_qrcode(file_path)
    else:
        print("No file selected.")

if __name__ == "__main__":
    open_file()
