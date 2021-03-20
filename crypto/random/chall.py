from base64 import b64encode
import secret

class LCG:
    def __init__(self, state):
        self.state = state
        self.modulus = secret.modulus
        self.multiplier = secret.multiplier
        self.increment = secret.increment

    def next(self):
        self.state = (self.state * self.multiplier + self.increment) % self.modulus
        return self.state

def gen_key(length):
    r = LCG(secret.seed)
    key = [r.next() for i in range(length)]
    return key

def encrypt(plain, key):
    cipher = ''.join([chr(ord(p) ^ k) for p,k in zip(plain,key)])
    return b64encode(cipher.encode())

if __name__ == "__main__":
    flag = secret.flag
    key = gen_key(len(flag))
    enc = encrypt(flag,key)

    with open('flag.enc','wb') as f:
        f.write(enc)