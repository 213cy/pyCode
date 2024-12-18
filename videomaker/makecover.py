from PIL import Image, ImageDraw, ImageFont
import random


def create_cover_image(config):
    with open(config.words_file, 'r', encoding="utf-8-sig") as f:
        line_list = f.readlines()
    words = list(line.split(' ')[0] for line in line_list if line != '\n')
    print("Number of words :", len(words))

    img = Image.open(config.background_file)
    # img = img.copy()
    Idrawer = ImageDraw.Draw(img)

    yy = config.HEIGHT/2
    xx = config.WIDTH/2

    lines_n = 14
    chars_n = 80
    repeat = int(lines_n * chars_n / len('    '.join(words)))+2
    # global words_rand
    words_rand = random.sample(words*repeat, len(words)*repeat)

    wordlines = []

    start = 0
    for k in range(lines_n):
        end = start + 1

        current_length = len(words_rand[start])
        next_length = current_length+3+len(words_rand[end])
        while next_length < chars_n:
            end += 1
            current_length = next_length
            next_length = current_length+4+len(words_rand[end])

        if current_length + next_length < chars_n + chars_n:
            wordlines.append('    '.join(words_rand[start:end+1]))
            start = end+1
        else:
            wordlines.append('    '.join(words_rand[start:end]))
            start = end
    median_color = tuple(int((a+b)/2) for a,b in zip(config.colorword,config.colorbackground))
    font = ImageFont.truetype(config.FONTNAME_EN_light, size=40)
    Idrawer.text((xx, yy), '\n'.join(wordlines),
                 align="center",
                 anchor="mm", font=font,
                 stroke_width=1, fill=median_color)


    font = ImageFont.truetype(config.FONTNAME_EN, size=250)
    Idrawer.text((xx, yy-50), config.regexp[0],
                 anchor="mm", font=font,
                 stroke_width=36, fill=config.colorbackground)

    font = ImageFont.truetype(config.FONTNAME_EN, size=250)
    Idrawer.text((xx, yy-50), config.regexp[0],
                 anchor="mm", font=font,
                 stroke_width=1, fill=config.colorword)

    img.save(config.cover_file)
    return img


if __name__ == "__main__":
    from configuration import config
    image = create_cover_image(config)
    image.show()
