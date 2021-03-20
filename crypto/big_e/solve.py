from Crypto.Util.number import long_to_bytes
import owiener      # https://github.com/orisano/owiener

f = open("pp.txt").read()
exec(f)     #n,pp,c

d = owiener.attack(pp,n)
m = pow(c,d,n)
m = long_to_bytes(m)
print(m)