# from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR
import socket
import struct
import threading
import time


# {"host":"broadcastlv.chat.bilibili.com","port":2243,"wss_port":2245,"ws_port":2244}

HOST = 'broadcastlv.chat.bilibili.com'    # The remote host
PORT = 2244
requestws = f"GET ws://{HOST}:{PORT}/sub HTTP/1.1\r\n" \
    "Host: broadcastlv.chat.bilibili.com\r\n" \
    "Connection: Upgrade\r\n" \
    "Upgrade: websocket\r\n" \
    "Sec-WebSocket-Version: 13\r\n" \
    "Sec-WebSocket-Key: gcrOWYzxBhDt1672Tc2XVA==\r\n" \
    "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n\r\n"


requestws = "GET /sub HTTP/1.1\r\n" \
    "Host: broadcastlv.chat.bilibili.com:2244\r\n" \
    "Upgrade: websocket\r\n" \
    "Connection: Upgrade\r\n" \
    "Sec-WebSocket-Key: hc2txBTVHmGxe1/gtM42Tw==\r\n" \
    "Sec-WebSocket-Version: 13\r\n" \
    "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n\r\n"

# "User-Agent: Chrome/83.0.4103.106\r\n" \


# Sec-WebSocket-Accept = base64.b64encode(hashlib.sha1((Sec-WebSocket-Key + magic_string)).encode('utf-8')).digest())

#######################

body = '{"uid":0,"roomid":24954721,"protover":1,"platform":"web","clientver":"1.4.0"}'
header = [0, 0, 0, 16 + len(body), 0, 16, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1]
authFrame = bytes(header)+bytes(body, 'utf-8')


def composeWebsocketFrame(msg_bytes):
    # 这里仅仅需要由客户端向服务端发送一些很短的数据帧
    # 所以下面很多字段都直接写死了

    token = b'\x82'
    # bytes([0x80 | 0x2])
    # FIN=1表示当前数据帧为消息的最后一个数据帧
    # Opcode =0x2 表示这是一个二进制帧

    Mask = 0x80
    # 户端向服务端发送数据，存在掩码操作
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack('B', length+Mask)
    elif length <= 0xFFFF:
        token += struct.pack('!BH', 126+Mask, length)
    else:
        token += struct.pack('!BQ', 127+Mask, length)

    masking_key = bytes.fromhex('662cf5a5')
    # masking_key = bytes.fromhex( random.random().hex()[4:12] )
    bytes_list = bytearray()
    for i in range(len(msg_bytes)):
        chunk = msg_bytes[i] ^ masking_key[i % 4]
        bytes_list.append(chunk)

    msg_body = bytes(bytes_list)
    msg = token + masking_key + msg_body

    return msg


wshello = composeWebsocketFrame(authFrame)

# base64.b64encode(heart) = AAAAHwAQAAEAAAACAAAAAVtvYmplY3QgT2JqZWN0XQ==
# base64.b64decode('AAAAHwAQAAEAAAACAAAAAVtvYmplY3QgT2JqZWN0XQ==') = heart
# a = 0x0000001f0010000100000002000000015b6f626a656374204f626a6563745d
# b = int('0000001f0010000100000002000000015b6f626a656374204f626a6563745d', 16)
# a == b, hex(a)
heart = bytes.fromhex(
    '0000001f0010000100000002000000015b6f626a656374204f626a6563745d')
wsheart = bytes.fromhex(
    '829f662cf505662cf51a663cf504662cf507662cf5043d43976f034f8125294e9f600558a8')
# wsheart = bytes.fromhex( composeWebsocketFrame(heart).hex() )
# wsheart = composeWebsocketFrame(heart)
wspong = bytes.fromhex('8a80af762118')
# bin( a[0] & 0xf )  # 9(0b1001)=ping 10(0b1010)=pong

#######################

a = 22
maxBody = 2048
# b站示例代码中说这是 Payload data 的长度
# 这里除了载荷数据还应该加上ws头的长度,但是省略了
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(bytes(requestws, 'utf-8'))
    print(22*'-')
    data = s.recv(maxBody)
    print('<Switching Protocol>', data.decode())

    s.sendall(wshello)
    print(22*'-')
    data = s.recv(maxBody)
    print('<Authorization>', data[-10:].decode())

    tic = time.time()

    while a:
        print('----------', a, '----------')
        data = s.recv(maxBody)

        if data[0] & 0xf == 9:
            print(f"<pingFrame> b'\\x89\\x00' == {data} ")
            s.sendall(wspong)
        else:
            # print(type(data))
            fin = (data[0] & 0x80) >> 7
            # ,int( data[2:10].hex(), 16)
            bbb = data[1], int(data[2:4].hex(), 16)
            print(f"<wsReceived> FIN={ ('0 (未完','1 (最后')[fin] }分片) , "
                  f"Payload length={bbb} , len(data)={len(data)} ")

        toc = time.time()
        if toc-tic > 22:
            print(f"[heartBeat] {time.strftime('%X')} ")
            s.sendall(wsheart)
            tic = toc

        a -= 1


###########
# s=socket(AF_INET, SOCK_STREAM)
# s.connect(('broadcastlv.chat.bilibili.com',2243))
# s.send(b'aaaaaaaa')
# b = s.recv(2048)
# s.shutdown(SHUT_WR)
