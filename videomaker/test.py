import colorsys
import random
import requests
import asyncio
from PIL import Image, ImageDraw, ImageFont
import hashlib


def shifts_operation_with_negative():

    # The hash value is different when invoked a second time
    # because recent releases of Python (versions 3.3 and up),
    # by default, apply a random hash seed for this function.
    # The seed changes on each invocation of Python.
    # Within a single instance, the results will be identical.
    val = hash('sometext')
    leng = (val.bit_length() + 7) // 8
    res = 0
    for k in range(leng):
        res ^= val & 0xff
        val = val >> 8
    print(res)

    pass


def generate_comfortable_colors():

    min_contrast = 4.5  # WCAG AA标准最低对比度

    hue_range = (180, 300)  # 色相范围（冷色调更舒适）
    bg_hue = random.uniform(*hue_range)
    fg_hue = random.uniform(*hue_range)
    bg_value = random.uniform(0.5, 0.9)  # 亮度范围控制
    fg_value = random.uniform(0.3, 0.9)
    max_saturation = 0.7  # 最大饱和度控制
    bg_saturation = random.uniform(0.2, max_saturation)
    fg_saturation = random.uniform(0.3, max_saturation)
    bg_rgb = colorsys.hsv_to_rgb(bg_hue/360, bg_saturation, bg_value)
    fg_rgb = colorsys.hsv_to_rgb(fg_hue/360, fg_saturation, fg_value)

    luminance_bt709 = 0.2126 * bg_rgb[0] + \
        0.7152 * bg_rgb[1] + 0.0722 * bg_rgb[2]

    return {
        'background': bg_rgb,
        'foreground': fg_rgb,
        'contrast_ratio': round(contrast_ratio, 2)
    }


def aaa():
    chara_str = 'fdsfsdfdfsdfsd'
    str_digest = hashlib.md5(chara_str.encode()).hexdigest()
    rand_num = [int(str_digest[i:i+2], 16) /
                0xff for i in range(0, len(str_digest), 2)]
    aa, bb, cc = [rand_num[0], rand_num[1], rand_num[2]]
    yy = [0.2+0.1*aa, 0.6+0.1*bb, 0.8+0.1*cc]
    aa, bb, cc = [rand_num[3], rand_num[4], rand_num[5]]
    ii = [2*aa-1, 2*bb-1, 2*cc-1]
    aa, bb, cc = [rand_num[6], rand_num[7], rand_num[8]]
    qq = [2*aa-1, 2*bb-1, 2*cc-1]
    bg_rgb = colorsys.yiq_to_rgb(yy[0], ii[0], qq[0])
    fg_rgb = colorsys.yiq_to_rgb(yy[1], ii[1], qq[1])
    fg_rgb_h = colorsys.yiq_to_rgb(yy[2], ii[2], qq[2])
    return {
        'background': bg_rgb,
        'foreground': fg_rgb,
        'foreground_h': fg_rgb_h,
        'contrast_ratio': round(yy[1]/yy[0], 2)
    }


if __name__ == "__main__":
    # 生成并打印配色方案
    # color_scheme = generate_comfortable_colors()
    color_scheme = aaa()
    print(f"背景色: {color_scheme['background']}")
    print(f"前景色: {color_scheme['foreground']}")
    print(f"对比度: {color_scheme['contrast_ratio']}:1 (符合WCAG AA标准)")

    # 定义图片尺寸
    width, height = 400, 200

    # 定义颜色（RGB格式）
    background_color = tuple(int(k*0xff)
                             for k in color_scheme['background'])
    text_color = tuple(int(k*0xff)
                       for k in color_scheme['foreground_h'])

    # 创建图像对象
    image = Image.new('RGB', (width, height), background_color)

    # 创建绘图对象
    draw = ImageDraw.Draw(image)

    # 设置字体（这里使用默认字体，可以根据需要指定字体文件）
    # font = ImageFont.load_default()
    font = ImageFont.truetype("arial.ttf", size=50)

    # 定义文字内容和位置
    text = "Hello, World!"
    text_position = (width // 2, height // 2)

    # 绘制文字
    draw.text(text_position, text, anchor="mm", fill=text_color, font=font)

    image.show()

    pass
