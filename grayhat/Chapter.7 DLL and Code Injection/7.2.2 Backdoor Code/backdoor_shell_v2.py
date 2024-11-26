#  for  setblocking(0)
import socket
import time

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
    #  non blocking
    conn.setblocking(0)
    with conn:
        print('[*] connection from', remotehost, remoteport)
        try:
            while 1:
                buffer = ""
                print(f"[*] Received:         [", end=' ')
                while 1:
                    try:
                        recv_buffer = conn.recv(BUFSIZE)
                        print(f"+{len(recv_buffer)}", end=' ')
                        buffer += recv_buffer.decode()
                        if recv_buffer.endswith(b'>') :
                            break
                        else:
                            time.sleep(0.1)
                    except  Exception as e:
                        print(f"+0({e.errno})", end=' ')
                        # print(e)
                        time.sleep(0.1)
                        continue

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
    print("sdfsdfsdf")
exit()


# 2222222222222222222222222222222
import socket
import select

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the socket to non-blocking mode
server.setblocking(0)

# Bind the socket to an address (e.g., localhost on port 12345)
server_address = ('localhost', 12345)
try:
    server.bind(server_address)
except socket.error as e:
    print(f"Bind failed: {e}")
    exit(1)

# Start listening for incoming connections
server.listen(5)
print(f"Listening on {server_address}")

# List to keep track of socket objects to read from
inputs = [server]
outputs = []

# Main loop
while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:
        if s is server:
            # Handle the server socket
            client_socket, client_address = s.accept()
            print(f"Accepted connection from {client_address}")
            client_socket.setblocking(0)
            inputs.append(client_socket)
        else:
            # Handle all other sockets
            data = s.recv(1024)
            if data:
                print(f"Received {data} from {s.getpeername()}")
                # Echo the data back to the client
                s.sendall(data)
            else:
                print(f"No data from {s.getpeername()}, closing socket")
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

    for s in writable:
        # In this simple example, there's nothing to write
        pass

    for s in exceptional:
        print(f"Handling exceptional condition for {s.getpeername()}")
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()