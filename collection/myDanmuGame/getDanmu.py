import random
import time
import socket
import struct
import asyncio
import websockets
import json
import zlib

class simDanmu():

    def __init__(self, *, dispInfoFcn=None):
        self.loopFlag = True
        self.index = 0
        self.disp = dispInfoFcn if dispInfoFcn else self.donothing
        ## self.danmuList = danmuList

    @staticmethod
    def donothing(*a,**b):
        pass

    def danmuCapture(self, danmuList):
        data = 0
        while self.loopFlag:
            self.index += 1

            da = random.random()
            data = round(data + da, 2)
            danmuList.append((self.index, data))

            self.disp(f'  >>>  put data= ( {self.index} : {data} )')

            time.sleep(1+da)

        print('simulate danmu thread done!')

    def stopLoop(self):
        self.loopFlag = False


class bilibiliDanmu():

    def __init__(self, roomid=24954721, *, dispInfoFcn=None):
        self.loopFlag = True
        self.disp = dispInfoFcn if dispInfoFcn else self.donothing
        self.uri = "ws://broadcastlv.chat.bilibili.com:2244/sub"
        self.uri2 = "wss://broadcastlv.chat.bilibili.com:2245/sub"
        self.body = f'{{"uid":0,"roomid":{roomid},"protover":1,"platform":"web","clientver":"1.4.0"}}'
        self.body2 = '{"uid":0,"roomid":24954721,"protover":1,"platform":"web","clientver":"1.4.0"}'
        self.heart = bytes.fromhex(
            '0000001f0010000100000002000000015b6f626a656374204f626a6563745d')

    @staticmethod
    def donothing(*a,**b):
        pass

    @staticmethod
    def pack(body, op):
        headerLen = 16
        ver = 0
        seq = 0
        packetLen = len(body) + headerLen
        buf = struct.pack('>ihhii', packetLen, headerLen, ver, op, seq)
        buf += body.encode()
        return buf

    @staticmethod
    def unpack(buf):
        finfo = struct.unpack('!ihhii', buf[0:16])
        ver = finfo[2]
        body = buf[16:]
        # print(f"[unpacked] {finfo}  len(body)={len(body)}")

        if ver == 0:
            bdict = json.loads(body.decode('utf-8'))
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
                for k in bilibiliDanmu.unpack(body[offset: offset+cmdSize]):
                    yield k
                offset += cmdSize
        else:
            pass
            # print(f'服务器收到心跳包的回复(ver=1,op=3),其他未知')

    async def heartBeat(self, websocket):
        # 长链的心跳包
        while self.loopFlag:
            await asyncio.sleep(30)
            # print(f"[heartBeat] {time.strftime('%X')} ")
            await websocket.send(self.heart)
        print("[------------EndHeart--------------]")

    async def recvLoop(self, websocket, danmuList):
        # 长链的接受循环
        while self.loopFlag:
            recvBuf = await websocket.recv()
            for k in self.unpack(recvBuf):
                if 'cmd' in k:
                    if k['cmd'] == 'DANMU_MSG':
                        self.disp('   <DANMU_MSG>   ',k['info'][2][1],':',k['info'][1] )
                        danmuList.append((k['info'][2][1], k['info'][1]))
                else:
                    print(f"[received] error : {k.keys()} ")
        print("[------------EndReceive--------------]")

    async def Bclient(self, danmuList):
        async with websockets.connect(self.uri) as websocket:
            print("[authorization] >>> ")
            await websocket.send(self.pack(self.body, 7))
            recvBuf = await websocket.recv()
            for k in self.unpack(recvBuf):
                print(f"[authorization] <<< {k}")

            await asyncio.gather(self.heartBeat(websocket), self.recvLoop(websocket, danmuList))

    def danmuCapture(self, danmuList):
        asyncio.run(self.Bclient(danmuList))

    def stopLoop(self):
        self.loopFlag = False


if __name__ == '__main__':
    a = []
    danmu = bilibiliDanmu(dispInfoFcn=print)
    danmu.danmuCapture(a)
