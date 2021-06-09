#!/usr/bin/env python

from z3 import *

serial = [BitVec(str(i),8) for i in range(31)]
s = Solver()

s.add(serial[5] == 45)
s.add(serial[11] == 45)
s.add(serial[17] == 45)
s.add(serial[23] == 45)
s.add(serial[0] * serial[15] - serial[1] == 6132)
s.add(serial[3] == 117)
s.add(serial[4] - serial[15] == 20)
s.add(serial[6] ^ serial[7] == 35)
s.add(serial[7] * serial[0] - serial[13] == 7424)
s.add(serial[8] == 114)
s.add(serial[9] * serial[9] + serial[24] == 13761)
s.add((serial[12] - 1) * serial[10] == 4182)
s.add(((serial[30] + serial[20]) ^ serial[12]) == 231)
s.add((serial[0] ^ serial[16]) ^ serial[13] == 10)
s.add(serial[18] + serial[20] - serial[22] == serial[6])
s.add(serial[19] - serial[10] == serial[29] - 9)
s.add(serial[21] & serial[25] == 68)
s.add(serial[26] + serial[27] == 162)
s.add(serial[28] == 89)
s.add(serial[29] - serial[30] == -12)
s.add(2 * (serial[0] + 1) == 180)
s.add(serial[2] * serial[13] + serial[23] == 3945)
s.add(serial[10] + serial[12] == 134)
s.add(serial[9] * 2 == 234)
s.add(8 * (serial[19] + serial[9]) == 1792)
s.add(serial[18] + 33 == serial[8])
s.add(serial[26] == 83)
s.add((serial[22] ^ serial[25]) == 4)
s.add(serial[2] == 75)
s.add(serial[21] == 102)
s.add(serial[14] == serial[21] - 2)
s.add(serial[15] == 70)

print(s.check())
model = s.model()

m = str(model).replace("[","{").replace("]","}").replace("=",":")
m = eval(m)
f = ''.join([chr(m[i]) for i in range(31)])
assert f == "YbKuZ-wTru3-S4dFg-QkgfA-HESOYAM"
print("FastTekno{%s}" % f)