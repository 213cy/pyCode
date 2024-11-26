import random
import os
import subprocess
import asyncio
import colorsys
import edge_tts

from PIL import Image, ImageDraw, ImageFont
from pagedir import Page


class Project:

    page_folder_header = "PAGE"
    VOICE = "en-GB-RyanNeural"
    ROOTPATH = "F:\\video"
    FONTFILENAME = "SourceHanSansSC-VF.ttf"
    FONTNAME_EN = "arial.ttf"
    # FONTNAME_EN = "F:\\video\\SourceHanSansSC-VF.ttf"
    # FONTNAME_ZH = "msyh.ttf"
    FONTNAME_ZH = "F:\\video\\SourceHanSansSC-VF.ttf"
    WIDTH = 1280
    HEIGHT = 720

    def __init__(self, path="F:\\video", titlekey="a", regexp="/^.?ang/"):

        # if not path :
        #     path = Project.ROOTPATH
        self.root = path
        self.regexp = regexp
        self.keyletter = titlekey
        letter = titlekey[0].lower()
        h0 = (ord(letter)-ord('a'))/(ord('z')-ord('a'))
        hls_h = (h0-0.33, 0.95, 0.05)
        hls_f = (h0+0.33, 0.50, 0.80)
        hls_f = (h0+0.33, 0.60, 0.75)
        self.hls_b = (h0, 0.31, 0.4)
        self.colorwordhilight = tuple(int(k*0xff)
                                      for k in colorsys.hls_to_rgb(*hls_h))
        self.colorword = tuple(int(k*0xff)
                               for k in colorsys.hls_to_rgb(*hls_f))
        self.colorbackground = tuple(int(k*0xff)
                                     for k in colorsys.hls_to_rgb(*self.hls_b))

        imagepath = f"{path}/background.png"
        self.filebackground = imagepath
        if os.path.exists(imagepath):
            self.imagebackground = Image.open(imagepath)
        else:
            self.init_background_image()

        f = open(f"{path}\words.txt", 'r', encoding="utf-8-sig")
        data = f.readlines()
        f.close()

        wordslist = [[]]
        ind = 0
        for k in data:
            if k != '\n':
                wordslist[ind].append(k.strip())
            elif len(wordslist[ind]) != 0:
                wordslist.append([])
                ind += 1

        self.pages = [Page(ind, val, self)
                      for ind, val in enumerate(wordslist)]
        self.pageN = len(self.pages)

    def show_benchcolor(self):
        benchRGB_str = ['ffffff', 'e79c19', '303070']
        benchRGB = list(
            map(lambda x: list(int(x[i:i+2], 16)/0xff for i in (0, 2, 4)), benchRGB_str))
        temp = [colorsys.rgb_to_hls(*k) for k in benchRGB]
        benchHLS = [tuple(round(c, 2) for c in hls) for hls in temp]
        aa = [(0.0, 1.0, 0.0), (0.10, 0.50, 0.80), (2/3, 0.31, 0.4)]
        print(aa, '\n', benchHLS)

    def init_background_image(self):
        w = self.WIDTH
        h = self.HEIGHT
        hls_b = self.hls_b
        img = Image.new('RGB', (w, h), self.colorbackground)
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

        self.filebackgroundimage = img
        img.show()
        img.save(self.filebackground)

    def make_cover_image(self):
        img = self.imagebackground.copy()
        Idrawer = ImageDraw.Draw(img)

        yy = 720
        xx = 1280/2

        font = ImageFont.truetype(self.FONTNAME_EN, size=250)
        Idrawer.text((xx, yy/3), self.regexp,
                     anchor="mm", font=font,
                     stroke_width=1, fill=self.colorword)
        # font = ImageFont.truetype(self.FONTNAME_EN, size=28)
        font = ImageFont.truetype(f"{self.root}/"+self.FONTFILENAME, size=28)
        words = [word for page in self.pages for word in page.words]
        wordline = ['    '.join(words[ind:ind+8])
                    for ind in range(0, int(len(words)), 8)]
        Idrawer.text((xx, yy*3/4), '\n'.join(wordline),
                     align="center",
                     anchor="mm", font=font,
                     stroke_width=1, fill=self.colorword)
    
        img.show()
        img.save(f"{self.root}/cover.png")

    async def amain(self) -> None:
        # tasks = [item for page in self.pages for item in page.tasks]
        tasks = [edge_tts.Communicate(word, self.VOICE).save(
            f"{page.folder}/{word}.mp3") for page in self.pages for word in page.words]
        await asyncio.gather(*tasks)

    def download(self):
        asyncio.run(self.amain())

    def step_generateimages(self):
        for k in self.pages:
            k.drawframes()

    def make_one_page_video(self, page):
        page.drawframes()
        page.set_audio_length()
        # print(page.timelength)
        page.make_word_video()
        page.make_page_video()

    def make_page_video(self):
        (self.make_one_page_video(pag) for pag in self.pages)

    def make_page_video(self):
        str = "|".join([f"{page.folder}\output.ts" for page in self.pages])
        commandstr = f"ffmpeg -i \"concat:{str}\" output.mp4 -y -loglevel warning"
        results = subprocess.run(commandstr, cwd=self.root,
                                 shell=True, capture_output=True, text=True)
# ==============================


maker = Project(titlekey="a")
# maker.download()
# maker.make_one_page_video(maker.pages[6])
# maker.make_one_page_video(maker.pages[7])
maker.make_cover_image()
# maker.make_page_video()
print("done !!!")
