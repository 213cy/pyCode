import colorsys
import hashlib
import math


def show_benchcolor():
    benchRGB_str = ['ffffff', 'e79c19', '303070']
    benchRGB = list(
        map(lambda x: list(int(x[i:i+2], 16)/0xff for i in (0, 2, 4)), benchRGB_str))
    temp = [colorsys.rgb_to_hls(*k) for k in benchRGB]
    benchHLS = [tuple(round(c, 2) for c in hls) for hls in temp]
    print(benchHLS)
    temp = [colorsys.rgb_to_yiq(*k) for k in benchRGB]
    benchYIQ = [tuple(round(c, 2) for c in yiq) for yiq in temp]
    print(benchYIQ)
    # [(1.0, 0.0, 0.0), (0.64, 0.34, -0.1), (0.22, -0.08, 0.08)]

    approximate = [(0.0, 1.0, 0.0), (0.10, 0.50, 0.80), (2/3, 0.31, 0.4)]
    print(approximate)
# show_benchcolor()


def color_set(chara_str, con):
    str_digest = hashlib.md5(chara_str.encode()).hexdigest()
    rand_num = [int(str_digest[i:i+2], 16) /
                0xff for i in range(0, len(str_digest), 2)]
    aa, bb, cc = [rand_num[0], rand_num[1], rand_num[2]]
    yy = [0.2+0.1*aa, 0.7+0.1*bb, 0.8+0.1*cc]

    temp = [rand_num[9] + k*2*math.pi/3 for k in range(3)]
    temp_x = [math.sin(k)/4 for k in temp]
    temp_y = [math.cos(k)/4 for k in temp]

    aa = 0.4
    bb = aa/2
    offset = [aa*rand_num[3]-bb, aa*rand_num[4]-bb, aa*rand_num[5]-bb]
    ii = [v+k for v, k in zip(temp_x, offset)]
    offset = [aa*rand_num[6]-bb, aa*rand_num[7]-bb, aa*rand_num[8]-bb]
    qq = [v+k for v, k in zip(temp_y, offset)]

    yiq_h = (yy[2], ii[2], qq[2])
    yiq_f = (yy[1], ii[1], qq[1])
    yiq_b = (yy[0], ii[0], qq[0])

    con.colorwordhilight = tuple(int(k*0xff)
                                 for k in colorsys.yiq_to_rgb(*yiq_h))
    con.colorword = tuple(int(k*0xff)
                          for k in colorsys.yiq_to_rgb(*yiq_f))
    con.colorbackground = tuple(int(k*0xff)
                                for k in colorsys.yiq_to_rgb(*yiq_b))
    pass


config = type('Config', (), {})
# ===============================

config.project_folder_name = 'pr[aeiou][cs]'
config.regexp = ["/^pr[aeiou][cs]/"]

# ===============================

config.ROOTPATH = "F:/video"
config.project_path = f"{config.ROOTPATH}/{config.project_folder_name}"
config.page_folder_prefix = "PAGE"
config.background_file = f"{config.project_path}/background.png"
config.cover_file = f"{config.project_path}/cover.png"
config.words_file = f"{config.project_path}/words.txt"
config.words_proto_file = f"{config.project_path}/words_proto.txt"


config.QUERYURL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
config.VOICE = "en-GB-RyanNeural"


# config.FONTNAME_EN = "arial.ttf"
# config.FONTNAME_EN = "FreeMono.ttf"
# config.FONTNAME_ZH = "msyh.ttf"
# config.FONTNAME_EN = "F:\\video\\SourceHanSansSC-VF.ttf"
config.FONTNAME_EN_light = "F:\\video\\SourceSans3-Light.ttf"
config.FONTNAME_EN = "F:\\video\\SourceSans3-Regular.ttf"
config.FONTNAME_ZH = "F:\\video\\SourceHanSansSC-VF.ttf"

config.WIDTH = 1280
config.HEIGHT = 720

# ===============================

color_set(' '.join(config.regexp), config)
