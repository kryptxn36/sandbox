from func_stash import pkcs7_padding

s = b'YELLOW SUBMARINE'
block_size = 20
padded = pkcs7_padding('pad', s, block_size)
print(padded)