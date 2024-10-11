import pytesseract
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar

def extract_text_from_image(img):  #Extracts Text from Image using Pytesseract
    try:
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(e)
        return None

def select_image_file():  # Upload a Image file
    img_path = filedialog.askopenfilename(title="Select Screenshot", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if img_path:
        img = Image.open(img_path)
        display_extracted_text(img)

def paste_image_from_clipboard():   # Take partial screenshot (Windows + shift + S) it will be saved in clipboard.
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            display_extracted_text(img)
        else:
            messagebox.showwarning("Error", "No image found in the clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Error accessing clipboard: {e}")

def capture_screenshot():  # Takes entire screen screenshot
    try:
        img = ImageGrab.grab()
        display_extracted_text(img)
    except Exception as e:
        messagebox.showerror("Error", f"Error capturing screenshot: {e}")

def display_extracted_text(img):  # Displaying extracted text from pytesseract
    text = extract_text_from_image(img)
    if text:
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, text)
    else:
        messagebox.showwarning("Error", "No text could be extracted or an error occurred.")

def main():
    global text_display  

    root = tk.Tk()
    root.title("Text Extractor with Python")

    text_frame = tk.Frame(root)
    text_frame.pack(pady=10)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_display = Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=15, width=60)
    text_display.pack()

    scrollbar.config(command=text_display.yview)

    btn_select_file = tk.Button(root, text="Select Image File", command=select_image_file, width=30)
    btn_select_file.pack(pady=10)

    btn_paste_clipboard = tk.Button(root, text="Paste Image from Clipboard", command=paste_image_from_clipboard, width=30)
    btn_paste_clipboard.pack(pady=10)

    btn_capture_screenshot = tk.Button(root, text="Capture Full Screen Screenshot", command=capture_screenshot, width=30)
    btn_capture_screenshot.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
