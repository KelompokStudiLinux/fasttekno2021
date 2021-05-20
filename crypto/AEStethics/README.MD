# How to solve
Diberikan file `chall.py` yang berisi source code dari service nc. Pada function `encrypt`, terlihat bahwa plaintext diencrypt dengan `AES_ECB`, lalu ada proses ini-itu sebelum di-append ke variabel `ciphertext`.

Potongan kode dibawah adalah proses enkripsi dan tambahan proses ini-itu
```python3
def encrypt(plaintext):
    aes = AES.new(KEY, AES.MODE_ECB)
    ciphertext = b""
    plaintext_block = [plaintext[i:i+16] for i in range(0,len(plaintext),16)]
    init = IV
    for block in plaintext_block:
        ciphertext_block = aes.encrypt(init)
        result = xor(ciphertext_block, block)
        ciphertext += result
        init = ciphertext_block

    return hexlify(ciphertext).decode()
```

Sebelum memulai loop, IV di-encrypt, lalu hasilnya di-XOR dengan `ciphertext_block`. hasil dari XOR tadi di-append ke var `ciphertext` dan value dari var `init` berubah dari `IV` menjadi `result`. Hal ini terus diulang sampai `plaintext_block` habis. Berdasarkan langkah-langkah tadi, ternyata plaintext tidak di-encrypt dengan mode `AES_ECB` melainkan `AES_OFB` seperti gambar berikut
![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/OFB_encryption.svg/1920px-OFB_encryption.svg.png)

Pada mode OFB, value dari `IV` harus random setiap kali melakukan enkripsi. Tapi pada soal ini, `IV` akan berubah setiap user connect ke service. Jadi cara untuk mendapatkan flag adalah dengan cara known-plaintext attack.

Caranya cukup sederhana
1. Get Flag
2. Encrypt message, panjang message &ge; panjang flag. Simpan hasil ciphertext
3. `keystream = xor(message, encrypted_message)`
4. `flag = xor(encrypted_flag, keystream)`