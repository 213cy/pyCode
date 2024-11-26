from ctypes import *
import time
import winsound 
import signal 

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    exit()
signal.signal(signal.SIGINT, handler)

msvcrt = cdll.msvcrt
counter = 0
buffer = c_char_p(b'AAAAAAA')
pid = windll.kernel32.GetCurrentProcessId()

while 1:
    msvcrt.printf(f"{pid} Loop iteration {counter}!\n".encode() )
    winsound.PlaySound('SystemHand',winsound.SND_ALIAS)
    time.sleep(2)
    counter += 1
    if counter == 9:
        msvcrt.strcpy(buffer, b"a"*99)