import pygame 
import random
import time
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
display_width = 1000
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
##music stuff
playlist=list()
music='audio.wav'
pygame.mixer.music.load(music)
pygame.mixer.music.queue(music)

class Character:
    def __init__(self, x=0, y=0, player=False):
        self.attacking=False
        if player:
            self.back1Img = pygame.image.load('playerDown1.png')
            self.back2Img = pygame.image.load('playerDown2.png')
            self.front1Img = pygame.image.load('playerUp1.png')
            self.front2Img = pygame.image.load('playerUp2.png')
            self.left1Img = pygame.image.load('playerLeft1.png')
            self.left2Img = pygame.image.load('playerLeft2.png')
            self.right1Img = pygame.image.load('playerRight1.png')
            self.right2Img = pygame.image.load('playerRight2.png')
            self.attackUp1= pygame.image.load('playerAttackUp1.png')
            self.attackUp2= pygame.image.load('playerAttackUp2.png')
            self.attackDown1= pygame.image.load('playerAttackDown1.png')
            self.attackDown2= pygame.image.load('playerAttackDown2.png')
            self.attackLeft1= pygame.image.load('playerAttackLeft1.png')
            self.attackLeft2= pygame.image.load('playerAttackLeft2.png')
            self.attackRight1= pygame.image.load('playerAttackRight1.png')
            self.attackRight2= pygame.image.load('playerAttackRight2.png')
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
        if self.attacking==True: #only true for players
            if self.direction=="up":
                if self.whatImg==0:
                    gameDisplay.blit(self.attackUp1, (self.x * 80, self.y * 80))
                else:
                    gameDisplay.blit(self.attackUp2, (self.x * 80, self.y * 80))
            if self.direction=="left":
                if self.whatImg==0:
                    gameDisplay.blit(self.attackLeft1, (self.x * 80, self.y * 80))
                else:
                    gameDisplay.blit(self.attackLeft2, (self.x * 80, self.y * 80))
            if self.direction=="right":
                if self.whatImg==0:
                    gameDisplay.blit(self.attackRight1, (self.x * 80, self.y * 80))
                else:
                    gameDisplay.blit(self.attackRight2, (self.x * 80, self.y * 80))
            if self.direction=="down":
                if self.whatImg==0:
                    gameDisplay.blit(self.attackDown1, (self.x * 80, self.y * 80))
                else:
                    gameDisplay.blit(self.attackDown2, (self.x * 80, self.y * 80))
        else:
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

    def getSelf(self, x, y):
        if self.x == x and self.y==y:
            return self 
        else:
            return None

    def isHere(self, x, y):
        if self.x == x and self.y == y:
            return True
        else:
            return False

    def attack(self, obj):
        obj.hp=obj.hp-self.dmg


board=[[0]*9 for _ in range(9)] #10 x 10 board that will be our playable area

player=Character(4,4,player=True)
board[4][4]=1
enemies=[]
numEnemies=3 #will always be 5, when one dies another is made
original_positions=[]
SCORE=0
HIGHSCORE=0
scoreInc=10
killInc=100
pause=False
pauseMsg="PAUSED"
with open('highScore.txt') as f:
    lines=f.readlines()
    HIGHSCORE=int(lines[0])
#waitCT is used to tell how long its been since the palyer moved
#if player waits too long then enemies start to move anyway

'''
*********************************** game functions ***********************************
'''
def makeEnemies():
    x=0
    y=0
    
    while len(enemies)<numEnemies:
        x=random.randint(0,8)
        y=random.randint(0,8)
        if (board[x][y]==0) and (abs(x-player.x)>2 and abs(y-player.y)>2):
            original_positions.append((x,y))
            board[x][y]=9
            #break
    
            enemy=Character(x,y)
            enemies.append(enemy)
    
def removeDeadEnemy():
    #enemies=[enemy for enemy in enemies if enemy.hp >0]
    x=-1
    y=-1
    for i in range(len(enemies)):
        if enemies[i].hp==0:
            x=enemies[i].x
            y=enemies[i].y
            enemies.pop(i)
            break
    if x>=0 and y>=0:
        board[x][y]=0

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, x, y, size):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)


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

def drawRules():
    r1='RULES: '
    r2='you and the enemies take turns moving'
    r3='you can only do one move per turn'
    r4='you can move up, down, left, or right'
    r5='move and attack by using arrow keys'
    r6='if an enemy is to your left, and you hit left,'
    r7='you will attack the enemy'
    message_display(r1, 860, 150, 40)
    message_display(r2, 860, 180, 10)
    message_display(r3, 860, 210, 10)
    message_display(r4, 860, 240, 10)
    message_display(r5, 860, 270, 10)
    message_display(r6, 860, 300, 10)
    message_display(r7, 860, 330, 10)

def drawScore():
    message_display("SCORE: ", 860, 40, 60)
    message_display(str(SCORE), 860, 100, 60)
    message_display("High Score: ", 860, 600, 40)
    message_display(str(HIGHSCORE), 860, 650, 30)

def drawState():
    gameDisplay.fill(white)
    drawBoard()
    drawEnemies()
    player.drawSelf()
    drawRules()
    drawScore()
    if pause==True:
        if pauseMsg=="PAUSED":
            message_display(pauseMsg, (display_width/2), (display_height/2), 115)
        else:
            msgs=pauseMsg.split('\n')
            h=100
            for msg in msgs:
                message_display(msg, (display_width/2), h, 60)
                h+=100


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
            enemy.attack(player)
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
    global pause
    global enemies
    global SCORE
    global HIGHSCORE
    global numEnemies
    global pauseMsg
    global scoreInc 
    global killInc 

    makeEnemies()
    pause=True #this is for selecting difficulty at the start
    pauseMsg="press E for easy\n M for medium\n and H for hard"
    pygame.mixer.music.play(-1)
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('highScore.txt', 'w') as f:
                    f.write(str(HIGHSCORE))
                pygame.quit()
                quit()           
            if pause==False:
                if player_turn:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player.direction="right"
                            if player.x<8:
                                #if the spot youre moving too has an enemy, attack
                                if board[player.x+1][player.y]==9:
                                    for enemy in enemies:
                                        if enemy.isHere(player.x+1, player.y)==True:
                                            player.attack(enemy)
                                            SCORE+=killInc
                                    removeDeadEnemy()
                                    player.attacking=True
                                else:
                                    player.x+=1
                                    player.attacking=False
                                player_turn=False
                                ''' used to be this
                                if waitCT%2==0:
                                    waitCT=0
                                else:
                                    waitCT=-1
                                '''
                                waitCT=abs(waitCT-30)
                            SCORE+=scoreInc
                        if event.key == pygame.K_LEFT:
                            player.direction="left"
                            if player.x>0:
                                if board[player.x-1][player.y]==9:
                                    for enemy in enemies:
                                        if enemy.isHere(player.x-1, player.y)==True:
                                            player.attack(enemy)
                                            SCORE+=killInc
                                    removeDeadEnemy()
                                    player.attacking=True
                                else:
                                    player.x-=1
                                    player.attacking=False
                                player_turn=False
                                waitCT=abs(waitCT-30)                                
                            SCORE+=scoreInc
                        if event.key == pygame.K_DOWN:
                            player.direction="down"
                            if player.y<8:
                                if board[player.x][player.y+1]==9:
                                    for enemy in enemies:
                                        if enemy.isHere(player.x, player.y+1)==True:
                                            player.attack(enemy)
                                            SCORE+=killInc
                                    removeDeadEnemy()
                                    player.attacking=True
                                else:
                                    player.y+=1
                                    player.attacking=False
                                player_turn=False
                                waitCT=abs(waitCT-30)
                            SCORE+=scoreInc
                        if event.key == pygame.K_UP:
                            player.direction="up"
                            if player.y>0:
                                if board[player.x][player.y-1]==9:
                                    for enemy in enemies:
                                        if enemy.isHere(player.x, player.y-1)==True:
                                            player.attack(enemy)
                                            SCORE+=killInc
                                    removeDeadEnemy()
                                    player.attacking=True
                                else:
                                    player.y-=1
                                    player.attacking=False
                                player_turn=False
                                waitCT=abs(waitCT-30)
                            SCORE+=scoreInc
            
            if event.type == pygame.KEYDOWN:
                if pauseMsg=="PAUSED":
                    if event.key == pygame.K_p:
                        pause=not pause
                else:
                    if event.key==pygame.K_e:#easy
                        scoreInc=10
                        killInc=100
                        numEnemies=3
                        pauseMsg="PAUSED"
                        pause=False
                    if event.key==pygame.K_m:#medium
                        scoreInc=15
                        killInc=125
                        numEnemies=5
                        pauseMsg="PAUSED"
                        pause=False
                    if event.key==pygame.K_h:#hard
                        scoreInc=20
                        killInc=150
                        numEnemies=7
                        pauseMsg="PAUSED"
                        pause=False
        if pause==False:
            #do other checks for game related functions
            if player_turn==False:
                #make the enemies move towards player. if they are adjacent, attack
                if waitCT%30==0:
                    make_enemy_turn()
                    if player.hp<=0:
                        gameExit=True
                    SCORE+=10
                    if len(enemies)<numEnemies:
                        makeEnemies()
                    player_turn=True
        if waitCT>600:
            #once youve gone 5 sec without moving, enemies will move anyway
            waitCT=0
            player_turn=False
        
        #after all game related inputs have been read, we update

        
        if waitCT%30==0:
            updateImgs()
        if HIGHSCORE<SCORE:
            HIGHSCORE=int(SCORE)
        #print(waitCT)
        #re print everything in the game
        drawState()

        #add final check for boundaries

        #
        waitCT=waitCT+1
        pygame.display.update()
        clock.tick(50)#we want 2 frames per second so that the game is a slow turn base
    #game is over, replay?
    message_display("game over", (display_width/2), (display_height/2), 115)
    pygame.display.update()
    with open('highScore.txt', 'w') as f:
        f.write(str(HIGHSCORE))
    time.sleep(2)
       

game_loop() 
pygame.quit()
quit()