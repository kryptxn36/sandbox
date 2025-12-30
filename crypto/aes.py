N = 10
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

def b2m(state: bytes) -> list | None:
    if type(state) is bytes:
        state = [state[i:i+16] for i in range(0, len(state), 16)]
        mtx = []
        state = list(state)
        for block in state:
            block = list(block)
            mtx.append([block[i:i+4] for i in range(0, 16, 4)])
        if len(mtx) > 1:
            return mtx
        elif len(mtx) == 1:
            return mtx[0]
    else: raise(TypeError(f"{type(state)} is not valid."))

def m2b(state: list) -> bytes:
    b = b''
    for block in state:
        for i in range(4):
            for j in range(4):
                element = hex(block[i][j])[2:].zfill(2)
                b += bytes.fromhex(element)
    return b

def m2h(s: list) -> list:
    s = [col[:] for col in s]
    hex_mtx = []
    for block in s:
        for i in range(4):
            for j in range(4):
                block[i][j] = hex(block[i][j])[2:].zfill(2)
        hex_mtx.append(block)
    return hex_mtx

def add_round_key(state: list, k: list) -> list:
    state = [col[:] for col in state]

    for i in range(4):
        for j in range(4):
            state[i][j] ^= k[i][j]
    return state

def sub_bytes(state: list, sbox=s_box) -> list:
    state = [col[:] for col in state]
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j]]
    return state

def shift_rows(state: list):
    state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]

def inv_shift_rows(state):
    for _ in range(3):
        shift_rows(state)

def gmul(a: int, b: int) -> int:
    p = 0
    hi_bit_set = 0
    for _ in range(8):
        if b & 1 == 1:
            p ^= a
        hi_bit_set = a & 0x80
        a = a << 1
        if hi_bit_set == 0x80:
            a ^= 0x1b
        b = b >> 1
    return p & 0xFF

def mix_columns(state: list, mode:str ="normal") -> list:
    state = [col[:] for col in state]
    for i in range(4):
        a0 = state[i][0]
        a1 = state[i][1]
        a2 = state[i][2]
        a3 = state[i][3]
        if mode == "normal":
            state[i][0] = gmul(a0, 2) ^ gmul(a1, 3) ^ gmul(a2, 1) ^ gmul(a3, 1)
            state[i][1] = gmul(a0, 1) ^ gmul(a1, 2) ^ gmul(a2, 3) ^ gmul(a3, 1)
            state[i][2] = gmul(a0, 1) ^ gmul(a1, 1) ^ gmul(a2, 2) ^ gmul(a3, 3)
            state[i][3] = gmul(a0, 3) ^ gmul(a1, 1) ^ gmul(a2, 1) ^ gmul(a3, 2)
        else:
            state[i][0] = gmul(a0, 14) ^ gmul(a1, 11) ^ gmul(a2, 13) ^ gmul(a3, 9)
            state[i][1] = gmul(a0, 9) ^ gmul(a1, 14) ^ gmul(a2, 11) ^ gmul(a3, 13)
            state[i][2] = gmul(a0, 13) ^ gmul(a1, 9) ^ gmul(a2, 14) ^ gmul(a3, 11)
            state[i][3] = gmul(a0, 11) ^ gmul(a1, 13) ^ gmul(a2, 9) ^ gmul(a3, 14)
            
    return state

def g(k: list, r: int) -> list:
    k = [col[:] for col in k]

    rcons = (0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 
            0x20, 0x40, 0x80, 0x1b, 0x36)

    'rotword'
    k[3][0], k[3][1], k[3][2], k[3][3] =\
    k[3][1], k[3][2], k[3][3], k[3][0]

    'subword'
    k = sub_bytes(k)

    'rcon'
    k[3][0] ^= rcons[r]
    return k

def key_expansion(k: list, r: int) -> list:
    k = [col[:] for col in k]
    w3 = g(k, r)[3]

    k[0][0], k[0][1], k[0][2], k[0][3] =\
    k[0][0] ^ w3[0], k[0][1] ^ w3[1], k[0][2] ^ w3[2], k[0][3] ^ w3[3]

    for i in range(1, 4):
        k[i][0], k[i][1], k[i][2], k[i][3] =\
        k[i][0] ^ k[i-1][0], k[i][1] ^ k[i-1][1], k[i][2] ^ k[i-1][2], k[i][3] ^ k[i-1][3]

    return k

def tohex(s: list) -> str:
    s = [col[:] for col in s]
    s = m2h(s)
    hexstring = ""
    for block in s:
        for i in block:
            for j in i:
                hexstring += j
    return hexstring

def tobytes(s: list) -> bytes:
    s = [col[:] for col in s]
    s = m2h(s)
    bytestring = b""
    for block in s:
        for i in block:
            for j in i:
                bytestring += bytes.fromhex(j)
    return bytestring

def pkcs7_padding(mode: str, data: bytes | str, block_size: int):
    if type(data) is str:
        data = data.encode()
    elif type(data) is bytes:
        pass
    else:
        raise(TypeError(f"{type(data)} is not valid."))
    l = [bytes([x]) for x in range(block_size)]
    data_length = len(data)
    if mode == 'pad':
        if data_length % block_size == 0:
            return data + bytes.fromhex(hex(block_size)[2:].zfill(2)) * block_size
        else:
            pad_value = block_size - data_length % block_size
            padded = data + l[pad_value] * pad_value
            return padded
    elif mode == 'unpad':
        pad_value = data[-1]
        return data[:-pad_value]

def encrypt(pt, k) -> list:
    pt = b2m(pt)
    k = b2m(k)[0]

    pt = add_round_key(pt, k)
    pt = sub_bytes(pt)
    shift_rows(pt)
    pt = mix_columns(pt)
    k = key_expansion(k, 1)
    pt = add_round_key(pt, k)

    for r in range(2, N):
        pt = sub_bytes(pt)
        shift_rows(pt)
        pt = mix_columns(pt)
        k = key_expansion(k, r)
        pt = add_round_key(pt, k)
    pt = sub_bytes(pt)
    shift_rows(pt)
    k = key_expansion(k, N)
    ct = add_round_key(pt, k)
    return ct

def decrypt(ct, k) -> list:
    ct = b2m(ct)
    k = b2m(k)[0]
    k_list = [k]

    for i in range(1, N + 1):
        k = key_expansion(k, i)
        k_list.append(k)

    ct = add_round_key(ct, k_list[-1])

    for r in range(2, N+1):
        k = k_list[-r]
        inv_shift_rows(ct)
        ct = sub_bytes(ct, inv_s_box)
        ct = add_round_key(ct, k)
        ct = mix_columns(ct, "inverse")

    inv_shift_rows(ct)
    ct = sub_bytes(ct, inv_s_box)
    pt = add_round_key(ct, k_list[0])
    return pt

def ecb(mode: str, data: bytes, k: bytes) -> str | bytes: 
    if mode == "encrypt":
        pt = data
        pt = pkcs7_padding("pad", pt, 16)
        k = pkcs7_padding("pad", k, 16)
        pt = [pt[i:i+16] for i in range(0, len(pt), 16)]
        ct = []
        for block in pt:
            ct.append(encrypt(block, k))
        ct = tohex(ct)
        return ct
    elif mode == "decrypt":
        ct = data
        ct = [ct[i:i+16] for i in range(0, len(ct), 16)]
        k = pkcs7_padding("pad", k, 16)
        pt = []
        for block in ct:
            pt.append(decrypt(block, k))
        pt = tohex(pt)
        pt = bytes.fromhex(pt) 
        pt = pkcs7_padding("unpad", pt, 16)
        return pt

def cbc(mode: str, data: bytes, iv: bytes, k: bytes) -> str:
    if mode == "encrypt":
        pt = data
        iv = b2m(iv)
        pt = pkcs7_padding("pad", pt, 16)
        k = pkcs7_padding("pad", k, 16)
        pt = [pt[i:i+16] for i in range(0, len(pt), 16)]
        ct = []
        pt_init = b2m(pt[0])
        pt_init = add_round_key(pt_init, iv)
        pt_init = bytes.fromhex(tohex([pt_init]))
        ct_init = encrypt(pt_init, k)
        ct.append(ct_init)
        for i in range(1, len(pt)):
            ct_block = add_round_key(b2m(pt[i]), ct[i - 1])
            ct_block = tobytes([ct_block])
            ct_block = encrypt(ct_block, k)
            ct.append(ct_block)
        ct = tohex(ct)
        return ct

    elif mode == "decrypt":
        ct = data
        iv = b2m(iv)
        k = pkcs7_padding("pad", k, 16)
        ct = [ct[i:i+16] for i in range(0, len(ct), 16)]
        pt = []

        for i in range(len(ct)):
            pt_block = decrypt(ct[i], k)
            pt_block = add_round_key(pt_block, iv)
            iv = b2m(ct[i])
            pt.append(pt_block)
        pt = tohex(pt)
        pt = bytes.fromhex(pt)
        pt = pkcs7_padding("unpad", pt, 16)
        return pt

def main():
    pass

if __name__ == '__main__':
    main()
