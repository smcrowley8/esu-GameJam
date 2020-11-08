import pygame
screen=pygame.display.set_mode([720, 720])
screen.fill([255, 255, 255])
red=255
blue=0
green=0
left=50
top=50
width=80
height=80
filled=0

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
def drawBoard():
    pygame.draw.rect(screen, white, [0,0,720,720],0)
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, black, [i*80, j*80, width, height], 1)


#pygame.draw.rect(screen, red, [30,50,200,500], 0)
front1Img = pygame.image.load('playerUp1.png')
drawBoard()
pygame.display.flip()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pygame.draw.rect(screen, red, [30,50,200,500], 0)
            if event.key == pygame.K_RIGHT:
                drawBoard()
            if event.key == pygame.K_UP:
                screen.blit(front1Img, (4 * 80, 4 * 80))
    pygame.display.flip()
pygame.quit()