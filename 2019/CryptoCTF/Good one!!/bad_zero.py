#!/usr/bin/env python

import random
from flag import flag

def cfcrypt(msg):
    msg = int(msg.encode('hex'), 16)
    while True:
        sta = random.randint(1, 2 << 16)
        if '0' not in repr(sta):
            break
    seq = [int(c) for c in str(msg).replace('0', repr(sta))]
    x, y = 1, 0
    for t in reversed(seq):
        x, y = y + x * t ** 2, x
    return 'enc = %s%s' % (x - y, y + x)

print cfcrypt(flag)