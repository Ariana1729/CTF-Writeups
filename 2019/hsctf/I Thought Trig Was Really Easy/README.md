# I Thought Trig Was Really Easy
>After finishing a hard lesson in geometry class, Keith decided that he wanted to put your understanding of trig and python to the test. Can you solve his challenge?
>[trig\_is\_really\_hard.py](trig_is_really_hard.py)

We are given [trig\_is\_really\_hard.py](trig_is_really_hard.py), which is basically a custom hashing algorithm.

## Details

This hashing algorithm output depend on the length on the input, more specifically, `2+3+...+(n+1)=n(n+3)/2`

The program 'hashes' our input, then compare with a preexisting hash. 

Playing around with this, we notice that any changes to the plaintext will only affect the characters afterwards, so all the digits that have been generate remain untouched.

## Solution

The length of the hash is `90`, thus the length of our solution is either `-15` or `12`. `-15` seems a bit hard to achieve so we'll assume `n=12`

Now we simply bruteforce each character, ensuring that the length remains at 12 and start matching more and more of the given hash.

> Flag: `hsctf{:hyperthonk:}`
