from ctypes import *
from ctypes import wintypes
import os
import subprocess
import time
from module_check import check_module_presence

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


architecture  = "64bit"
print("!!!", architecture , "!!!")

time.sleep(2)
#  ===============================

# Resolve the address for LoadLibraryA of 64bit
kernel32.GetModuleHandleA.restype = c_void_p
kernel32.GetProcAddress.restype = c_void_p

dll_handle = kernel32.GetModuleHandleA(b"KERNELBASE.dll")
print(f"{'dll_handle (KERNELBASE.dll)':30}: {dll_handle:#x}")
fun_address = kernel32.GetProcAddress(c_void_p(dll_handle), b"Beep")
print(f"{'fun_address (Beep)':30}: {fun_address:#x}")

dll_handle = kernel32.GetModuleHandleA(b"kernel32.dll")
print(f"{'dll_handle (kernel32.dll)':30}: {dll_handle:#x}")
LoadLibrary_fun = kernel32.GetProcAddress(c_void_p(dll_handle),
                                          b"LoadLibraryA")
print(f"{'LoadLibrary_fun (LoadLibraryA)':30}: {LoadLibrary_fun:#x}")
FreeLibrary_fun = kernel32.GetProcAddress(c_void_p(dll_handle), b"FreeLibrary")
print(f"{'FreeLibrary_fun (FreeLibrary)':30}: {FreeLibrary_fun:#x}")


# ==================================

# Open the process
# PROCESS_QUERY_INFORMATION = 0x0400
# PROCESS_VM_READ           = 0x0010
# hProcess = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
# Define access rights / Get a handle to the process we are injecting into.
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if not h_process:
    raise WinError(get_last_error())


def new_remote_thread(start_address, raw_parameter):
    if isinstance(raw_parameter, str):
        bytes_to_write = raw_parameter.encode()
        bytes_size = len(bytes_to_write)

        PAGE_READWRITE = 0x04
        PAGE_EXECUTE_READWRITE = 0x40
        VIRTUAL_MEM = (0x1000 | 0x2000)
        # Allocate some space for the DLL path
        kernel32.VirtualAllocEx.restype = c_void_p
        parameter = kernel32.VirtualAllocEx(h_process, 0, bytes_size,
                                            VIRTUAL_MEM, PAGE_READWRITE)
        print(f"        {'parameter'}: {parameter:#x}")

        # Write the DLL path into the allocated space
        written = c_int(0)
        kernel32.WriteProcessMemory(h_process, parameter,
                                    bytes_to_write, bytes_size, byref(written))
    elif isinstance(raw_parameter, int):
        parameter = wintypes.HANDLE(raw_parameter)
        # bytes_to_write = raw_parameter.to_bytes(8, 'little')
    else:
        raise TypeError("Input must be either a string or an integer.")

    # ==================================
    # create the remote thread, with the entry point set to start_address
    # and a pointer to parameter as it's single parameter
    thread_id = c_ulong(0)
    h_thread = kernel32.CreateRemoteThread(h_process, None, 0,
                                           c_void_p(start_address), 
                                           parameter,
                                           0, byref(thread_id))
    if not h_thread:
        raise WinError(get_last_error())

    # kernel32.VirtualFreeEx(h_process,parameter, bytes_size,
    # [in] DWORD  dwFreeType
    # )
    kernel32.CloseHandle(h_thread)

    return thread_id.value


load_time = 0
while True:
    print(f'----------- dll reference count : {load_time} -----------')
    print("1. Inject DLL\n2. Check DLL presence\n3. Free Library\n4. Exit")
    choice = input("Choose an option >>> ").strip()

    if choice == '1':
        print("    Injecting DLL...")
        tid = new_remote_thread(LoadLibrary_fun, dll_path)
        load_time += 1
        print(f"    Created remote thread with ID: {tid}")

    elif choice == '2':
        print("    Checking for DLL presence...")
        module_handle = check_module_presence(pid, dll_name)
        print(
            f"    DLL '{dll_name}' is present in process {pid} at address {module_handle:#x}")

    elif choice == '3':
        print("    Freeing Library...")
        module_handle = check_module_presence(pid, dll_name)
        if module_handle > 0:
            new_remote_thread(FreeLibrary_fun, module_handle)
            load_time -= 1
            print(f"    Freed DLL '{dll_name}' from process {pid} once.")
        else:
            print(f"    DLL '{dll_name}' is not present in target process")

    elif choice == '4':
        print("    Exiting...")
        break
    else:
        print("!!! Invalid option. Please choose again !!!")

kernel32.CloseHandle(h_process)
