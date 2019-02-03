from PIL import Image

im1=Image.new('RGB',(2,2),'white')
im1.putdata([(0,0,0)]*3+[(0,0,0)])
im1.save('im1.png')

im2=Image.new('RGB',(2,2),'white')
im2.putdata([(0,0,0)]*3+[(0,0,1)])
im2.save('im2.png')
