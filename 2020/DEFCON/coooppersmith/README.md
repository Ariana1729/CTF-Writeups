# coooppersmith

> I was told by a cooopersmith that I should send hackers encrypted messages because it is secure.

Files: [service](service)

## Challenge(RE)

The challenge first asks for some user input in hex that is at most 120 characters long, we shall denote the number that it represents by `a1`

The challenge is primarily located at offset `1E25`, the previous function was initializing values and final function is freeing values.

#### Offset `18C4`

The input value is passed to a function at offset `18C4` that has a loop to increment some number until it passes a prime check. This number is generated in a strange manner: `x = int(a1,16)<<((0x80 - len(a1))*4) + randint(0,1<<((0x80 - len(a1))*2)-1)`

Note that `int(a1,16)<<((0x80 - len(a1))*4)` basically shifts our input until it is larger than `16^128` while the second part randomizes the lower `((0x80 - len(a1))*2)` bits. Since `a1` is at most of length `120`, this randomizes at least the last `2` bytes.

The function then increments this until either the upper `a1` portion gets overwritten, in that case it chooses another random integer, or stops when it is prime.

One can also verify that the prime check is not faulty by breaking at offset `1A43` in gdb and tracing the pointer path from `$rbp-0x28`:

```
(gdb) x/2gx $rbp-0x28
0x7fffffffe508:	0x0000555555758df0	0x0000555555758e10
(gdb) x/2gx 0x0000555555758df0
0x555555758df0:	0x0000555555758fe0	0x0000000900000008
(gdb) x/10gx 0x0000555555758fe0
0x555555758fe0:	0xffffffff00001f01	0xffffffffffffffff
0x555555758ff0:	0xffffffffffffffff	0xffffffffffffffff
0x555555759000:	0xffffffffffffffff	0xffffffffffffffff
0x555555759010:	0xffffffffffffffff	0xffffffffffffffff
0x555555759020:	0x0000000000000000	0x0000000000000051
```
and indeed verify that `0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00001f01` is a prime

So now we have a prime that we know the top bits off, in fact since only the bottom 2 bytes are unknown, those can be brute forced(alternatively later on we can use coppersmith's algorithm as intended)

#### Offset `1DD8`

Next, this prime is passed into the function at offset `1DD8` that generates a RSA key. This function calls the function at offset `14D8` twice. This function outputs possible primes and takes in 2 parameter, first is the prime `a` that was generated, then the next a parameter is some number such that it would not output that number, this is to avoid having a key of the form `p^2`. Then a RSA key is generated from these primes.

#### Offset `14D8`

This function generates some random integer, `r`, that is less than `a`. Then it output `2ra+1` if it is probably a prime with a really strange check.

First it runs Miller-Rabin with base 3, then for `p=2ra+1` it checks if the gcd of `k^r%p` and `p` and checks if it is 1 for `k=3,5,7`. This seems to be a pretty bad check as counterexamples are very common, but it does work for primes as the whatever the gcd outputs is a factor of `p`.

By debugging with gdb after both calls to offset `14D8` are done(which takes a few seconds), then we can trace the pointer path from `$rbp-0x8` and `$rbp-0x10` to check if they are indeed prime, which seems true for most of the time, and we can also verify that these primes are indeed of the form `2ra+1`.

These primes are then fed into a RSA key generation function and is passed to the function at offset `1B3E` and if the function outputs `True`, the encrypted flag will be printed

#### Offset `1B3E`

This function isn't too interesting, it seeds `srand` with `time(0)` and encrypts `What's the sum of {rand()} and {rand()}` and asks for the user to give that value, which can easily be done by just running a separate C program right when the prompt is given instead of decrypting the message.

## Challenge(Crypto)

The crypto part isn't too interesting but there are several ways to go about solving it.

A tl;dr of RE portion, we have a prime `a` and `2` random numbers `r1,r2` less than `a` such that `2r1a+1` and `2r2a+1` are primes. These primes are used to construct the RSA key.

We can control the top `80` bytes of `a` and only the lowest `2` bytes remain unknown. Since `N%(2a)=1`, this allows us to easily brute force `a`. Alternatively, we have an extremely good approxmation of `a` since out of `64` bytes, only `2` are unknown, so we can run coppersmith with `N-1` as the modulus, or even better, factor out the small primes form `N-1` before running coppersmith.

Now that we have recovered `a`, notice that `N=4a^2r1r2+2a(r1+r2)+1` with `r1<a` and `r2<a`. This allows us to easily recover `r1` and `r2`, hence the primes and decrypt the flag:

```
(N-1)/(2a) % 2a = r1+r2
(N-1-2a(r1+r2))/(4a^2) = r1r2
```

> Flag: `OOO{Be_A_Flexible_Coppersmith}`
