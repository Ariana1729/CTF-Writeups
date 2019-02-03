# MHA(Lighter)
>I made a very silly hashing algorithm, but I love it cause its mine.
>And I also live in denial that it has no collisions.
>Just find me one collision and take the flag.
>[Code](hash.py)
>[Website](http://35.198.113.131:9000/)

We are given [code](hash.py), which is a hashing function for images, and are asked to find a hash collision.

Reading the code, a very clear flaw appears

```python
size=int(math.floor(math.sqrt(len(pic))))
pic=pic[0:size*size]
```

if `len(pic)` is non-square, then some parts of `pic` are spliced away. If we just change the parts that are spliced, we have an extremely trivial collision.

```python
    for i in range(small):
        curr=[]
        for j in range(i,small):
            curr.append(pix[i,j])
        for j in range(i+1,small):
            curr.append(pix[j,i])
        <computes sum,mul,sub based on curr>
        pic.append((sum%256,mul%256,sub%256))
```

Consider a `2x2` image, with pixels `[(a1,a2,a3),(b1,b2,b3),(c1,c2,c3),(d1,d2,d3)]`.

In the first iteration of the for loop, `cur=[(a1,a2,a3),(b1,b2,b3),(c1,c2,c3)]`

In the second iteration of the for loop, `cur=[(d1,d2,d3)]`

Other possiblities of collision is simply letting `a1+b1+c1` or `a2*b2*c2` or `a3+b3+c3` stay invariant in both images under `mod 256`, but there is a even simpler collision.

Since `pic` is spliced, `pic` would only get affected by the first iteration, so `(d1,d2,d3)` have absolutely no effects on the hash. Thus we just [generate](gen.py) 2 2x2 images with the bottom right pixel different and we're done

> Flag: `evlz{md5_is_lub}ctf`
