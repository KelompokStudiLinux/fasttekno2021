from base64 import *
from pwn import xor

f = b64decode(open("flag.enc").read())
known_flag = "FastTekno"
key = xor(known_flag, f[:9])
flag = xor(f,key)
print(flag)