from func_stash import keygen, ecb

key = keygen(16)

parse = lambda x: dict((k.strip(), v.strip()) for k,v in (item.split('=') for item in x.split("&")))

def profile_for(address: str) -> str:
    uid = 10
    address = address.replace('&', '')
    address = address.replace('=', '')
    encoded = f'email={address}&uid={uid}&role=user'
    return encoded

def enc_profile(profile: str) -> str:
    global key
    profile = profile.encode()
    encrypted = ecb('encrypt', profile, key)
    return encrypted

def dec_profile(profile: str) -> dict:
    global key
    profile = bytes.fromhex(profile)
    decrypted = ecb('decrypt', profile, key)
    decrypted = decrypted.decode()
    decrypted = parse(decrypted)
    return decrypted

def exploit_cut_and_paste():
    address = 'foooo@bar.admin\v\v\v\v\v\v\v\v\v\v\vcom'
    encoded = profile_for(address)
    encrypted = enc_profile(encoded)
    enc = encrypted[:32] + encrypted[64:96] + encrypted[32:64]
    decrypted = dec_profile(enc)
    return decrypted

def main():
    decrypted = exploit_cut_and_paste() 
    print(decrypted)

if __name__ == "__main__":
    main()
