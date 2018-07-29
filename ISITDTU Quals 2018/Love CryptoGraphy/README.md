# Love Cryptography
>We are given a [love\_cryptography.py](love_cryptography.py) and a [enc](enc)

This looks like a simple cipher where the character is multiplied and then added by a constant modulo n

>ciphertext[i]=(m*ord(message[i])+c)%n

This looks quite easy to exploit, each character will be mapped to the same sequence.

Furthermore part of the ciphertext is given to us

>assert "ISITDTU" in mes

So firstly I tried to find instances of "I?IT?T", however my script accidentally double printed and I was left thinking that this wasn't the right way to solve

```python
for i in range(2,len(enc)):
    if(enc[i] not in seen):
        seen.append(enc[i])
    if(enc[i]==enc[i-2]):
        print(str(seen.index(enc[i]))+"True")
    print(seen.index(enc[i]))
#try to spot the fatal error
```

I saw 

```
19
20
19True
19
21
22
21True
```

in the output, which seemed like my code found "I?IIT?T", however I forgot to write an ```else:```, causing it to double print, spent an hour trying to figure out why it didn't work until my teammate(Tuan Linh) gave me the position of "I?IT?T"

Now knowing where ISITDTU is, we can finally start the calculating m,n,c

## Exploit

First, notice that S,T,U are constitutive ASCII letters, that means that ```ord(S)+1=ord(T)``` and ```ord(T)+1=ord(U)```

Now if we look at how the ciphertext is generated, we found an easy way to calculate m%n, which can be treated as m under integers mod n

```
m1=enc[pos of T]-enc[pos of S]
m2=enc[pos of U]-enc[pos of T]
```

When we run this to find m1 and m2, we see that m1 is positive but m2 is negative. This means that enc[pos of T]+m>n, thus enc[pos of U]=enc[pos of T]+m-n

Thus we got m and n already, c can also be obtained easily

m*ord(S)+c=enc\[pos of S\](mod n)

and c is easily obtained

Thus we have a simple code to calculate m,n and c

```python
m1=enc[T]-enc[S]
m2=enc[U]-enc[T]
n=abs(m1-m2)#empirically observed that m2 is negative and m1 is positive
m=m1%n#just in case i mess up
c=(enc[S]-m*ord("S"))%n
```

Since we know ```ciphertext[i]=(m*message[i]+c)%n```, we can calculate message[i] by ```message[i]=(k*(ciphertext[i]-c))%n``` where k is a number that satisfies ```k*m mod n=1```, which can be easily computed with the Euclidean algorithm

[exploit.py](exploit.py)

>Flag: ISITDTU{break_LCG_unknown_all}
