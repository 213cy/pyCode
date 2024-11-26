
// This code is only for x86 MSVC compilers, 
// and not only differs from the original shellcode
// but alse will fail when run.

#include <stdio.h>
int main() {
    int i = 0;
    int nopcount = 0;
    int comcount = 0;

    printf("============");
    goto entry;
    __asm {
        nop;
        nop;
    }
        __asm {
x0:     cld
x1:     push   ebp
x2:     jmp    x51
x4:     call   x2
x9:     pushad
xa:     mov    ebp,DWORD PTR [esp+0x24]
xe:     mov    eax,DWORD PTR [ebp+0x3c]
x11:    mov    edi,DWORD PTR [ebp+eax*1+0x78]
x15:    add    edi,ebp                      ; edi = IMAGE_EXPORT_DIRECTORY
x17:    mov    ecx,DWORD PTR [edi+0x18]     ; ecx = NumberOfNames(Functions)
x1a:    mov    ebx,DWORD PTR [edi+0x20]
x1d:    add    ebx,ebp                      ; ebx = AddressOfNames
x1f:    dec    ecx
x20:    mov    esi,DWORD PTR [ebx+ecx*4]
x23:    add    esi,ebp
x25:    xor    eax,eax
x27:    cdq
x28:    lods   al
x29:    test   al,al
x2b:    je     x34
x2d:    ror    edx,0xd
x30:    add    edx,eax
x32:    jmp    x28
x34:    cmp    edx,DWORD PTR [esp+0x28]
x38:    jne    x1f
x3a:    mov    ebx,DWORD PTR [edi+0x24]
x3d:    add    ebx,ebp
x3f:    mov    cx,WORD PTR [ebx+ecx*2]
x43:    mov    ebx,DWORD PTR [edi+0x1c]
x46:    add    ebx,ebp
x48:    add    ebp,DWORD PTR [ebx+ecx*4]
x4b:    mov    DWORD PTR [esp+0x1c],ebp
x4f:    popad
x50:    ret
x51:    xor    ebx,ebx
x53:    mov    eax,DWORD PTR fs:[ebx+0x30]
x57:    mov    eax,DWORD PTR [eax+0xc]
x5a:    mov    esi,DWORD PTR [eax+0x1c]
x5d:    lods   eax
x5e:    mov    esi,eax
x60:    lods   eax
x61:    mov    eax,DWORD PTR [eax+0x8]      ; eax = kernel32.dll
x64:    pop    esi
x65:    push   0xe8afe98                    ; WinExec hash
x6a:    push   eax
x6b:    call   esi
x6d:    push   ebx
x6e:    mov    edx,esi
x70:    add    edx,0x72
x73:    push   edx
x74:    call   eax                          ; call WinExec
x76:    add    esp,0xc
x79:    pop    ebp
x7a:    ret
        }
    __asm {
        nop;
        nop;
    }

entry:
    // unsigned int * ppp = (unsigned int *) main;
    unsigned char *ppp = (unsigned char *)main;

    do {
        //   printf("%d-",i);
        int by = *(ppp + i);
        if (by == 0x90) {
            nopcount++;
        } else {
            if (nopcount == 2) {
            printf("%02x ", by);
            comcount++;
            if (comcount == 2){
                printf("6a ", by);
                comcount++;
            }
            if (comcount % 16 == 0) {
                printf("\\\n");
            }
        }
        }
        i++;
    } while (nopcount < 3 || i > 0x2ff);

    printf("\n%02x -- %02x\n", (unsigned int)main, *ppp);
    printf("%02x -- %02x", *(unsigned int *)main, *(int *)ppp);
    return 0;
}

