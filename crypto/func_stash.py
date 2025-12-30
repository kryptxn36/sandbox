from math import gcd, sqrt
from random import randint
from aes import ecb, cbc
import base64

def phi(n: int):
    count = 0
    for i in range(n):
        if gcd(i, n) == 1:
            count += 1
        else:
            continue
    return count

def hex2b64(a):
    a = bytes.fromhex(a)
    a = base64.b64encode(a)
    return a

def xor(a, b):
    if type(a) and type(b) is not bytes:
        a, b = bytes.fromhex(a), bytes.fromhex(b)
    r = bytes([x ^ y for x, y in zip(a, b)])
    r = r.hex()
    return r

def repeating_key_xor(pt, k): 
    if type(pt) is str:
        pt = pt.encode()
    if type(k) is str:
        k = k.encode() 
    ct = bytes([pt[i] ^ k[i % len(k)] for i in range(len(pt))])
    return ct.hex()

def freq_analysis(t):
    stat = dict()
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    if type(t) is bytes:
        t = str(t)
    txt_size = len(t)
    for char in alphabet:
        c = t.count(char) / txt_size
        stat.update({f'{char}': c})
    return stat

occurance_eng = {
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}

def fq_counter(t):
    x_stat = freq_analysis(t)
    fq = 0
    for letter in occurance_eng:
        fq += abs(occurance_eng[f'{letter}'] - x_stat[f'{letter}'])
    fq /= len(t)
    return fq

def txt_score(txt):
    score = 0
    freq_list = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
    for c in txt:
        if c in freq_list:
            score += 1
    return score

def single_byte_xor(ct):
    last_score = 0
    max_score = 0

    for i in range(256):
        pt_candidate = bytes([ct[char] ^ i for char in range(len(ct))])
        pt_encoded = ('').join([chr(b) for b in pt_candidate])
        last_score = txt_score(pt_encoded)
        if last_score > max_score:
            pt = pt_candidate
            max_score = last_score
            k = i
    return pt, k

def detect_english(candidate_list):
    fq_min = None
    for c in candidate_list:
        fq = fq_counter(c)
        if fq_min is None or fq < fq_min:
            fq_min = fq
            pt = c
            return pt
    return None

def d_hamming(a: bytes, b: bytes):
    if type(a) is str:
        a = a.encode()
    a = list(map(bin, a))
    a = ''.join([i[2:].zfill(8) for i in a])
    
    if type(b) is str: 
        b = b.encode()
    b = list(map(bin, b))
    b = ''.join([i[2:].zfill(8) for i in b])
    
    if len(a) != len(b):
        max_length = max(len(a), len(b))
        if max_length == len(a):
            b = b.zfill(max_length)
        else:
            a = a.zfill(max_length)
    else:
        max_length = len(a)

    d = 0
    for i in range(max_length):
        if a[i] != b[i]:
            d += 1
        else:
            continue
    return d

def xor_calc_keysize(ct: bytes, bottom: int, top: int) -> int | None:
    d_histogram = {}
    for k in range(bottom, top + 1):
        block1 = ct[:4*k]
        block2 = ct[4*k:8*k]
        d = d_hamming(block1, block2) / k
        d_histogram.update({k: round(d, 4)})
    d_min = min(d_histogram.values())
    for x in d_histogram.items():
        if d_min == x[1]:
            keysize = x[0]
            return keysize
        else:
            continue
    return None

def transpose(data, size):
    data_transp = []
    for i in range(size):
        block = b''
        for b in data[:len(data) - 1]:
            b = bytes.fromhex(hex(b[i])[2:].zfill(2))
            block += b
        data_transp.append(block)
    return data_transp

def xor_find_key(data):
    key = ''
    for block in data:
        key += chr(single_byte_xor(block)[1])
    key = key.encode()
    return key

def detect_ecb(candidates: list):
    for c in candidates:
        buff = []
        for i in range(0, len(c), 32):
            block = c[i:i+32]
            buff.append(block)
            for item in buff:
                if buff.count(item) > 1:
                    return c
                else:
                    continue

def pkcs7_padding_scheme(mode: str, data: bytes | str, block_size: int):
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
    
def factor_fermat(n: int) -> tuple | None:
    m = int(sqrt(n))
    for x in range(n):
        q = (m + x) ** 2 - n
        if q > 0:
            if sqrt(q) * 10 % 10 == 0:
                b = int(sqrt(q))
                a = m + x
                p = a + b
                q = a - b
                return p, q
            else: continue
        else: continue
    return None

def factor_roh_pollard(n):
    x_prev = 1
    x_buff = []
    for _ in range(n):
        x_prev = pow(x_prev ** 2 + 1, 1, n)
        x_buff.append(x_prev)
        x = pow(x_prev ** 2 + 1, 1, n)
        for x_i in x_buff:
            d = gcd(abs(x - x_i), n)
            if d != 1 and abs(x-x_prev) != 1:
                p = d
                q = n // p
                return p, q
            else:
                continue

def mul(args: list):
    prod = 1
    for i in range(len(args)):
        prod *= args[i]
    return prod

def factor_p_1_pollard(n):
    b = 10
    p_list = []
    for i in range(b):
        if isPrime(i): p_list.append(i)
    for i in range(len(p_list)):
        for j in range(len(p_list)):
            candidate = p_list[i] ** j
            if candidate < b and candidate not in p_list: p_list.append(candidate)
            else: continue
    
    for i in range(2, 5):
        p_list.remove(i)

    m = mul(p_list)
    a = 2
    am = pow(a, m, n)
    p = gcd(n, am - 1)
    q = n // p
    return p, q, p_list

def genfold_shanks(a: int, b: int, p: int) -> int | None:
    m = int(sqrt(p)) + 1
    i_table = [pow(a ** (m * i), 1, p) for i in range(1, m + 1)]
    j_table = [pow(b * a ** j, 1, p) for j in range(0, m + 1)]
    for idx in range(len(i_table)):
        if i_table[idx] in j_table:
            i = idx + 1
            j = j_table.index(i_table[idx])
            x = m * i - j
            return x
        else: continue
    return None

def keygen(size) -> bytes:
    key = b""
    for _ in range(size):
        key += randint(0, 255).to_bytes(1, 'big')
    return key

def encryption_oracle(plaintext: bytes) -> str:
    key = keygen(16)
    apdx_size = randint(5, 10)
    apdx_value = randint(0, 255).to_bytes(1, "big")
    plaintext = apdx_value * apdx_size + plaintext + apdx_value * apdx_size
    case = randint(0, 1)
    if case == 0:
        ciphertext = ecb("encrypt", plaintext, key)
    else:
        iv = keygen(16)
        ciphertext = cbc("encrypt", plaintext, iv, key)
    return ciphertext

def detect_ecb_cbc(candidate) -> str:
    if detect_ecb([candidate]):
        return "ECB"
    else:
        return "CBC" 

def main():
    pass

if __name__ == '__main__':
    main()
