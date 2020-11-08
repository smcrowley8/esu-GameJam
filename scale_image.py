from PIL import Image, ImageDraw
from math import floor

path='playerUp2.png'
'''
first we scale
'''
inImg=Image.open(path)
inPxls=inImg.load()

newSize=(80,80)

outImg=Image.new("RGB", newSize)
draw=ImageDraw.Draw(outImg)

x_scale=inImg.width / outImg.width
y_scale=inImg.height / outImg.height

for x in range(outImg.width):
    for y in range(outImg.height):
        xp, yp = floor(x*x_scale), floor(y*y_scale)
        draw.point((x,y), inPxls[xp,yp])

outImg.save(path)
