## 一个棋盘塔防游戏
## https://live.bilibili.com/25566274

import http.client
import time
from PIL import Image
##https://curlconverter.com/python/

cookies = {
    'buvid3': '155B0A80-A099-FA20-3389-6344D7C2711E95646infoc',
    '_uuid': '4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc',
    'rpdid': '|(~k|J|~YYu0J\'uYluJ|~lYk',
    'buvid4': '2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D',
    'buvid_fp_plain': 'undefined',
    'DedeUserID': '95646000',
    'DedeUserID__ckMd5': '78ca4e2360d6e904',
    'hit-dyn-v2': '1',
    'LIVE_BUVID': 'AUTO3016520350052760',
    'nostalgia_conf': '2',
    'i-wanna-go-back': '-1',
    'b_ut': '5',
    'CURRENT_FNVAL': '4048',
    'go_old_video': '1',
    'fingerprint3': '7ec4168cbbf9c55a0d62623a83075445',
    'fingerprint': 'e9193052b3bd91b249237ebd6ebe02e4',
    'is-2022-channel': '1',
    'blackside_state': '1',
    'CURRENT_BLACKGAP': '1',
    'buvid_fp': 'e9193052b3bd91b249237ebd6ebe02e4',
    'b_nut': '100',
    'dy_spec_agreed': '1',
    'CURRENT_QUALITY': '64',
    'bp_article_offset_95646000': '714648237146898472',
    'bp_video_offset_95646000': '716132616494907400',
    'SESSDATA': 'bc88dce8%2C1681128280%2C8211a%2Aa1',
    'bili_jct': '117c6a729e1e5fa79f907515fb67103c',
    'sid': '7h2nlz7l',
    '_dfcaptcha': '6ea1646f180883f1e8f377fa242a6cef',
    'PVID': '4',
    'b_lsid': 'E558D73C_183CD920748',
}


######################################################################

headers_c = {'cookie': repr(cookies)[2:-2].replace("': '",'=').replace("', '",'; ').replace('\': "','=').replace('", \'', '; ')        }
headers_c = {'cookie': "buvid3=155B0A80-A099-FA20-3389-6344D7C2711E95646infoc; _uuid=4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc; rpdid=|(~k|J|~YYu0J'uYluJ|~lYk; buvid4=2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D; buvid_fp_plain=undefined; DedeUserID=95646000; DedeUserID__ckMd5=78ca4e2360d6e904; hit-dyn-v2=1; LIVE_BUVID=AUTO3016520350052760; nostalgia_conf=2; i-wanna-go-back=-1; b_ut=5; CURRENT_FNVAL=4048; go_old_video=1; fingerprint3=7ec4168cbbf9c55a0d62623a83075445; fingerprint=e9193052b3bd91b249237ebd6ebe02e4; is-2022-channel=1; blackside_state=1; CURRENT_BLACKGAP=1; buvid_fp=e9193052b3bd91b249237ebd6ebe02e4; b_nut=100; dy_spec_agreed=1; CURRENT_QUALITY=64; SESSDATA=410e29e9%2C1681224478%2C5a0d7%2Aa1; bili_jct=ef525c2c1634d57d9f985d84a729b314; bp_video_offset_95646000=716751083211325400; bp_article_offset_95646000=716730725047468000; PVID=17; b_lsid=CC9E3ADE_183D6347A09"}
headers_c['content-type']='application/x-www-form-urlencoded;charset=utf-8'

data = { "bubble": "0",
         "color": "16777215",
         "mode": "1",
         "fontsize": "25",
         "rnd": "1665745588",
         "roomid": "25566274",
         "csrf": "ef525c2c1634d57d9f985d84a729b314",
         "csrf_token": "ef525c2c1634d57d9f985d84a729b314",
         "msg": "9999"
         }

params=repr(data)[2:-2].replace('\': \'','=').replace('\', \'','&')
pre = params[:params.find('9999')]

######################################################################
f = Image.open("Background.png")
im=f.convert ()
f.close()
block1 = [k+1 for k,p in enumerate( im.getdata(0) ) if p >100 ]
block2 = [k+1 for k,p in enumerate( im.getdata(1) ) if p >100 ]

##blocks = list(range(149,161))+list(range(317,329))+list(range(177,317,28))+list(range(188,328,28))\
##         +list(range(90,108))+list(range(370,388))+list(range(118,370,28))+list(range(135,387,28))\
##         +list(range(31,55))+list(range(423,447))+list(range(59,423,28))+list(range(82,446,28))
##
tower={2:block1,1:block2}
######################################################################
ind = 0
conn = http.client.HTTPSConnection( 'api.live.bilibili.com' )
for epoch in range(3):
        
    for k ,v in tower.items():
        count = len(v)
        ind = 0
        
        for n in range(count-1, -1, -1 ):

            loc = v[n]

            conn.request("POST","/msg/send",f'{pre}{loc} {k}', headers_c)

            response = conn.getresponse()
            print(response.length, 'bytes    ', response.status,response.reason,end='\t')
            info = eval( response.read() )
            print( f'code : {info["code"]}',end='\t')

            if info['code'] == 0  :
                v.remove(loc)
                ind +=1
                print( f'({epoch}: {ind}/{count})',end='\t')

            print(' .')
            time.sleep(1.2)    
####################

# conn.connect()
conn.close()

print(33*'=')
