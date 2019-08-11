# Time Capsule

> You neither need 35 years nor even 20 years to solve this problem!

## Challenge

The goal is basically to compute `l = pow(2, pow(2, t), n)`.

Note that `pow(2, x, n) = pow(2, x % phi(n), n)`

`n` is easily factored with yafu, and the calculation is trivial from there

> Flag : `CCTF{_______________________________________________Happy_Birthday_LCS______________________________________________}`
