from gmpy2 import invert,iroot
exec(open('massive.txt').read())
p=iroot(n,2)[0]
d=invert(e,n-1)
m=pow(c,d,n)
print hex(m)[2:].decode('hex')
