import random
import colorsys
from PIL import Image, ImageDraw, ImageFont


def create_background_image(config):
    w = config.WIDTH
    h = config.HEIGHT
    bg_rgb = config.colorbackground
    coff_rgb = [ 1 if k < 128  else -1 for k in bg_rgb]

    img = Image.new('RGB', (w, h), config.colorbackground)
    Idrawer = ImageDraw.Draw(img)

    for ind in range(1, 11):
        di = random.random() * (w + h) / (ind + 1) + 10
        x = random.random() * (w + di) - di / 2
        y = random.random() * (h + di) - di / 2
        # hh = hls_b[0] + ind/100
        # ll = hls_b[1] + ind/100
        # ss = hls_b[2] + ind/100
        # _rgb = tuple(int(k*0xff) for k in colorsys.hls_to_rgb(hh, ll, ss))
        _rgb = tuple(k+c*3*ind for k,c in zip(bg_rgb,coff_rgb))
        Idrawer.ellipse(((x, y), (x+di, y+di)), fill=_rgb)
        # , outline=(0, 0, 255), width=5)

    # img.show()
    img.save(config.background_file)
    return img

if __name__ == "__main__":
    from configuration import config
    image = create_background_image(config)
    image.show()

