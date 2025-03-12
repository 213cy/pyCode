from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np


def aaa():
    filepath = "E:\Documents\pyCode\paperwar3\Assets\Lords_Dirt.blp"
    # Open the RGB image
    img_rgb = Image.open(filepath)
    # image_width,image_height = img_rgb.size
    print(img_rgb.size)
    print(img_rgb.mode)
    print(img_rgb.getbands())

    # Convert the RGB image to RGBA
    img_rgba = img_rgb.convert('RGBA')
    print(img_rgb.size)

    # img_data = img.tobytes()
    # Load the image data into a list of pixel tuples
    pixels = img_rgba.load()
    width, height = img_rgba.size
    print(pixels[2, 333])
    p = 0
    # Iterate over each pixel and set the alpha value of black pixels to 0
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if r == p and g == p and b == p:  # Check if the pixel is black
                pixels[x, y] = (r, g, b, 0)  # Set alpha value to 0

    img_rgba.show()
    rr, gg, bb, aa = img_rgba.split()
    print(type(aa))
    ImageOps.invert(aa).show()
    # aa.show()
    exit()
    pass


def bbb():
    filepath = "E:\Documents\pyCode\paperwar3\Assets\Lords_Dirt.blp"
    # Open the RGB image
    img_rgb = Image.open(filepath)
    img_np = np.array(img_rgb)
    img_alpha_np = np.any(img_np != [0, 0, 0], axis=2)
    img_alpha_np = (img_alpha_np * 255).astype(np.uint8)
    img_alpha = Image.fromarray(img_alpha_np, mode="L")
    img_alpha.show()
    img_rgba = Image.merge("RGBA", (*img_rgb.split(), img_alpha))
    # Image.alpha_composite(img_rgb, img_alpha)
    img_rgba.show()
    pass


filepath = "E:\Documents\pyCode\paperwar3\Assets\Lords_Dirt.tga"
img_rgba = Image.open(filepath)
rr, gg, bb, aa = img_rgba.split()

font_size=  25
fnt = ImageFont.truetype("arial.ttf", font_size)
# fnt = ImageFont.truetype("msyh.ttf", font_size)
# fnt = ImageFont.truetype("symbol.ttf", font_size)
# fnt = ImageFont.truetype("tahoma.ttf", font_size)

# get a drawing context
d = ImageDraw.Draw(img_rgba)

for ind in range(32):
    x, y = divmod(ind, 4)
    xx, yy = 64*x+32, 64*y+32
    # print(xx, yy)
    d.text((xx, yy), str(ind), font=fnt,
           anchor="mm", fill=( 115, 255, 115, 255))


img_rgba.show()
# Save the modified RGBA image
img_rgba.save(f"{filepath}.tga")
pass