#!/usr/bin/env python3
import os

def enc(plain,key):
    cipher = ""
    for i in range(len(plain)):
        cipher += chr(ord(plain[i]) ^ ord(key))
    return cipher

key = os.urandom(1)
flag = open("flag.txt","r").read()
ciphertext = enc(flag,key)

with open("flag.enc","w") as g:
    g.write(ciphertext)