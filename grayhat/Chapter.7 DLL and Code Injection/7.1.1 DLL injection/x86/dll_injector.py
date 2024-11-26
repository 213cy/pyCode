
from ctypes import *
import x64_to_x86
import os

# kernel32 = windll.kernel32
kernel32 = WinDLL('kernel32', use_last_error=True)

# C:\Windows\SysWOW64\calc.exe
pid = 3888
dll_name = 'ghp_inject.dll'
dll_path = os.getcwd() + os.sep + dll_name
dll_path = os.path.dirname(__file__) + os.sep + dll_name
dll_len = len(dll_path)


str = "64bit version of " \
    "<OpenProcess,VirtualAllocEx,WriteProcessMemory,CreateRemoteThread> "\
    "all work well for 32bit process ?"
print("!!!", str, "!!!")

#  ===============================

# Define access rights

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
# Get a handle to the process we are injecting into.
h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if not h_process:
    raise WinError(get_last_error())


PAGE_READWRITE = 0x04
VIRTUAL_MEM = (0x1000 | 0x2000)
# Allocate some space for the DLL path
arg_address = kernel32.VirtualAllocEx(
    h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
print(f"{'arg_address':12}: 0x{arg_address:08x}")

# Write the DLL path into the allocated space
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address,
                            dll_path.encode(), dll_len, byref(written))

# Resolve the address for LoadLibraryA of 32bit
# h_kernel32 = kernel32.GetModuleHandleA(b"kernel32.dll")
h_kernel32_x86 = x64_to_x86.GetModuleHandle(h_process, "kernel32.dll")
print(f"{'h_kernel32_x86':12}: 0x{h_kernel32_x86:08x}")
# h_loadlib  = kernel32.GetProcAddress(h_kernel32,b"LoadLibraryA")
h_loadlib_x86 = x64_to_x86.GetProcAddress(
    h_process, h_kernel32_x86, "LoadLibraryA")
print(f"{'h_loadlib_x86':12}: 0x{h_loadlib_x86:08x}")
# h_loadlib_x86 = 0x776c49a7

# Now we try to create the remote thread, with the entry point set
# to LoadLibraryA and a pointer to the DLL path as it's single parameter
thread_id = c_ulong(0)
if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib_x86, arg_address, 0, byref(thread_id), 0):
    raise WinError(get_last_error())

print(f"created Remote thread PID : {thread_id.value}")
print("Reloading an already loaded DLL doesn't call its entry-point again .... ")

# ==========================
kernel32.CloseHandle(h_process)
