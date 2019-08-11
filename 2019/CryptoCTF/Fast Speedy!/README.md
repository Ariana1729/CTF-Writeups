# Fast Speedy!

> You can’t connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future.

## Challenge

This is basically a XOR cipher on a picture, with a unknown key and a known key generation function

## Cipher

```python
def drift(R, B):
    n = len(B)
    ans, ini = R[-1], 0
    for i in B:
        ini ^= R[i-1]
    R = [ini] + R[:-1]
    return ans, R
```
Notice that the order of `B` doesn't matter since XOR is commutative

```python
r = random.randint(7, 128)
s = random.randint(2, r)
R = [random.randint(0, 1) for _ in xrange(r)]
B = [i for i in xrange(s)]
random.shuffle(B)
```
Here `random.shuffle(B)` doesn't matter as XOR is commutative. Here we get bounds for the size of `R` and `B`

```python
for i in range(len(flag)):
    ans, R = drift(R, B)
    A = A + [ans]
    enc = enc + [int(flag[i]) ^ ans]
```
Encryption basically takes the first output of `drift` and XORs it into the flag. Looking at drift, the first `r` outputs is basically `R[::-1]`, and we use this to bruteforce possible `R` and `B`

## Bruteforce

The first `16` characters of a PNG file is likely to be `0x89504e470d0a1a0a0000000d49484452`, so we simply take the first few bits, run drift on all possible values of `B` and check if it matches, else take more bits, this is done at [findR.py](findR.py).

Large `R` length may not be correct as it basically takes most of the known text to predict `R`, so we choose the smallest output

```
r = 13
b = 5
R = [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1]
```

Since XOR is its own inverse, we simply rerun the script, but the encrypted file is used as input and output is the decrypted file. The decrypted file is a picture of the flag

> Flag : `CCTF{LFSR__In___51mPL3___w0rD5}`
