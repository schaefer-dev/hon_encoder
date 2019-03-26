from typing import List, Generator

bit_1_mask = int('00000001', 2)
bit_2_mask = int('00000010', 2)
bit_3_mask = int('00000100', 2)
bit_4_mask = int('00001000', 2)
bit_5_mask = int('00010000', 2)
bit_6_mask = int('00100000', 2)
bit_7_mask = int('01000000', 2)
bit_8_mask = int('10000000', 2)

def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:

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

        yield bytes([byte1])
        yield bytes([byte2])


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


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    byte_half = int('00000000', 2)
    byte_stored = False

    for byte in source:
        number = byte[0]

        if not byte_stored:
            # Read first byte
            number = fix_byte(number)

            byte_half = int('00000000', 2)
            byte_half |= (number & bit_6_mask) << 2
            byte_half |= (number & bit_4_mask) << 3
            byte_half |= (number & bit_3_mask) << 3
            byte_half |= (number & bit_2_mask) << 3

            par1 = (number & bit_8_mask) << 7
            par2 = (number & bit_7_mask) << 6
            par3 = (number & bit_5_mask) << 4

            # TODO: correct errors using parity bits here
            byte_stored = True
        else:
            # Read second byte
            number = fix_byte(number)

            byte_half |= (number & bit_6_mask) >> 2
            byte_half |= (number & bit_4_mask) >> 1
            byte_half |= (number & bit_3_mask) >> 1
            byte_half |= (number & bit_2_mask) >> 1

            # TODO: correct errors using parity bits here

            byte_stored = False
            yield bytes([byte_half])
