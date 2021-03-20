f = open("flag.enc").read()

for key in range(256):
    plain = ''.join([chr(ord(p) ^ key) for p in f])
    if "FastTekno" in plain:
        print(plain)
        break
