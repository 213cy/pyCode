import my_debugger
from my_debugger_defines import *

kernel32 = windll.kernel32
path_to_exe = b'C:\\Windows\\System32\\calc.exe'
command_line = None
path_to_exe = None
command_line = b'D:\\Python38\\python.exe printf_loop.py'
path_to_exe = b'D:\\Python38\\python.exe'
command_line = b'-m printf_loop.py'
PID = 3628
# ===============================
creation_flags = CREATE_NEW_CONSOLE
# creation_flags = DEBUG_PROCESS

# instantiate the structs
startupinfo = STARTUPINFO()
process_information = PROCESS_INFORMATION()

# The following two options allow the started process
# to be shown as a separate window. This also illustrates
# how different settings in the STARTUPINFO struct can affect
# the debuggee.
startupinfo.dwFlags = 0x1
startupinfo.wShowWindow = 0x1

# We then initialize the cb variable in the STARTUPINFO struct
# which is just the size of the struct itself
startupinfo.cb = sizeof(startupinfo)

if kernel32.CreateProcessA(path_to_exe,
                            command_line,
                            None,
                            None,
                            None,
                            creation_flags,
                            None,
                            None,
                            byref(startupinfo),
                            byref(process_information)):

    print("[*] We have successfully launched the process!")
    print("[*] The Process ID I have is: %d" %
            process_information.dwProcessId)
    PID = process_information.dwProcessId
    
    kernel32.CloseHandle(process_information.hProcess)
    kernel32.CloseHandle(process_information.hThread)
else:
    print("[*] Error with error code %d." %
            kernel32.GetLastError())

# exit()

# ==================================================================


debugger = my_debugger.debugger()

printf_address = debugger.func_resolve(b"msvcrt.dll", b"printf")
print("[*] Address of printf: 0x%016x" % printf_address)


def action():
    act = input(
        f'select breakpoint[printf @ 0x{printf_address:x}] type[1,2,3] >>> ')
    # return True
    try:
        if act == '1':
            print("[*1*] Set soft breakpoint !!!")
            debugger.bp_set(printf_address)
        elif act == '2':
            print("[*2*] Set hardware breakpoint !!!")
            debugger.bp_set_hw(printf_address, 1, HW_EXECUTE)
        elif act == '3':
            print("[*3*] Set memory breakpoint !!!")
            debugger.bp_set_mem(printf_address, 10)
        else:
            return False
    except Exception:
        print('exception')
    return True


# debugger.load(b'C:\\Windows\\System32\\calc.exe')
# debugger.run()
# ======================
# pid = input("Enter the PID of the process to attach to: ")
# debugger.attach(int(pid))
debugger.attach(PID)

# print('before enumerate_threads', kernel32.GetLastError())
lst = debugger.enumerate_threads()
# print('after enumerate_threads', kernel32.GetLastError())
for it in lst:
    con = debugger.get_thread_context(it)
    print(f'Rip = 0x{con.Rip:016x} Rax = 0x{con.Rax:016x} TID:{it}')


debugger.run(action)
debugger.detach()
