from PIL import Image, ImageDraw
from math import floor
path='enemyUp2.png'
img=Image.open(path)
img=img.convert("RGBA")
datas=img.getdata()

newData=[]
for item in datas:
    if item[0] > 0:
        newData.append((0,item[1],item[2],item[3]))
    else:
        newData.append(item)

img.putdata(newData)
img.save(path)