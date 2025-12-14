from func_stash import single_byte_xor, detect_english
path = 'D:\code'

with open(path + r'\chall\assets\cryptopals\4.txt', 'r') as f:
    data = []
    for line in f:
        data.append(line.strip())

def main():
    data_bytes = list(map(bytes.fromhex, data))
    pt_candidates = []
    for item in data_bytes:
        pt_candidates.append(single_byte_xor(item)[0])
    plaintext = detect_english(pt_candidates)
    print(plaintext)
    pass

if __name__ == '__main__':
    main()