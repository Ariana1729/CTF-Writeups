while True:
    s = randint(1,2^150)
    if is_prime(6*s*(1+2*s)+1):
        p = 6*s*(1+2*s)+1
        break
while True:
    b = randint(1,p)
    if EllipticCurve(GF(p), [0, b]).order()==p:
        break
P = EllipticCurve(GF(p), [0, b]).random_point()
print(f"0\n{b}\n{p}\n{P[0]}\n{P[1]}")
