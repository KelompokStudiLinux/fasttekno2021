from pwn import *
from binascii import unhexlify

p = process("./chall.py")

p.recvuntil("Your flag is: ")
enc_flag = unhexlify(p.recvline().strip())

p.sendline("1")
plain = "A"*len(enc_flag)
p.sendline(plain)
p.recvuntil("Your encrypted message is: ")
cipher = unhexlify(p.recvline().strip())
p.close()

keystream = xor(plain, cipher)
flag = xor(enc_flag, keystream)

print(flag)