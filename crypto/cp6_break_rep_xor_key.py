from func_stash import xor_find_key, transpose, xor_calc_keysize, repeating_key_xor
from base64 import b64decode

with open(r'.\assets\cryptopals\6.txt', 'r') as f:
    data_concat = b''
    for line in f.readlines():
        data_concat += b64decode(line)

keysize = xor_calc_keysize(data_concat, 2, 40)

data_split = []
for i in range(0, len(data_concat), keysize):
    data_split.append(data_concat[i:i+keysize])
data_transp = transpose(data_split, keysize)
key = xor_find_key(data_transp)

plaintext = repeating_key_xor(data_concat, key)
print(str(bytes.fromhex(plaintext)))
print(key)