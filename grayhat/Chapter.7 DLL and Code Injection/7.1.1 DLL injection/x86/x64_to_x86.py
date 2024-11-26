# Resolve the address for LoadLibraryA of 32bit
# https://www.52pojie.cn/thread-1935674-1-1.html
# h_kernel32 => EnumProcessModulesEx
# h_loadlib  => parse module PE

from ctypes import *
from ctypes import wintypes
import subprocess
import time

# kernel32 = windll.kernel32
# psapi = windll.psapi
# print(f"--------- {kernel32.GetLastError()},{get_last_error()} --------")
# Load the necessary DLLs
kernel32 = WinDLL('kernel32', use_last_error=True)
psapi = WinDLL('psapi', use_last_error=True)
print(f"--------- {kernel32.GetLastError()},{get_last_error()} --------")


class IMAGE_EXPORT_DIRECTORY(Structure):
    _fields_ = [
        ("ExportFlags",          wintypes.DWORD),
        ("TimeDateStamp",        wintypes.DWORD),
        ("VersionMajor",         wintypes.WORD),
        ("VersionMinor",         wintypes.WORD),
        ("Name",                 wintypes.DWORD),
        ("OrdinalBase",          wintypes.DWORD),
        ("Number_Entries",       wintypes.DWORD),
        ("Number_Names",         wintypes.DWORD),
        ("Table_ExportAddress",  wintypes.DWORD),
        ("Table_NamePointer",    wintypes.DWORD),
        ("Table_Ordinal",        wintypes.DWORD),
    ]


# kernel32.GetModuleHandleA(b"kernel32.dll")
def GetModuleHandle(h_process, dll_name=None):
    if dll_name:
        dll_name = dll_name.lower().encode()

    # Allocate buffer for module handles
    buffer_size = 64  # Start with a reasonable size
    buffer = (wintypes.HMODULE * buffer_size)()
    required_size = wintypes.DWORD()
    LIST_MODULES_32BIT = 0x01
    if not psapi.EnumProcessModulesEx(h_process, buffer, sizeof(buffer), byref(required_size), LIST_MODULES_32BIT):
        raise WinError(get_last_error())

    # Iterate over the module handles and get their names
    module_count = required_size.value // sizeof(wintypes.HMODULE)
    print(f">>> The count of modules in the specified process is {module_count} ")

    module_names = []
    # Define constants
    MAX_NAME = 64
    module_name_buffer = create_string_buffer(MAX_NAME)
    for i in range(module_count):
        module_handle = buffer[i]
        size = psapi.GetModuleBaseNameA(
            h_process, module_handle, module_name_buffer, MAX_NAME)
        if size == 0:
            raise WinError(get_last_error())
        module_name = module_name_buffer.value
        if module_name.lower() == dll_name:
            return module_handle
        module_names.append(module_name)

    return module_names


# kernel32.GetProcAddress(h_kernel32,b"LoadLibraryA")
def GetProcAddress(h_process, h_module, fun_name=None):
    if fun_name:
        fun_name = fun_name.encode()

    read = c_uint()
    e_lfanew = c_uint()
    # base_address=wintypes.DWORD(h_module+0x3c)
    kernel32.ReadProcessMemory(h_process, h_module+0x3c,
                               byref(e_lfanew), 4, byref(read))

    off_address = e_lfanew.value+0x18+0x60
    export_table = wintypes.DWORD()
    kernel32.ReadProcessMemory(h_process, h_module+off_address,
                               byref(export_table), 4, None)

    off_address = export_table.value
    export_directory = IMAGE_EXPORT_DIRECTORY()
    kernel32.ReadProcessMemory(h_process, h_module+off_address,
                               byref(export_directory), sizeof(export_directory), None)

    # --------------------
    fun_count = export_directory.Number_Entries
    print(f">>> The count of functions in the module is {fun_count} ")
    name_count = export_directory.Number_Names
    print(f">>> The count of name entries in the module is {name_count} ")
    # --------------------

    name_pointer_table = (wintypes.DWORD*fun_count)()
    kernel32.ReadProcessMemory(h_process, h_module+export_directory.Table_NamePointer,
                               byref(name_pointer_table), 4*fun_count, None)

    ordinal_table = (wintypes.WORD*fun_count)()
    kernel32.ReadProcessMemory(h_process, h_module+export_directory.Table_Ordinal,
                               byref(ordinal_table), 2*fun_count, None)

    export_address_table = (wintypes.DWORD*fun_count)()
    kernel32.ReadProcessMemory(h_process, h_module+export_directory.Table_ExportAddress,
                               byref(export_address_table), 4*fun_count, None)

    base_pointer = name_pointer_table[0]
    # Start with a reasonable size
    buffer_size = name_pointer_table[-1]-name_pointer_table[0]+32
    name_buffer = create_string_buffer(buffer_size)
    kernel32.ReadProcessMemory(h_process, h_module+base_pointer,
                               byref(name_buffer), buffer_size, None)

    # --------------------
    function_names = []

    for i, pointer in enumerate(name_pointer_table):
        name_entry = pointer - base_pointer
        # Find the end of the current function name in name_buffer
        end_index = name_buffer.raw.find(b'\x00', name_entry)
        # Extract the function name from name_buffer
        name = name_buffer[name_entry:end_index]
        # Check if the extracted name matches the function name we're looking for
        if name == fun_name:
            offset = export_address_table[ordinal_table[i]]
            return h_module + offset
        function_names.append(name)

    return function_names


# Example usage
if __name__ == "__main__":
    subpp = subprocess.Popen('C:\Windows\SysWOW64\calc.exe')
    process_id = subpp.pid
    # process_id = 2400  # Replace with the actual process ID
    print(f"create process with PID = {process_id}")
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    # Open the process
    hProcess = kernel32.OpenProcess(
        PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, process_id)
    print(f"open process with p_handle = {hProcess}")

    # waiting for target process to complete its initialization
    time.sleep(0.2)
    #
    modules = GetModuleHandle(hProcess)
    for module in modules:
        print(module)
    #
    hModule = GetModuleHandle(hProcess, 'kernel32.dll')
    print(f"the handle to the kernel32.dll module : 0x{hModule:08x}")
    #
    funAddress = GetProcAddress(hProcess, hModule, "LoadLibraryA")
    print(f"the address of LoadLibraryA function : 0x{funAddress:08x}")
    #
    kernel32.CloseHandle(hProcess)
    print('done!')
