from base64 import b64decode
from func_stash import aes_ecb_dec

with open(r'.\assets\cryptopals\7.txt', 'r') as f:
    data = ''
    for line in f.readlines():
        data += line.strip()
    data = b64decode(data)
print(data)
key = b"YELLOW SUBMARINE"

plaintext = aes_ecb_dec(data, key)
print(plaintext)