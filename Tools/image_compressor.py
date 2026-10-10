from PIL import Image
file_path = "path_of_image"
img = Image.open(file_path)
height, width = img.size
compressed = img.resize((height, width), Image.ANTIALIAS)
compressed.save("compressedImage.jpg", optimize=True, quality=9)
