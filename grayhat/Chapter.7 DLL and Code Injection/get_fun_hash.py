# Helper function for rotate-right on 32-bit architectures
def ror(number, bits):
    return ((number >> bits) | (number << (32 - bits))) & 0xffffffff

# Define hashing algorithm


def get_hash(string):
    # data = string.lower().encode()
    data = string.encode()
    result = 0
    # Loop each character
    # for b in data[::-1]:
    for b in data:
        # Rotate DllHash right by 0x0D bits
        result = ror(result, 0x0D)
        # Add character to DllHash
        result = (result + b) & 0xffffffff
    return result


functionname = 'GetProcAddress'
functionname = 'LoadLibraryA'  # 0xec0e4e8e
functionname = 'ExitThread'  # 0x60e0ceef
functionname = 'WinExec'  # 0x0e8afe98

res = get_hash(functionname)
print(f"0x{res:08x}")
