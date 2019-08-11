# Clever Girl

> There is no barrier to stop a [clever girl](clever_girl.py)!

## Challenge

This is basically a normal RSA, with some condition for the primes

```
 p    q+1   2s-X   2N+p+q+1
--- + --- = ---- = --------
p+1    q     s+Y     N+q
```

It's quite unlikely that the fraction simplifies so we simply assume we have 2 equations:

```
2s-X = 2N + p + q + 1
s+Y = N + q
```

Simplifying this to solve for the primes, we get

```
2Y + X = q - p + 1
(2Y + X - 1)q = q^2 - N
```

and the quadratic can easily be solved for `q`, thus `p` can also easily be solved

## Getting the flag

Since `e=0x20002`, we calculate `m^2` by using `e=0x10001`, then using CRT, we compute `m mod p` and `m mod q` and find `m mod N`

```sage
mp = mod(m2,p).sqrt()
mq = mod(m2,q).sqrt()
m = crt([int(mp),int(mq)],[p,q])
```

> Flag : `CCTF{4Ll___G1rL5___Are__T4len73E__:P}`
