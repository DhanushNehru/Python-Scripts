#Importing required module
from PIL import Image
from glob import glob

# Printing list of .png files
print(glob("*.png"))


# main loop
for img_file in glob("*.png"):
    img = Image.open(img_file)# Opening the image file
    rgb_img = img.convert("RGB")# Converting it into RGB 
    rgb_img.save(img_file.replace("png","jpg"), quality=95)# Saving the img as .jpg
