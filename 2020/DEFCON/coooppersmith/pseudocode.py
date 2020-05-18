from random import randint
import gmpy2

word203038 = 0
word203040 = 1
word203048 = 3
word203050 = 5
word203058 = 7 #set by f1312

def f18c4(a1):#new prime
    '''
    v30 = v28 = v20 = v18 = v10 = 0
    v34 = (0x80 - len(a1))*4
    v40 = 0
    v3c = 0x64
    v30 = int(a1,16)
    v18 = v30<<v34
    v20 = 1<<(v34/2)
    while(v3c!=0):
        v10 = randint(0,v20-1)
        v28 = v18 + v10
        while(v28>>v34==v30):
            if gmpy2.is_prime(v28): #maybe need weaker prime check
                v40 = 1
                break
            v28 += 1
        if(v40 == 1):
            break
        v3c -= 1
    if(v40 == 1):
        quit()
    '''
    return gmpy2.next_prime(int(a1,16)<<((0x80 - len(a1))*4) + randint(0,1<<((0x80 - len(a1))*2)-1))

def f13e2(a1,a2,a3,a4,a5):
    v10 = pow(3, a4, a1)
    if v10 == a5:
        return 0
    v10 = pow(a2, a3, a1)
    v10 += 1
    v10 = gmpy2.gcd(v10, a1)
    if v10 == 1:
        return 1
    return 0

def f14d8(a1, a2):
    v28 = v20 = v18 = v10 = v8 = 0
    v8 = a1 + 1
    v2c = 0
    while True:
        while True:
            v20 = randint(1,v8)
            v10 = a1 * v20
            v18 = v10 << 1
            v28 = v18 + 1
            if a2 == 0 or v28 != a2:
                break
        v2c += 1
        if(f13e2(v28, 3, v20, v10, v18)==1 or f13e2(v28, 5, v20, v10, v18)==1 or f13e2(v28, 7, v20, v10, v18)==1):
            break
    return v28 # probable prime of the form a1*v5*2+1

def f1dd8(a1):
    v8 = f14d8(a1, 0)
    v10 = f14d8(a1, v8) # 2 diff primes
    return f165e(v8,v10) # gen rsa

def f1e25():
    word207080 = raw_input("Please input prefix IN HEX with length no more than 120")
    v10 = f18c4(word207080)
    v8 = f1dd8(v10)
    return

def f1390():
    return
