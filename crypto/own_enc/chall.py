from base64 import *
import os

def enc(plain,key):
    cipher = ''
    for p in plain:
        cipher += chr((p ^ key) + 3)
    
    return b64encode(cipher.encode('latin1'))

key = ord(os.urandom(1))
flag = open("flag.txt","rb").read()
cipher = enc(flag,key)

with open("flag.enc","wb") as g:
    g.write(cipher)