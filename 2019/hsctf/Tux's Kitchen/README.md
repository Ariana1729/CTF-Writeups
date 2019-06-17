# Tux's Kitchen
>I need to bake it!
>[problem.py](problem.py)

We are given [problem.py](problem.py), which is a interesting cipher/hash algorithm.

## Solution

The hash basically takes our input, multiplies it with basically a random number for our purposes, and XORs every element with a fixed value, and adds the value a whole bunch of times to the last number(not sure if this was a typo)

Since XOR is reversible, we simply reverse the XOR, and take the GCD of multiple attempts

Strangely the flag is different before and after the ctf, not exactly sure why

> Flag(during ctf): `hsctf{th1s_1s_0ne_v3ry_l0ng_fl@g_b3ca8s3_t5x_l0v3z_vveR9_LOn9_flaGs7!}`
> Flag(after ctf): `hsctf{thiii111iiiss_isssss_yo0ur_b1rthd4y_s0ng_it_isnt_very_long_6621}`
