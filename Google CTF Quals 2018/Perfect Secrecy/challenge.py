#!/usr/bin/env python3
import sys
import random

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import gmpy2
p=43534508735687346583563487563148789
q=91347596138746329462837649328743337
n=p*q
ln=(p-1)(q-1)
e=65537
d=gmpy2.invert(e,ln)
m=0x4354467b466c6167737d#CTF{Flags}
c=pow(m,r,n)

'''
[*] n: 153314286737753283255547252902231988923677001570537670823569737192417931917849858323550190365704182153062786056662711312188848241990605760007378096173801480759292810572306932509446953082431394351272757346605609898944553806892979792999103404028562806843687533668219905113924888506316958727392199113512716600273
[*] e: 65537


'''
def ReadPrivateKey(filename):
  return serialization.load_pem_private_key(
      open(filename, 'rb').read(), password=None, backend=default_backend())


def RsaDecrypt(private_key, ciphertext):
  return pow(c,d,n)


def Challenge(private_key, reader, writer):
  try:
    m0 = "A"
    m1 = "B"
    ciphertext = reader.read(128)
    dice = RsaDecrypt(private_key, ciphertext)
    for rounds in range(100):
      p = [m0, m1][dice & 1]
      c = (ord(p) + random.randint(0, 2)) % 2
      writer.write(bytes((c,)))
    writer.flush()
    return 0

  except Exception as e:
    return 1


def main():
  private_key = d
  return Challenge(private_key, sys.stdin.buffer, sys.stdout.buffer)


if __name__ == '__main__':
  sys.exit(main())
