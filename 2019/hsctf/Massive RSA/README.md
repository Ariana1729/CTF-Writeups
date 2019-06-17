# massiversa
>I was scared that my RSA would be broken, so I made sure that the numbers were massive.
>[massive.txt](massive.txt)

We are given [massive.txt](massive.txt), which are RSA parameters.

Running yafu on `n`, we see that `n` is very likely a prime, and passes the fermat test.

The solution is pretty simple, since `phi(p)=p-1` for all primes, and we simply calculate `ed=1(mod n-1)` and `m=pow(c,d,n)`.

> Flag: `hsctf{forg0t_t0_mult1ply_prim3s}`
