#DM Collision
>Can you find a collision in this compression function?
We are given a `challenge.py` and a `not_des.py`.

`not_des.py` looks like a typical DES implimentation, but with S-boxes are in this order:
>SBOXES = [S6, S4, S1, S5, S3, S2, S8, S7]

From `challenge.py`, we notice that 3 conditions need to be satisfied:

>output = Xor(DESEncrypt(inp, key), inp)
>
>if b1.key + b1.input != b2.key + b2.input
>
>if b1.output == b2.output
>
>if b3.output == [0]*8
>


The first condition prevents a identical key and text to be encrypted.

The second condition is colliding `Xor(DESEncrypt(inp, key), inp)`

The third condition is finding a input that maps to itself under a key.

##Solution for first 2 conditions

Firstly, notice that `XOR(a,b)=XOR(b,a)`, thus we need to find an input, when encrypted twice with different/same key, results in the same output.

This is quite a well-known vulnurablity, there are 4 weak keys and 6 semi-weak key pairs.

Weak keys: When a message is encrypted with a weak key twice, it results in the same message. The 4 weak keys are:
>0x0101010101010101
>
>0xFEFEFEFEFEFEFEFE
>
>0xE0E0E0E0F1F1F1F1
>
>0x1F1F1F1F0E0E0E0E
>

Semi-weak key pairs: When a message is encrypted with a one semi-weak key, it can be decrypted with another key. The 6 semi-weak key pairs are:

>0x011F011F010E010E and 0x1F011F010E010E01
>
>0x01E001E001F101F1 and 0xE001E001F101F101
>
>0x01FE01FE01FE01FE and 0xFE01FE01FE01FE01
>
>>0x1FE01FE00EF10EF1 and 0xE01FE01FF10EF10E
>
>0x1FFE1FFE0EFE0EFE and 0xFE1FFE1FFE0EFE0E
>
>0xE0FEE0FEF1FEF1FE and 0xFEE0FEE0FEF1FEF1
>

This allows for a extremely trivial solution

`XOR(DESEncrypt(m,k),m)=XOR(DESEncrypt(DESEncrypt(m,k),k),DESEncrypt(m,k))`


