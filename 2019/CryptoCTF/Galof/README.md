# Galof

> A group of sheaves of grain stood on end in a field!

The description makes this challenge sound complicated, with abstract algebra and algebraic geometry but the challenge is actually quite simple

## Challenge

The cipher is basically doing `c=k1/m+k2 mod b` where these are polynomials instead of integers, however most normal operations works for polynomials.

We are also given a lot of `m,c` pairs, though only `2` was needed

Furthermore everything is done in `GF(2)`, which simplifies a lot, addition and subtraction are also the same thing which is quite convenient

## Solution

Using `2` pairs of `m,c`, we get(under mod b):

```
c1 = k1/m1 + k2
c2 = k1/m2 + k2
c1m1 = k1 + k2m1
c2m2 = k1 + k2m2
k2 = (c1m1+c2m2)/(m1+m2)
k1 = m1*(c1+k2)
```

Now using these keys, we can easily retrive the flag

> Flag : `CCTF{GF2_F1nI73_Crc13_f1elds}`
