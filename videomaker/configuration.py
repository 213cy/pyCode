import colorsys


def show_benchcolor():
    benchRGB_str = ['ffffff', 'e79c19', '303070']
    benchRGB = list(
        map(lambda x: list(int(x[i:i+2], 16)/0xff for i in (0, 2, 4)), benchRGB_str))
    temp = [colorsys.rgb_to_hls(*k) for k in benchRGB]
    benchHLS = [tuple(round(c, 2) for c in hls) for hls in temp]
    print(benchHLS)
    approximate = [(0.0, 1.0, 0.0), (0.10, 0.50, 0.80), (2/3, 0.31, 0.4)]
    print(approximate)


def color_set(letter, con):
    h0 = (ord(letter)-ord('a'))/(ord('z')-ord('a'))
    hls_h = (h0-0.33, 0.90, 0.25)
    hls_f = (h0+0.33, 0.50, 0.80)
    hls_f = (h0+0.33, 0.55, 0.80)
    hls_b = (h0, 0.31, 0.4)
    con.hls_b = (h0, 0.31, 0.4)
    con.colorwordhilight = tuple(int(k*0xff)
                                 for k in colorsys.hls_to_rgb(*hls_h))
    con.colorword = tuple(int(k*0xff)
                          for k in colorsys.hls_to_rgb(*hls_f))
    con.colorbackground = tuple(int(k*0xff)
                                for k in colorsys.hls_to_rgb(*hls_b))


config = type('Config', (), {})
# ===============================

config.project_folder_name = 'bbddffggppttzzle'
config.regexp = ["/(.)\\1le$/","/[bdfgptz]{2}le$/"]

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

color_set(config.project_folder_name[0], config)
