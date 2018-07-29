from sympy import integer_nthroot


def execute(key):
	limit=10000
        a, exact = integer_nthroot(key, 2)
        max = a + limit
        while a < max:
            b2 = a*a - key
            if b2 >= 0:
                b, exact = integer_nthroot(b2,2)
                if b*b == b2:
                    break
            a += 1
        if a < max:
            p = a+b
            q = a-b
            return True, p, q
        else:
            return False
execute(603040899191765499692105412408128039799635285914243838639458755491385487537245112353139626673905393100145421529413079339538777058510964724244525164265239307111938912323072543529589488452173312928447289267651249034509309453696972053651162310797873759227949341560295688041964008368596191262760564685226946006231)
