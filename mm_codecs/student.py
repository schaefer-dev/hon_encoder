from typing import List, Generator


def mm_encode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    bit_1_mask = int('00000001', 2)
    bit_2_mask = int('00000010', 2)
    bit_3_mask = int('00000100', 2)
    bit_4_mask = int('00001000', 2)
    bit_5_mask = int('00010000', 2)
    bit_6_mask = int('00100000', 2)
    bit_7_mask = int('01000000', 2)
    bit_8_mask = int('10000000', 2)

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


def mm_decode(source: Generator[bytes, None, None]) -> Generator[bytes, None, None]:
    byte_half = int('00000000', 2)
    byte_stored = False

    bit_1_mask = int('00000001', 2)
    bit_2_mask = int('00000010', 2)
    bit_3_mask = int('00000100', 2)
    bit_4_mask = int('00001000', 2)
    bit_5_mask = int('00010000', 2)
    bit_6_mask = int('00100000', 2)
    bit_7_mask = int('01000000', 2)
    bit_8_mask = int('10000000', 2)

    for byte in source:
        number = byte[0]

        if not byte_stored:
            # Read first byte
            byte_half = int('00000000', 2)
            byte_half |= (number & bit_6_mask) << 2
            byte_half |= (number & bit_4_mask) << 3
            byte_half |= (number & bit_3_mask) << 3
            byte_half |= (number & bit_2_mask) << 3

            # TODO: correct errors using parity bits here
            byte_stored = True
        else:
            # Read second byte
            byte_half |= (number & bit_6_mask) >> 2
            byte_half |= (number & bit_4_mask) >> 1
            byte_half |= (number & bit_3_mask) >> 1
            byte_half |= (number & bit_2_mask) >> 1

            byte_stored = False
            yield bytes([byte_half])
