import math
import hashlib
from PIL import Image

def HashImage(image): 
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    im=image
    pix=im.load()
    width, height = im.size
    small=height if width>height else width
    pic=[]

    for i in range(small):
        curr=[]
        for j in range(i,small):
            curr.append(pix[i,j])
        for j in range(i+1,small):
            curr.append(pix[j,i])
        sum,mul,sub=0,1,1000000

        if i%3==0:
            for pixel in curr:
                sum+=pixel[0]
                mul*=pixel[1]
                sub-=pixel[2]

        elif i%3==1:
            for pixel in curr:
                sum+=pixel[2]
                mul*=pixel[0]
                sub-=pixel[1]
        else:
            for pixel in curr:
                sum+=pixel[1]
                mul*=pixel[2]
                sub-=pixel[0]

        pic.append((sum%256,mul%256,sub%256))
        
    size=int(math.floor(math.sqrt(len(pic))))
    pic=pic[0:size*size]

    im2 = Image.new('RGB', (size,size),'white')
    im2.putdata(pic)
    im2.save("hash.jpg")
    return md5('hash.jpg')
