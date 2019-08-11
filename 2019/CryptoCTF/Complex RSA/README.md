# Complex RSA

> Things in this world sometimes are different than they appear!

> nc 167.71.62.250 14559

## Challenge

```
Challenge loading... be patinet :)
|-------------------------------------|
| Options: 	  	              |
|	[E]ncrypted message           |
|	[K]ey generation function     |
|	[S]end the decrypted message  |
|	[T]ry encryption              |
|	[Q]uit                        |
|-------------------------------------|
```

The key gen function:

```
def gen_key(e, nbit):
	p = getPrime(nbit << 2)
	q = getPrime(nbit >> 2)
	print 'p =', p
	print 'q =', q
	n = p * q
	return (e, n)
```

Here one prime would be small, so factorization should be quite easy

```
Send your Options:
T
Send your input as a pair (a, b):
(2,0)
((a + b √-1) ** e) (mod n) = (123370139733460288741582133541967208151544163810581515437516558669972425636530931666673004837858749022601996874821486288752958977088089060539584311969624273734612352083467285311016219043536527442528687720647804943357024821973693691292035336507137095064124150626846570159166238804148372798356772669L, 0L)
Send your Options:
T
Send your input as a pair (a, b):
(0,1)
((a + b √-1) ** e) (mod n) = (0L, 1L)
Send your Options:
T
Send your input as a pair (a, b):
(-1,0)
((a + b √-1) ** e) (mod n) = (337390295386784062735892530953812027731217626577827868683652203476748859812364337575664693191200613632654265062075499825596838397609731917692839810645496096834742890659029158682118916487432458937074956757871632389547383580967613523944154703997016734902928913508657661928209328770940675037982298198L, 0L)
```

Trying some inputs, we see that this basically extends RSA into the gaussian integers, and negative numbers works too.

Since negative numbers works, finding `n` is trivial `n = (n-1)+1`

Assuming `e` is small, finding `e` is simple by discrete log

Now we need a way to do complex modular arithmetic

## Complex modular arithmetic

Adding amd multiplying is trivial, exponentiation is done by square and multiply:

```
def cadd(a,b,n):
    return (a[0]+b[0]%n,a[1]+b[1]%n)

def cmul(a,b,n):
    return ((a[0]*b[0]-a[1]*b[1])%n,(a[0]*b[1]+a[1]*b[0])%n)

def cpow(a,k,n):
    if(k==0):
        return (1,0)
    if(k==1):
        return a
    if(k%2==0):
        a=cmul(a,a,n)
        return cpow(a,k/2,n)
    else:
        return cmul(a,cpow(cmul(a,a,n),(k-1)/2,n),n)
```

## Order of multiplicative group

Usually in RSA, we simply compute `phi(n)` then invert `e` under `phi(n)`, but now it's with complex numbers, so this may not work

We first consider the order of `C/pC*` where `p` is a prime. The real and imaginary parts ranges from `0` to `p-1`, so a valid assumption is that the order is a multiple of `p*p-1`(since `0,0` can't be in the group). The order is exactly `p*p-1` for `p=3 mod 4` since it cannot be expressed as the sum of `2` squares, but for `p=1 mod 4` it is less, and it is a multiple of `p*p-1`.

Thus if we want to find `g` given `g^e=a mod p`, we simply invert `e` under `p*p-1`.

For `n=pq`, the order is a multiple of `lcm(p*p-1,q*q-1)`, then it's trivial

For factoring `n` we simply use yafu

> Flag : `CCTF{_____e^(i*PI)=-1_____}`
