import filecmp

from PIL import Image, PngImagePlugin


# Create two simple black and white images with different sizes
def create_test_images():
    # Image 1: 100x100 pixels
    img1 = Image.new("L", (100, 100), color=0)  # Black image

    # Image 2: 200x200 pixels with same visual content (scaled)
    img2 = Image.new("L", (100, 100), color=0)  # Black image

    # Add different metadata
    meta1 = PngImagePlugin.PngInfo()
    meta1.add_text("Title", "Test Image 1")
    meta1.add_text("Author", "Generator")

    # Save with different metadata
    img1.save("image1.png", pnginfo=meta1)
    img2.save("image2.png")


create_test_images()

print(filecmp.cmp("image1.png", "image2.png", shallow=False))
