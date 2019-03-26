from typing import List, Generator

bit_1_mask = int('00000001', 2)
bit_2_mask = int('00000010', 2)
bit_3_mask = int('00000100', 2)
bit_4_mask = int('00001000', 2)
bit_5_mask = int('00010000', 2)
bit_6_mask = int('00100000', 2)
bit_7_mask = int('01000000', 2)
bit_8_mask = int('10000000', 2)

buffer_order = [0, 2, 1, 3]

def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:

    buffer = []

    for byte in source:
        # TODO: Do something sensible.
        byte1 = int('00000000', 2)
        byte2 = int('00000000', 2)

        number = byte[0]

        byte1 |= (number & bit_8_mask) >> 2
        byte1 |= (number & bit_7_mask) >> 3
        byte1 |= (number & bit_6_mask) >> 3
        byte1 |= (number & bit_5_mask) >> 3

        byte2 |= (number & bit_4_mask) << 2
        byte2 |= (number & bit_3_mask) << 1
        byte2 |= (number & bit_2_mask) << 1
        byte2 |= (number & bit_1_mask) << 1

        par1 = (int((byte1 & bit_6_mask) >> 5) + int((byte1 & bit_4_mask) >> 3) + int((byte1 & bit_2_mask) >> 1)) % 2
        par2 = (int((byte1 & bit_6_mask) >> 5) + int((byte1 & bit_3_mask) >> 2) + int((byte1 & bit_2_mask) >> 1)) % 2
        par3 = (int((byte1 & bit_4_mask) >> 3) + int((byte1 & bit_3_mask) >> 2) + int((byte1 & bit_2_mask) >> 1)) % 2

        if par1 > 0:
            byte1 |= bit_8_mask
        if par2 > 0:
            byte1 |= bit_7_mask
        if par3 > 0:
            byte1 |= bit_5_mask

        par1 = (int((byte2 & bit_6_mask) >> 5) + int((byte2 & bit_4_mask) >> 3) + int((byte2 & bit_2_mask) >> 1)) % 2
        par2 = (int((byte2 & bit_6_mask) >> 5) + int((byte2 & bit_3_mask) >> 2) + int((byte2 & bit_2_mask) >> 1)) % 2
        par3 = (int((byte2 & bit_4_mask) >> 3) + int((byte2 & bit_3_mask) >> 2) + int((byte2 & bit_2_mask) >> 1)) % 2

        if par1 > 0:
            byte2 |= bit_8_mask
        if par2 > 0:
            byte2 |= bit_7_mask
        if par3 > 0:
            byte2 |= bit_5_mask


        buffer.append(bytes([byte1]))
        buffer.append(bytes([byte2]))
        if len(buffer) >= 4:
            yield buffer[buffer_order[0]]
            yield buffer[buffer_order[1]]
            yield buffer[buffer_order[2]]
            yield buffer[buffer_order[3]]
            buffer.clear()

    # TODO: padding case:
    if len(buffer) != 0:
        while (len(buffer) != 4):
            buffer.append(bytes(1))
        yield buffer[buffer_order[0]]
        yield buffer[buffer_order[1]]
        yield buffer[buffer_order[2]]
        yield buffer[buffer_order[3]]
        buffer.clear()


def fix_byte(input_number) -> int:
    result_number = 0

    p1 = (input_number & bit_8_mask) >> 7
    p2 = (input_number & bit_7_mask) >> 6
    c3 = (input_number & bit_6_mask) >> 5
    p4 = (input_number & bit_5_mask) >> 4
    c5 = (input_number & bit_4_mask) >> 3
    c6 = (input_number & bit_3_mask) >> 2
    c7 = (input_number & bit_2_mask) >> 1

    s1 = False if (p1 + c3 + c5 + c7) % 2 == 0 else True
    s2 = False if (p2 + c3 + c6 + c7) % 2 == 0 else True
    s3 = False if (p4 + c5 + c6 + c7) % 2 == 0 else True

    # fix errors
    if s1:
        if s2:
            if s3:
                c7 = (c7 + 1) % 2
            else:
                c3 = (c3 + 1) % 2
        else:
            if s3:
                c5 = (c5 + 1) % 2
            else:
                p1 = (p1 + 1) % 2
    else:
        if s2:
            if s3:
                c6 = (c6 + 1) % 2
            else:
                p2 = (p2 + 1) % 2
        else:
            if s3:
                p4 = (p4 + 1) % 2


    result_number = p1 * 128 + p2 + 64 + c3 * 32 + p4 * 16 + c5 * 8 + c6 * 4 + c7 * 2

    return result_number

def reconstructFromBytes(byte1, byte2) -> bytes:
    number1 = fix_byte(byte1[0])
    number2 = fix_byte(byte2[0])
    byte_result= int('00000000', 2)
    byte_result |= (number1 & bit_6_mask) << 2
    byte_result |= (number1 & bit_4_mask) << 3
    byte_result |= (number1 & bit_3_mask) << 3
    byte_result |= (number1 & bit_2_mask) << 3
    byte_result |= (number2 & bit_6_mask) >> 2
    byte_result |= (number2 & bit_4_mask) >> 1
    byte_result |= (number2 & bit_3_mask) >> 1
    byte_result |= (number2 & bit_2_mask) >> 1

    return bytes([byte_result])


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    byte_half = int('00000000', 2)
    buffer = []

    for byte in source:

        buffer.append(byte)

        if len(buffer) >= 4:
            yield reconstructFromBytes(buffer[buffer_order[0]], buffer[buffer_order[1]])
            yield reconstructFromBytes(buffer[buffer_order[2]], buffer[buffer_order[3]])
            buffer.clear()