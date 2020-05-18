from pwn import *
from gmpy2 import invert, isqrt, next_prime
from Crypto.PublicKey import RSA


pubkey = '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAx+S9hsKIKl5tniedzskRVFL8Bx/BOk1v89JXacI5IFZ8O3cuAcNU
WBoF5kkfMNNwbzo8fYFnDQGcusLEA0bBe4+0f8d6BNH1Me1lI1itU6nCXqXnep45
SQoiLzl0qYNpqu1tcBl3XBC50NrEXfFXntJDxPL+IzGzpZ8k3pceVJ2ttB1M9Vos
92NWkq90cAeBNYVjl2pKJ6ih09CPlEQzk6dxV1B/SonT/seGW6JpgOj6JoDwUhNT
DC29vLD50i1tIUNDgakfBirkziRgZ4cyZ+UMjnY45O6AdY9vXwzV1L/OYeuK0AsR
XzYIQNzdpFQnkjf4VG+2icR1AbM2AOvINwIDAQAB
-----END RSA PUBLIC KEY-----'''
enc = 0x447f863cf38dc1468a9b17db11d1fa80224be841e72f63f4943fd55533e5d9a981bc354ef8c2c58763e8a1adae4012ea2f9b0df9d261c1f23c4753f38aa408513437976a884f8baad4cb329beb041cb6b9d4aaeb7a985692d7b419c06821f100afcbbe19e884c41e5a6703055a8a9c7f9bdc96691a563594507336f34c5fac22f0dd834efebc2f21f17d4bbf43633440dbba0e2949c371bfe47c58cd893c3bae75e97d0259c1919ff98fc3da3587b59a256849fed1c6ef21578cfeb8c3dc143fbfaeb5e362e2c5fce55e427898334215412b97b0d168f301a8a7dc3202c83eb24196569c09600f0404d28f855a181e215ca504ceaafc8d511018c6b8bf5a6ad


a1 = 'f'*120
r = remote('coooppersmith.challenges.ooo',5000)
r.recvuntil('120: ')
r.sendline(a1)
print 'Waiting for data'
r.recvline()
pubkey = r.recvuntil('-----END RSA PUBLIC KEY-----\n')
r.recvline()
r.recvline()
r.sendline(process('./prng').readline())
r.recvline()
enc = int(r.recvline(),16)

pubkey = RSA.importKey(pubkey)
N = pubkey.n
e = pubkey.e
print 'N = ' + hex(N)
print 'e = ' + hex(e)
print 'enc = ' + hex(enc)

a = int(a1,16)<<((0x80 - len(a1))*4)
for _ in range(1<<((0x80 - 120)*2)):
    if N%(2*a)==1:
        break
    a += 1
else:
    a = gmpy2.next_prime(a)
    if N%(2*a)!=1:
        print 'Params are bad'
        exit()

s = ((N-1)/(2*a)) % (2*a)
p = (N-1-(2*a*s))/(4*a*a)
d = isqrt(s*s-4*p)
r1 = (s+d)/2
r2 = (s-d)/2
if 0:
    p = 2*a*r1 + 1
    q = 2*a*r2 + 1
    print 'p = ' + hex(p)
    print 'q = ' + hex(q)

d = invert(e, 2*a*r1*r2)
if 2!=pow(pow(2,e,N),d,N):
    print 'Params are bad'
    exit()
privkey = RSA.construct((N, e, long(d)))
msg = hex(privkey.decrypt(enc))[2:].rstrip('L')
msg = ('0'*(len(msg)%2)+msg).decode('hex')
print "Flag: " + msg
