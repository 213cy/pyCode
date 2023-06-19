import requests
from shutil import copyfileobj
from urllib.request import urlopen

url = 'http://flv4.people.com.cn/videofile3/pvmsvideo/2017/2/15' \
'/WeiQingCheng_cc06ea9b0474c6727ddd490bee2583cc.mp4'

local_filename = 'aaa.mp4'

# proxy = {'http': 'http://127.0.0.1:8590'}
# r = requests.get(url, proxies=proxy)
# r = requests.get(url, stream=True)

'''
with requests.get(url, stream=True) as r:
    with open(local_filename, 'wb') as f:
        print(r.headers.get('content-length'))
        for content in r:
            # print('==========', len(content))
            f.write(content)
print('done!')
raise SystemExit
'''

# ###################################################
'''
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=64*1024):
            # print('==========', len(chunk))
            f.write(chunk)
print('done!')
raise SystemExit
'''
# ###################################################


'''
with requests.get(url, stream=True) as r:
    with open(local_filename, 'wb') as f:
        copyfileobj(r.raw, f)
print('done!')
raise SystemExit
'''

# ###################################################


with urlopen(url) as fsrc, open(local_filename, 'wb') as fdst:
    copyfileobj(fsrc, fdst)