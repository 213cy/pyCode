import random

d = bytes(random.randint(0, 255) for _ in range(4))
a = int.from_bytes(d, byteorder='big')
b = ~-(0x1_0000_0000-a)
c = a ^ 0xffffffff

print(0x7fffffff ^ 0)
print((0x7fffffff + 1) ^ 0)
print(hex(b), hex(c))