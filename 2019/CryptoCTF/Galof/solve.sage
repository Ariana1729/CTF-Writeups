m1='uXu2FTYWpCWSXcPwpv4mc0V8nhl2T7'
c1=0x582c7d41f27a92ad373dec06175f8b0d399bc5d858253bb4b6530c6c608992b1
m2='PBFnf2mSWiHUNxMr90KJC6TubsKjU9'
c2=0x186f2f1f0eeab93e621b34dbc1fa515b5b74fc761afb9e74a560598844ab9160

F.<x> = GF(2)[]
base = x^255 + x^199 + 1

m1 = bin(int(m1.encode('hex'), 16))[2:]
f1, e = 0, 0
for b in m1[::-1]:
	f1 += int(b) * x^e
	e += 1

m2 = bin(int(m2.encode('hex'), 16))[2:]
f2, e = 0, 0
for b in m2[::-1]:
	f2 += int(b) * x^e
	e += 1

c1 = bin(c1)[2:]
h1, e = 0, 0
for b in c1[::-1]:
    h1 += int(b) * x^e
    e += 1

c2 = bin(c2)[2:]
h2, e = 0, 0
for b in c2[::-1]:
    h2 += int(b) * x^e
    e += 1

key_2 = (h1*f1+h2*f2)*inverse_mod(f1+f2,base)%base
key_1 = (h1+key_2)*f1 % base

key = key_1, key_2

c3 = 0x46c5c88ef8c8f6d49ffc763d56e9cd33176d9aa14c039281d506b834d48c1066
c3 = bin(c3)[2:]
h3, e = 0, 0
for b in c3[::-1]:
    h3 += int(b) * x^e
    e += 1

f3 = inverse_mod(h3-key_2,base)*key_1%base

EXP = f3.exponents()
m3 = ''
for i in range(256):
	if i in EXP:
		m3 += '1'
	else:
		m3 += '0'
m3 = hex(int(m3[::-1], 2)).lstrip('0x').rstrip('L').zfill(64)
print m3.decode('hex')
