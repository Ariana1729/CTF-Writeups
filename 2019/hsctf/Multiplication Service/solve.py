from gmpy2 import invert,iroot

def bsgs(g, h, p, o):
    print "Solving %d^x=%d mod %d where order is %d"%(g,h,p,o)
    N = iroot(o,2)[0]+1
    t = {pow(g, i, p): i for i in range(N)}#python hash map basically
    c = invert(pow(g,N,p),p)
    for j in xrange(N):
        y = (h * pow(c, j, p)) % p
        if y in t:
            print "x = %d"%(j*N+t[y])
            return j * N + t[y]
    print "No solutions found"
    return None

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * invert(p, n_i) * p
    return sum % prod

p=2**448 - 2**224 - 1
g=65537
h=17295249384460627529659678526265464341448466952645144305360373644006427247104357706004957425907414265691248156367907501366015348955943L
fact=[2 , 641 , 18287 , 196687 , 1466449 , 2916841 , 6700417, 1469495262398780123809, 167773885276849215533569, 596242599987116128415063, 37414057161322375957408148834323969]
order=[2 , 641 , 18287 , 196687 , 1466449 , 2916841 , 6700417, 2**40, 2**40, 2**40, 2**40]
n=p-1
gi=[pow(g,n/i,p) for i in fact]
hi=[pow(h,n/i,p) for i in fact]
xi=[bsgs(gi[i],hi[i],p,order[i]) for i in range(len(fact))]
xi[0]=0
print chinese_remainder(fact,xi)
xi[0]=1
print chinese_remainder(fact,xi)
