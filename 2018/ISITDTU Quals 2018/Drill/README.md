# Drill
>We are given [drill](drill), which looks like a text file that contains hex

The file we are given looks a lot like hex, thus we simply converted the hex values into an [actual file](hexfile)

PK\x01\x02 and PK\x05\x06 can be found in the file, thus we could just replace(from TuanLinh) or insert(actual solution, from DutChen18) PK\x03\x04 at the start, then we can fix the [zip file](500.zip)

After fixing it, we see a 499.zip and a password prompt, using rockyou to crack the zip, we see 499.zip contains 498.zip and a password prompt, seems like the number will just slowly count down, a [script](unzip.py) is used to automate this process, it seems to go by much faster than expected. After the competition I realized the 500 passwords are actually the 500 most common passwords, which will be at the start of the rockyou database.

Now we are presented with a [0.zip](0.zip), which is unzipped to give us a [file](0)

In this file we are presented with a [key.png](0/key.png) and a [box.zip](box.zip), containing flag.txt and requires a password. After unsuccessfully running rockyou. Looking at the key.png, we realize that the red pixel values are actually morse code(from DutChen18)

Decoding the [morse code](0/decode.py), we finally get the key, and then converting the letters to lower case, we [unlock the zip](0/flag.txt)

>Flag: ISITDTU{4\_g00d\_hunt3r\_0n\_th3\_c0mput3r!}
