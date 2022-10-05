#imports
from PIL import Image

#image to be inserted
img=Image.open("icon.png")
#edit the dimension of the image
dimension=(300,100,500,200)
cropImg=img.crop(box=dimension)
#This will show the image
cropImg.show()