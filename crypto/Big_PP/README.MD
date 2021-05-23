# How to solve
Diberikan file `chall.py` dan `pp.txt` yang berisi nilai `n, pp, c`. Variabel `pp` disini adalah public key.

Pada bagian kode dibawah:
```python
while True:
    e = getrandbits(512)
    if GCD(e,phi) == 1:
        d = inverse(e,phi)
        pp = d
        break
```
Terlihat bahwa pp adalah private key, sehingga rolenya dibalik (private jadi public, dan sebaliknya). Hal ini bisa saja dilakukan, dan proses encrypt dan decrypt dapat berjalan seperti biasa. Tapi karena nilai `pp` besar, dan juga sudah diketahui bahwa nilai `e` lumayan kecil, kita bisa mencari `e` dengan cara [Wiener Attack](https://en.wikipedia.org/wiki/Wiener%27s_attack "Wiener's Attack").