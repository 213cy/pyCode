import re
import requests
from createnewxml import create_new_xml

def aaa():
    url = "https://www.bilibili.com/video/BV1V4411Z7VA"
    hs = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
    bvid = url.split('/')[4]
    res = requests.get(url, headers=hs)
    cid = re.findall(bvid+r'","cid":(.*?),', res.text)[0]
    print(cid)

    # cid = 111098298
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    url = f'https://comment.bilibili.com/{cid}.xml'
    res = requests.get(url, headers=hs)
    print(res.status_code,res.reason)
    res.encoding = 'utf-8'
    fileinfo = {"drawingphase": '1',
                "videourl": url}
    create_new_xml(res.text, fileinfo, "output.xml")


aaa()