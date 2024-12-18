
from PIL import Image, ImageDraw, ImageFont
import subprocess
from concurrent.futures import ThreadPoolExecutor


class Page:
    def __init__(self, ind, lines_list, backimage, config):
        self.index = ind
        self.lines = lines_list
        self.backimage = backimage
        self.config = config

        page_folder = f"{config.project_path}/{config.page_folder_prefix}{ind:02d}"
        # if not os.path.exists(page_folder):
        #     os.makedirs(page_folder)
        self.folder = page_folder

        self.wordN = len(lines_list)
        self.words = [k[0] for k in lines_list]
        self.phone = [k[1] for k in lines_list]
        self.fores = [f"{k} {j} - " for k, j in zip(self.words, self.phone)]
        rears = [k[2].strip().split('#') for k in lines_list]
        self.rears = [k[0] for k in rears]
        self.images = [k[1:] for k in rears]

        [size_en, size_zh] = self.pre_set_line_width()
        self.lineHeight = round(size_en * 10/8)
        self.font_en = ImageFont.truetype(config.FONTNAME_EN, size=size_en)
        self.font_zh = ImageFont.truetype(config.FONTNAME_ZH, size=size_zh)
        self.y0 = (720 - self.wordN * self.lineHeight + self.lineHeight)/2
        maxlinewidth = self.get_max_line_width()
        self.x0 = round((1280 - maxlinewidth) / 2)

    def pre_set_line_width(self):
        font_en = ImageFont.truetype(self.config.FONTNAME_EN, size=80)
        font_zh = ImageFont.truetype(self.config.FONTNAME_ZH, size=70)
        imdrawer = ImageDraw.Draw(self.backimage)
        forewidths = [imdrawer.textlength(line, font_en)
                      for line in self.fores]
        rearwidths = [imdrawer.textlength(line, font_zh)
                      for line in self.rears]
        imagewidths = [65*len(line) for line in self.images]
        w = [a+b+c for a, b, c
             in zip(forewidths, rearwidths, imagewidths)]
        # suppose character height + line spacing = 80 + 40 = 90 ~ 120
        # 720 / 120 * 0.8 = 4.8 ~= 5.5
        # 720 / 100 * 0.8 = 5.67 ~= 5.5
        # 720 / 90 * 0.8 = 6.4 ~= 5.5
        # max(h) = (80+20)*wordN => 720*0.xxx / h => 5.5/wordN
        c = min(1280*0.8 / max(w), 5.5/self.wordN)
        return (int(80*c), int(70*c))

    def get_max_line_width(self):
        imdrawer = ImageDraw.Draw(self.backimage)
        self.forewidths = [imdrawer.textlength(line, self.font_en)
                           for line in self.fores]
        self.rearwidths = [imdrawer.textlength(line, self.font_zh)
                           for line in self.rears]
        imagewidths = [65*len(line) for line in self.images]
        w = [a+b+c for a, b, c
             in zip(self.forewidths, self.rearwidths, imagewidths)]
        return max(w)

    def set_audio_length(self):
        # result = subprocess.run(
        #     "dir", shell=True, capture_output=True, text=True)
        # print(result.stdout)
        commandstr = f"ffprobe -v error -i {{0}}.mp3 "
        commandstr += "-show_entries format=duration -of default=noprint_wrappers=1:nokey=1"

        def command(x): return subprocess.run(commandstr.format(x),
                                              cwd=self.folder,  # shell=True,
                                              capture_output=True, text=True)

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(command, self.words))

        # print(type(results[1].stdout), results[1].stdout)
        self.timelength = [float(res.stdout)+1.600 for res in results]

    def make_word_video(self):
        commandstr = f"ffmpeg -hide_banner -loglevel warning -y "
        commandstr += f" -loop 1 -i {{0}}.png -i {{0}}.mp3 "
        commandstr += f" -pix_fmt yuv420p -c:v libx264 -af apad -shortest "
        commandstr += f" -t {{1:.3f}} {{2:02d}}.ts"

        def command(x, y, z): return subprocess.run(commandstr.format(x, y, z),
                                                    cwd=self.folder,  # shell=True,
                                                    capture_output=True, text=True)

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(command, self.words,
                           self.timelength, list(range(self.wordN))))

    def make_page_video(self):
        str = "|".join([f"{k:02d}.ts" for k in range(self.wordN)])
        commandstr = f"ffmpeg -i \"concat:{str}|{str}\" -c copy output.ts -y  -loglevel warning"
        results = subprocess.run(commandstr, cwd=self.folder,  # shell=True,
                                 capture_output=True, text=True)
        res=results.stderr
        print(res if res else 'success .')

    def drawframes(self):
        for indline in range(self.wordN):
            img = self.backimage.copy()
            Idrawer = ImageDraw.Draw(img)

            for ind in range(self.wordN):
                yy = self.y0+ind*self.lineHeight
                if ind == indline:
                    Idrawer.text((self.x0, yy),
                                 self.fores[ind], anchor="lm", font=self.font_en,
                                 stroke_width=2, fill=self.config.colorwordhilight)
                    Idrawer.text((self.x0 + self.forewidths[ind], yy),
                                 self.rears[ind], anchor="lm", font=self.font_zh,
                                 stroke_width=1, fill=self.config.colorwordhilight)
                else:
                    Idrawer.text((self.x0, yy),
                                 self.fores[ind], anchor="lm", font=self.font_en,
                                 stroke_width=1, fill=self.config.colorword)
                    Idrawer.text((self.x0 + self.forewidths[ind], yy),
                                 self.rears[ind], anchor="lm", font=self.font_zh,
                                 stroke_width=1, fill=self.config.colorword)

                for i, f in enumerate(self.images[ind]):
                    img_source = Image.open(f"{self.config.root}/{f}")
                    xx = self.x0 + self.forewidths[ind] + \
                        self.rearwidths[ind] + i * 84 + 20
                    img.paste(img_source, (int(xx), int(yy-32)))
            # Save the edited image
            img.save(f"{self.folder}/{self.words[indline]}.png")

    def showimage(self, ind):
        image = Image.open(f"{self.folder}/{self.words[ind]}.png")
        image.show()

    def pasteimage(self, imagefile):
        img_source = Image.open(imagefile)
        for ind in range(self.wordN):
            img_dest = Image.open(f"{self.folder}/{self.words[ind]}.png")
            img_dest.paste(img_source, (300, 300))
            img_dest.save(f"{self.folder}/{self.words[ind]}.png")
