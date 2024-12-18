# https://www.cnblogs.com/shine-lee/p/10717521.html

def parse_tag_value(byte_sequence, start_index):
    current_byte = byte_sequence[start_index]
    bytes_parsed = 0
    value = 0
    while current_byte > 0x7f:
        value |= (current_byte & 0x7f) << (7*bytes_parsed)
        bytes_parsed += 1
        current_byte = byte_sequence[start_index+bytes_parsed]

    value |= (current_byte & 0x7f) << (7*bytes_parsed)
    bytes_read = bytes_parsed+1
    return value, bytes_read


def parse_os_data(data):
    output_list = []
    next_block_tag_pointer = 0
    tag_pointer = 0

    while tag_pointer < len(data):
        tag_value = data[tag_pointer]
        if tag_value == 0x0a:
            if tag_pointer != next_block_tag_pointer:
                raise ValueError("Data block end tag mismatch")
            value, length = parse_tag_value(data, tag_pointer+1)

            tag_pointer = tag_pointer + length + 1
            next_block_tag_pointer = tag_pointer + value

            current_list = [0,'ffffffff',0,'']
        elif tag_value & 2:
            value, length = parse_tag_value(data, tag_pointer+1)
            if tag_value == 0x32:
                # string midHash = 6; 6/2 =3
                index = tag_pointer+1+length
                text = data[index:index+value]
                current_list[1] = text.decode()
            elif tag_value == 0x3a :
                # string content = 7;
                index = tag_pointer+1+length
                text = data[index:index+value]
                current_list[3]=text.decode()
            tag_pointer = tag_pointer+1+length+value
        else:
            value, length = parse_tag_value(data, tag_pointer+1)
            if tag_value == 0x10:
                # int32 progress = 2; 2/2 =1
                current_list[0] =value
            if tag_value == 0x40 :
                # int64 ctime = 8; 8/2=4
                current_list[2]=value
            tag_pointer = tag_pointer+1+length

        if tag_pointer == next_block_tag_pointer:
            output_list.append(current_list)

    return output_list


if __name__ =="__main__":
    fp = open('aaa.so', 'rb')
    data = fp.read()
    fp.close()

    output = parse_os_data(data)
    print(len(output))