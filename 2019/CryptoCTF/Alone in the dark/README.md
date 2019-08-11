# Alone in the dark
> We are alone in the dark with a [single line](alone_in_the_dark.py)!

The python script only has one line that constraints the variables

```python
assert ((u+1)**2 + u**2 - v**2)**2 + ((x+1)**3 - x**3 - y**2)**4 + (gmpy2.is_prime(v) + 1)**6 + (gmpy2.is_prime(y) - 1)**8 + (len(bin(u)[2:]) - 664)**10 + (len(bin(x)[2:]) - 600)**12 == 664 - 600
```

Notice that the exponents are even and get pretty large, while the RHS is 64

## Splitting the constraints

We write a simple script to brute force what are the possible values of the multiple constraints:

```python
for a in range(9):
    for b in range(0,3):
        for c in range(0,3):
            for d in range(0,1):
                for e in range(0,1):
                    for f in range(0,1):
                        if(a**2+b**4+c**6+d**8+e**10+f**12==64):
                            print (a,b,c,d,e,f)
```

This code outputs `2` values, 

```
(0, 0, 2, 0, 0, 0)
(8, 0, 0, 0, 0, 0)
```
The second one isn't possible as it implies `gmpy2.is_prime(v) + 1 = 0`, but `is_prime` would either be `0` or `1`, so only the first output is possible, this translates to

```
(u+1)**2 + u**2 == v**2 # 1
(x+1)**3 == x**3 + y**2 # 2
gmpy2.is_prime(v) == 1 # 3
gmpy2.is_prime(y) == 1 # 4
len(bin(u)[2:]) == 664 # 5
len(bin(x)[2:] == 600 # 6
```

## Solving the constraints

### 1, 3, 5
This is basically a Twin Pythagorean Triple, which has a closed form solution from the Pell's equation

```python
( (sqrt(2)+1)^(2*r+1) - (sqrt(2)-1)^(2*r+1) )/4 + (-1)^r/2
```
Notice that the second term is insignificant, so we use the first term to approximate `r`, since we know this value is about `2^664`, some simple logs givess us a value of about `r=261`, using this value, we get

```python
u = 38870796548368940451592529482185869982938448205812640195914560739542103841403178847163517462769143179065031576973812014377488506777895445800461891869308645201761858965032907136032847098509289762520539
v = 54971607658948646301386783144964782698772613513307493180078896702918825851648683235325858118170150873214978343601463118106546653220435805362395962991295556488036606954237309847762149971207793263738989
```

which satisfies conditions 1,3,5

### 2, 4, 6

Simplifying condition `2`, we get `3x^2+3x+1=y^2` which is a simple conic section, and by abusing Pell's equation again, the solutions of x are

```python
( (-3-2*sqrt(3))*(7-4*sqrt(3))^r + (-3+2*sqrt(3))*(7+4*sqrt(3))^r - 6 )/12
```
again a similar analysis gives us a `r` of about `159`, and using this we obtain

```python
x = 2929219721139577720733862051859801690342725739320715630102152440665051724895027651815801589822478988305846846083549661332897318938724576681923803796059612952236038798314710140134264
y = 5073557383546487137945410473466556718830129339025213837451156233563658135296353459994544781708539660966095175852902937975236171859961262538393568510313468641105066779787434237464141
```

which satisfies 2,4,6

### Flag

The flag is given by

```

flag = 'CCTF{' + sha256(str(u) + str(v) + str(x) + str(y)).hexdigest() + '}'
```

> Flag: `CCTF{07f594e5fb8f6d5f82e5cce06e2a2c74c1bffce370cd904821fdd71027faa084}`
