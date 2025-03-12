from PIL import Image, ImageDraw, ImageFont
import win32api
import win32gui


def enumerate_fonts():
    def func_dummy(a, b, c, d):
        print(a.lfFaceName)
        return True
    hdc = win32gui.GetDC(0)
    win32gui.EnumFontFamilies(hdc, None, func_dummy)
    win32gui.ReleaseDC(0, hdc)

# enumerate_fonts()


print(Image.__version__)
# exit()
canvas_size = (400, 200)
canvas_center = (200, 100)
font_size = 24


msg_str = 'string string string'
msg_str = "Hello"+" World" + "\n"+"Hello"+" World"

# make a blank image for the text, initialized to transparent text color
image = Image.new("RGBA", canvas_size, (30, 30, 30, 30))
# get a drawing context
img_drawer = ImageDraw.Draw(image)

# get a font
# fnt = ImageFont.truetype("arial.ttf", font_size)
fnt = ImageFont.truetype("msyh.ttf", font_size)
# fnt = ImageFont.truetype("symbol.ttf", font_size)
# fnt = ImageFont.truetype("tahoma.ttf", font_size)


img_drawer.text(canvas_center, msg_str , font=fnt,
                anchor="mm", align="left", fill=(0, 255, 0, 255))
#  ,align="center"
img_drawer.multiline_text(canvas_center, msg_str, font=fnt,
                        anchor="mm", fill=(255, 255, 255, 255))
# print(img_drawer.textlength(string , font=fnt))
bbox = img_drawer.multiline_textbbox(
    canvas_center, msg_str, font=fnt, anchor="mm")
bbox_extend = [bbox[0]-12, bbox[1]-12, bbox[2]+12, bbox[3]+12,]
img_drawer.rounded_rectangle(
    bbox_extend, radius=10, fill=None, outline=(243, 193, 44, 255), width=2)
bbox_border = [bbox[0]-13, bbox[1]-13, bbox[2]+14, bbox[3]+14,]

img = image.crop(bbox_border)
img.show()
# print()
# image.show()
