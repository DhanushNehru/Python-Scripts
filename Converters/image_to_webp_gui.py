from tkinter import Label, Tk, simpledialog
from PIL import Image, ImageTk
import tkinter.filedialog as tkFileDialog
import os

# Initialize the Tkinter root window
root = Tk()
root.withdraw()  # Hide the root window

# Open file dialog to select multiple image files
paths = tkFileDialog.askopenfilenames(filetypes=[("Image Files", ('.jpg', '.jpeg', '.png', '.bmp', '.gif'))])
webp_paths = []

if paths:
    # Open directory dialog to select the save directory
    save_directory = tkFileDialog.askdirectory()
    if save_directory:
        # Ask user for the quality of the output WebP images
        quality = simpledialog.askinteger("Quality", "Enter quality (1-100):", minvalue=1, maxvalue=100)
        if quality:
            for path in paths:
                if path:
                    # Open the image file
                    im = Image.open(path)
                    base_name = os.path.basename(path)
                    name, ext = os.path.splitext(base_name)
                    # Define the save path for the WebP image
                    save_path = os.path.join(save_directory, f"{name}.webp")
                    # Save the image as WebP with the specified quality
                    im.save(save_path, 'webp', quality=quality)
                    webp_paths.append(save_path)
                    print(f"Image converted and saved to: {save_path}")

# Close the Tkinter window
root.destroy()  # Close the Tkinter window