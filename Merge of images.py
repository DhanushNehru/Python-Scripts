##install pillow before using this.
from PIL import Image

# Open the two images you want to merge
image1 = Image.open("image1.jpg")
image2 = Image.open("image2.jpg")

# Ensure both images have the same size
if image1.size != image2.size:
    raise ValueError("Images must have the same dimensions")

# Merge the two images
merged_image = Image.blend(image1, image2, alpha=0.5)  # You can adjust the alpha value to control the blending

# Save the merged image
merged_image.save("merged_image.jpg")

# Display the merged image (optional)
merged_image.show()
