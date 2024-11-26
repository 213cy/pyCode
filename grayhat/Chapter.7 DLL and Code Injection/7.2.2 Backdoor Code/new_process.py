from ctypes import *
from ctypes import wintypes
import time


class STARTUPINFO(Structure):
    _fields_ = [
        ("cb",              wintypes.DWORD),
        ("lpReserved",      wintypes.LPSTR),
        ("lpDesktop",       wintypes.LPSTR),
        ("lpTitle",         wintypes.LPSTR),
        ("dwX",             wintypes.DWORD),
        ("dwY",             wintypes.DWORD),
        ("dwXSize",         wintypes.DWORD),
        ("dwYSize",         wintypes.DWORD),
        ("dwXCountChars",   wintypes.DWORD),
        ("dwYCountChars",   wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags",         wintypes.DWORD),
        ("wShowWindow",     wintypes.WORD),
        ("cbReserved2",     wintypes.WORD),
        ("lpReserved2",     wintypes.LPBYTE),
        ("hStdInput",       wintypes.HANDLE),
        ("hStdOutput",      wintypes.HANDLE),
        ("hStdError",       wintypes.HANDLE),
    ]


class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess",    wintypes.HANDLE),
        ("hThread",     wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId",  wintypes.DWORD),
    ]


def create_process(*args):
    if len(args) > 1:
        path_to_exe = args[0].encode(encoding='latin1')
    else:
        # This is the original executable
        path_to_exe = b"C:/Windows/SysWOW64/cmd.exe"
        path_to_exe = b"C:/Windows/SysWOW64/calc.exe"

    creation_flags = CREATE_NEW_CONSOLE = 0x00000010

    startupinfo = STARTUPINFO()
    startupinfo.cb = sizeof(startupinfo)
    # startupinfo.dwFlags = STARTF_USESHOWWINDOW = 0x00000001
    
    # startupinfo.wShowWindow = SW_HIDE = 0
    # startupinfo.wShowWindow = SW_SHOW = 5

    process_information = PROCESS_INFORMATION()

    kernel32 = windll.kernel32
    # First things first, fire up that second process
    # and store it's PID so that we can do our injection
    a = kernel32.CreateProcessA(path_to_exe,
                                None,
                                None,
                                None,
                                None,
                                creation_flags,
                                None,
                                None,
                                byref(startupinfo),
                                byref(process_information))
    if (a == 0):
        print(f"CreateProcess failed ! error= {GetLastError()}")
        return 0
    else:
        print(
            f"CreateProcess succeeds ! PID = {process_information.dwProcessId}")
        # Wait until child process exits.
        INFINITE = 0xFFFFFFFF
        # kernel32.WaitForSingleObject(process_information.hProcess, INFINITE)

        time.sleep(0.2)
        # Close process and thread handles.
        kernel32.CloseHandle(process_information.hProcess)
        kernel32.CloseHandle(process_information.hThread)
        time.sleep(0.2)
        return process_information.dwProcessId


if __name__ == "__main__":
    print(create_process())
