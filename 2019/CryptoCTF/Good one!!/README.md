# Good one!!

> So you work, and you pay

> And you break your back for another day

This isn't really a crypto chal, its more of a programming challenge

## Challenge

We are given some fancy cipher that expands the message into decimal, replaces `0` with a random string and runs the cipher

x, y = 1, 0
    for t in reversed(seq):
        x, y = y + x * t ** 2, x

We are given `'enc = %s%s' % (x - y, y + x)`

Since `y` is about a order of magnitude smaller than `x`, we can assume that `x-y` and `y+x` have roughly the same order of magnitude, with `x-y<y+x`, so we simply slice [the encrypted flag](flag.enc) to half and check if that condition holds. And from these `2` values we easily obtain `x` and `y`.

Now we basically undo the operation with optimised brutefroce.

## Bruteforce

First notice that `t` is bounded from above, and a large `t` would terminate faster than a small `t`, so we bruteforce from `t=9` down to `t=1`(all `0`s are replaced)

```python
def solve(x,y,c):
    #some stopping condition to return -1
    i=9
    while x<y*i*i:
        i-=1
    while i>0:
        t=solve(y,x-y*i*i,c+[i])
        if(t!=-1):
            return t
        i-=1
```

Here the function takes `3` inputs, the history(`c`), and `x,y`. The previous `x,y` are simply computed as `y,x-y*i*i`. Now we need to figure some condition that terminates this recursion, and return `-1`, or some condition that is a success.

Notice that if `y=0` but `x!=1`, this is not possible, so we terminate any paths that end here. However if `y=0` and `x=1`, this is the starting values, so the path must be a possible solution. However, there may be other solutions so we simply print this.

```python

def solve(x,y,c):
    if(y==0):
        if(x==1):
            print c
        return -1
    i=9
    while x<y*i*i:
        i-=1
    while i>0:
        t=solve(y,x-y*i*i,c+[i])
        if(t!=-1):
            return t
        i-=1
```

Running this, we only get one output:
```
[3, 2, 7, 5, 1, 7, 9, 4, 7, 5, 1, 7, 9, 1, 2, 8, 6, 8, 9, 3, 8, 2, 5, 8, 9, 2, 2, 1, 7, 5, 1, 7, 9, 6, 6, 4, 4, 7, 5, 1, 7, 9, 7, 7, 7, 5, 1, 7, 9, 2, 8, 7, 1, 2, 7, 3, 1, 7, 6, 7, 8, 3, 8, 2, 1, 5, 4, 3, 4, 4, 5, 7, 3, 8, 4, 3, 7, 5, 1, 7, 9, 6, 1, 3, 6, 6, 1, 7, 5, 1, 7, 9, 7, 5, 1, 7, 9, 2, 3, 7, 3, 2, 8, 2, 9, 6, 6, 6, 2, 2, 3, 2, 7, 5, 1, 7, 9, 9, 7, 5, 1, 7, 9, 2, 7, 9, 9, 1, 6, 6, 9, 1, 5, 3, 6, 7, 5, 1, 7, 9, 7, 5, 1, 7, 9, 5, 1, 8, 2, 9, 2, 6, 6, 9, 7, 5, 1, 7, 9, 5, 8, 5, 5, 8, 8, 7, 5, 1, 7, 9, 4, 6, 4, 2, 5, 7, 5, 1, 7, 9, 7, 5, 1, 7, 9, 2, 6, 5, 9, 7, 5, 1, 7, 9, 8, 7, 7, 5, 1, 7, 9, 7, 9, 8, 2, 6, 2, 9, 2, 2, 5, 5, 9, 7]
```

## Finding the 0s

Putting this together, we get the string
```
3275179475179128689382589221751796644751797775179287127317678382154344573843751796136617517975179237328296662232751799751792799166915367517975179518292669751795855887517946425751797517926597517987751797982629225597
```
Now we simply check for which string is the most common(in vim simply `/<guessed string>`)

The string `75179` appears extremely often, so it is replaced with `0` and then converted to an integer, which gives us the flag

> Flag : `CCTF{C0nt1nu3D_Fr4ct1oN_Al9ori7hm_iN__EncryP7iOn_iZ__viv1D}`
