from base64 import *
import os

def enc(plain,key):
    cipher = ''
    for i in range(len(plain)):
        cipher += chr(plain[i] ^ key[i%len(key)])
    
    return b64encode(cipher.encode('latin1'))

key = os.urandom(9)
flag = open("flag.txt","rb").read()
cipher = enc(flag,key)

with open("flag.enc","wb") as g:
    g.write(cipher)