from pwn import *
import re

def dlp(g,p,a): # returns g^x = a
    i=0
    while True:
        if(pow(g,i,p)==a):
            return i
        i+=1

def send(x): # returns g^(x dot v)
    global r
    r.sendline('n')
    r.sendline('y')
    r.sendline(str(x))
    r.recvuntil('| f_a(n + 0) = ')
    return int(r.recvline())

r=remote('167.71.62.250',23549)
chal=re.match('Submit a printable string X, such that (.*)\(X\)\[-6:\] = ([0-9a-f]{6})',r.recvline())
h=chal.group(1)
v=chal.group(2)
print(h+"(x) = "+v)
i=0
exec('from hashlib import '+h+'\nwhile True:\n if('+h+'(str(i)).hexdigest()[-6:]=="'+v+'"):break\n i+=1')
print "x = %d"%i
r.sendline(str(i))
r.interactive()
r.recvuntil('| (p, g) = (0x')
p=int(r.recvuntil(', 0x')[:-4] ,16)
g=int(r.recvuntil(')')[:-1],16)
r.recvuntil('[Q]uit')
print 'p = %d'%p
print 'g = %d'%g

sol=[None]*128

a=send(2**127)
sol[127]=dlp(g,p,a)

a=send(2**126)
sol[126]=dlp(g,p,a)

r.recvuntil('| f_a(n + 1) = ')
a=int(r.recvline())
sol[0]=dlp(g,p,a)-sol[126]

r.recvuntil('| f_a(n + 2) = ')
a=int(r.recvline())
sol[1]=dlp(g,p,a)-sol[126]

r.recvuntil('| f_a(n + 4) = ')
a=int(r.recvline())
sol[2]=dlp(g,p,a)-sol[126]

for i in range(3,126):
    a=send(2**126+2**i)
    sol[i]=dlp(g,p,a)
    if(i%4==2):
        print sol
r.interactive()

