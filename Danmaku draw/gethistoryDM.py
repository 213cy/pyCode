# https://member.bilibili.com/platform/inter-active/danmu:
# https://api.bilibili.com/x/v2/dm/search?oid=27141538375&type=1&keyword=&order=ctime&sort=desc&pn=1&ps=50&cp_filter=false


import requests
from parseosfile import parse_os_data
from cookie import cookies
from getVideoInfo import get_video_info

# "https://www.bilibili.com/video/BV1V4411Z7VA"
url = "https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=111098298&date=2024-11-28"
hs = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
      "cookie": cookies}
res = requests.get(url, headers=hs)
print(res.status_code, res.reason)
if len(res.text) < 100:
      raise Exception(res.text.split('"')[5])

data = parse_os_data(res.content)
sorted_data = sorted(data, key=lambda x: int(x[0]))
print("total entries :", len(sorted_data))
s = set()
sanitized_data = []
# for progress, midHash, ctime, content in sorted_data:
#       if midHash not in s:
#             s.add(midHash)
#             sanitized_data.append([progress, midHash, ctime, content])
for data_entry in sorted_data:
      if data_entry[1] not in s:
            s.add(data_entry[1])
            sanitized_data.append(data_entry)
print("logged entries :", len(sanitized_data))

url = "https://www.bilibili.com/video/BV1V4411Z7VA"
videoData = get_video_info(url)
witness_data = [videoData['duration'] * 1000,
                  videoData['owner']['mid'],
                  videoData['ctime'],
                  videoData['owner']['name'] + "_" +
                  videoData['title']+"_"+videoData['bvid']
                  ]
sanitized_data.append(witness_data)


import csv
with open('danmus.csv', 'w', encoding='utf_8_sig',newline='') as file:
      writer = csv.writer(file,delimiter=' ')
      writer.writerows(sanitized_data)
#     f.writelines([line+'\n' for line in danmus])

exit()
# res.encoding = 'utf-8'
fileinfo = {"drawingphase": '1',
            "videourl": url}


