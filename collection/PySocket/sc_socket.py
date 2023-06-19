"""
Remote python server.
Execute Python commands remotely and send output back.
"""

import sys,os,io,time
from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR
import traceback
import subprocess
import psutil

PORT = 4127
BUFSIZE = 1024


#######################################################

def server():
    port = PORT
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    while True:
        conn, (remotehost, remoteport) = s.accept()
        with conn:
            print('connection from', remotehost, remoteport)
            while 1:
                request = conn.recv(BUFSIZE)
                # print(request.decode())
                reply = execute(request.decode())
                if not reply:
                    reply = '[no data out!]'
                conn.send(reply.encode())

def execute(request):
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = sys.stderr = fakefile = io.StringIO()
    try:
        try:
            a = exec(request, {}, {})
        except:
            print()
            traceback.print_exc(100)
            print()

    finally:
        sys.stderr = stderr
        sys.stdout = stdout
    return fakefile.getvalue()
#######################################################

def client():
    # sys.exit(2)
    host = '127.0.0.1'
    port = PORT

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host, port))

        command = input("type '!exit' to quit ==>")
        while command != '!exit':
            s.send(command.encode())
            
            reply = s.recv(BUFSIZE)
            print(reply.decode(), end='')

            command = input("type '!exit' to quit ==>")
            
        s.shutdown(SHUT_WR)
        
#######################################################
print('===================')
print(sys.prefix)
print(sys.executable)
filename = sys.argv[0].lower()
print(filename,'   pid =',os.getpid())
print('-------------------')

pd = {}
for prcs in psutil.process_iter():
    a = list( map(str.lower, prcs.cmdline()) )
    # print(prcs.pid ,a)
    if filename in a:
        pd[prcs.pid] = a.index(filename)
        print(prcs.pid,'---',os.getppid(),a)

if len(pd) == 0 or os.getpid() not in pd:
    print( 'in python idle,first run' )
    isFirst = True
elif len(pd) == 1:
    print( 'in cmd, first run' )
    isFirst = True
elif len(pd) == 2 and pd[os.getpid()] == 1 :
    print( 'form python idle,second run')
    isFirst = False
elif len(pd) == 3 and pd[os.getpid()] == 1 :
    print( 'form cmd,second run')
    isFirst = False

elif pd[os.getpid()] > 1:
    print('in VS debug,first run')
    isFirst = True
elif pd[os.getpid()] == 1:
    print( 'in VS debug,second run' )
    isFirst = False


# os.getppid()
# os.getpid() 
# prcs = psutil.Process(pid)
# prcs.cmdline()
# prcs.name() == 'python.exe':
# prcs.pid == pid
                
print('-------------------',pd)
# time.sleep(60)
# raise SystemExit

#######################################################

if not isFirst:
    print('server start!')
    server()
    raise SystemExit
else :
    a=subprocess.Popen(filename,shell=True,
    stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('new processes spawned !')
    # a.wait(10)
    # print(a.stdout.read().decode())

# time.sleep(2)
print('type some python commands :')
client()
a.kill()
print('closed client and server sockets ')
print(a.stdout.read().decode())


##    raise KeyboardInterrupt

