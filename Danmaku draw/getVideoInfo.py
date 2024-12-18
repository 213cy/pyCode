import re
import requests
import json


def get_video_info(url):
    hs = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
          }
    res = requests.get(url, headers=hs)
    searchObj = re.search(r'"videoData"', res.text)

    bvid = url.split('/')[4]
    cid = re.findall(bvid+r'","cid":(.*?),', res.text)[0]
    print(f'debug: bvid={bvid},cid={cid}')

    start_p = 0
    end_p = 0
    pointer = searchObj.span()[1]
    while True:
        pointer += 1
        char = res.text[pointer]
        if char == "{":
            start_p = pointer
            break
    deep = 1
    while True:
        pointer += 1
        char = res.text[pointer]
        if char == "{":
            deep += 1
        if char == "}":
            deep -= 1
            if deep == 0:
                end_p = pointer
                break

    videoData = json.loads(res.text[start_p:end_p+1])

    return videoData


if __name__ == "__main__":
    url = "https://www.bilibili.com/video/BV1V4411Z7VA"
    videoData = get_video_info(url)

    # cid = 111098298
    print(f"output: bvid={videoData['bvid']},cid={videoData['cid']}")

    author_data = [videoData['duration'] * 1000,
                   videoData['owner']['mid'],
                   videoData['ctime'],
                   videoData['owner']['name'] + "_" +
                   videoData['title']+"_"+videoData['bvid']
                   ]
    print(author_data)
