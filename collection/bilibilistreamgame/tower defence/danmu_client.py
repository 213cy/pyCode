import requests
import random

# 棋盘塔防游戏
# https://live.bilibili.com/25566274
# https://live.bilibili.com/5520542
# -----------------------------------------------
# copy from   https://curlconverter.com/python/
# data for multipart/form-data  提交方式

##a=document.cookie
##a.replace(/ /g, '"\n"')
#################################################

a=("buvid3=155B0A80-A099-FA20-3389-6344D7C2711E95646infoc;"
"_uuid=4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc;"
"buvid4=2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D;"
"buvid_fp_plain=undefined;"
"DedeUserID=95646000;"
"DedeUserID__ckMd5=78ca4e2360d6e904;"
"hit-dyn-v2=1;"
"LIVE_BUVID=AUTO3016520350052760;"
"i-wanna-go-back=-1;"
"b_ut=5;"
"go_old_video=1;"
"fingerprint3=7ec4168cbbf9c55a0d62623a83075445;"
"fingerprint=e9193052b3bd91b249237ebd6ebe02e4;"
"is-2022-channel=1;"
"blackside_state=1;"
"CURRENT_BLACKGAP=1;"
"b_nut=100;"
"dy_spec_agreed=1;"
"hit-new-style-dyn=0;"
"rpdid=|(YYR|um|lu0J'uYY)l)YR~);"
"AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg=1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0;"
"nostalgia_conf=2;"
"CURRENT_FNVAL=4048;"
"buvid_fp=e9193052b3bd91b249237ebd6ebe02e4;"
"bp_article_offset_95646000=771342930792153100;"
"header_theme_version=CLOSE;"
"home_feed_column=4;"
"CURRENT_QUALITY=16;"
"bili_jct=95beb5cdc49770a1e30fc5d200f41d52;"
"sid=7o82v22l;"
"bp_video_offset_95646000=774641504305020900;"
"GIFT_BLOCK_COOKIE=GIFT_BLOCK_COOKIE;"
"PVID=6;"
"b_lsid=10E654557_186F8890DF8;"
"_dfcaptcha=967d521f02db3761960d307e1461179f;"
"SESSDATA=72d02bb5%2C1694699192%2Cb7372%2A31"   
)
b=a.replace(' ','').split(';')
cookies=dict(map(lambda x :x.split('='),b))

fn = 'aaa.txt'
fp = open(fn, 'r')
aa=fp.read()
fp.close()
bb=aa.split('\'cookie: ')[1].split('\' ')[0]
c=bb.split('; ')
cookies=dict(map(lambda x :x.split('='),c))
######################################################################

headers = {
    'authority': 'api.live.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Chrome/83.0.4103.106',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryXi2AWjbZP81iKxoi',
    'accept': '*/*',
    'origin': 'https://live.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.bilibili.com/5520542',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'}

d = ['',
 '\r\nContent-Disposition: form-data; name="bubble"\r\n\r\n0\r\n',
 '\r\nContent-Disposition: form-data; name="msg"\r\n\r\nAAAAAAAAAAAA\r\n',
 '\r\nContent-Disposition: form-data; name="color"\r\n\r\n16777215\r\n',
 '\r\nContent-Disposition: form-data; name="mode"\r\n\r\n1\r\n',
 '\r\nContent-Disposition: form-data; name="fontsize"\r\n\r\n25\r\n',
 '\r\nContent-Disposition: form-data; name="rnd"\r\n\r\n1677829055\r\n',
 '\r\nContent-Disposition: form-data; name="roomid"\r\n\r\n5520542\r\n',
 '\r\nContent-Disposition: form-data; name="csrf"\r\n\r\nFFFFFFFFFFFFF\r\n',
 '\r\nContent-Disposition: form-data; name="csrf_token"\r\n\r\nFFFFFFFFFFFFF\r\n',
 '--\r\n']

sep = '--'+headers['content-type'].split('=')[-1]
da=sep.join(d)
data = cookies['bili_jct'].join( da.split('FFFFFFFFFFFFF') )
##  data = da.replace( 'FFFFFFFFFFFFF' ,cookies['bili_jct'])
predata , postdata = data.split('AAAAAAAAAAAA')


##p1 = data.find('msg')
##p2 = data[p1+8:p1+33].find('\r')
##predata = data[0:p1+8]
##postdata = data[p1+8+p2:]

######################################################################

def danmu_send(string):
    newdata = f'{predata}{string}{postdata}'
    try :
        response = requests.post('https://api.live.bilibili.com/msg/send',
                                 cookies=cookies, headers=headers,
                                 data=newdata.encode() ,
                                 timeout = 1)
        if int(response.headers['Content-Length']) < 555:
            a=response.text
            print(a)
            return a[26:30]
        return response.status_code
    except BaseException as e:
##        print(e)
        print( 'TimeoutError !')
        return 'err'

def danmu_send_test(string):
    return random.choice([200,200,100])

######################################################################

def diff_dict(a,b):
    samekey =set( filter(lambda x: a[x]==b[x], set(a) & set(b)) )
    diffkey = set(a) - samekey
    print(diffkey)
##    {'SESSDATA', 'bili_jct', 'sid', '_dfcaptcha', 'b_lsid', 'bp_video_offset_95646000', 'PVID'}
##    for k in diffkey : print(k,a[k],b[k])
##>>> diff_dict(cook,cookies)
##{'bili_jct', 'CURRENT_QUALITY', 'PVID', 'b_lsid', 'SESSDATA', 'sid', '_dfcaptcha'}
##>>> diff_dict(cookies,cook)
##{'GIFT_BLOCK_COOKIE', 'bili_jct', 'CURRENT_QUALITY', 'PVID', 'b_lsid'}
##diff_dict(cookies,cookies2)
