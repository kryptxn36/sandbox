from func_stash import repeating_key_xor

plaintext = b"Burning 'em, if you ain't quick and nimble\n\
I go crazy when I hear a cymbal"
key = b"ICE"
ciphertext = repeating_key_xor(plaintext, key)

print(ciphertext)
