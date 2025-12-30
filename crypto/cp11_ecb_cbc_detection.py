from func_stash import encryption_oracle, detect_ecb_cbc

def main():
    plaintext = b"A" * 128
    for i in range(24):
        ciphertext = encryption_oracle(plaintext)
        print(detect_ecb_cbc(ciphertext))

if __name__ == "__main__":
    main()
