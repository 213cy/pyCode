
import subprocess
from PIL import Image
from pagedir import Page

class Project:

    def __init__(self, config):
        self.root = config.project_path
        f = open(config.words_file, 'r', encoding="utf-8-sig")
        data = f.readlines()
        f.close()
        #   --------------------------
        block_list = []
        current_block = []

        for line in data:
            stripped_line = line.strip()
            if stripped_line:
                current_block.append(stripped_line.split(' ',2))
            elif current_block:
                block_list.append(current_block)
                current_block = []

        if current_block:
            block_list.append(current_block)
        #   --------------------------

        imagebackground = Image.open(config.background_file)
        self.pages = [Page(ind, val, imagebackground,config)
                      for ind, val in enumerate(block_list)]
        self.pageN = len(self.pages)



    def step_generate_frames(self):
        for k in self.pages:
            k.drawframes()

    def make_one_page_video(self, page):
        page.drawframes()
        page.set_audio_length()
        # print(page.timelength)
        page.make_word_video()
        page.make_page_video()

    def make_page_video(self):
        N = len(self.pages)
        for ind,pag in enumerate(self.pages):
            self.make_one_page_video(pag) 
            print(f"page {ind+1}/{N}")

    def make_final_video(self):
        commandstr = f"ffmpeg -hide_banner -loglevel warning -y "
        commandstr += f" -loop 1 -i background.png "
        commandstr += f" -f lavfi -t 1 -i anullsrc "
        commandstr += f" -pix_fmt yuv420p -c:v libx264 "
        commandstr += f" -shortest startpad.ts"

        results = subprocess.run(commandstr, # shell=True,
                                cwd=self.root, capture_output=True, text=True)
        res=results.stderr
        print(res if res else 'success .')

        str = "|".join([f"{page.folder}\output.ts" for page in self.pages])
        str = "startpad.ts|" + str
        commandstr = f"ffmpeg -i \"concat:{str}\" output.mp4 -y -loglevel warning"
        results = subprocess.run(commandstr, cwd=self.root,
                                 capture_output=True, text=True)
        res=results.stderr
        print(res if res else 'success .')

# ==============================

if __name__ == "__main__":
    from configuration import config

    maker = Project(config)
    # maker.pages[0].set_audio_length()
    # maker.make_one_page_video(maker.pages[4])
    # maker.make_one_page_video(maker.pages[7])

    # maker.make_page_video()
    maker.make_final_video()
    print("done !!!")
