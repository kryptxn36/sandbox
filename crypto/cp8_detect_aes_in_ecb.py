from func_stash import detect_ecb
with open(r'.\assets\cryptopals\8.txt', 'r') as f:
    data = []
    for line in f.readlines():
        data.append(line.strip())

target = detect_ecb(data)
print(target)