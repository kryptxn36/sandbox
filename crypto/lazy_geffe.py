#!/usr/bin/python
import argparse
import re
import os
import subprocess

parser = argparse.ArgumentParser(
    prog="lazy_geffe",
    description="A program doing a routine of cracking a file\
    performing a basic Siegenthaler's attack on a Geffe generator.\
    But if you are using this program you already know what it does anyway.\
    Supported formats:\n\
    .pdf\n\
    .vsdx\n\
    .docx\n\
    .xlsx\n\
    .pptx",
    usage="lazy_geffe.py <encrypted_file>")
parser.add_argument('encrypted_file')
args = parser.parse_args()

def extract_header(filename: str) -> str:
    with open(filename, 'rb') as f:
        data = f.read()
    header = data[:8].hex()
    return header

def xor(a: str | bytes, b: str | bytes, output_format="bin", size=64) -> str | bytes | None:
    if type(a) and type(b) is not bytes:
        a, b = bytes.fromhex(a), bytes.fromhex(b)
    if len(a) == len(b):
        r = bytes([x ^ y for x, y in zip(a, b)])
    else:
        if len(a) < len(b):
            c = a
            a = b            
            b = c
            del(c)
        r = bytes([a[i] ^ b[i % len(b)] for i in range(len(a))])
    r = r.hex()
    if output_format == "bin":
        return bin(int(r, 16))[2:].zfill(size)
    elif output_format == "hex":
        return r
    elif output_format == "bytes":
        return bytes.fromhex(r)
    else:
        return None

def lfsr(degrees: list, state: str, rounds=64) -> str:
    degrees.sort()
    degrees.reverse()
    gamma = ''
    for i in range(rounds):
        gamma += state[-1]
        state = str(int(state[degrees[1]]) ^ int(state[-1])) + state[:-1]
    return gamma

def correlation(x: str, y: str) -> float:
    x, y = [int(bit) for bit in x], [int(bit) for bit in y]
    mean_x, mean_y = sum(x) / len(x), sum(y) / len(y)
    diff_x, diff_y = [i - mean_x for i in x], [j - mean_y for j in y]
    numenator = sum(i * j for i, j in zip(diff_x, diff_y))
    denominator = (sum([i ** 2 for i in diff_x]) * sum([j ** 2 for j in diff_y])) ** 0.5
    return numenator / denominator

gen_init_states = lambda bit_depth: [bin(i)[2:].zfill(bit_depth) for i in range(2 ** bit_depth)][1:] # all-zero state is forbidden, should be aware of that

def max_correlation(gamma: str, register: list) -> str:
    bit_depth = list(reversed(sorted(register)))[0]
    states = gen_init_states(bit_depth)
    correl_values = []
    for state in states:
        gamma_part = lfsr(register, state)
        correl_values.append(correlation(gamma, gamma_part))
    return states[correl_values.index(max(correl_values))]

def gen_keys(gamma: str, registers: list) -> list:
    keys = gen_init_states(3)
    registers.sort()
    state_1 = max_correlation(gamma, registers[0])
    state_2 = max_correlation(gamma, registers[1])
    keys = [state_1 + key + state_2 for key in keys]
    return keys

def geffe(registers: list, key_1: str, key_3: str, key_2='001', gamma_length=64) -> str:
    registers = sorted(registers)
    registers.insert(1, registers.pop(0)) # put registers in the right order

    gamma_1 = lfsr(registers[0], key_1, gamma_length)
    gamma_2 = lfsr(registers[1], key_2, gamma_length)
    gamma_3 = lfsr(registers[2], key_3, gamma_length)

    combined_output = [gamma_1, gamma_2, gamma_3]
    f = []
    for i in range(gamma_length):
        x1 = int(combined_output[0][i])
        x2 = int(combined_output[1][i])
        x3 = int(combined_output[2][i])
        r_output = (x1 & x2) ^ (int(not x2) & x3)
        f.append(r_output)
    f = list(map(str, f))
    f = ''.join(f)
    return f

def geffe_analysis(registers: list, gamma: str, key_1: str, key_3: str) -> str:
    registers = sorted(registers)
    registers.insert(1, registers.pop(0)) # put registers in the right order
    x = gen_init_states(3)
    candidates = []
    for state in x: # f(x1, x2, x3) = (x1 & x2) ^ (!x2 & x3)
        f = geffe(registers, key_1=key_1, key_2=state, key_3=key_3)
        candidates.append(f)
    correl_list = []
    for c in candidates:
        correl_list.append(correlation(c, gamma))
    key_2 = x[correl_list.index(max(correl_list))]
    return key_2

def siegenthaler_autonomous() -> None:
    '''
    this could work but the parameters in given geffe binary are unknown
    so for now it's impossible to omit its usage
    geffe binary will be integrated in this script in order for it to work
    '''
    register_1 = [4, 2, 0]
    register_2 = [3, 1, 0]
    register_3 = [5, 2, 0]
    registers = [register_1, register_2, register_3]

    headers = {
        "pdf": "255044462d312e35",
        "vsdx": "504b030414000600",
        "docx": "504b030414000600",
        "xlsx": "504b030414000600",
        "pptx": "504b030414000600"
        } # these MS Office files happen to share the same signature
    enc_file = args.encrypted_file
    if not os.path.exists(enc_file):
        print(f'File "{enc_file}" not found!')
    else:
        filename = re.search(r"(\d{1,}_\d{1,})", enc_file).group(1)
        try:
            filetype = re.search(r"(?<=\.)([a-z]{1,})(?=\.)", enc_file).group(1)
        except:
            print(f"Can not decrypt provided file.")
        else:
            if filetype not in headers:
                print(f'"{filetype}" is not supported')
            else:
                dec_file = f"{filename}.{filetype}"
                enc_header = extract_header(enc_file)
                gamma_part = xor(enc_header, headers[f"{filetype}"])
                key_1 = max_correlation(gamma_part, registers[0])
                key_3 = max_correlation(gamma_part, registers[2])
                key_2 = geffe_analysis([register_1, register_2, register_3], gamma_part, key_1, key_3)
                gamma = geffe(registers, key_1=key_1, key_2=key_2, key_3=key_3, gamma_length=3255)
                with open(f"{enc_file}", 'rb') as f:
                    data = f.read()
                if len(gamma) % 2: 
                    gamma += '0'
                gamma = int(gamma, 2)
                gamma = hex(gamma)[2:]
                decrypted = xor(data, bytes.fromhex(gamma), "bytes")
                with open(f"{dec_file}", 'wb') as d:
                    d.write(decrypted)
                return None

def siegenthaler_dependent() -> str | None:
    if not os.path.exists("geffe"):
        print('Required binary file "geffe" not found.')
        print('Put it as well as the "registers.txt" file in the working directory')
        return None
    else:
        register_1 = [4, 2, 0]
        register_2 = [3, 1, 0]
        register_3 = [5, 2, 0]
        registers = [register_1, register_2, register_3]

        headers = {
            "pdf": "255044462d312e35",
            "vsdx": "504b030414000600",
            "docx": "504b030414000600",
            "xlsx": "504b030414000600",
            "pptx": "504b030414000600"
            }
        enc_file = args.encrypted_file
        if not os.path.exists(enc_file):
            print(f'File "{enc_file}" not found!')
        else:
            filename = re.search(r"^.*?(?=-|\.)", enc_file).group(0)
            try:
                filetype = re.search(r"(?<=\.)([a-z]{1,})(?=\.)", enc_file).group(1)
            except:
                print(f"Can not decrypt provided file.")
            else:
                if filetype not in headers:
                    print(f'"{filetype}" is not supported.')
                else:
                    dec_file = f"{filename}.{filetype}"
                    enc_header = extract_header(enc_file)
                    gamma_part = xor(enc_header, headers[f"{filetype}"])
                    keys = gen_keys(gamma_part, [register_1, register_3])
                    for key in keys:
                        with open("key.txt", "w") as k:
                            k.write(key)
                            k.close()
                            pass
                        subprocess.run(f'./geffe registers.txt key.txt g.txt > /dev/null', shell='/bin/bash')
                        with open("g.txt", 'r') as g:
                            gamma = g.read()
                        with open(f"{enc_file}", 'rb') as e:
                            data = e.read()
                        if len(gamma) % 2: 
                            gamma += '0'
                        gamma = int(gamma, 2)
                        gamma = hex(gamma)[2:]
                        decrypted = xor(data, bytes.fromhex(gamma), "bytes")
                        if decrypted.hex()[:16] == headers[f"{filetype}"]:
                            with open(f"{dec_file}", "wb") as d:
                                d.write(decrypted)
                            print(f"{enc_file} has been successfully decrypted as {dec_file}")
                            print(f"Key: {key}")
                            print(f"Gamma is saved to g.txt")
                            return None
                        else:
                            continue
                    print("Decryption failed")

def main():
    siegenthaler_dependent()

if __name__ == "__main__":
    main()
