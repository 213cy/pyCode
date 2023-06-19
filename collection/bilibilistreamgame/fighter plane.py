# 弹幕战机
# https://live.bilibili.com/26270342

import requests
import threading
##import time


######################################################################
# copy from   https://curlconverter.com/python/
# data for multipart/form-data  提交方式
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
    'hit-new-style-dyn': '0',
    'rpdid': "|(YYR|um|lu0J'uYY)l)YR~)",
    'AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg': '1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0',
    'nostalgia_conf': '2',
    'bp_article_offset_95646000': '748786634393124900',
    'CURRENT_FNVAL': '4048',
    'bp_video_offset_95646000': '764222858562896000',
    'SESSDATA': 'dc5c295f%2C1692383149%2Ca2372%2A21',
    'bili_jct': '5df687b3880acd9c8b037f45f43b7d0e',
    'buvid_fp': 'e9193052b3bd91b249237ebd6ebe02e4',
    'CURRENT_QUALITY': '64',
    'b_lsid': '45689B4D_1866D2D022D',
    'sid': '8qrfeskc',
    '_dfcaptcha': '4200396cb95f44a6fe8d8d45a00186ad',
    'PVID': '11',
}

headers = {
    'authority': 'api.live.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryiCxXUHs8ELJWkQW1',
    'accept': '*/*',
    'origin': 'https://live.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.bilibili.com/26270342',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': "buvid3=155B0A80-A099-FA20-3389-6344D7C2711E95646infoc; _uuid=4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc; buvid4=2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D; buvid_fp_plain=undefined; DedeUserID=95646000; DedeUserID__ckMd5=78ca4e2360d6e904; hit-dyn-v2=1; LIVE_BUVID=AUTO3016520350052760; i-wanna-go-back=-1; b_ut=5; go_old_video=1; fingerprint3=7ec4168cbbf9c55a0d62623a83075445; fingerprint=e9193052b3bd91b249237ebd6ebe02e4; is-2022-channel=1; blackside_state=1; CURRENT_BLACKGAP=1; b_nut=100; dy_spec_agreed=1; hit-new-style-dyn=0; rpdid=|(YYR|um|lu0J'uYY)l)YR~); AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg=1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0; nostalgia_conf=2; bp_article_offset_95646000=748786634393124900; CURRENT_FNVAL=4048; bp_video_offset_95646000=764222858562896000; SESSDATA=dc5c295f%2C1692383149%2Ca2372%2A21; bili_jct=5df687b3880acd9c8b037f45f43b7d0e; buvid_fp=e9193052b3bd91b249237ebd6ebe02e4; CURRENT_QUALITY=64; b_lsid=45689B4D_1866D2D022D; sid=8qrfeskc; _dfcaptcha=4200396cb95f44a6fe8d8d45a00186ad; PVID=11",
}

data = '------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="bubble"\r\n\r\n0\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="msg"\r\n\r\n456\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="color"\r\n\r\n16777215\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="mode"\r\n\r\n1\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="fontsize"\r\n\r\n25\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="rnd"\r\n\r\n1676869064\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="roomid"\r\n\r\n26270342\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="csrf"\r\n\r\n5df687b3880acd9c8b037f45f43b7d0e\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1\r\nContent-Disposition: form-data; name="csrf_token"\r\n\r\n5df687b3880acd9c8b037f45f43b7d0e\r\n------WebKitFormBoundaryiCxXUHs8ELJWkQW1--\r\n'

######################################################################

p1 = data.find('msg')
p2 = data[p1+8:p1+33].find('\r')
predata = data[0:p1+8]
postdata = data[p1+8+p2:]


def senddanmu(string):
##    return 999
    newdata = f'{predata}{string}{postdata}'
    try :
        response = requests.post('https://api.live.bilibili.com/msg/send',
                                 cookies=cookies, headers=headers,
                                 data=newdata.encode() ,
                                 timeout = 1)
        if int(response.headers['Content-Length']) < 555:
            print(response.text, end = ' ')
        return response.status_code
    except BaseException as e:
##        print(e)
        print( 'Read timed out', end=' ')
        return 0


######################################################################

##// 导弹=13s
##// 吃盾=20s
##// 撞机=开始=73s
##// 升级=30s
    
padval = 2.5 + 0.5 #
padval_boom_pre = 1.8
padval_boom_suf = 1.2


x = None
do_boom = False
circount_boom = 0

positions = [1, 10]
direction = 0

t=0
interval =0

def PlaneController():
    global t , x , interval
    global positions, direction
    global do_boom , circount_boom

    t += interval
    print(f'{round(t/60,2):05.2f}',end='  ')
    if x is not None :
        stat = senddanmu( x )
        print( f'x={x} [{stat:03}]')
        if stat != 0:
            x = None
            interval =2.6 
        else :           
            interval =padval
            
    
    elif do_boom:     
##        stat = senddanmu( '导弹' );        
        stat = senddanmu( '升级' );
##        stat = 888
        print( '导弹',f'[{stat:03}]')
        if stat != 0:
            do_boom = False
            interval = padval_boom_suf

    else :
        stat = senddanmu( positions[direction] );
        print( f'=>{positions[direction]:2} [{stat:03}]')
        if stat != 0:
            direction = 1-direction
            last_turn = t
            
            circount_boom += 1
            if circount_boom %33 == 2 : # %3 == 2
                do_boom = True
                interval = padval_boom_pre
            else:
                interval = padval


                        
    if t < 3600:
##        print(interval,circount_boom)
        threading.Timer(interval, PlaneController ) .start()
    else:
        print('done!' )

PlaneController()

##################################
raise SystemExit

x = None
next_turn = 0
next_act = 10
next_cmd = 1

##// 导弹=13s
##// 吃盾=20s
##// 撞机=24s
##// 升级=30s

a = 12
shieldtype = ['升级', '导弹', '导弹', '导弹', '导弹', '导弹', '导弹', '导弹']
shieldtime = [30+a, 13+a, 13+a, 13+a, 13+a, 13+a, 13+a, 13+a]
action = 0
N = len(shieldtime)
positions = [1, 10]
direction = 0

t=0
interval =1.3


def PlaneController():
    global t , x , interval
    global positions, direction
    global shieldtype , shieldtime , action , N
    global next_turn, next_act, next_cmd

    print(f'{round(t/60,2):05.2f}',end='  ')
    if type(x) is int :
        if next_cmd == 1:
            stat = senddanmu( x )
            print( f'>> {x:2} [{stat:03}]')
            if stat != 0:
                next_cmd -= 1
        else :
            print( '==',x )
            if next_cmd == 0:
                x = None
                next_cmd = 1
    else :
        if (t>next_act and ( shieldtype[action] != '导弹' or t < next_turn - 1 ) ):
            stat = senddanmu( shieldtype[action]  );
            print( '#',shieldtype[action],f'[{stat:03}]')
            if stat != 0:
                next_act = t + shieldtime[action]
                action = (action + 1) % N

        else :
            if (t>next_turn):
                stat = senddanmu( positions[direction] );
                print( f'=> {positions[direction]:2} [{stat:03}]')
                if stat != 0:
                    direction = 1-direction
                    next_turn = t + 2*interval + 0.1
            else :
                print( 'xxxxxxxxxxxx' )

    t += interval
    if t < 3600:
        threading.Timer(interval, PlaneController ) .start()
    else:
        print('done!' )

PlaneController()
