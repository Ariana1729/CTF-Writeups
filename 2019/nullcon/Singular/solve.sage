import hashlib
from Crypto.Cipher import AES

a2=330762886318172394930696774593722907073441522749
a4=6688528763308432271990130594743714957884433976
a6=759214505060964991648440027744756938681220132782
p=785482254973602570424508065997142892171538672071

def add(A, B):
    (u, v), (w, x) = A, B
    assert u != w or v == x
    if u == w: m = ((3*u*u + 2*a2*u + a4)/(2*v)) % p
    else: m = (x-v)/(w-u) % p
    y = m*m -a2 - u - w 
    z = m*(u-y) - v
    return y % p, z % p

def mul(t, A, B=0):
    if not t: return B
    return mul(t//2, add(A,A), B if not t&1 else add(B,A) if B else A)

#Points given
G=(1, 68596750097555148647236998220450053605331891340)
P=(453762742842106273626661098428675073042272925939, 680431771406393872682158079307720147623468587944)
Q=(353016783569351064519522488538358652176885848450, 287096710721721383077746502546881354857243084036) 

#degenerating to additive curve
k=413400541209677581972773119133520959089878607131
G_=(G[0]-k, G[1])
P_=(P[0]-k, P[1])
Q_=(Q[0]-k, Q[1])
aG = (G_[0])/(G_[1]) % p
aP = (P_[0])/(P_[1]) % p
aQ = (Q_[0])/(Q_[1]) % p

#solving DLP under additive group
d1=(aP/aG)%p
d2=(aQ/aG)%p
(x,y)=mul(d1*d2,G)

#getting flag
k=hashlib.sha256(str(x)).hexdigest().decode('hex')
c='480fd106c9a637d22fddd814965742236eb314c1b8fb68e70a7c7445ff04476082f8b9026c49d27110ba41b95e9f51dc'.decode('hex')
cipher = AES.new(k, AES.MODE_ECB)
print cipher.decrypt(c)
