# https://github.com/cwuom/GetDanmuSender/blob/main/main.py
import timeit
# ===================================
# ===================================

CRCPOLYNOMIAL = 0xEDB88320
crctable = [0] * 256

def create_table():
    for i in range(256):
        crcreg = i
        for _ in range(8):
            if (crcreg & 1) != 0:
                crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
            else:
                crcreg = crcreg >> 1
        crctable[i] = crcreg


def crc32(id):
    crcstart = 0xFFFFFFFF
    # crcstart = 0x0
    for i in str(id):
        index = crcstart & 0xff ^ ord(i)
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart


def crc32_last_index(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return index


def get_crc_index(t):
    for i in range(256):
        if crctable[i] >> 24 == t:
            return i
    return -1


def deep_check(i, index):
    string = ""
    tc = 0x00
    hashcode = crc32(i)
    tc = hashcode & 0xff ^ index[2]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[2]] ^ (hashcode >> 8)
    tc = hashcode & 0xff ^ index[1]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[1]] ^ (hashcode >> 8)
    tc = hashcode & 0xff ^ index[0]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[0]] ^ (hashcode >> 8)
    return [1, string]


def getuid_x(string):
    # create_table()
    index = [0 for x in range(4)]
    i = 0
    ht = int(f"0x{string}", 16) ^ 0xffffffff
    for i in range(3, -1, -1):
        index[3-i] = get_crc_index(ht >> (i*8))
        snum = crctable[index[3-i]]
        ht ^= snum >> ((3-i)*8)
    for i in range(100000000):
        lastindex = crc32_last_index(i)
        if lastindex == index[3]:
            deepCheckData = deep_check(i, index)
            if deepCheckData[0]:
                break
    if i == 100000000:
        return -1
    return f"{i}{deepCheckData[1]}"


def getuid(string):
    ht = int(string, 16) ^ 0xffffffff

    for i in range(95000000,100000000):
        crcstart = 0xFFFFFFFF
        # crcstart = 0x0
        for k in str(i):
            index = crcstart & 0xff ^ ord(k)
            crcstart = (crcstart >> 8) ^ crctable[index]
        
        if ht == crcstart:
            return str(i)
    return 'x'


def aaa():
    create_table()
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
    create_table()

    current_hashstr=''
    backto_midstr = ['']
    def timefun():
        # global backto_midstr
        backto_midstr[0] = getuid(current_hashstr)



    # 8bcda38e 95646000
    current_mid = 95646000
    current_hashed = crc32(current_mid) ^ 0xffffffff
    current_hashstr = hex(current_hashed)[2:]
    # t = timeit.timeit("timefun()" , number=1,globals=globals())
    # print(t)
    t = timeit.timeit(timefun , number=1)
    print(f"{t:.4f}s  ",hex(current_hashed),"=>", backto_midstr)

    exit()
    #  efb3f424 1647605377
    current_mid = 1647605377
    current_hashed = crc32(current_mid) ^ 0xffffffff
    current_hashstr = hex(current_hashed)[2:]
    t = timeit.timeit(timefun , number=1)
    print(f"{t:.4f}s  ",hex(current_hashed),"=>", backto_midstr)