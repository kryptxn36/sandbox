from func_stash import ecb, keygen, detect_ecb_cbc
from base64 import b64decode

key = keygen(16)
unknown =\
b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def encryption_oracle(input):
    global key, unknown
    ct = ecb("encrypt", input + unknown, key)
    return ct

def get_block_size(oracle_function):
    payload = b"A"
    ct = oracle_function(payload)
    init_len = len(ct)

    while init_len == len(ct):
        payload += b"A"
        ct = encryption_oracle(payload)
    block_size = (len(ct) - init_len) // 2 # output format is hex so division by 2 is required
    return block_size

def byte_at_a_time_decryption(oracle_function):
    block_size = get_block_size(oracle_function)
    pt = []

    payload = b"A" * (block_size - 1)
    ct1 = oracle_function(payload)

    for b in range(256):
        payload = b"A" * (block_size - 1) + b.to_bytes()
        ct = oracle_function(payload)
        if ct[:32] == ct1[:32]:
            #print(b.to_bytes())
            pt.append(b)
            break

    start = 0
    end = 32
    for i in range(1, len(unknown)):
        if not (i % 16):
            start += 32
            end += 32
        else:
            pass
        scope = slice(start, end)
        payload = b"A" * (block_size - (1 + i % block_size))
        ct1 = oracle_function(payload)

        for b in range(256):
            payload = b"A" * (block_size - (1 + i % block_size)) + bytes(pt) + b.to_bytes()
            ct = oracle_function(payload)
            if ct[scope] == ct1[scope]:
                #print(b.to_bytes())
                pt.append(b)
                break
    pt = bytes(pt)
    return pt

def main():
    plaintext = byte_at_a_time_decryption(encryption_oracle)
    print(plaintext)

if __name__ == "__main__":
    main()
