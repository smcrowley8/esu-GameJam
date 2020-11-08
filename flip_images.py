from PIL import Image, ImageDraw

# Load image:
input_image = Image.open("enemyRight2.png")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Copy pixels
for x in range(output_image.width):
    for y in range(output_image.height):
        xp = input_image.width - x - 1
        #forhorizontal flip

        #yp=input_image.height - y -1
        #for virtical flip
        draw.point((x, y), input_pixels[xp, y]) #for hor
        #draw.point((x,y), input_pixels[x,yp])#for vir

output_image.save("enemyLeft2.png")