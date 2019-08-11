from pwn import *
import re

r=remote('167.71.62.250',14559)
r.recvline()
r.recvline()
r.recvline()
chal=re.match('Submit a printable string X, such that (.*)\(X\)\[-6:\] = ([0-9a-f]{6})',r.recvline())
h=chal.group(1)
v=chal.group(2)
print(h+"(x) = "+v)
i=0
exec('from hashlib import '+h+'\nwhile True:\n if('+h+'(str(i)).hexdigest()[-6:]=="'+v+'"):break\n i+=1')
print "x = %d"%i
r.sendline(str(i))
r.recvuntil('Send your Options:')
r.sendline('E')
enc=()
r.recvline()
exec(r.recvline())
print "Flag encrypted : "+str(enc)
r.sendline('T')
r.sendline('(-1,0)')
r.recvuntil(') ** e) (mod n) = (')
n=int(r.recvuntil('L, 0L)')[:-6])+1
r.sendline('T')
r.sendline('(2,0)')
r.recvuntil(') ** e) (mod n) = (')
a=int(r.recvuntil('L, 0L)')[:-6])
e=0
t=1
while True:
    e+=1
    t=t*2%n
    if(t==a):
        break
print "n = %d"%n
print "e = %d"%e
r.interactive()
