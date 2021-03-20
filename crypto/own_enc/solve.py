from base64 import *

def dec(cipher,key):
    cipher = b64decode(cipher)
    plain = ''.join([chr((c-3) ^ key) for c in cipher])
    return plain

f = open("flag.enc").read()
for i in range(256):
    plain = dec(f,i)
    if "FastTekno" in plain:
        print(plain)
        break
