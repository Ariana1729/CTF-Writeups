# Baby
>nc 35.185.178.212 33337 or nc 35.185.178.212 33338
We are given a [baby.py](baby.py)

It looks like the server just sha512s (flag|input) and then sends the hash to us, which allows for a very simple exploit.

## Exploit

First, we send 0, obtaining the sha512 of the flag.

Next, we send 2^(i-1), checking if the hash changed, if the hash changed, then set the ith bit of the flag to 0, else if the hash is still the same, set the ith bit of the flag to 1

### Logic

Consider a simple flag 0b01

First, we send 0, obtaining the sha512 of 0b1001

Next, we send 0b1, we get the sha512 hash of 0b1001|0b1=0b1001, which did not change. The only way it won't change is if the OR operation did not affect our flag, or more mathematically, FLAG|INPUT=FLAG. Since 1|1=1 and 0|1=1, the first bit must be 1

Next, we send 0b10, we get the sha512 hash of 0b1001|0b10=0b1011, which is different(only one bit changed, idt it's possible to hash collide?). Therefore the second bit is 0.

We continue this till we obtain every bit of the flag.

[exploit](exploit.py)


>Flag: ISITDTU{bit\_flipping\_is\_fun}

p.s. the server response is incredible, probably the fastest I've ever seen, especially for such a challenge where you have to solve bit by bit
