def pack_left_shift_u16(value, shift, mask):
    return int((value << shift) & mask)

def pack_right_shift_u16(value, shift, mask):
    return int((value >> shift) & mask)

def pack_left_shift_u8(value, shift, mask):
    return int((value << shift) & mask)

def pack_right_shift_u8(value, shift, mask):
    return int((value >> shift) & mask)