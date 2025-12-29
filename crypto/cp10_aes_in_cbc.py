from aes import cbc
from base64 import b64decode
import os

def main():
    with open(f'{os.path.join("assets", "cryptopals", "10.txt")}') as f:
        ciphertext = f.read()
    ciphertext = b64decode(ciphertext)
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * 16
    plaintext = cbc("decrypt", ciphertext, iv, key)
    print(plaintext)

if __name__ == "__main__":
    main()
