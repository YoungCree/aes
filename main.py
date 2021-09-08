
# takes a state and uses ff_multiply() to perform the matrix multiplication
def mix_columns(state):
    # make a copy of state
    tmp = [row[:] for row in state]

    # perform matrix multiplication using ff_multiply()
    for i in range(4):
        state[0, i] = ff_multiply(0x02, tmp[0, i]) ^ ff_multiply(0x03, tmp[1, i]) ^ tmp[2, i] ^ tmp[3, i]
        state[1, i] = tmp[0, i] ^ ff_multiply(0x02, tmp[1, i]) ^ ff_multiply(0x03, tmp[2, i]) ^ tmp[3, i]
        state[2, i] = tmp[0, i] ^ tmp[1, i] ^ ff_multiply(0x02, tmp[2, i]) ^ ff_multiply(0x03, tmp[3, i])
        state[3, i] = ff_multiply(0x03, tmp[0, i]) ^ tmp[1, i] ^ tmp[2, i] ^ ff_multiply(0x02, tmp[3, i])
    
    
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
            adds.append(times)
        
        bit = bit << 1

    # xor (add) the xtime vals (found above) together
    ret = adds[0]
    for i in range(1, len(adds)):
        ret = ret ^ adds[i]


    return ret


def main():
    
    
    return 0 
