# Simple RSA
>We are given a [simple_rsa.py](simple_rsa.py)

This is just a typical RSA factorization attack, just fancier and forces you to either be amazing at getting code from github and/or know how RSA works

First we notice that N isn't just made from 2 primes, it actually is 4 primes multiplied together. These 4 primes satisfy the relation

```
p2=10p1+c1
p3=10p2+c2
p4=10p3+c3
```

where `c1,2,3` are some small constants so that `p2,3,4` are prime and `p1` is 251 bits long. 

## Factoring

Using `p1*p4≈1000p1^2=(100p1)*(10p1)≈p2*p3`, we see that this is a basic setup for fermat factorization, thus I just went to github to grab some [fermat factorization code](fermat.py) to find `p1*p4` and `p2*p3`

```
p1*p4=24556891073418994576751524607635760117996811894972202516187698043229292302109114380884247668494990605537878648233446996676371523211326680052450374168750431
p2*p3=24556891073418994576751524607635760117996811894972202516187698043229292302185592473522031534536176858756163591603824821794497153855658790721132779232081801
```

We know that p4≈1000p1 and p3≈10p2, thus we can use coppersmith attack on it. MeePwn recently had a similar challenge where 7331q≈1337p but the last 512 bits are scrambled. For here, after some approximation using Daniel Goldston, János Pintz and Cem Yıldırım's estimation of prime gaps(2007), I chose the error to be 17 bits, then I used p4's code, [modified a little](coppersmith.sage), ran on [sagecell](http://sagecell.sagemath.org/), and got all 4 [primes](primes.txt).

## Decrypting message

Ok so we got all 4 primes, how do we decrypt?

We know that `m^e mod N=c`, thus we need to find a number d such that `m^(ed) mod N=m=c^d`

Using Euler's theorem, we know that `ed mod φ(N)=1`, and since N is just a product of 4 primes, `φ(n)=(p1-1)(p2-1)(p3-1)(p4-1)`

With this we can easily [decrypt](decrypt.py) and get the flag

>Flag: ISITDTU{f6b2b7472273aacf803ecfe93607a914}

p.s. I believe that `p1` is 251 bits long to emulate 512-bit RSA. Notice how `N=p1*p2*p3*p4≈(1000p1^2)^2`, `1000p1^2` is likely to be 512 bits long(`log2(10)^3+251*3=511.965784...`)
