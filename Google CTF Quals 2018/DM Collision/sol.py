from not_des import *
for k in range(8):
     for i in range(4):
          for j in range(16):
               if(SBOXES[k][i][j]==0):
                 print(str(k)+','+('0'*(4-len(bin(i)))+bin(i)[2:])[:1]+('0'*(6-len(bin(j)))+bin(j)[2:])+('0'*(4-len(bin(i)))+bin(i)[2:])[1:])
print '\n'*10+'Reversed:'
for k in range(8):
     for i in range(4):
          for j in range(16):
               if(SBOXES[k][i][j]==0):
                 print(str(k)+','+('0'*(4-len(bin(3-i)))+bin(3-i)[2:])[:1]+('0'*(6-len(bin(15-j)))+bin(15-j)[2:])+('0'*(4-len(bin(3-i)))+bin(3-i)[2:])[1:])





























1 to 7 done, 2 possiblities

10000100000011010011110011010????0
10000100000011010011110011001????0


8,001010
8,000011
8,111000
8,110101

'''