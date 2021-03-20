from base64 import b64decode
from Crypto.Util.number import GCD, inverse
from functools import reduce

# vanilla LCG
class LCG:
    def __init__(self, state, modulus, multiplier, increment):
        self.state = state
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
    
    def next(self):
        self.state = (self.state * self.multiplier + self.increment) % self.modulus
        return self.state

# https://security.stackexchange.com/questions/4268/cracking-a-linear-congruential-generator
# https://tailcall.net/blog/cracking-randomness-lcgs/
def crack_LCG(states):
    # crack modulus
    t = []
    for i in range(len(states) - 1):
        t.append(states[i+1] - states[i])
    u = []
    for i in range(len(t) - 2):
        result = abs(t[i+2] * t[i] - t[i+1]**2)
        u.append(result)
    modulus = reduce(GCD, u)

    # crack multiplier
    multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus

    # crack increment
    increment = (states[1] - states[0]*multiplier) % modulus

    return modulus, multiplier, increment

# cman xor biasa, str^str = str
def xor(a,b):
    res = ''
    for x,y in zip(a,b):
        res += chr(ord(x) ^ ord(y))
    return res

if __name__ == '__main__':
    # read encrypted flag
    f = open('flag.enc').read()
    enc = b64decode(f).decode()

    # karena format flag diketahui, langsung xor format flag dengan enc
    format_flag = 'FastTekno{'
    keystream = xor(enc, format_flag)
    keystream = [ord(k) for k in keystream]

    # crack LCG, sc malink akwoawkowa
    n,m,c = crack_LCG(keystream)

    # seed adalah index terakhir dari keystream
    seed = keystream[-1]
    r = LCG(seed,n,m,c)

    # karena variabel tersembunyi sudah diketahui, tinggal gunakan var tsb untuk generate ulang key
    for i in range(len(keystream), len(enc)):
        keystream.append(r.next())
    keystream = [chr(k) for k in keystream]

    # decrypt flag
    flag = xor(enc,keystream)
    print(flag)