from base64 import *

def decrypt(ciphertext, key):
    plaintext = ''
    for i in range(len(ciphertext)):
        res = ((ciphertext[i]-i) ^ key[i % len(key)]) % 256
        plaintext += chr(res)
    return plaintext

f = open("flag.enc").read()

ciphertext = b64decode(f)
key = decrypt(ciphertext[:10], b"FastTekno{").encode('latin1')

flag = decrypt(ciphertext, key)
print(flag)