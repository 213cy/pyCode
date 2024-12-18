from PIL import Image, ImageDraw, ImageFont

work_folder = "F:/video/test"
backimage = Image.open(f"{work_folder}/black.png")

font_folder = "F:/video/SourceHanSansCN"
font_name = f"{font_folder}/SourceHanSansCN-Regular.otf"

def bold_entire():
    X0 = 1280/2
    Y0 = 720/2-50
    font_zh = ImageFont.truetype(font_name, size=240)
    imdrawer.text((X0, Y0), content, anchor="mm", font=font_zh,
                fill=(237, 38, 46))#stroke_width=0,

def bold_title():
    X0 = 1280/2
    Y0 = 120
    line_height = 90
    font_zh = ImageFont.truetype(font_name, size=60)
    imdrawer.text((X0, Y0), line_list[0], anchor="mm", font=font_zh,
                fill=(237, 38, 46))#stroke_width=0,

    font_zh = ImageFont.truetype(font_name, size=20)
    for index, line in enumerate(line_list[1:]):
        yy = Y0+index * line_height+line_height
        imdrawer.text((X0, yy), line, anchor="mm", font=font_zh,
                    fill=(237, 38, 46))#stroke_width=0,


def normallines():
    Y0 = 100
    X0 = 200
    line_height = 60
    font_zh = ImageFont.truetype(font_name, size=40)
    for index, line in enumerate(line_list):
        yy = Y0+index * line_height
        imdrawer.text((X0, yy), line, anchor="lm", font=font_zh,
                    fill=(237, 38, 46))#stroke_width=0,


if __name__ == "__main__":
    pass

content = '''
抽奖唯一参与条件:       向此视频发送弹幕

开奖条件:
1, 参与抽奖的人数超过100
2, 在条件1满足的前提下,本视频至少产生一次
     历史弹幕后,将启动开奖流程
3, 本up完成开奖流程(短则一个月,长则三年五载)
'''

line_list = content.split('\n')

font_zh = ImageFont.truetype(font_name, size=40)

imdrawer = ImageDraw.Draw(backimage)

# wlist = [imdrawer.textlength(line, font_zh) for line in line_list]
# width_max = max(wlist)
# X0 = round((1280-width_max)/2)
normallines()


backimage.show()

# Save the edited image
# backimage.save(f"{work_folder}/03.png")
