
// for msvc x86
 
int main()
{
    char *shellcode ="\x33\xC9\x64\x8B\x41\x30";
    C_Dest: 

    __asm {
        mov al, 3
        bbb:    
        mov dx, 0xD007
        out dx, al
    }

    __asm {
        a_dest:    ; 
        jmp shellcode;
        jmp C_Dest;
        jmp bbb;
        jmp BBB;
    }
    goto C_Dest;

    return 0;
}

// for gcc x64 with -masm=intel
int main2() {
    char* aaaa="\0x56\0x55";
    bbbb:
    __asm ("mov al, 5\n"
         "\tjmp aaaa");

    // __asm {
    // };
	__asm__("jmp aaaa");
    __asm__("jmp bbbb");
    goto bbbb;
}