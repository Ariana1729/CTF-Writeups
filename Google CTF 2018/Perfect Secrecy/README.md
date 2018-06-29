# Perfect Secrecy
>This crypto experiment will help you decrypt an RSA encrypted message.
We are given a [key_pub.pem](./key_pub.pem) [challenge.py](./challenge.py) and a [flag.txt](./flag.txt)

Lets look at the public key and flag

```
# python ./RsaCtfTool/RsaCtfTool.py --dumpkey --key ./key_pub.pem 
[*] n: 153314286737753283255547252902231988923677001570537670823569737192417931917849858323550190365704182153062786056662711312188848241990605760007378096173801480759292810572306932509446953082431394351272757346605609898944553806892979792999103404028562806843687533668219905113924888506316958727392199113512716600273
[*] e: 65537
# cat flag.txt 
��e���}Bg�i���4��
                   ��k��j���П,a��
�g��<LU�C�Lp��*�4�9�7�9Ǎ�R:�����5!�T� i�BC�c���͌���E��#���;l���s����"0(����0�V# hexdump flag.txt 
0000000 c5a9 cb65 cfc2 7d1c 6742 17fd dc69 f0e9
0000010 8134 0b80 e8ba b06b 6a92 17e6 e6a7 9fd0
0000020 612c d7a9 850a 8367 3c97 554c 43bf 4ca2
0000030 701d b0f7 c02a ff34 c539 ab37 c739 908d
0000040 3a52 0781 98a0 9501 35df d621 d754 6920
0000050 42f9 0882 1c43 63c7 f3de cd9b d38c 9dea
0000060 e945 239e 81f7 a00f 6c3b 06e9 f4d6 7313
0000070 e2e0 c0a7 3022 2818 f8d7 d30e 30c6 56ae
0000080

```

Looks like flag.txt is a ciphertext with 1024 bits and we are given a 1024-bit public key and a large exponent.

After trying yafu to factor the public key and various online sites, the number still resisted factorization, so now let's look into the python script.

## Python code

```python
def main():
  private_key = ReadPrivateKey(sys.argv[1])
  return Challenge(private_key, sys.stdin.buffer, sys.stdout.buffer)
```

Firstly, the main function reads a private key from a file, likely in the flag's server, then it calls challenge

Now let's focus on Challenge:

```
def Challenge(private_key, reader, writer):
  try:
    m0 = reader.read(1)
    m1 = reader.read(1)
    ciphertext = reader.read(private_key.public_key().key_size // 8)
    dice = RsaDecrypt(private_key, ciphertext)
    for rounds in range(100):
      p = [m0, m1][dice & 1]
      k = random.randint(0, 2)
      c = (ord(p) + k) % 2
      writer.write(bytes((c,)))
    writer.flush()
    return 0

  except Exception as e:
    return 1
```

We know that the key size is 1024 bits, so challenge reads in 1+1+128 characters. Then it decrypts the last 128 characters with the private key, so if we could get the variable `dice` we'll have gotten the flag. After that, we see a loop with a random number. It seems like the loop is checking the flag's parity, then adding a random number to it mod 2. This does not seem possible. However, after playing with random.randint(0,2), I realized it actually outputs 0,1 or 2 instead of 0 or 1. Since there is a higher chance a even number comes out, we can deduce the parity of the flag from this. This is basicaly a RSA parity oracle.

Ok so we are able to get one bit of the flag. How are we supposed to get the rest? 

# Solution

Consider the parity of `2m mod N` where `m<N`. Assuming `2m<N`, this is trivially even. However, if `2m>N`, it will be odd(2m>2N). Now we can tell if `m<N/2` or 'm>N/2`. Now how do we continue getting stricter bounds?

We can continue with 4m, 8m, 16m, etc. With similar login, you can keep changing the lower and upper bounds of m and slowly squeeze m out.

Plan:
1. Set lowerbound=0,upperbound=n,i=1
2. Find the parity of `2^n m`
3. If the parity comes out to be odd, increase the lower bound to the median, else, decrease the upper bound to the median.

So how do we find the parity of `2^n m`?

### RSA recap:

m^e mod N = c
c^d mod N = m where ed mod (φ(N)) = 1
ab mod N = (a mod N)(b mod N) mod N
Since we have m^e, we can find (km)^e=(k^e)(m^e)=k^e c

Thus if we send 2^(ne)c to the oracle, we will(hopefully) get the parity of 2^n m.

Since N is 1024-bits, we will need to ping the oracle 1024 times. That's quite a lot. Even if we have receive 100 0s and 1s, there's a tiny chance that we get a incorrect parity.

### Checking our chances

This is really just to gauge how often we will get a incorrect flag.

Assume that the oracle should reply with 0

The chance of it replying with 0 for one of the characters is 2/3, and 1 is 1/3. We can find how often 50 or more 0s are replied with $\sum_{k=0}^{50}(1/3)^k(2/3)^{100-k}C^{100}_k$

Since we need 1024 pings, we raise this to the 1024th power, and get around 65%(65.083747...%). Hmm not that high. Maybe we should open the exploit multiple times.

Now we'll just have to send 'BA'+long_to_bytes(c*pow(2,i*e,N)%N) for i=1 to i=1025 times... this will take quite some time.

# Script

Working with large numbers will be prone to errors so it's better to keep what we received as an array then calculate the flag at the end, calculations can also easily be redone if messed up.

[Script](./script.py)

After waiting for like 20 mins, the flag is revealed,

>CTF{h3ll0\_\_17\_5\_m3\_1\_w45\_w0nd3r1n6\_1f\_4f73r\_4ll\_7h353\_y34r5\_y0u\_d\_l1k3\_70\_m337}


