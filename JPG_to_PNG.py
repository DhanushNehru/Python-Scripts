from PIL import Image

# open JPG image

try :

    image = Image.open(r"C:\Users\ABHILASH\OneDrive\Desktop\iron man_jpg.jpeg") # Repalce path with our own image path 
    
    # You can also provide an absolute path if you want to save it elsewhere
    image.save("iron man.png") # image is saved in the same dir
    
except Exception as e :

    print(f" Error occurred: {e}")