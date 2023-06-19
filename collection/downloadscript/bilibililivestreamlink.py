# 获取哔哩哔哩直播的真实流媒体地址，默认获取直播间提供的最高画质
# https://github.com/wbt5/real-url/blob/master/douyu.py

import requests


header = { 'User-Agent': 'Mozilla/5.0 (iPod; CPU iPhone OS 14_5    like Mac OS X) AppleWebKit/605.1.15 (KHTML, ' 'like Gecko)    CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1', }

url = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo'

##room_id=24954721&protocol=0,1&format=0,1,2&codec=0,1&qn=10000&platform=web&ptype=8&dolby=5&panorama=1
# qn=150高清
# qn=250超清
# qn=400蓝光
# qn=10000原画
##r = input('请输入bilibili直播房间号：\n')
param = {
    'room_id': 24954721,
    'protocol': '0,1',
    'format': '0,1,2',
    'codec': '0,1',
    'qn': 10000, 
    'platform': 'h5',
    'ptype': 8,
}
res = requests.get(url, headers=header, params=param).json()
stream_info = res['data']['playurl_info']['playurl']['stream']

##raise SystemExit
        
stream_urls = []
# flv流无法播放，暂修改成获取hls格式的流，
for data in stream_info:
    format_name = data['format'][0]['format_name']
    if format_name == 'ts':
        base_url = data['format'][-1]['codec'][0]['base_url']
        url_info = data['format'][-1]['codec'][0]['url_info']
        for i, info in enumerate(url_info):
            host = info['host']
            extra = info['extra']
            stream_urls.append(f'{host}{base_url}{extra}')
        break
##return stream_urls

print(len(stream_urls))
print(stream_urls[0])
