from PIL import Image
from glob import glob

print(glob("*.png"))

for img_file in glob("*.png"):
    img = Image.open(img_file)
    rgb_img = img.convert("RGB")
    rgb_img.save(img_file.replace("png","jpg"), quality=95)
