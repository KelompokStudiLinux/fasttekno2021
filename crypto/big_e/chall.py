from Crypto.Util.number import GCD, getPrime, bytes_to_long, long_to_bytes, inverse
from random import getrandbits

p = getPrime(1024)
q = getPrime(1024)
n = p*q
phi = (p-1)*(q-1)

while True:
    e = getrandbits(512)
    if GCD(e,phi) == 1:
        d = inverse(e,phi)
        pp = d
        break

flag = open("flag.txt","rb").read()
flag = bytes_to_long(flag)
c = pow(flag,pp,n)

print(f"n = {n}")
print(f"pp = {pp}")
print(f"c = {c}")