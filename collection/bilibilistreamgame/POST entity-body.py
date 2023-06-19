## application/x-www-form-urlencoded and multipart/form-data
## http module and request module
## 四种常见的 POST 提交数据方式 https://juejin.cn/post/6996901713122852895

import http.client , urllib.parse
import time
import requests


######################################################################
## copy from   https://curlconverter.com/python/
## data for multipart/form-data  提交方式
######################################################################
cookies = {
    'buvid3': '155B0A80-A099-FA20-3389-6344D7C2711E95646infoc',
    '_uuid': '4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc',
    'buvid4': '2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D',
    'buvid_fp_plain': 'undefined',
    'DedeUserID': '95646000',
    'DedeUserID__ckMd5': '78ca4e2360d6e904',
    'hit-dyn-v2': '1',
    'LIVE_BUVID': 'AUTO3016520350052760',
    'nostalgia_conf': '2',
    'i-wanna-go-back': '-1',
    'b_ut': '5',
    'go_old_video': '1',
    'fingerprint3': '7ec4168cbbf9c55a0d62623a83075445',
    'fingerprint': 'e9193052b3bd91b249237ebd6ebe02e4',
    'is-2022-channel': '1',
    'blackside_state': '1',
    'CURRENT_BLACKGAP': '1',
    'b_nut': '100',
    'dy_spec_agreed': '1',
    'buvid_fp': 'e9193052b3bd91b249237ebd6ebe02e4',
    'hit-new-style-dyn': '0',
    'rpdid': "|(YYR|um|lu0J'uYY)l)YR~)",
    'AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg': '1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0',
    'CURRENT_FNVAL': '4048',
    'bp_article_offset_95646000': '741999349127446500',
    'CURRENT_QUALITY': '80',
    'bp_video_offset_95646000': '746967973455986700',
    'SESSDATA': '57b25f58%2C1688372109%2C79a78%2A11',
    'bili_jct': 'feecb819e20b7abf8df94b764275346a',
    'sid': '8t5zi0ff',
    '_dfcaptcha': 'a8d2d83f1b0b18b8e6a11dab7224a6e6',
    'b_lsid': '9B976C7E_1858157B706',
    'PVID': '7',
}

headers = {
    'authority': 'api.live.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryuUTl8ztsxciaTeTC',
    'accept': '*/*',
    'origin': 'https://live.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.bilibili.com/25566274',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': "buvid3=155B0A80-A099-FA20-3389-6344D7C2711E95646infoc; _uuid=4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc; buvid4=2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D; buvid_fp_plain=undefined; DedeUserID=95646000; DedeUserID__ckMd5=78ca4e2360d6e904; hit-dyn-v2=1; LIVE_BUVID=AUTO3016520350052760; nostalgia_conf=2; i-wanna-go-back=-1; b_ut=5; go_old_video=1; fingerprint3=7ec4168cbbf9c55a0d62623a83075445; fingerprint=e9193052b3bd91b249237ebd6ebe02e4; is-2022-channel=1; blackside_state=1; CURRENT_BLACKGAP=1; b_nut=100; dy_spec_agreed=1; buvid_fp=e9193052b3bd91b249237ebd6ebe02e4; hit-new-style-dyn=0; rpdid=|(YYR|um|lu0J'uYY)l)YR~); AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg=1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0; CURRENT_FNVAL=4048; bp_article_offset_95646000=741999349127446500; CURRENT_QUALITY=80; bp_video_offset_95646000=746967973455986700; SESSDATA=57b25f58%2C1688372109%2C79a78%2A11; bili_jct=feecb819e20b7abf8df94b764275346a; sid=8t5zi0ff; _dfcaptcha=a8d2d83f1b0b18b8e6a11dab7224a6e6; b_lsid=9B976C7E_1858157B706; PVID=7",
}

data = '------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="bubble"\r\n\r\n0\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="msg"\r\n\r\n456\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="color"\r\n\r\n16777215\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="mode"\r\n\r\n1\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="fontsize"\r\n\r\n25\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="rnd"\r\n\r\n1672913361\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="roomid"\r\n\r\n25566274\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="csrf"\r\n\r\nfeecb819e20b7abf8df94b764275346a\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC\r\nContent-Disposition: form-data; name="csrf_token"\r\n\r\nfeecb819e20b7abf8df94b764275346a\r\n------WebKitFormBoundaryuUTl8ztsxciaTeTC--\r\n'

######################################################################
## data for application/x-www-form-urlencoded  提交方式
######################################################################

##headers_c = headers.copy()
headers_c = {'cookie': repr(cookies)[2:-2].replace("': '",'=').replace("', '",'; ').replace('\': "','=').replace('", \'', '; ')   }

data_dict= dict(zip(data.split('"')[1::2], data.split('\r\n')[3::4]))
##data_dict_like = { "bubble": "0",
##"msg": "789987",
##"color": "16777215",
##"mode": "1",
##"fontsize": "25",
##"rnd": "1665390364",
##"roomid": "25566274",
##"csrf": "3e10a9621bbed1028f7bfbb09e88642f",
##"csrf_token": "3e10a9621bbed1028f7bfbb09e88642f"
##         }
data_url = urllib.parse.urlencode(data_dict)
data_url2= repr(data_dict)[2:-2].replace('\': \'','=').replace('\', \'','&')
assert data_url == data_url2


######################################################################
#                               使用 requests 包
## post 流程
##response = requests.post('https://api.live.bilibili.com/msg/send', cookies=cookies, headers=headers, data=data)
##print( response.text )
##
##raise SystemExit
######################################################################

'''

p1=data.find('msg')
p2=data[p1+8:p1+33].find('\r')
pre = data[0:p1+8]
pos = data[p1+8+p2:]


a= 56
b= 6
newdata  =f'{pre}{a} {b}{pos}'
 
response = requests.post('https://api.live.bilibili.com/msg/send', cookies=cookies, headers=headers, data=newdata)
print( response.text )

##raise SystemExit
'''


##response = requests.post('https://api.live.bilibili.com/msg/send', cookies=cookies, headers=headers_c, data=data_url)
##print( response.text )
##
##raise SystemExit



######################################################################
#                               使用 python 自带的 http 包
## post 流程
##params = urllib.parse.urlencode(data_dict)
##conn = http.client.HTTPSConnection( "api.bilibili.com" )
##conn = http.client.HTTPSConnection( 'api.live.bilibili.com' ,source_address=('192.168.0.10',59999))
##conn.request("POST", "/x/v2/dm/post" ,params, headers)

##conn = http.client.HTTPSConnection( "www.python.org" )
##conn.request("GET", "/")
######################################################################

'''    

##  multipart/form-data  提交方式


headers_c['content-type']=headers['content-type']
conn = http.client.HTTPSConnection( 'api.live.bilibili.com' )
conn.request("POST","/msg/send",data, headers_c)

'''

##  application/x-www-form-urlencoded  提交方式


headers_c['content-type']='application/x-www-form-urlencoded;charset=utf-8'

conn = http.client.HTTPSConnection( 'api.live.bilibili.com' )
conn.request("POST","/msg/send",data_url, headers_c)

##'''

####################

response = conn.getresponse()
print(response.length,9*' ', response.status,response.reason)

text = response.read()
print( eval(text) )

# conn.connect()
conn.close()

