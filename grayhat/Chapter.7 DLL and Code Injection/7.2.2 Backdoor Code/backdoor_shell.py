import socket

BUFSIZE = 4096

host = "192.168.1.55"
host = "127.0.0.1"
port = 4444
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
print("[*] Server bound to %s:%d" % (host, port))
server.listen(5)

while True:
    print('[*] waiting for connecting ... ')
    conn, (remotehost, remoteport) = server.accept()
    with conn:
        print('[*] connection from', remotehost, remoteport)
        try:
            while 1:
                buffer = ""
                print(f"[*] Received:         [", end=' ')
                while 1:
                    recv_buffer = conn.recv(BUFSIZE)
                    print(f"+", end=' ')
                    buffer += recv_buffer.decode()
                    if len(recv_buffer) < BUFSIZE:
                        break
                    elif recv_buffer[-1] != b'\n':
                        break

                print(']')
                print( buffer)
                print(f"[*] ---------------------")

                # We've received everything, now it's time to send some input
                command = input("Enter Command> ")
                conn.sendall(command.encode() + b"\r\n")
                print(f"[*] Sent => {command}")
        except Exception as e:
            print()
            print("[exception]", e)
            continue
        except KeyboardInterrupt as e:
            print()
            print("[exception]", e)
            exit()

