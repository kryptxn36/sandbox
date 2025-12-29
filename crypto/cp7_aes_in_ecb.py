from base64 import b64decode
from aes import ecb
import os

with open(f'{os.path.join("assets", "cryptopals", "7.txt")}', 'r') as f:
    ciphertext = f.read()

ciphertext = b64decode(ciphertext)
key = b"YELLOW SUBMARINE"
plaintext = ecb("decrypt", ciphertext, key)
plaintext = bytes.fromhex(plaintext)
print(plaintext)
