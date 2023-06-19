# copy /b *.ts aa.ts

import multiprocessing
from shutil import copyfileobj
from urllib.request import urlopen
import time

url = 'https://ee-h.hncdn.com/hls/videos/202108/27/393679371/'\
        ',480P_2000K,_393679371.mp4.urlset/seg-5-v1-a1.ts?'\
        'validfrom=1682697557&validto=1682704757&ipa=216.218.223.57'\
        '&hdl=-1&hash=k4g%2Fmhf18qh5daDTOk%2BWT%2FPF20k%3D&&'
urlpre, urlfix = url.split('seg-5')


def download(index):
    url = urlpre + f'seg-{index}' + urlfix
    filename = f'ts/{index:03}.ts'

    # print(filename)
    # time.sleep(2)
    # print(len(urlpre))

    # with urlopen(url) as fsrc, open(filename, 'wb') as fdst:
    #     copyfileobj(fsrc, fdst)


print('load module...')
if __name__ == '__main__':
    # rOut = multiprocessing.Value(ctypes.c_char_p,'bb')
    ran = range(17, 21)
    pList = [multiprocessing.Process(target=download, args=(k, )) for k in ran]
    [p.start() for p in pList]
    [p.join() for p in pList]
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
