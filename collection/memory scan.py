##MemoryScan
from ctypes import *
import psutil
import win32con

# 从C#到Python手把手教你用Python实现内存扫描获取指定字符串
# https://blog.csdn.net/as604049322/article/details/127573200


##kernel32 = cdll.LoadLibrary("kernel32.dll")
##kernel32 = windll.LoadLibrary("kernel32.dll")
kernel32 = windll.kernel32

GetLastError = kernel32.GetLastError
OpenProcess = kernel32.OpenProcess
VirtualQueryEx = kernel32.VirtualQueryEx
ReadProcessMemory = kernel32.ReadProcessMemory

DWORD = c_ulong
WORD = c_ushort
PVOID = c_void_p
PVOID = c_ulonglong
SIZE_T = c_size_t


class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [('BaseAddress', PVOID),
                ('AllocationBase', PVOID),
                ('AllocationProtect', DWORD),
                ('PartitionId', WORD),
                ('RegionSize', SIZE_T),
                ('State', DWORD),
                ('Protect', DWORD),
                ('Type', DWORD)
                ]


StateTab = {0: '0x0', win32con.MEM_RESERVE: 'RESERVE',
            win32con.MEM_FREE: 'FREE', win32con.MEM_COMMIT: 'COMMIT'}
TypeTab = {win32con.MEM_IMAGE: 'IMAGE',
           win32con.MEM_MAPPED: 'MAPPED', win32con.MEM_PRIVATE: 'PRIVATE'}


def ScanMemory(addr, size):
    data_type = c_char * size
    MemBuf = data_type()
    NumberOfBytes = c_ulong()
    result = ReadProcessMemory(process, addr, byref(
        MemBuf), size, byref(NumberOfBytes))
    print(
        f'ReadSuccess: {result} , ReadFrom: {addr.value:#010x} , ReadBytes: {NumberOfBytes.value}')
    ind = MemBuf.raw.find(partten)
    if ind >= 0:
        #  MemBuf[ind:ind+50].decode()
        #  MemBuf[ind].value
        print(MemBuf.raw[:200].replace(b'\x00', b''))
        print(MemBuf[ind:ind+50])
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


nameprocess = 'calc.exe'
nameprocess = 'notepad.exe'

partten = 'zzzzz'.encode()
partten = b'This program'
partten = b'zzzzzzzzzzzzzzzzzz'

for prcs in psutil.process_iter():
    if prcs.name().lower() == nameprocess:
        ObjProc = prcs
        print(
            f'target process:  name = {ObjProc.name()}  , id = {ObjProc.pid}  ')


process = OpenProcess(win32con.PROCESS_ALL_ACCESS, False, ObjProc.pid)
mbi = MEMORY_BASIC_INFORMATION()

addr_start = 0x1_0000_0000
addr_start = 0x7fe_fdb0_0000
addr_start = 0x80000000000
addr_start = 0x00
loop_count = 20
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

lpAddr = c_ulonglong(addr_start)

for k in range(loop_count):
    t = VirtualQueryEx(process, lpAddr, byref(
        mbi), sizeof(MEMORY_BASIC_INFORMATION))
    if mbi.State != win32con.MEM_FREE:
        print(f'{k}  ', end='\t')
        b = mbi.AllocationProtect & (
            win32con.PAGE_EXECUTE | win32con.PAGE_NOACCESS | win32con.PAGE_NOCACHE)
        if not b:
            ScanMemory(lpAddr, mbi.RegionSize)

    lpAddr.value = lpAddr.value + mbi.RegionSize

raise SystemExit
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

# verbose version
lpAddr = addr_start

for k in range(loop_count):
    t = VirtualQueryEx(process, c_ulonglong(lpAddr), byref(
        mbi), sizeof(MEMORY_BASIC_INFORMATION))
##    print(t, GetLastError())
    if mbi.State != win32con.MEM_FREE:
        print(10*'-', f'  {k}  ', 10*'-')
        print(f"BaseAddress={mbi.BaseAddress:#010x},"
              f"Protect={mbi.Protect:#x}")
        b = mbi.AllocationProtect & (
            win32con.PAGE_EXECUTE | win32con.PAGE_NOACCESS | win32con.PAGE_NOCACHE)
        if b:
            print(25*'x')
        if not b:
            print(f"AllocationBase={mbi.AllocationBase:#010x},"
                  f"AllocationProtect={mbi.AllocationProtect:#x},"
                  f"RegionSize={mbi.RegionSize:#010x},"
                  f"State={StateTab[mbi.State]},Type={TypeTab.get(mbi.Type,mbi.Type)}")

            # ScanMemory(lpAddr,mbi.RegionSize)

    lpAddr = lpAddr + mbi.RegionSize
    # if lpAddr >= 0x1_0000_0000: #2**32
    #     break
print(f'done!  lpAddr = {lpAddr}')

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

lpAddr = 2**32
print(10*'-', '  LastError  ', 10*'-')
print(GetLastError())
try:
    t = VirtualQueryEx(process, lpAddr, byref(
        mbi), sizeof(MEMORY_BASIC_INFORMATION))
except BaseException as e:
    print(e)
print(GetLastError())
print(10*'-', '  LastError  end  ', 10*'-')

lpAddr = c_ulonglong(0x1_0000_0000)
t = VirtualQueryEx(process, lpAddr, byref(
    mbi), sizeof(MEMORY_BASIC_INFORMATION))
