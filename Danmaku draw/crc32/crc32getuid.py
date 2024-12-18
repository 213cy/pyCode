
import timeit
# ===================================
# ===================================


crctable = [0] * 256

def create_table_recursion(crc=0, ind=0, p=0):
    CRCPOLYNOMIAL = 0xEDB88320

    if p == 8:
        crctable[ind] = crc
        return
    crc_1 = CRCPOLYNOMIAL ^ crc >> 1
    crc_0 = crc >> 1
    ind_1 = ind | 1 << p
    ind_0 = ind
    p += 1
    if crc & 1:
        create_table_recursion(crc_0, ind_1, p)
        create_table_recursion(crc_1, ind_0, p)
    else:
        create_table_recursion(crc_0, ind_0, p)
        create_table_recursion(crc_1, ind_1, p)

create_table_recursion()
# ========================================

indextable = [0] * 256

for k,c in enumerate(crctable):
    indextable[c>>24] = k

rainbow_0 = [0] * 10000
def make_rainbow():
    for i in range(10000):
        rainbow_0[i] = crc32(bytes(ord(k) for k in str(i)))
# ========================================

def update_crc(crc, bbb):
    return ((crc >> 8) ^ crctable[(crc & 0xff) ^ bbb])


def crc32(bbb, init=1):
    crcstart = 0xFFFFFFFF * init
    for k in bbb:
        index = (crcstart & 0xff) ^ k 
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart 

  

def getuid(uid):
    if isinstance(uid,str):
        uid = int(uid,16)
    UID = uid  ^ 0xffffffff
    RESULT = []
    STOP_ID = 10**8

    def addonedigit(cr,id):
        for i in range(10):
            c = (cr >> 8) ^ crctable[(cr & 0xff) ^ i+48]
            id_1 = id *10 + i
            if c == UID:
                RESULT.append(id_1)
            elif id_1 < STOP_ID:
                addonedigit(c,id_1)

    for i in range(1000):
        crc = crc32(bytes(ord(k) for k in str(i)))
        if crc == UID:
            RESULT.append(i)

    for i in range(9500,10000):
        crc = crc32(bytes(ord(k) for k in str(i)))
        if crc == UID:
            RESULT.append(i)
        addonedigit(crc,i)

    return RESULT
    for _ in range(4):
        ind = indextable[crcreg>>24]
        crcreg = crctable[ind] ^ crcreg<<8

    # create_table()


def bbb():
    create_table_recursion()
    # a=getuid(crc32(b'41') ^ 0xffffffff)
    a=getuid(0x8bcda38e)
    print(a)
    pass


def aaa():
    create_table_recursion()
    a=[k >> 24 for k in crctable]
    aa=sorted(a)
    print(any(j-k==1 for k,j in zip(aa[:-2],aa[1:-1])))
    b=[k >> 28 for k in crctable]
    bb=sorted(b)
    c=[0] *16
    for k in bb:
        c[k] +=1 
    pass


if __name__ == "__main__":
    bbb()
    exit()

    # ==================================================
    current_hashstr=''
    backto_midstr = ['']
    def timefun():
        # global backto_midstr
        backto_midstr[0] = getuid(current_hashstr)

    #  efb3f424 1647605377
    current_mid = 1647605377
    current_hashstr = "efb3f424"
    t = timeit.timeit(timefun , number=1)
    print(f"{t:.4f}s  ",current_hashstr,"=>", backto_midstr)


    # 8bcda38e 95646000
    current_mid = 95646000
    current_hashstr = '8bcda38e'
    # t = timeit.timeit("timefun()" , number=1,globals=globals())
    # print(t)
    t = timeit.timeit(timefun , number=1)
    print(f"{t:.4f}s  ",current_hashstr,"=>", backto_midstr)

