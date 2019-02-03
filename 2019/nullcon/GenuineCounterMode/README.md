# GeniuneCounterMode
>server runs on
>nc crypto.ctf.nullcon.net 5000
>can you get the flag?

We are given a [server.py](./server.py).

This challenge wants us to forge a message that is encoded with AES CTR, and there's a MAC code(GHASH)

##AES CTR forging

AES CTR is relatively simple to forge, given a plaintext(pt) and a ciphertext(ct), if the nonce is the same, `pt^ct` is always constant.

##GHASH

GHASH function is a pseudo-hashing function.

First it calculates 

`c = AES.new(key, AES.MODE_ECB).encrypt(nonce + bytes(3) + b'\x01')`

`H = AES.new(key, AES.MODE_ECB).encrypt(bytes(16))`

and splits the ciphertext into blocks of 128 bits(`b1,b2,b3...`)

The GHASH is then calculated by `c+b1H^1+b2H^2+...+bnH^n` where `n` is the number of blocks and each of the summand is under `mod n`

c constant for a fixed nonce, and H is constant throughout, this suggests a nonce reuse attack. Luckily the nonce is calculated using `sessionid + Random.get_random_bytes(2)`, so nonce reuse will be very common.

##Calculating c and H


Since we need to forge 2 blocks in the final payload, our payload should be 2 blocks

First we find 2 plaintext-ciphertext pairs with the same nonce, we label them as `pt11+pt12`,`pt21+pt22` and `ct11+ct12`,`ct21+ct22`(where `xxx1` is the first block and `xxx2` is the second block), and the respective GHASH as `g1`,`g2`.

The GASHes in terms of the pt,ct,c,H are :

`g1=c+ct11*H+ct12*H**2`
`g2=c+ct21*H+ct22*H**2`

Supposing `ct12=ct22`(equivalent to `pt11=pt12`), `c` and `H` can easily be found:

`g1-g2=ct11*H-ct21*H`
`H=(g1-g2)/(ct11-ct21) (mod n)`
`c=g1-ct11*H-ct12*H**2 (mod n)`

##Forging

Forging is now very simple. The text we want to forge is `f="may i please have the flag"`

Let the nonce be the nonce that was repeated(so that we know what c is)

The ciphertext is simply `pt11^f^ct11`

GASH is `c+f1*H+f2*H**2` where `f1` is the first 16 characters/128 bits

Full exploit: [solve.py](./solve.py)

> Flag: `hackim19{forb1dd3n_made_e4sy_a7gh12}`

p.s. A much simpler way of getting c is literally xoring the last block of the ciphertext with the plaintext, since `c=AESECB(k,nonce+'\x00\x00\x00\x01)` and the first plaintext is xored with the exact same value
