# [CRC校验]手算与直观演示 https://www.bilibili.com/video/BV1V4411Z7VA/
# https://github.com/Michaelangel007/crc32
# 了解crc以及crc32算法(查表法)的python实现 https://www.bilibili.com/video/BV1cK4y1t7uK/

import zlib
import random


def aaa():
    # 1647605377  efb3f424
    a = zlib.crc32('1647605377'.encode())
    print('1647605377', hex(a))
    # 123456789     cbf43926
    a = zlib.crc32('123456789'.encode())
    print('123456789', hex(a))
    # 95646000    8bcda38e
    a = zlib.crc32(b'95646000')
    print('95646000', hex(a))


def bbb():
    a = random.randint(0, 0xff)
    b = random.randint(0, 0xff)
    byte_a = bytes.fromhex(f'{a:02x}')
    byte_b = bytes.fromhex(f'{b:02x}')
    crc_ab = zlib.crc32(byte_a+byte_b)

    crc_a = zlib.crc32(byte_a)
    crc_b = zlib.crc32(byte_b)
    temp = (crc_a & 0xff) ^ b
    byte_temp = bytes.fromhex(f'{temp:02x}')
    crc_temp = zlib.crc32(byte_temp)
    crc_ab2 = (crc_a >> 8) ^ crc_temp
    print(f"{crc_ab:#x},{crc_ab2:#x}")


def ccc():
    a = zlib.crc32(b'\xff\xff\xff\xff\x80')
    a = zlib.crc32(b'\xff\xff\xff\x7f')
    POLY = 0x04C11DB7
    POLY_ref = 0xEDB88320
    print('POLYNOMIAL_ref =', hex(POLY_ref))
    print(hex(a), hex(a ^ 0xffffffff), hex(reflect32(a)))
    print('POLYNOMIAL     =', hex(POLY))
    print(hex(reflect32(a ^ 0xffffffff)), hex(reflect32(a) ^ 0xffffffff))

    b = b'\xff'
    for k in range(5):
        print(b*k, hex(zlib.crc32(b*k)))
    
    f_mask = 0xffffffff
    a=zlib.crc32(b'\xff\xff\xff\xff\x01') ^ 0xffffffff
    b=zlib.crc32(b'\x30') ^ 0xffffffff
    c=zlib.crc32(b'\x31') ^ 0xffffffff
    print(a^c^b)

    hash_mask = zlib.crc32(b'\xff\xff\xff\xff')
    for _ in range(3):
        a = random.randint(0, 0xff)
        b = random.randint(0, 0xff)

        aa=zlib.crc32(bytes([a]))
        bb=zlib.crc32(bytes([b]))
        cc=zlib.crc32(bytes([a^b]))
        # 0xd202ef8d
        offset = aa^bb^cc
        print(hex(offset))

    a = 0
    aa = 0
    for _ in range(3):
        t = random.randint(0, 0xff)
        a ^= t
        aa ^= zlib.crc32(bytes([t])) ^ offset
    
    aaa=zlib.crc32(bytes([a])) ^ offset
    print(hex(aa),hex(aaa))
    

    crcreg = 0xffffffff
    CRCPOLYNOMIAL = 0xEDB88320
    for _ in range(8):
        if (crcreg & 1) != 0:
            crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
        else:
            crcreg = crcreg >> 1

    print(hex(crcreg^0xffffffff ), '0xd202ef8d')

def ddd():
    d = bytes(random.randint(0, 255) for _ in range(4))
    a = int.from_bytes(d, byteorder='big')
    b = ~-(0x1_0000_0000-a)
    c = a ^ 0xffffffff
    print(hex(b), hex(c))

# ===================================
# ===================================


def reflect32(int32=None):
    if int32 is None:
        int32 = 0x04c11db7
        int32_ref = reflect32(int32)
        int32_ori = reflect32(int32_ref)
        print(f"{int32:#x},{int32_ref:#x},{int32_ori:#x}")
    return int(bin(int32 | 1 << 32)[-1:2:-1], 2)


def reflect8(int8):
    if random.random() > 0.5:
        return int(bin(int8 | 1 << 8)[-1:2:-1], 2)
    else:
        return sum(1 << 7-k for k in range(8) if int8 & 1 << k)


def crc32_formula_normal(data):
    CRCPOLY = 0x04c11db7 | 0x1_0000_0000
    if isinstance(data, str):
        data = data.encode('latin-1')

    data = bytes(reflect8(k) for k in data)

    byte_count = len(data)
    data = int.from_bytes(data, 'big')
    crc_init = data << 32
    # p = len(bin( crc_init )) - 2
    crc = crc_init ^ 0xffffffff << (8*byte_count)
    p = len(bin(crc)) - 2
    while p > 32:
        crc = crc ^ CRCPOLY << (p-33)
        p = len(bin(crc)) - 2
    res = reflect32(crc ^ 0xffffffff)
    # res = crc ^ 0xffffffff
    return res


def crc32_formula_normal_noreverse(data):
    CRCPOLY = 0x04c11db7 | 0x1_0000_0000
    if isinstance(data, str):
        data = data.encode('latin-1')
    byte_count = len(data)
    data = int.from_bytes(data, 'big')
    crc_init = data << 32
    # p = len(bin( crc_init )) - 2
    crc = crc_init ^ 0xffffffff << (8*byte_count)
    p = len(bin(crc)) - 2
    while p > 32:
        crc = crc ^ CRCPOLY << (p-33)
        p = len(bin(crc)) - 2
    # res = reflect32(crc ^ 0xffffffff)
    res = crc ^ 0xffffffff
    return res

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


def create_table():
    CRCPOLYNOMIAL = 0xEDB88320
    for i in range(256):
        crcreg = i
        for _ in range(8):
            if (crcreg & 1) != 0:
                crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
            else:
                crcreg = crcreg >> 1
        crctable[i] = crcreg


def time_measure():
    import timeit

    execution_time = timeit.timeit(create_table_recursion, number=50)
    print(f"Execution time: {execution_time:.4f} seconds")
    crctable_a = crctable
    execution_time = timeit.timeit(create_table, number=50)
    print(f"Execution time: {execution_time:.4f} seconds")

    print(len(crctable_a),len(crctable))
    debug_rec = list(map(lambda x, y: x-y == 0, crctable_a, crctable))
    print(all(debug_rec))

# ===================================
# ===================================


def crc32(data):
    if isinstance(data, str):
        data = data.encode('latin-1')
    crcstart = 0xFFFFFFFF
    # crcstart = 0x0
    for i in data:
        index = (crcstart & 0xff) ^ i
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart


if __name__ == "__main__":

    ccc()
    exit()
    checksum = zlib.crc32(b'123456789')
    print("--- CRC32 checksum of '123456789' should be ", hex(checksum))
    checksum2 = crc32_formula_normal(b'123456789')
    # create_table()
    create_table_recursion()
    checksum3 = crc32('123456789')
    print(hex(checksum2), hex(checksum3 ^ 0xffffffff))

    a = zlib.crc32(b'95646000')
    print("--- CRC32 checksum of '95646000' should be 0", hex(a))
    hash_b = crc32(b'95646000')
    hash_c = crc32('95646000')
    print(hex(hash_b ^ 0xffffffff), hex(hash_c ^ 0xffffffff))
