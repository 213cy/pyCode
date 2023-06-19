# Singleton process and 
# Non-Blocking receive from stdin (no way for now)

import subprocess
import sys,os,io
import time

from win32api import CloseHandle,GetLastError
from win32event import CreateMutex,WaitForSingleObject

hMutex =CreateMutex(None, False ,'ZZZ')
doServer = WaitForSingleObject(hMutex,200)

if doServer: # True: # 
    ##reader = io.open(sys.stdin.fileno())
    ##os.fdopen()

    # buf = io.StringIO()
    # oldin = sys.stdin
    # sys.stdin = buf
    
    buf = sys.stdin
    a=15
    while a>0:
        # r=buf.readline()  # 阻塞在这
        print('dfsdf')
        r=buf.read(1)  # 阻塞在这
    ##    if len(r)>0:
        print(a,'>',r,'<',sep='') # ,end=' '
        a -=1
        time.sleep(1)
else:
    filename = sys.argv[0].lower()
    proc=subprocess.Popen(['python',filename],shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    print('new processes  spawned !')
##    raise SystemExit
    # a.wait(10)

    # time.sleep(3)
    line = '---'
    aa = 'readline 在idle中运行不正确',
    bb = 'communicate 在什么情况下都不好使'
    while proc.poll() is None: 
        # line = proc.stdout.readline()
        aa,bb = proc.communicate(input=b'input\n', timeout=3)
        # aa,bb = proc.communicate()
        # proc.stdout.flush() # 刷新缓存，防止缓存过多造成卡死 #
        # line = line.decode("utf8") 
        print(line,aa,bb)

    print('++++++++')
    print(proc.stdout.read().decode())
    print('++++++++')
    print(proc.stdout.read().decode())
    print('++++++++')


    # raise SystemExit
##    raise KeyboardInterrupt


CloseHandle(hMutex)


#########################




