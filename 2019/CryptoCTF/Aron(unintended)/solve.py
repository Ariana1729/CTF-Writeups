from pwn import *
import re

r=remote('167.71.62.250',12439)
chal=re.match('Submit a printable string X, such that (.*)\(X\)\[-6:\] = ([0-9a-f]{6})',r.recvline())
h=chal.group(1)
v=chal.group(2)
print(h+"(x) = "+v)
i=0
exec('from hashlib import '+h+'\nwhile True:\n if('+h+'(str(i)).hexdigest()[-6:]=="'+v+'"):break\n i+=1')
print "x = %d"%i
r.sendline(str(i))
r.interactive()
