# How to solve
Diberikan file `chall.py` dan `flag.enc` yang berisi flag yang dienkripsi. Cara enkripsinya dengan cara XOR, tetapi `len(key) == len(plain)`. Hanya saja, algoritma random yang digunakan adalah LCG atau Linear Congruental Generator. 

Untuk mencari key, kita harus menebak inner state dari LCG, yaitu modulus, multiplier, dan increment. Selain itu, output dari random juga diperlukan. Cara untuk mendapatkan states random ini dengan cara melakukan XOR format flag `FastTekno{` dengan `enc_flag`
`states[] = xor("FastTekno{", enc_flag)	#list berisi integer`

Untuk mencari modulus
1. Hitung `Tn = Sn+1 - Sn` dan `Un = |Tn+2 Tn - T2n+1|`
2. Hitung `GCD(U1, U2, U3, ..., Un)`,  hasil dari GCD adalah nilai modulus

Untuk mencari multiplier, cukup
`multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus`

Untuk mencari increment,
`increment = states[1] - states[0] * multiplier % modulus`

Jika sudah mendapatkan inner state dari LCG, cukup generate ulang LCG dengan `seed = states[-1]` dan lanjutkan proses generate. Hasil dari random tadi di-XOR dengan `enc_flag`.