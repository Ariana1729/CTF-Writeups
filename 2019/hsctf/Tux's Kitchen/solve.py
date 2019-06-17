from pwn import *
from gmpy2 import gcd
f=None
s=29486316
for i in range(10):
    r=remote('crypto.hsctf.com',8112)
    exec("b="+r.recvall().split('\n')[-1]+"")
    r.close()
    b=[i^s for i in b]
    if(f==None):
        f=b
    else:
        for i in range(len(f)):
            f[i]=gcd(f[i],b[i])
        if(all(i<=0x7f for i in f)):
            print ''.join(chr(i) for i in f)
