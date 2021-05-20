#!/usr/bin/env python3
from binascii import hexlify
from Crypto.Cipher import AES
import os

KEY = os.urandom(16)
IV = os.urandom(16)

def xor(a, b):
    return b"".join([chr(x^y).encode("latin1") for x,y in zip(a,b)])

def encrypt(plaintext):
    aes = AES.new(KEY, AES.MODE_ECB)
    ciphertext = b""
    plaintext_block = [plaintext[i:i+16] for i in range(0,len(plaintext),16)]
    init = IV
    for block in plaintext_block:
        ciphertext_block = aes.encrypt(init)
        result = xor(ciphertext_block, block)
        ciphertext += result
        init = ciphertext_block

    return hexlify(ciphertext).decode()

flag = open("flag.txt", "rb").read().strip()
enc_flag = encrypt(flag)
print(f"Your flag is: {enc_flag}")

while True:
    print("Menu:")
    print("[1] Encrypt message")
    print("[2] Exit")
    inp = input("Input: ")
    
    if inp == "1":
        plain = input("Your message: ").encode("latin1")
        enc = encrypt(plain)
        print(f"Your encrypted message is: {enc}")
    elif inp == "2":
        exit()
    else:
        print("Unknown input...")
    print()