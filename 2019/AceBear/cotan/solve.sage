from Crypto.Cipher.AES import AESCipher
p=1361129467683753853853498429727072846149
F=IntegerModRing(p)
i=mod(-1, p).sqrt()
v=F(2)
c=F(675847830679148875578181214123109335717)
#key = hex(((c+i)/(c-i)).log((v+i)/(v-i))).decode('hex')
key = '0d15eb486aa9901e40e636cac171d6ac'.decode('hex')
print(AESCipher(key).decrypt('4e8f206f074f895bde336601f0c8a2e092f944d95b798b01449e9b155b4ce5a5ae93cc9c677ad942c32d374419d5512c'.decode('hex')))
