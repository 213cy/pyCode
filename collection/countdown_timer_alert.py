import os
import time
import threading
import subprocess
import winsound


def aaa(hint_type=[1]):

    if 1 in hint_type:
        os.system(r'E:\Desktop\9991210.mp4')
    if 2 in hint_type:
        subprocess.run(["cmd", "/c", "dir"],
                       capture_output=True, text=True, check=True)
    if 3 in hint_type:
        subprocess.run(["E:\Desktop\9991210.mp4"],
                       capture_output=True, text=True, check=True,    shell=True)
    if 4 in hint_type:
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    if 5 in hint_type:
        winsound.PlaySound('C:\Windows\Media\Windows Print complete.wav',
                           winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        input()
        winsound.PlaySound(None, winsound.SND_PURGE)

time.sleep(1)
minutes = 0.1
task = threading.Timer(60*minutes, aaa)
task.start()
