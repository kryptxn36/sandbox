from func_stash import detect_ecb
import os
with open(f'{os.path.join("assets", "cryptopals", "8.txt")}', 'r') as f:
    data = []
    for line in f.readlines():
        data.append(line.strip())

target = detect_ecb(data)
print(target)
