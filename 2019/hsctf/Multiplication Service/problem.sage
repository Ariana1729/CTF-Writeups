# privkey is an integer
from secret import privkey, flag

def welcome():
    print("Welcome to our multiplication service")
    print("Enter one of the following:")
    print("0 : get curve params")
    print("1 : get multiple on point")
    print("2 : guess private key")
    choice = raw_input("enter choice\n")
    if choice == '0':
        print("Ed448")
        print("ax^2 + y^2 = 1 + dx^2y^2, x,y in F_p")
        print("a = 1")
        print("d = -39081")
        print("p = 2^448 - 2^224 - 1")
    elif choice == '1':
        print("Enter point in the form `x,y`")
        coordinate = raw_input()
        coords = coordinate.split(",")
        point = (int(coords[0]), int(coords[1]))
        print(sign(point))
    else:
        print("enter private key guess as an integer")
        guess = int(raw_input())
        if guess == privkey:
            print(flag)
        else:
            print("Try again!")


p = 2^448 - 2^224 - 1
a = 1 % p
d = (-39081) % p

# Naive twisted edwards point addition, returns p3 = p1 + p2
def TwistedEdwardsPointAdd(p1, p2):
    denominator_prod = d * p1[0] * p2[0] * p1[1] * p2[1]
    p3_x = p1[0] * p2[1] + p2[0] * p1[1] % p
    p3_x *= inverse_mod(1 + denominator_prod, p)
    p3_x %= p
    p3_y = p1[1] * p2[1] - a * p1[0] * p2[0] % p
    p3_y *= inverse_mod(1 - denominator_prod, p)
    p3_y %= p
    return (p3_x, p3_y)

# privkey is generated according to this
def keygen():
    rand1 = randint(1, 132156247253163728496320586201074)
    rand2 = randint(1, 2**40)
    rand3 = randint(1, 2**40)
    rand4 = randint(1, 2**40)
    rand5 = randint(1, 2**40)
    key = CRT([rand1, rand2, rand3, rand4, rand5], [132156247253163728496320586201074, 1469495262398780123809, 167773885276849215533569, 596242599987116128415063, 37414057161322375957408148834323969])
    return key

def scalar_mul(point, scalar):
    if scalar == 0:
        return 0
    if scalar == 1:
        return point
    if scalar % 2 == 1:
        return TwistedEdwardsPointAdd(point, scalar_mul(point, scalar - 1))
    else:
        return scalar_mul(TwistedEdwardsPointAdd(point, point), scalar / 2)

def sign(point):
    return scalar_mul(point, privkey)

if __name__ == "__main__":
    try:
        welcome()
    except:
        print("bad input")
        pass