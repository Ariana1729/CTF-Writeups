# cotan
>(lost)

The challenge name suggests that the elliptic curve is singular.

## cotangent

In real numbers, this is effectively finding `n` given `cot(n*acot(2))=k`, however, the challenge is in a `Z/pZ` group

Consider how cotangent is related to the complex exponent: `cot(x)=i(e^(2ix)+1)/(e^(2ix)-1)` and `cot(nx)=i(e^(2nix)+1)/(e^(2nix)-1)`. Performing the substitution `u=e^(2ix)` and setting , we get `cot(x)=i(u+1)/(u-1)` and `cot(2x)=i(u^n+1)/(u^n-1)`

## i in Z/nZ

Plugging in the values from the challenge, we have `2=i(u+1)/(u-1)` and `c=i(u^n+1)/(u^n-1)`(where `c=0x4e8f206f074f895bde336601f0c8a2e092f944d95b798b01449e9b155b4ce5a5ae93cc9c677ad942c32d374419d5512c`)

Now we need to somehow express `i` in `Z/pZ`. Since `i=sqrt(-1)`, we simply need to find a number such that `x^2=p-1 (mod p)`, which is trivial for `p!=1 (mod 8)`(here `p=5 (mod 8)`). Both solutions would work here.

## solving for u, u^n and n

```
2=i(u+1)/(u-1)
2u-2=iu+i
(2-i)u=i+2
u=(2+i)/(2-i)
```
Similarly, 

```
c=i(u^n+1)/(u^n-1)
u^n=(c+i)/(c-i)
```

Now it's just a discrete log problem, which takes some time to [solve](solve.sage)(15mins on my old and broken laptop)

> Flag: `AceBear{_I_h0p3__y0u_3nj0y3d_1t_}`
