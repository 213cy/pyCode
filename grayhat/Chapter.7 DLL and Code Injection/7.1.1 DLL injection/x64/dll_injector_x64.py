import os
from ctypes import *
import subprocess
import time

# kernel32 = windll.kernel32
kernel32 = WinDLL('kernel32', use_last_error=True)

new_process_file = 'C:\Windows\SysWOW64\calc.exe'
new_process_file = 'C:\Windows\System32\calc.exe'
subpp = subprocess.Popen(new_process_file)
pid = subpp.pid

dll_name = 'ghp_inject.dll'
dll_name = 'injectdll.dll'
dll_path = os.getcwd() + os.sep + dll_name
dll_path = os.path.dirname(__file__) + os.sep + dll_name
dll_len = len(dll_path)


str = "64bit"
print("!!!", str, "!!!")

time.sleep(2)
#  ===============================

# Open the process
# PROCESS_QUERY_INFORMATION = 0x0400
# PROCESS_VM_READ           = 0x0010
# hProcess = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
# Define access rights / Get a handle to the process we are injecting into.
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if not h_process:
    raise WinError(get_last_error())


PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40
VIRTUAL_MEM = (0x1000 | 0x2000)
# Allocate some space for the DLL path
kernel32.VirtualAllocEx.restype = c_void_p
arg_address = kernel32.VirtualAllocEx(
    h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
print(f"{'arg_address':30}: {arg_address:#016x}")

# Write the DLL path into the allocated space
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address,
                            dll_path.encode(), dll_len, byref(written))

# ==================================

# Resolve the address for LoadLibraryA of 64bit
kernel32.GetModuleHandleA.restype = c_void_p
kernel32.GetProcAddress.restype = c_void_p


dll_handle = kernel32.GetModuleHandleA(b"KERNELBASE.dll")
print(f"{'dll_handle (KERNELBASE.dll)':30}: {dll_handle:#016x}")
fun_address = kernel32.GetProcAddress(c_void_p(dll_handle), b"Beep")
print(f"{'fun_address (Beep)':30}: {fun_address:#016x}")

dll_handle = kernel32.GetModuleHandleA(b"kernel32.dll")
print(f"{'dll_handle (kernel32.dll)':30}: {dll_handle:#016x}")
fun_address = kernel32.GetProcAddress(c_void_p(dll_handle), b"LoadLibraryA")
print(f"{'fun_address (LoadLibraryA)':30}: {fun_address:#016x}")

# ==================================

# Now we try to create the remote thread, with the entry point set
# to LoadLibraryA and a pointer to the DLL path as it's single parameter
thread_id = c_ulong(0)
if not kernel32.CreateRemoteThread(h_process, None, 0, c_void_p(fun_address), arg_address, 0, byref(thread_id)):
    raise WinError(get_last_error())

kernel32.CloseHandle(h_process)
print(f"    created Remote thread PID : {thread_id.value}")
