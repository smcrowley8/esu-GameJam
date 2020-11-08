from PIL import Image, ImageDraw
from math import floor
path='playerUp2.png'
img=Image.open(path)
img=img.convert("RGBA")
datas=img.getdata()

newData=[]
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2]==255:
        newData.append((0,0,0,0))
    else:
        newData.append(item)

img.putdata(newData)
img.save(path)