import os
pw=os.popen("fcrackzip -D -u -p ../../../Resources/rockyoudict.txt fixed.zip").read().split(" ")[-1][:-1]
os.popen("unzip -P "+pw+" fixed.zip")
i=500
while(i>1):
    i=i-1
    pw=os.popen("fcrackzip -D -u -p ../../../Resources/rockyoudict.txt "+str(i)+".zip").read().split(" ")[-1][:-1]
    os.popen("unzip -P "+pw+" "+str(i)+".zip")
    os.popen("rm "+str(i)+".zip")
