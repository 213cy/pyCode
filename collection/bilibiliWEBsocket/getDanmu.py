import asyncio
import websockets
import struct
import time
import zlib
import json


bodymir = {}

def pack(body, op, headerLen=16, ver=0, seq=0):
    # https://open-live.bilibili.com/document/doc&tool/api/websocket.html#_2-%E5%8F%91%E9%80%81%E5%BF%83%E8%B7%B3
    packetLen = len(body) + headerLen
    buf = struct.pack('>i', packetLen)
    buf += struct.pack('>h', headerLen)
    buf += struct.pack('>h', ver)
    buf += struct.pack('>i', op)
    buf += struct.pack('>i', seq)
    buf += body.encode()
    return buf


def unpack(buf):
    finfo = struct.unpack('!ihhii', buf[0:16])
    ver = finfo[2]
    body = buf[16:]
##    global bodymir
##    bodymir = body
    print(f"[unpacked] {finfo}  len(body)={len(body)}")

    if ver == 0:
        # 这里做回调
        bdict = json.loads( body.decode('utf-8') )
        yield bdict
    elif ver == 2:
        # 解压
        body = zlib.decompress(body)
        bodyLen = len(body)
        offset = 0
        while offset < bodyLen:
            cmdSize = struct.unpack('>i', body[offset:offset+4])[0]
            if offset + cmdSize > bodyLen:
                break
            for k in unpack(body[offset: offset+cmdSize]):
                yield k
            offset += cmdSize
    else:
        print(f'服务器收到心跳包的回复(ver=1,op=3),其他未知')


uri = "ws://broadcastlv.chat.bilibili.com:2244/sub"
uri = "wss://broadcastlv.chat.bilibili.com:2245/sub"
body = '{"uid":0,"roomid":24954721,"protover":1,"platform":"web","clientver":"1.4.0"}'
heart = bytes.fromhex(
    '0000001f0010000100000002000000015b6f626a656374204f626a6563745d')

MaxRecv = 22


async def heartBeat(websocket):
    # 长链的心跳包
    global MaxRecv
    while True:
        await asyncio.sleep(30)
        if MaxRecv < 1:
            break
        print(f"[heartBeat] {time.strftime('%X')} ")
        await websocket.send(heart)
    print("[------------EndHeart--------------]")


async def recvLoop(websocket):
    # 长链的接受循环
    global MaxRecv
    while MaxRecv:
        print(f"[------------{MaxRecv}--------------]")
        recvBuf = await websocket.recv()
        for k in unpack(recvBuf):
            if 'cmd' in k:
                print(f"[received] cmd = {k['cmd']} ")
                if k['cmd']=='DANMU_MSG':
                    print('   <DANMU_MSG>   ',k['info'][2][1],':',k['info'][1] )
            else:
                print(f"[received] error : {k.keys()} ")

        MaxRecv -= 1
    print("[------------EndReceive--------------]")


async def Bclient():
    async with websockets.connect(uri) as websocket:
        print("[authorization] >>> ")
        await websocket.send(pack(body, 7))
        recvBuf = await websocket.recv()
        for k in unpack(recvBuf):
            print(f"[authorization] <<< {k}")

        await asyncio.gather(heartBeat(websocket), recvLoop(websocket))


asyncio.run(Bclient())
