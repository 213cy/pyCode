
def shifts_operation_with_negative():

    def repr_val(val):
        val_byte_len = (val.bit_length()+7) // 8
        val_bytes_little = val.to_bytes(
            val_byte_len, byteorder='little', signed=True)
        val_bytes_big = val.to_bytes(
            val_byte_len, byteorder='big', signed=True)
        print('<<', val, '>>')
        print(hex(val))
        print(val_bytes_little)
        print(val_bytes_little.hex())
        print(val_bytes_big)
        print(val_bytes_big.hex())
        return hex(val) ,val_bytes_big.hex()
    def repr_vals(val):
        hex_strs = repr_val(val)
        val_shifted = val >> 8
        hex_shifted_strs = repr_val(val_shifted)
        print(" ! "*9)
        print(hex_strs)
        print(hex_shifted_strs)
        print(hex_shifted_strs[0][-2:],'-',hex_strs[0][-4:-2], '= 1')
        print(hex_shifted_strs[1][-2:],'-',hex_strs[1][-4:-2], '= 0')

    # The hash value is different when invoked a second time 
    # because recent releases of Python (versions 3.3 and up),
    # by default, apply a random hash seed for this function. 
    # The seed changes on each invocation of Python. 
    # Within a single instance, the results will be identical.
    val = hash('sometext')
    if val < 0 : val =-val
    print('++++++++ a postive number ++++++++')
    repr_vals(val)
    val_neg = -val
    print('++++++++ a negative number ++++++++')
    repr_vals(val_neg)

shifts_operation_with_negative()
