import re
reg=re.compile("[0-9a-zA-Z_@!?-]")
c=[162,215,38,129,202,180,99,202,175,172,36,182,179,180,125,205,200,180,84,151,169,208,56,205,179,205,124,212,156,247,97,200,208,221,38,155,168,254,74]

sols=[]
print("Possible h(x):")
for i in range(4):
 ls=[a for a in range(256)]
 for j in range(i,len(c),4):
  for k in range(256):
   if(k in ls and not reg.match(chr(c[j]^k))):
    ls.remove(k)
 sols.append(ls)
print(sols)

flagxor=[[253,149,21,249],[253,153,21,249]]
print('\nPossible solutions:')
for i in flagxor:
 for j in range(len(c)):
  print(chr(c[j]^i[j%4]),end='')
 print('\n')

'''
def h(s):
  a=2714
  b=33310
  for(i=0;i!=s.length;i++):
    a=((typeof a=='undefined'?1:a)+ord(str(s[i])))%65521;
    b=((typeof b=='undefined'?0:b)+a)%65521
  return chr(b>>8)+chr(b&0xFF)+chr(a>>8)+chr(a&0xFF)#b->2 characters, a->2 characters

def c(a,b):
  c=''
  for(i=0;i!=a.length;i++):
    c=c+chr(ord(a[i])^ord(b[i%b.length]));
  return c;
'''
