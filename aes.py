import copy
import sys

# public vals
r_con = [  "00000000", 
           "01000000", "02000000", "04000000", "08000000", 
           "10000000", "20000000", "40000000", "80000000", 
           "1B000000", "36000000", "6C000000", "D8000000", 
           "AB000000", "4D000000", "9A000000", "2F000000", 
           "5E000000", "BC000000", "63000000", "C6000000", 
           "97000000", "35000000", "6A000000", "D4000000", 
           "B3000000", "7D000000", "FA000000", "EF000000", 
           "C5000000", "91000000", "39000000", "72000000", 
           "E4000000", "D3000000", "BD000000", "61000000", 
           "C2000000", "9F000000", "25000000", "4A000000", 
           "94000000", "33000000", "66000000", "CC000000", 
           "83000000", "1D000000", "3A000000", "74000000", 
           "E8000000", "CB000000", "8D000000"]

s_box = [
    [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76 ] ,
    [ 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0 ] ,
    [ 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15 ] ,
    [ 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75 ] ,
    [ 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84 ] ,
    [ 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf ] ,
    [ 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8 ] ,
    [ 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2 ] ,
    [ 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73 ] ,
    [ 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb ] ,
    [ 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79 ] ,
    [ 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08 ] ,
    [ 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a ] ,
    [ 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e ] ,
    [ 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf ] ,
    [ 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 ]
    ]

inv_s_box = [
    [ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb ] ,
    [ 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb ] ,
    [ 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e ] ,
    [ 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 ] ,
    [ 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92 ] ,
    [ 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 ] ,
    [ 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06 ] ,
    [ 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b ] ,
    [ 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73 ] ,
    [ 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e ] ,
    [ 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ] ,
    [ 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4 ] ,
    [ 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f ] ,
    [ 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef ] ,
    [ 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 ] ,
    [ 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d ]
    ]

nr = 10 #changes based on key length
nb = 4
nk = 4 #changes

# vars for testing
test_key = [ 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c ]

test_expanded = [ "0x2b7e1516", "0x28aed2a6", "0xabf71588", "0x09cf4f3c",
                "0xa0fafe17", "0x88542cb1", "0x23a33939", "0x2a6c7605",
                "0xf2c295f2", "0x7a96b943", "0x5935807a", "0x7359f67f",
                "0x3d80477d", "0x4716fe3e", "0x1e237e44", "0x6d7a883b",
                "0xef44a541", "0xa8525b7f", "0xb671253b", "0xdb0bad00",
                "0xd4d1c6f8", "0x7c839d87", "0xcaf2b8bc", "0x11f915bc",
                "0x6d88a37a", "0x110b3efd", "0xdbf98641", "0xca0093fd",
                "0x4e54f70e", "0x5f5fc9f3", "0x84a64fb2", "0x4ea6dc4f",
                "0xead27321", "0xb58dbad2", "0x312bf560", "0x7f8d292f",
                "0xac7766f3", "0x19fadc21", "0x28d12941", "0x575c006e",
                "0xd014f9a8", "0xc9ee2589", "0xe13f0cc8", "0xb6630ca6" ]

test_w = [None] * (nb * (nr+1))

test_state = [[0x19,0xa0,0x9a,0xe9],
                [0x3d,0xf4,0xc6,0xf8],
                [0xe3,0xe2,0x8d,0x48],
                [0xbe,0x2b,0x2a,0x08]]

test_inn = [ 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d,
                    0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 ]

# functions...

# takes a state and uses ff_multiply() to perform the matrix multiplication
def mix_columns(state):
    # make a copy of state
    tmp = copy.deepcopy(state)

    # perform matrix multiplication using ff_multiply()
    for i in range(4):
        state[0][i] = ff_multiply(0x02, tmp[0][i]) ^ ff_multiply(0x03, tmp[1][i]) ^ tmp[2][i] ^ tmp[3][i]
        state[1][i] = tmp[0][i] ^ ff_multiply(0x02, tmp[1][i]) ^ ff_multiply(0x03, tmp[2][i]) ^ tmp[3][i]
        state[2][i] = tmp[0][i] ^ tmp[1][i] ^ ff_multiply(0x02, tmp[2][i]) ^ ff_multiply(0x03, tmp[3][i])
        state[3][i] = ff_multiply(0x03, tmp[0][i]) ^ tmp[1][i] ^ tmp[2][i] ^ ff_multiply(0x02, tmp[3][i])
    
    
    return state


# takes in a finite field (ff) and multiplies it by {02}, subtracting if necessary
# to keep it in range
def xtime(ff):
    isOverflow = False

    # if leading bit is 1, we will have to subtract
    if ff & (0x01 << 7) == 0x80:
        isOverflow = True

    # left shift (multiply by {02})
    ff = ff << 1

    # conditional xor (subtraction to get in range)
    if isOverflow:
        ff = ff ^ 0x11b 

    return ff


# takes in finite fields (a, b) and multiplies them together using xtime() and XOR
def ff_multiply(a, b):
    bit = 0x01
    times = list()
    times.append(a)
    adds = list()

    # calculate all xtimes for a
    for i in range(7):
        times.append(xtime(times[i]))

    # add needed xtime vals to a list
    for val in times:
        if b & bit == bit:
            adds.append(val)
        
        bit = bit << 1

    # xor (add) the xtime vals (found above) together
    if len(adds) > 0:
        ret = adds[0]
    else:
        return 0
    for i in range(1, len(adds)):
        ret = ret ^ adds[i]


    return ret


def sub_word(word):
    for i in range(len(word)):
        tmp = word[i]
        word[i] = s_box[tmp >> 4][tmp & 0x0f]

    return word


def rot_word(word):
    tmp_front = word[0]
    #print(tmp_front)
    #print(len(word))
    for i in range(len(word) - 1):
        word[i] = word[i+1]

    word[3] = tmp_front


    return word


def xor_bytearr(a, b):
    c = bytearray()
    for i in range(len(a)):
        c.append(a[i] ^ b[i])

    return c


# n = 4 in our case
def key_expansion(key, w, n=4):
    for i in range(n):
        w[i] = bytearray([key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]])

    for i in range(n, len(w)):
        temp = copy.deepcopy(w[i-1])
        if i % n == 0:
            temp = xor_bytearr(sub_word(rot_word(temp)), bytearray.fromhex(r_con[i//n]))
        elif n > 6 and i % n == 4:
            temp = sub_word(temp)
        
        w[i] = xor_bytearr(w[i-n], temp)

    return w


def sub_bytes(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            tmp = state[i][j]
            state[i][j] = s_box[tmp >> 4][tmp & 0x0f]

    return state


def shift_rows(state):
    for i in range(1, len(state)):
        tmp = copy.copy(state[i])
        for j in range(len(state[i])):
            if (j + i) >= len(state[i]):
                state[i][j] = tmp[j+i-len(state[i])]
            else:
                state[i][j] = tmp[j+i]

    return state   


def add_round_key(state, w):
    for i in range(len(state)):
        for j in range(len(state[i])):
            state[i][j] = state[i][j] ^ w[j][i]

    return state


def cipher(inn, w, in_key_size):
    state = copy.deepcopy(inn)

    if in_key_size == "128":
        nk = 4
        nr = 10
    elif in_key_size == "192":
        nk = 6
        nr = 12
    elif in_key_size == "256":
        nk = 8
        nr = 14

    print("round 0: ")
    print_hex_pretty(state)

    add_round_key(state, w[0:nb])
    print("round 0 add_round_key: ")
    print_hex_pretty(state)


    for i in range(1, nr):
        sub_bytes(state)
        print("round {} sub_bytes: ".format(i))
        print_hex_pretty(state)

        shift_rows(state)
        print("round {} shift_rows: ".format(i))
        print_hex_pretty(state)

        mix_columns(state)
        print("round {} mix_columns: ".format(i))
        print_hex_pretty(state)

        add_round_key(state, w[i*nb:(i+1)*nb])
        print("round {} add_round_key: ".format(i))
        print_hex_pretty(state)

    sub_bytes(state)
    print("round {} sub_bytes: ".format(nr))
    print_hex_pretty(state)

    shift_rows(state)
    print("round {} shift_rows: ".format(nr))
    print_hex_pretty(state)

    add_round_key(state, w[nr*nb:(nr+1)*nb])
    print("round {} add_round_key: ".format(nr))
    print_hex_pretty(state)

    out = state

    return out


def inv_mix_columns(state):
    # make a copy of state
    tmp = copy.deepcopy(state)

    # perform matrix multiplication using ff_multiply()
    for i in range(4):
        state[0][i] = ff_multiply(0x0e, tmp[0][i]) ^ ff_multiply(0x0b, tmp[1][i]) ^ ff_multiply(0x0d, tmp[2][i]) ^ ff_multiply(0x09, tmp[3][i])
        state[1][i] = ff_multiply(0x09, tmp[0][i]) ^ ff_multiply(0x0e, tmp[1][i]) ^ ff_multiply(0x0b, tmp[2][i]) ^ ff_multiply(0x0d, tmp[3][i])
        state[2][i] = ff_multiply(0x0d, tmp[0][i]) ^ ff_multiply(0x09, tmp[1][i]) ^ ff_multiply(0x0e, tmp[2][i]) ^ ff_multiply(0x0b, tmp[3][i])
        state[3][i] = ff_multiply(0x0b, tmp[0][i]) ^ ff_multiply(0x0d, tmp[1][i]) ^ ff_multiply(0x09, tmp[2][i]) ^ ff_multiply(0x0e, tmp[3][i])
    
    
    return state


def inv_shift_rows(state):
    for i in range(1, len(state)):
        tmp = copy.copy(state[i])
        for j in range(len(state[i])-1, -1, -1):
            if (j - i) < 0:
                state[i][j] = tmp[len(state) - i + j]
            else:
                state[i][j] = tmp[j-i]

    return state   


def inv_sub_bytes(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            tmp = state[i][j]
            state[i][j] = inv_s_box[tmp >> 4][tmp & 0x0f]

    return state


def inv_cipher(inn, w, in_key_size):
    state = copy.deepcopy(inn)

    if in_key_size == "128":
        nk = 4
        nr = 10
    elif in_key_size == "192":
        nk = 6
        nr = 12
    elif in_key_size == "256":
        nk = 8
        nr = 14

    print("round 0: ")
    print_hex_pretty(state)

    add_round_key(state, w[nr*nb:(nr+1)*nb])
    print("round 0 add_round_key: ")
    print_hex_pretty(state)

    for i in range(nr-1, 0, -1):
        inv_shift_rows(state)
        print("round {} inv_shift_rows: ".format(i))
        print_hex_pretty(state)

        inv_sub_bytes(state)
        print("round {} inv_sub_bytes: ".format(i))
        print_hex_pretty(state)

        add_round_key(state, w[i*nb:(i+1)*nb])
        print("round {} add_round_key: ".format(i))
        print_hex_pretty(state)

        inv_mix_columns(state)
        print("round {} inv_mix_columns: ".format(i))
        print_hex_pretty(state)

    inv_shift_rows(state)
    print("round {} inv_shift_rows: ".format(nr))
    print_hex_pretty(state)

    inv_sub_bytes(state)
    print("round {} inv_sub_bytes: ".format(nr))
    print_hex_pretty(state)

    add_round_key(state, w[0:nb])
    print("round {} add_round_key: ".format(nr))
    print_hex_pretty(state)

    out = state

    return out


def print_state(state):
    print("current state:\n")
    for i in range(len(state)):
        for j in range(len(state[i])):
            print(state[i][j])

    print("\n\n")


def print_hex_pretty(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            print(str(hex(state[j][i]).split('x')[-1]).zfill(2), end="")

    print("\n")


def test_cases():
    # byarr = bytearray()
    # byarr.append(0x40)
    # byarr.append(0x50)
    # byarr.append(0x60)
    # byarr.append(0x70)

    # print(byarr.hex())
    # print(sub_word(byarr).hex())

    # help = bytearray.fromhex(r_con[2])
    # help2 = bytearray.fromhex("09cf4f3c")
    # xor = xor_bytearr(help, help2)
    # print("xored hex: \n")
    # print(xor.hex())
    # print("bytearray to hex: \n")
    # print(help.hex())

    # print("given: \n")
    # print(test_expanded)
    # print("new: \n")
    # new_key = key_expansion(test_key, test_w)
    # for key in new_key:
    #     print(key.hex())

    # print("sub_bytes_test: \n")
    # new_state = sub_bytes(test_state)
    # for i in range(len(new_state)):
    #     for j in range(len(new_state[i])):
    #         print(new_state[i][j])

    # print("shift_bytes_test: \n")
    # new_state = shift_rows(new_state)
    # for i in range(len(new_state)):
    #     for j in range(len(new_state[i])):
    #         print(new_state[i][j])

    # print("mix_columns_test: \n")
    # new_state = mix_columns(new_state)
    # for i in range(len(new_state)):
    #     for j in range(len(new_state[i])):
    #         print(new_state[i][j])

    # print("round_key_test after first round: \n")
    # newer_state = add_round_key(new_state, new_key[4:8])
    # for i in range(len(newer_state)):
    #     for j in range(len(newer_state[i])):
    #         print(newer_state[i][j])

    print("testing cipher: \n")
    w = key_expansion(test_key, test_w)
    state = [[0 for i in range(4)] for j in range(4)]
    print_state(state)
    k = 0
    for col in range(len(state)):
        for row in range(len(state[col])):
            state[row][col] = test_inn[k]
            k = k + 1

    result = cipher(state, w)
    for i in range(len(result)):
        for j in range(len(result[i])):
            print(result[i][j])


def main():
    in_user = input("Enter text to encrypt or decrypt: ")
    in_key = input("Enter your key: ")
    in_key_size = input("Enter the size of your key (128, 192, 256): ")
    is_encrypt = input("Enter (e) to encrypt, (d) to decrypt: ")

    in_array = bytes.fromhex(in_user)
    in_key_array = bytes.fromhex(in_key)

    if in_key_size == "128":
        nk = 4
        nr = 10
    elif in_key_size == "192":
        nk = 6
        nr = 12
    elif in_key_size == "256":
        nk = 8
        nr = 14

    test_w = [None] * (nb * (nr+1))
    w = key_expansion(in_key_array, test_w, nk)

    state = [[0 for i in range(4)] for j in range(4)]
    k = 0
    for col in range(len(state)):
        for row in range(len(state[col])):
            state[row][col] = in_array[k]
            k = k + 1

    if is_encrypt == "e":
        result = cipher(state, w, in_key_size)
    else:
        result = inv_cipher(state, w, in_key_size)

    print("result: ")
    print_hex_pretty(result)


if __name__=="__main__":
    main()
