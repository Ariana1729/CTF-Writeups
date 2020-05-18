from pwn import *
print 'Generating curve'
data = process('sage gencurve.sage', shell=True).recvall()
print 'Curve generated, connecting to server'
r = remote('notbefoooled.challenges.ooo',5000)
r.sendline(data)
r.recvuntil('Here is the answer: ')
print 'Flag: ' + r.recvall()
