import pygame 
import random

pygame.init()
'''
*********************************** game variables ***********************************
'''

'''
the window is 720 by 720 and divided into a 9x9 board
each sqare is 80x80
square i,j starts at (i*80, j*80) 
character x and y correlates to that square
the upper left square is (0,0), the bottom right is (8,8)\

board represents the game board. 9 on the board is an enemy, 1 is the player, 0 is empty
'''
display_width = 720
display_height = 720

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green=(0,255,0)
purple = (148, 0, 211)

img_width=80

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('only one move at a time')
clock = pygame.time.Clock()

class Character:
    def __init__(self, x=0, y=0, player=False):
    
        if player:
            self.back1Img = pygame.image.load('playerDown1.png')
            self.back2Img = pygame.image.load('playerDown2.png')
            self.front1Img = pygame.image.load('playerUp1.png')
            self.front2Img = pygame.image.load('playerUp2.png')
            self.left1Img = pygame.image.load('playerLeft1.png')
            self.left2Img = pygame.image.load('playerLeft2.png')
            self.right1Img = pygame.image.load('playerRight1.png')
            self.right2Img = pygame.image.load('playerRight2.png')
        else:
            self.back1Img = pygame.image.load('enemyDown1.png')
            self.back2Img = pygame.image.load('enemyDown2.png')
            self.front1Img = pygame.image.load('enemyUp1.png')
            self.front2Img = pygame.image.load('enemyUp2.png')
            self.left1Img = pygame.image.load('enemyLeft1.png')
            self.left2Img = pygame.image.load('enemyLeft2.png')
            self.right1Img = pygame.image.load('enemyRight1.png')
            self.right2Img = pygame.image.load('enemyRight2.png')
        
        self.direction="up"
        self.attacking=False
        self.whatImg=0
        self.x=x
        self.player=player
        self.y=y
        if player==True:
            self.hp=100
        else:
            self.hp=5
        self.dmg=5
        
    def drawSelf(self):
        
        if self.direction=="up":
            if self.whatImg==0:
                gameDisplay.blit(self.front1Img, (self.x * 80, self.y * 80))
            else:
                gameDisplay.blit(self.front2Img, (self.x * 80, self.y * 80))
        if self.direction=="left":
            if self.whatImg==0:
                gameDisplay.blit(self.left1Img, (self.x * 80, self.y * 80))
            else:
                gameDisplay.blit(self.left2Img, (self.x * 80, self.y * 80))
        if self.direction=="right":
            if self.whatImg==0:
                gameDisplay.blit(self.right1Img, (self.x * 80, self.y * 80))
            else:
                gameDisplay.blit(self.right2Img, (self.x * 80, self.y * 80))
        if self.direction=="down":
            if self.whatImg==0:
                gameDisplay.blit(self.back1Img, (self.x * 80, self.y * 80))
            else:
                gameDisplay.blit(self.back2Img, (self.x * 80, self.y * 80))
        '''
        if self.player==True:
            pygame.draw.rect(gameDisplay, purple, [self.x*80, self.y*80, 80, 80])
        else:
            pygame.draw.rect(gameDisplay, red, [self.x*80, self.y*80, 80, 80])
        '''
        #now draw the hp bar
        pygame.draw.rect(gameDisplay, black, [self.x*80, self.y*80, 80, 10], 1)
        #outline
        hpX=80
        if self.player==True:
            color=green
            hpX=int(4*self.hp/5)
        else:
            color=red
            hpx=80
        pygame.draw.rect(gameDisplay, color, [self.x*80, self.y*80, hpX, 10], 0)
##### character is a basic object in the game. will be both the player and all enemies

board=[[0]*9 for _ in range(9)] #10 x 10 board that will be our playable area

player=Character(4,4,player=True)
board[4][4]=1
enemies=[]
numEnemies=3 #will always be 5, when one dies another is made
original_positions=[]
for i in range(numEnemies):
    #make random position
    x=0
    y=0
    
    while True:
        x=random.randint(0,8)
        y=random.randint(0,8)
        if (x,y) not in original_positions:
            original_positions.append((x,y))
            board[x][y]=9
            break
    
    enemy=Character(x,y)
    enemies.append(enemy)


#waitCT is used to tell how long its been since the palyer moved
#if player waits too long then enemies start to move anyway

'''
*********************************** game functions ***********************************
'''

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    #time.sleep(2)

    #game_loop()

def drawBoard():
    #draw each inner rectangle
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(gameDisplay, black, [i*80, j*80, 80, 80], 1)

def drawEnemies():
    for enemy in enemies:
        enemy.drawSelf()

def drawState():
    gameDisplay.fill(white)
    drawBoard()
    drawEnemies()
    player.drawSelf()

def updateImgs():
    for enemy in enemies:
        if enemy.whatImg==1:
            enemy.whatImg=0
        else:
            enemy.whatImg=1
    if player.whatImg==1:
        player.whatImg=0
    else:
        player.whatImg=1

def make_enemy_turn():
    for enemy in enemies:
        xdiff=enemy.x-player.x
        ydiff=enemy.y - player.y
        if (abs(xdiff)==1 and abs(ydiff)==0) or (abs(xdiff)==0 and abs(ydiff)==1):
            #enemy will attack
            pass
        else:
            nextX=int(enemy.x)
            nextY=int(enemy.y)
            if abs(xdiff)==0:
                if ydiff<0:
                    nextY+=1
                else:
                    nextY-=1
            elif abs(ydiff)==0:
                if xdiff<0:
                    nextX+=1
                else:
                    nextX-=1
            elif abs(xdiff) > abs(ydiff):
                if xdiff<0:
                    nextX+=1
                else:
                    nextX-=1
            else:
                if ydiff<0:
                    nextY+=1
                else:
                    nextY-=1
            if board[nextX][nextY]==0:
                #unoccupioed so move there
                board[enemy.x][enemy.y]=0
                enemy.x=nextX
                enemy.y=nextY 
                board[enemy.x][enemy.y]=9
            #if not 0 then occupied and cant move there
        
'''
*********************************** game itself ***********************************
'''

def game_loop():
    gameExit = False
    player_turn=True
    waitCT=0
    pause=False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()            
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_p:
                    pause=not pause
            if not pause==True:
                if player_turn:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player.direction="right"
                            if player.x<8:
                                player.x+=1
                        if event.key == pygame.K_LEFT:
                            player.direction="left"
                            if player.x>0:
                                player.x-=1
                        if event.key == pygame.K_DOWN:
                            player.direction="down"
                            if player.y<8:
                                player.y+=1
                        if event.key == pygame.K_UP:
                            player.direction="up"
                            if player.y>0:
                                player.y-=1
                #do other checks for game related functions
            
                if waitCT>10:
                    #once youve gone 5 sec without moving, enemies will move anyway
                    waitCT=0
                    player_turn=False
                if player_turn==False:
                    #make the enemies move towards player. if they are adjacent, attack
                    if waitCT%2==0:
                        make_enemy_turn()
                #after all game related inputs have been read, we update

                updateImgs()
                #re print everything in the game
                drawState()

                #add final check for boundaries

                #
                print(waitCT)
                waitCT=waitCT+1
                pygame.display.update()
                clock.tick(2)#we want 2 frames per second so that the game is a slow turn base
            else:
                message_display("PAUSED")



game_loop() 
pygame.quit()
quit()