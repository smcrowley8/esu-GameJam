from PIL import Image, ImageDraw
from math import floor
import numpy as np
path='playerUp1.png'
img=Image.open(path)
img=img.convert("RGBA")
datas=img.getdata()


print(np.shape(datas))
'''

newData=[]
for i in range(len(datas)):
    for j in range(len(datas[i])):
        if (i >= 80 and i < len(datas[i][j])) and (j>=40 and j<60):
            newData.append((255,255,255))
        else:
            newData.append(datas[i][j])

img.putdata(newData)
img.save('test.png')
'''