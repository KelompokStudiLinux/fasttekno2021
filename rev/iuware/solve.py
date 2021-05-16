import random
import os

def shuffle_secret():
  secret_out = ''
  secret_str = ''.join('fastIUteknoIU2021'.split("IU"))
  for count, loop in enumerate(secret_str):
    if count % 2 == 0:
      secret_out += ''.join([chr(ord(ch) + 0x3) for ch in loop])
    else:
      secret_out += loop
  return secret_out

def encryption(shift):
  shift_ = ((shift ^ random.randint(3, 300)) << (shift >> random.randint(3, 300)))

  alphabet = shuffle_secret() * 10000
  shifted_alphabet = alphabet[shift_:] + alphabet[:shift_]

  for root, dirs, files in os.walk("./secrets"):
    for file in files:
      readFile = open(root + "/" + file, "rb").read()
      print file
      enc = ''.join([chr((ord(a) ^ ord(b) & 0xff)) for a, b in zip(readFile, shifted_alphabet)])
      open("./decrypted/" + file[:-3], "wb").write(enc)
  

random.seed(shuffle_secret())
shift = random.randint(0, 0xff)
encryption(shift)