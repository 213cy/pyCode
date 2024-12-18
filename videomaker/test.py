from PIL import Image, ImageDraw, ImageFont


def create_cover_image(config):

    img = Image.open(config.background_file)
    # img = img.copy()
    Idrawer = ImageDraw.Draw(img)

    yy = config.HEIGHT/2
    xx = config.WIDTH/2

           
    text = "fragile [ˈfrædʒaɪl] 易碎(easy to fragment)"
    median_color = tuple(int((a+b)/2) for a,b in zip(config.colorword,config.colorbackground))
    font = ImageFont.truetype(config.FONTNAME_EN_light, size=40)
    Idrawer.text((xx, yy), text,
                 align="center",
                 anchor="mm", font=font,
                 stroke_width=1, fill=median_color)


    font = ImageFont.truetype(config.FONTNAME_EN, size=50)
    Idrawer.text((xx, yy-100), text,
                 anchor="mm", font=font,
                 stroke_width=1, fill=config.colorword)

    font = ImageFont.truetype(config.FONTNAME_ZH, size=50)
    Idrawer.text((xx, yy+100), text,
                 anchor="mm", font=font,
                 stroke_width=1, fill=config.colorword)

    return img


if __name__ == "__main__":
    from configuration import config
    image = create_cover_image(config)
    image.show()

