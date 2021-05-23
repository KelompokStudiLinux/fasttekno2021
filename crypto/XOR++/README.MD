# How to solve
Diberikan file `solve.py` dan `flag.enc` berisi flag yang diencrypt. Pada potongan kode dibawah:
```python
for i in range(len(plain)):
        res = ((plain[i] ^ key[i%len(key)]) + i) % 256
        cipher += chr(res)
```
Terlihat bahwa `plain` di XOR dengan `key`, lalu hasilnya ditambah dengan `i`yang merupakan nilai index.

Misalkan, 
```python
plain = "ABC"
key = "XYZ"
```
Pada index ke-0, karakter `A` di XOR dengan key `X`, lalu hasilnya akan ditambah dengan `0` (karena sekarang sedang memproses index ke-0)
`ct[0] = ord("A") ^ ord("X") + 0`

Pada index ke-1, karakter `B` di XOR dengan key `Y`, lalu hasilnya akan ditambah dengan `Y` (karena sekarang sedang memproses index ke-1). Begitu seterusnya.

Cara membaliknya sederhana, yaitu melakukan operasi pengurangan, lalu operasi XOR. Jadi tadi yang sebelumnya
`ct[0] = (ord("A") ^ ord("1")) + 0`

sekarang dibalik menjadi
`pt[0] = (ct[0] - 0) ^ ord("1")`

Ok, index diketahui, tapi bagaimana caranya mencari key?
Kita tau panjang key adalah 10, dan format flag adalah `FastTekno{}`. Panjang string `FastTekno{` pas 10, jadi kita bisa mencari key dengan cara
`key = xor("FastTekno{", ct[:10])`

Jangan lupa, proses XOR dilakukan setelah ciphertext dikurangi oleh index. Kalau key sudah didapat, terapkan cara decrypt diatas.