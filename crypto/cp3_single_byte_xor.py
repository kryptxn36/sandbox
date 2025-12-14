from func_stash import single_byte_xor
def main():    
    ciphertext = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    ciphertext = bytes.fromhex(ciphertext)
    plaintext = single_byte_xor(ciphertext)
    print(plaintext)
    pass

if __name__ == '__main__':
    main()