def drift(R, B):
    n = len(B)
    ans, ini = R[-1], 0
    for i in B:
        ini ^= R[i-1]
    R = [ini] + R[:-1]
    return ans, R

out = bin(0x7006d570000627b6fcf3881fbe2f1817^0x89504e470d0a1a0a0000000d49484452)[2:]
out = [int(i) for i in out]

for r in range(7,128):
    for b in range(2,r):
        R = out[:r][::-1]
        B = [i for i in range(b)]
        for i in range(len(out)):
            t, R = drift(R,B)
            if(t != out[i]):
                break
        if(i > len(out)-2):
            print "r = %d"%r
            print "b = %d"%b
            print "R = "+str(out[:r][::-1])
