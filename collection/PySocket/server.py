from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR

PORT = 4127
BUFSIZE = 1024
s = socket(AF_INET, SOCK_STREAM)
s.bind(('', PORT))

def aaa():
    s.listen(1)
    while True:
        conn, (remotehost, remoteport) = s.accept()
        with conn:
            print('connection from', remotehost, remoteport)
            while 1:
                conn.send(b'reply.encode()')
                print('aaaaaaaaaa')
                request = conn.recv(BUFSIZE)
                print(request)

		
aaa()
