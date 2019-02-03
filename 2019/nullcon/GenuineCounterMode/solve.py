from pwn import *
from Crypto.Cipher import AES
from Crypto.Util import Counter
from gmpy2 import invert
n = 327989969870981036659934487747327553919
def pad(x):return x+"a"*(26-len(x))
p=remote('crypto.ctf.nullcon.net',5000)
#p=process(['python3','./server.py'])
p.recvuntil(': ')
p.sendline('ariana')

#finding H
data=[]
i=0
while(True):
    p.recvuntil('> ')
    p.sendline('1')
    p.recvuntil(': ')
    p.sendline(pad(str(i)))
    t=p.recvline()[:-1].split(':')
    data.append([int(t[0],16),t[1],int(t[2],16),i])
    k=0
    while(k<i):
        if(data[-1][0]==data[k][0]):
            data=[data[k]]+[data[-1]]
            break
        k+=1
    if(k!=i):
        break
    i=i+1
    if(i%10==0):print i
H=(data[1][2]-data[0][2])*invert(int(data[1][1][:32],16)-int(data[0][1][:32],16),n)%n
print "H=0x%x" % H

#forging
okm=int(pad(str(data[0][3])).encode('hex'),16)#known msg
kc=int(data[0][1],16)#known cipher text
ne=data[0][0]#nounce
forge=int("may i please have the flag".encode('hex'),16)
mask=forge^okm
ct=kc^mask
c=(data[0][2]-int(data[0][1][:32],16)*H-int(data[0][1][32:],16)*H**2)%n
tag=c+(int(hex(ct)[2:34],16)*H)%n+(int(hex(ct)[34:],16)*H**2)%n
print "%x:%x:%x"%(ne,ct,tag)
p.interactive()
