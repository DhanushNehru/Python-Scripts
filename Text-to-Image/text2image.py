from PIL import Image, ImageDraw, ImageFont

def main():
    # Get filename for image
    filename = input("What would you like your image to be called?")
    # Create white background image
    img = Image.new(mode="RGB", size=(1920,1080), color='#FFFFFF')
    d1 = ImageDraw.Draw(img)
    # Get text for the image
    writing = input("Write your text here: ")
    # Choose the font
    fnt = ImageFont.truetype("Python-Scripts/Text-to-Image/fonts/Roboto-Black.ttf", 40)
    # Write the text
    d1.text((65, 10), writing, fill=(255,0,0), font=fnt)
    #  Show & save the image
    img.show()
    img.save(filename + ".jpeg")

if __name__ == '__main__':
    main()