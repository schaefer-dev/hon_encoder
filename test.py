byte = int('10011001', 2)

# Index 0 will always remain empty!!!
byte_arr1 = [False] * 8
byte_arr2 = [False] * 8

byte1 = int('00000000', 2)
byte2 = int('00000000', 2)

bit_1_mask = int('00000001', 2)
bit_2_mask = int('00000010', 2)
bit_3_mask = int('00000100', 2)
bit_4_mask = int('00001000', 2)
bit_5_mask = int('00010000', 2)
bit_6_mask = int('00100000', 2)
bit_7_mask = int('01000000', 2)
bit_8_mask = int('10000000', 2)


byte1 |= (byte & bit_8_mask) >> 2
byte1 |= (byte & bit_7_mask) >> 3
byte1 |= (byte & bit_6_mask) >> 3
byte1 |= (byte & bit_5_mask) >> 3

byte2 |= (byte & bit_4_mask) << 2
byte2 |= (byte & bit_3_mask) << 1
byte2 |= (byte & bit_2_mask) << 1
byte2 |= (byte & bit_1_mask) << 1

print("byte1 before encoding: " + format(byte1,'08b'))

par1 = (int((byte1 & bit_6_mask) >> 5) + int((byte1 & bit_4_mask) >> 3) + int((byte1 & bit_2_mask) >> 1)) % 2
par2 = (int((byte1 & bit_6_mask) >> 5) + int((byte1 & bit_3_mask) >> 2) + int((byte1 & bit_2_mask) >> 1)) % 2
par3 = (int((byte1 & bit_4_mask) >> 3) + int((byte1 & bit_3_mask) >> 2) + int((byte1 & bit_2_mask) >> 1)) % 2

print("par1: " + str(par1))
print("par2: " + str(par2))
print("par3: " + str(par3))

if par1 > 0:
    byte1 |= bit_8_mask
if par2 > 0:
    byte1 |= bit_7_mask
if par3 > 0:
    byte1 |= bit_5_mask

# LSB will always be zero because we only get 7 bits from our encoding
print("byte1 after encoding: " + format(byte1,'08b'))

print("byte2 before encoding: " + format(byte2,'08b'))

par1 = (int((byte2 & bit_6_mask) >> 5) + int((byte2 & bit_4_mask) >> 3) + int((byte2 & bit_2_mask) >> 1)) % 2
par2 = (int((byte2 & bit_6_mask) >> 5) + int((byte2 & bit_3_mask) >> 2) + int((byte2 & bit_2_mask) >> 1)) % 2
par3 = (int((byte2 & bit_4_mask) >> 3) + int((byte2 & bit_3_mask) >> 2) + int((byte2 & bit_2_mask) >> 1)) % 2

if par1 > 0:
    byte2 |= bit_8_mask
if par2 > 0:
    byte2 |= bit_7_mask
if par3 > 0:
    byte2 |= bit_5_mask

# LSB will always be zero because we only get 7 bits from our encoding
print("byte2 after encoding: " + format(byte2,'08b'))