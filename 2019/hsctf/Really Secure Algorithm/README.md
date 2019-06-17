# Really Secure Algorithm
>I heard about RSA, so I took a go at implementing it.
>[secure.txt](secure.txt)

We are given [secure.txt](secure.txt), which are RSA parameters.

Running yafu on `n`, we see that `n` is `p^2` where `p` is a large prime.

The solution is pretty simple, since `phi(p^2)=(p-1)p` when `p` is prime, and we simply calculate `ed=1(mod p(p-1))` and `m=pow(c,d,n)`.

> Flag: `hsctf{square_number_time}`
