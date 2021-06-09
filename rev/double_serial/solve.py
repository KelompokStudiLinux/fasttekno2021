from base64 import b64decode
from Crypto.Util.number import inverse
from pwn import xor

flag_enc = [35, 82, 26, 88, 3, 121, 31, 7, 6, 95, 88, 47, 14, 44, 58, 15, 49, 102, 104, 35, 60, 14, 100, 80, 63, 12, 42, 28, 4, 1, 84, 44, 38, 1, 0, 4, 50, 102, 108, 44, 18, 103, 9, 88, 63, 13, 42, 17, 6, 41, 35, 54, 38, 103, 81, 15, 37, 88, 119, 103, 63, 85, 18, 73, 61, 85, 20, 90, 1, 60, 80, 100]

s1 = [0 for i in range(20)]
s2 = [0 for i in range(20)]

s1[0] = 74
s1[1] = 111
s1[2] = 104
s1[3] = 110
s1[4] = 68
s1[5] = s1[1]
s1[6] = s1[3] - 9
s1[7] = 45
s1[8] = s1[7] + 4
s1[9] = s1[8] + 2
s1[10] = s1[9]
s1[11] = s1[9] + 4
s1[12] = 45
s1[13] = s1[8] + 3
s1[14] = s1[8] + 1
s1[15] = s1[8] - 1
s1[16] = 45

s2[17] = 116
s2[18] = s2[17] + 3
s2[19] = 60

inv = 32
mult = inverse(inv,127)
inc = 17

for i in range(17):
    s2[i] = (s1[i]*mult + inc) % 127

for i in range(17,20):
    s1[i] = (inv*(s2[i]-inc)) % 127

s1 = "".join([chr(c) for c in s1])
s2 = "".join([chr(c) for c in s2])

assert s2 == ";P4L#P(FV^^nFbZRFtw<"
assert s1 == "JohnDoe-1337-420-xYj"

key = xor(s1,s2)
flag = b64decode(xor(key, flag_enc))
print(flag)