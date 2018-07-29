# aes\_cnv
>nc 35.185.111.53 13337
>
>See more challenges: [chung96vn](https://github.com/chung96vn/challenges)

We're given a [AES\_CNV.py](AES_CNV.py) and a [challenge.py](challenge.py)

The AES\_CNV looks like a modified type of AES, should be pretty interesting

The goal of this would be to find a ciphertext with and IV that results in `Give me the flag` as the first block

However, the encryption oracle does not allow encrypting anything with `Give me the flag` as the first block

## Analyzing AES\_CNV

Padding function:

```python
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
```

Notice that pad will actually add an extra block at the end, `"\x10"*16`, if the input size is a multiple of 16, like a typical AES_CBC(and other schemes too) padding


toblock(): splits array at every 16 bytes

tostr(): concatenates everything in array

xor(a,b): XORs the highest bytes of a and b and outputs it, if either is empty, output the other input


```python
def encode(self, m):
    m_ar = toblock(pad(m))
    p_ar = []
    for i in range(len(m_ar)):
        p_ar.append(xor(m_ar[i], self.secret[i%len(self.secret)]))
    p = tostr(p_ar)
    return self.aes.encrypt(p, os.urandom(BLOCK_SIZE))
```

Here we see that our message is first padded, converted to a block, then XORed with some unknown secret, probably 16 bytes long(otherwise I'm not sure if it's easily solvable), and this **secret is fixed, and finite**. After that the result is sent to be encrypted with a random IV

```python
def encrypt(self, plain_text, iv):
    assert len(iv) == 16
    plain_text = pad(plain_text)
    assert len(plain_text)%BLOCK_SIZE == 0
    cipher_text = ''
    aes = AES.new(self.key, AES.MODE_ECB)
    h = iv
    for i in range(len(plain_text)//BLOCK_SIZE):
        block = plain_text[i*16:i*16+16]
        block = xor(block, h)
        cipher_block = aes.encrypt(block)
        cipher_text += cipher_block
        h = md5(cipher_block).digest()
    return b64encode(iv+cipher_text)
```

Firstly, our input is padded yet again, even though our initial input is already padded, then it encrypts every block with ECB except for 1 difference - the IV changes based on the **md5 of the cipher_block**

## Vulnerability 

There are 2 flaws in this system, firstly, the secret XOR is fixed, and finite, and we can also predict the IV used to encrypt the next block from the md5 of the previous cipherbox.

Thus we can send a known block, repeated until the secret repeats, then send `Give me the flag`. We can obtain the IV and the ciphertext of `Give me the flag`

Our attack would proceed as follows:

Chose a random block, `0123456789ABCDEF` is chosen for convenience

Prepend `Give me the flag` with the block n times, where n is looped until the solution is found

The ciphertext we receive will have the structure:

>randomIV|multiple encrypted 0123456789ABCDEF|encrypted Give me the flag|encrypted "\n"+"\x0f"\*15|encrypted "\x10"\*16

Using the ciphertext, calculate the IV used to encrypt Give me the flag, and set that as the new iv, the payload would look like

>newIV|encrypted Give me the flag|encrypted "\n"+"\x0f"\*15|encrypted "\x10"\*16

(you can remove the last 2 blocks but it doesn't affect the final result, server checks if decrypted message starts with Give me the flag)

Now slowly loop through n to get the flag, as eventually the secret used to XOR our message is used to XOR the ciphertext(i%len(self.secret) has a cycle length of len(self.secret))

[exploit.py](exploit.py)

>Flag: ISITDTU{chung96vn\_i5\_v3ry\_h4nds0m3}

