import random
import colorsys
from PIL import Image, ImageDraw, ImageFont


def create_background_image(config):
    w = config.WIDTH
    h = config.HEIGHT
    hls_b = config.hls_b
    img = Image.new('RGB', (w, h), config.colorbackground)
    Idrawer = ImageDraw.Draw(img)

    for ind in range(1, 11):
        di = random.random() * (w + h) / (ind + 1) + 10
        x = random.random() * (w + di) - di / 2
        y = random.random() * (h + di) - di / 2
        hh = hls_b[0] + ind/100
        ll = hls_b[1] + ind/100
        ss = hls_b[2] + ind/100
        rgb_b = tuple(int(k*0xff) for k in colorsys.hls_to_rgb(hh, ll, ss))
        Idrawer.ellipse(((x, y), (x+di, y+di)), fill=rgb_b)
        # , outline=(0, 0, 255), width=5)

    # img.show()
    img.save(config.background_file)
    return img

if __name__ == "__main__":
    from configuration import config
    image = create_background_image(config)
    image.show()

