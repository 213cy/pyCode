
from ctypes import *
from ctypes import wintypes


MAX_MODULE_NAME32 = 255
MAX_PATH = 260
class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize",          wintypes.DWORD),
        ("th32ModuleID",    wintypes.DWORD),
        ("th32ProcessID",   wintypes.DWORD),
        ("GlblcntUsage",    wintypes.DWORD),
        ("ProccntUsage",    wintypes.DWORD),
        ("modBaseAddr",     POINTER(wintypes.BYTE)),
        ("modBaseSize",     wintypes.DWORD),
        ("hModule",         wintypes.HMODULE),
        ("szModule",        c_char*(MAX_MODULE_NAME32 + 1)),
        ("szExePath",       c_char*(MAX_PATH)),
    ]


# kernel32 = windll.kernel32
kernel32 = WinDLL('kernel32', use_last_error=True)


def check_module_presence(pid, module_name=None):
    if module_name:
        module_name = module_name.encode()

    module_entry = MODULEENTRY32()
    # set the size of the struct or the call will fail
    module_entry.dwSize = sizeof(MODULEENTRY32)
    module_list = []

    # kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    TH32CS_SNAPMODULE = 0x00000008
    snapshot = kernel32.CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE, pid)
    # print(f"snapshot={snapshot:016x}")

    if snapshot is not None:
        success = kernel32.Module32First(snapshot, byref(module_entry))

        while success:
            if module_entry.szModule == module_name:
                return module_entry.hModule

            module_list.append(module_entry.szModule)
            success = kernel32.Module32Next(snapshot, byref(module_entry))

        kernel32.CloseHandle(snapshot)
    else:
        raise WinError(get_last_error())

    if module_name:
        return 0
    else:
        return module_list

# Example usage
if __name__ == "__main__":
    import subprocess
    import time
    subpp = subprocess.Popen('C:\Windows\SysWOW64\calc.exe')

    time.sleep(1)
    modules = check_module_presence(subpp.pid)
    for module in modules:
        print(module)

    dll_name = "ntdll.dll"
    h = check_module_presence(subpp.pid ,dll_name)
    print(f"Process has module {dll_name} with handle: {h:#x}")
