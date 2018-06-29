# DM Collision
>Can you find a collision in this compression function?
We are given a [challenge.py](./challenge.py) and a [not_des.py](not_des.py).

`not_des.py` looks like a typical DES implementation, but with S-boxes are in this order:
>SBOXES = [S6, S4, S1, S5, S3, S2, S8, S7]

From `challenge.py`, we notice that 3 conditions need to be satisfied:

>output = Xor(DESEncrypt(inp, key), inp)
>
>if b1.key + b1.input != b2.key + b2.input
>
>if b1.output == b2.output
>
>if b3.output == [0]*8
>


The first condition prevents a identical key and text to be encrypted.

The second condition is colliding `Xor(DESEncrypt(inp, key), inp)`

The third condition is finding a input that maps to itself under a key.

## Solution for first 2 conditions

Firstly, notice that `XOR(a,b)=XOR(b,a)`, thus we need to find an input, when encrypted twice with different/same key, results in the same output.

This is quite a well-known vulnerability, there are 4 weak keys and 6 semi-weak key pairs.

Weak keys: When a message is encrypted with a weak key twice, it results in the same message. The 4 weak keys are:
* 0x0101010101010101
* 0xFEFEFEFEFEFEFEFE
* 0xE0E0E0E0F1F1F1F1
* 0x1F1F1F1F0E0E0E0E

Semi-weak key pairs: When a message is encrypted with a one semi-weak key, it can be decrypted with another key. The 6 semi-weak key pairs are:

* 0x011F011F010E010E and 0x1F011F010E010E01
* 0x01E001E001F101F1 and 0xE001E001F101F101
* 0x01FE01FE01FE01FE and 0xFE01FE01FE01FE01
* 0x1FE01FE00EF10EF1 and 0xE01FE01FF10EF10E
* 0x1FFE1FFE0EFE0EFE and 0xFE1FFE1FFE0EFE0E
* 0xE0FEE0FEF1FEF1FE and 0xFEE0FEE0FEF1FEF1

This allows for a extremely trivial solution

`XOR(DESEncrypt(m,k),m)=XOR(DESEncrypt(DESEncrypt(m,k),k),DESEncrypt(m,k))`

```
>>> DESEncrypt(b'\x01\x01\x01\x01\x01\x01\x01\x01',b'\x01\x01\x01\x01\x01\x01\x01\x01')
b'\xe9A\x8a\x94\xde\x9aM\xbd'
>>> DESEncrypt(b'\x01\x01\x01\x01\x01\x01\x01\x01',b'\x01\x01\x01\x01\x01\x01\x01\x01')
b'\xe9A\x8a\x94\xde\x9aM\xbd'
>>> 
# python -c "print '\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\xe9\x41\x8a\x94\xde\x9a\x4d\xbd'+'A'*16" | nc dm-col.ctfcompetition.com 1337
0 pre-image not found.
```

The payload works!

Now we're left with finding a message and key that maps back to the same message, since `XOR(m,m)=0`

Bruteforce would take way too long so lets start trying to understand the algorithm.

Looking at the `DESEncrypt` function, we see that the message is first permuted and then split into 2 strings, L and R, then they go through some transforms before being concatenated and permuted back.

```python
plaintext = [plaintext[IP[i] - 1] for i in range(64)]
L, R = plaintext[:32], plaintext[32:]
for ki in KeyScheduler(key):
  L, R = R, Xor(L, CipherFunction(ki, R))
ciphertext = Concat(R, L)
ciphertext = [ciphertext[IP_INV[i] - 1] for i in range(64)]
`
Looking through the whole function, the only line that changes the message is:

`L, R = R, Xor(L, CipherFunction(ki, R))`

Since we want the message to remain the same, we see that `L=R` and `R=Xor(L, CipherFunction(ki, R))` which implies that `CipherFunction(ki, R)=0` 

`ki` can easily be predicted with weak keys -> These weak keys remain the same even after the key schedule algorithm

Now lets look into `CipherFunction`

```python
res = Xor(Expand(inp), key)
  sbox_out = []
  for si in range(8):
    sbox_inp = res[6 * si:6 * si + 6]
    sbox = SBOXES[si]
    row = (int(sbox_inp[0]) << 1) + int(sbox_inp[-1])
    col = int(''.join([str(b) for b in sbox_inp[1:5]]), 2)
    bits = bin(sbox[row][col])[2:]
    bits = '0' * (4 - len(bits)) + bits
    sbox_out += [int(b) for b in bits]
```

So firstly our input goes into the Expand function -> `Expands 32bits into 48 bits.` , then it gets XORed with the key. Now with the resultant bits we use these as a lookup table. The first and last bit are used for the row and the middle 4 are for the column, for example, `sbox_inp=100101` being looked up would be `sbox[b11][b0010]=sbox[3][2]`, the lookup is then converted into a 4bit string and concatenated to the return value. 

We would like the return value to be 0, so the lookups should be 0. Let's look at what key options we have

Key                | ki
------------------ | --------
0x0101010101010101 | 00000000
0xFEFEFEFEFEFEFEFE | FFFFFFFF
0xE0E0E0E0F1F1F1F1 | FFFF0000
0x1F1F1F1F0E0E0E0E | 0000FFFF

We notice that there are 2 pairs of keys, if one works the other would(by just flipping all the bits), thus we only need to look at 2 keys, the first and the last.

So now we need to find a input such that `Expand(inp)` results in lookup of only 0.

```python
E = [
  32,  1,  2,  3,  4,  5,
   4,  5,  6,  7,  8,  9,
   8,  9, 10, 11, 12, 13,
  12, 13, 14, 15, 16, 17,
  16, 17, 18, 19, 20, 21,
  20, 21, 22, 23, 24, 25,
  24, 25, 26, 27, 28, 29,
  28, 29, 30, 31, 32,  1,
]
def Expand(v):
  """Expands 32bits into 48 bits."""
  assert (len(v) == 32)
  return [v[E[i] - 1] for i in range(48)]
```

This can also be visualised by having a array of length 32, being split into 8 arrays of 4, each array gets one element from the 2 arrays adjacent to it, then all the arrays are concatenated.

```
>>> Expand([i for i in range(32)])
[31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
```

Since this is then split into 8 arrays of 6, we'll have to ensure that the last 2 elements on an array are identical to the first to elements of the next array.

Firstly let's write a [script](sol.py) to print out every element that ends with a zero in the format required by CipherFunction(so like `[2][10]->101010`).

```
Format: SBOX[n],bin number for lookup
0,101111
0,100110
0,001101
0,000100
1,110111
1,110010
1,011001
1,011010
...
6,001000
7,110101
7,111100
7,000111
7,001010
```

Since there is quite little elements, trying to find a valid string by hand will be quite fast.

We try for a ki of all 0 first:

```
First lookup possible solutions:
101111
100110
001101
000100

Second lookup possible solutions:
101111110111
101111110111
001101011001
001101011010

etc...
```
[Full list](./possiblesols.txt)

However we realize that we can only do 7 lookups with all 0, but the 8th lookup can never be 0 since the last 2 digits for the 7th lookup does not correspond to the first 2 digits of the 8th lookup.

Luckily, we have another key, let's try that!

We see that we have only one solution - `010000001000000001010011111010101100001111110101`
Now 'de-expanding' it, we get `10000100000010011101011001111010`

To make sure we did not mess up:

```
>>> '010000001000000001010011111010101100001111110101'==''.join(Expand('10000100000010011101011001111010'))
True

```
Now we just have to concat 2 of this together and invert the permutation, then we're done!

```
>>> ''.join(['1000010000001001110101100111101010000100000010011101011001111010'[IP_INV[i] - 1] for i in range(64)])
'0011000000001111110011000011001100001111000000110000111111001100'
```
Now let's update the payload

```
python -c "print '\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\xe9\x41\x8a\x94\xde\x9a\x4d\xbd'+'\x1F\x1F\x1F\x1F\x0E\x0E\x0E\x0E'+'\x30\x0F\xCC\x33\x0F\x03\x0F\xCC'" | nc dm-col.ctfcompetition.com 1337
CTF{7h3r35 4 f1r3 574r71n6 1n my h34r7 r34ch1n6 4 f3v3r p17ch 4nd 175 br1n61n6 m3 0u7 7h3 d4rk}
```

Another solution also exist due to the weak keys being invertible, the other solution(trivially) is

```
python -c "print '\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\x01\x01\x01\x01\x01\x01\x01\x01'+'\xe9\x41\x8a\x94\xde\x9a\x4d\xbd'+'\xE0\xE0\xE0\xE0\xF1\xF1\xF1\xF1'+'\xCF\xF0\x33\xCC\xF0\xFC\xF0\x33'" | nc dm-col.ctfcompetition.com 1337
CTF{7h3r35 4 f1r3 574r71n6 1n my h34r7 r34ch1n6 4 f3v3r p17ch 4nd 175 br1n61n6 m3 0u7 7h3 d4rk}
```

> Flag: CTF{7h3r35 4 f1r3 574r71n6 1n my h34r7 r34ch1n6 4 f3v3r p17ch 4nd 175 br1n61n6 m3 0u7 7h3 d4rk}

p.s. when using ip instead of ip_inv, i got \xCC\xCC\x55\x22\x55\x88\xAA\xCC, just a interesting observation

