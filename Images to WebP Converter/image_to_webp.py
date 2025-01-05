import argparse
from PIL import Image
import os

# Set up argument parser
parser = argparse.ArgumentParser(description="Convert images to WebP format.")
parser.add_argument("files", nargs='+', help="Paths to the image files to convert.")
parser.add_argument("save_directory", help="Directory to save the converted WebP images.")
parser.add_argument("quality", type=int, help="Quality of the output WebP images (1-100).")

args = parser.parse_args()

webp_paths = []

for path in args.files:
    if path:
        # Open the image file
        im = Image.open(path)
        base_name = os.path.basename(path)
        name, ext = os.path.splitext(base_name)
        # Define the save path for the WebP image
        save_path = os.path.join(args.save_directory, f"{name}.webp")
        # Save the image as WebP with the specified quality
        im.save(save_path, 'webp', quality=args.quality)
        webp_paths.append(save_path)
        print(f"Image converted and saved to: {save_path}")

# python image_to_webp.py <image_files> <save_directory> <quality>
# python image_to_webp.py image1.jpg image2.png /path/to/save/directory 80