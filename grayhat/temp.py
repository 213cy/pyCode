from ctypes import *
from ctypes import wintypes
from my_debugger_defines import *

# Load the kernel32 library
kernel32 = WinDLL('kernel32', use_last_error=True)

kernel32= windll.kernel32


# ++++++++++++++++++++++++++++


# system_info = SYSTEM_INFO()
# kernel32.GetSystemInfo(byref(system_info))

print(kernel32.GetLastError())

wintypes.DOUBLE
# PROCESS_ALL_ACCESS = 0x001FFFFF
# pid = 2084
# h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
# print(f"h_process={h_process}")
# kernel32.OpenProcess.restype = c_ulonglong
# h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
# print(f"h_process {h_process} {c_ulonglong(h_process)}")


# # ++++++++++++++++++++++++++++++++++++++++++++


# def handler(signum, frame):
#     print('Signal handler called with signal', signum)
#     exit()
# signal.signal(signal.SIGINT, handler)


# Wow64Process = c_ushort(1)
# kernel32.IsWow64Process(h_process, byref(Wow64Process))
# print(f"pid={pid} h_process={h_process} Wow64Process={Wow64Process.value}")
