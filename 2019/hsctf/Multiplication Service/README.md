# Multiplication
>Multiplication is safe, right?
>[problem.sage](problem.sage)

We are given [problem.sage](problem.sage), and a server to nc to.

## Problem

The challenge server implements a twisted Edwards curve(Ed448), and has a point multiplication oracle. 

However, the oracle does not check if our point is on the curve, allowing us to input arbituary points

## Exploit

If we multiply the point `(0,y)` by s, we get `(0,y^s)`, so we have effectively reduced this into a Diffie-Hellman problem.

Solving Diffie-Hellman for a large non-smooth number would not be possible. Fortunately, we got bounds on `s%pn` where `pn` are multiples of `p-1`. The usual attack for Diffie-Hellman is with Pohlig-Hellman, and solving the subgroups with BSGS.

Since we have bounds(b) on the solution to the smaller subgroup, we can store `g^n` from `0` to `sqrt(b)`, and check if `h/g^(sqrt(b)n)` from `0` to `sqrt(b)` is in.

There are `2` solutions since `g^0=g^1=1(mod 2)`, we simply try both solutions, and by using another point, we notice only the case g^0=1(mod2) works, so we simply use that in the CRT to obtain the private key.

Solution script at [solve.py](solve.py) 

> Flag: `hsctf{41W4YZ_v4lid473_those_curve_points_a94hg39}`
