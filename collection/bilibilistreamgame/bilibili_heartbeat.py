import requests
import time

# copy from   https://curlconverter.com/python/
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
    'SESSDATA': 'f30ccf89%2C1688475275%2Cc1b5e%2A11',
    'bili_jct': '32797655001318b52f8ff57061311d9e',
    'b_lsid': '1ED17B7B_18585BDCC44',
    '_dfcaptcha': '1eb5b02a40e5b120e297bdd7f5d1dd81',
    'PVID': '4',
}

headers = {
    # 'authority': 'live-trace.bilibili.com',
    # 'authority': 'api.live.bilibili.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://live.bilibili.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://live.bilibili.com/26270342',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': "buvid3=155B0A80-A099-FA20-3389-6344D7C2711E95646infoc; _uuid=4C31FA9F-C88F-36110-B910E-BA9247C7995345452infoc; buvid4=2A0DB74D-647F-C445-725E-19AC482663B562971-022043016-grEc33TlGpC8bl1t9DXZGg%3D%3D; buvid_fp_plain=undefined; DedeUserID=95646000; DedeUserID__ckMd5=78ca4e2360d6e904; hit-dyn-v2=1; LIVE_BUVID=AUTO3016520350052760; nostalgia_conf=2; i-wanna-go-back=-1; b_ut=5; go_old_video=1; fingerprint3=7ec4168cbbf9c55a0d62623a83075445; fingerprint=e9193052b3bd91b249237ebd6ebe02e4; is-2022-channel=1; blackside_state=1; CURRENT_BLACKGAP=1; b_nut=100; dy_spec_agreed=1; buvid_fp=e9193052b3bd91b249237ebd6ebe02e4; hit-new-style-dyn=0; rpdid=|(YYR|um|lu0J'uYY)l)YR~); AMCV_98CF678254E93B1B0A4C98A5%40AdobeOrg=1176715910%7CMCMID%7C35130866472924013203684883487680602469%7CMCAAMLH-1669468857%7C11%7CMCAAMB-1669468857%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1668871258s%7CNONE%7CvVersion%7C5.4.0; CURRENT_FNVAL=4048; bp_article_offset_95646000=741999349127446500; CURRENT_QUALITY=80; bp_video_offset_95646000=746967973455986700; SESSDATA=f30ccf89%2C1688475275%2Cc1b5e%2A11; bili_jct=32797655001318b52f8ff57061311d9e; b_lsid=1ED17B7B_18585BDCC44; _dfcaptcha=1eb5b02a40e5b120e297bdd7f5d1dd81; PVID=4",
}

params = {
    'hb': 'NjB8MjYyNzAzNDJ8MXww',
    'pf': 'web',
}

######################################################
MaxRecv = 9

while MaxRecv > 0:

    response = requests.get(
        'https://live-trace.bilibili.com/xlive/rdata-interface/v1/heartbeat/webHeartBeat',
        params=params, cookies=cookies, headers=headers, )
    print(f"[rdata] {time.strftime('%X')} " , response.text )

    time.sleep(50) 

    response = requests.get(
        'https://live-trace.bilibili.com/xlive/rdata-interface/v1/heartbeat/webHeartBeat',
        params=params, cookies=cookies, headers=headers, )
    print(f"[rdata] {time.strftime('%X')} " , response.text )

    time.sleep(25) 

    response = requests.get('https://api.live.bilibili.com/relation/v1/Feed/heartBeat',
                                    cookies=cookies,
                                    headers=headers)
    print(f"[relation] {time.strftime('%X')} ", response.text )

    time.sleep(25)
