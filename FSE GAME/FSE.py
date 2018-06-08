#FSE.py
from pygame import *
from datetime import datetime
from math import *
from random import *
from tkinter import *
from pprint import pprint
init()
root=Tk()
root.withdraw()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"

offset = 0
size = width, height = 1080, 720
screen = display.set_mode(size)

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,139)
LightBLue = (66, 238, 244)
WHITE=(255,255,255)    ## basic colors that doesnt change in capital
BLACK=(0,0,0)
YELLOW=(255,255,0)

X=0 
Y=1
VY=2
ONGROUND=3

level = "1"
HEALTH = 100
heal = 290
Dir = 1
BATMAN = [540,650,0,True]  # Batmans position in the game
FLASH = [4050,650,0,True]
Boss = False
####################################################### Making the aliens
aliens = [[randint(1100,2000),650] for x in range(5)]
aliensRect = []
for i in range(5):
    aliensRect.append(Rect(aliens[i][0],660,44,60))
##pprint(aliens)
aliensAlive = []
dead = False

EhealthList = [100 for x in range(5)]
ehealList = [35 for x in range(5)]
########################################################

firstBack = image.load("images/firstBack.png")
cont_button = image.load("images/continue-button.png")
backgroundRect=Rect(0,0,1080,720)
buttonRect = Rect(940,10,130,50)
display.set_caption("THE AVENGERS AND JUSTICE LEAGUE")  #naming the program
## Global varaiables

bullets = []
bullets2 = []
rapid = 10
music_List = ["Music/Game music 1.mp3", "Music/Game music 2.mp3", "Music/Game music.mp3", "Music/StoryMusic.mp3"] # This is the music list 


def menu(): # function for the menu screen
    global music_List
    mixer.music.load(music_List[0])
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    buttons = [Rect(85,y*80+420,130,50) for y in range(4)]
    vals = ["game","instructions","story","credits"]
    vals2 = ["  START ","HOW TO","  STORY"," CREDIT"]
    arialFont=font.SysFont("Arial",38)

    while running:
        for evt in event.get():          
            if evt.type == QUIT:
                return "exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()

        keys = key.get_pressed()

        screen.blit(firstBack,backgroundRect)
        # print(mpos)
        for i in range(len(buttons)):
            title=arialFont.render(vals2[i],True,BLUE)
            draw.rect(screen,WHITE,buttons[i])
            screen.blit(title,buttons[i])
            if buttons[i].collidepoint(mpos):
                title=arialFont.render(vals2[i],True,BLACK)
                draw.rect(screen,BLACK,buttons[i],2)
                screen.blit(title,buttons[i])

                if mb[0]==1:
                    return vals[i]
            else:
                draw.rect(screen,YELLOW,buttons[i],2)            
        display.flip()
                
def makeMove(name,start,end):
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))        
    return move

def moveEnemy(name,start,end):
    move2 = []

    for i in range(start,end+1):
        move2.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move2

def moveFlash(name,start,end):
    move3 = []

    for i in range(start,end+1):
        move3.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move3

def health(): # This is the player health function
    draw.rect(screen,BLUE,(5,5,300,25),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,RED,(10,10,heal,15),0)
    draw.rect(screen,LightBLue,(10,40,215,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(6)] ## This creates a row of rectangles 
    for i in range (len(Gems)):
        draw.rect(screen,BLACK,Gems[i],2)

def reset(): ## this function resets player position enemy position everytime the game restarts
    global level, HEALTH, heal, Dir, BATMAN, aliens, aliensRect, aliensAlive, EhealthList, ehealList, FLASH, Boss
    level = "1"
    HEALTH = 100
    heal = 290
    Dir = 1
    BATMAN = [540,650,0,True]  # Batmans position in the game
    FLASH = [4050,650,0,True]
    Boss = False

    aliens = [[randint(1100,2000),650] for x in range(5)]
    aliensRect = []
    for i in range(5):
        aliensRect.append(Rect(aliens[i][0],660,44,60))
    ##pprint(aliens)
    aliensAlive = []
    dead = False
    EhealthList = [100 for x in range(5)]
    ehealList = [35 for x in range(5)]

def Game():
    global BATMAN, heal, HEALTH, ALIEN, move, dead, frame, Ecounter, rapid, music_List, bullets, bullets2, bullet1, bullet, move2, frame2, HEALTH, heal, bullets, Ehealth, eheal, Dir, hit, aliens, frame3, move3, FLASH, Boss
    reset()
    mixer.music.stop()
    mixer.music.load(music_List[1])
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    ## Loading all images
    bullet = image.load("Bullet/bullet.png")
    batmobile = image.load("images/batmobile.jpg")
    batmobilepic = transform.scale(batmobile,(225,75))
    bullet1 = transform.flip(bullet,True,False)
    ###########################################

    if level == "1":
        LEVEL1back=image.load("images/Level1Back.png")

    while running:

        offset = 540 - BATMAN[X]
        screen.blit(LEVEL1back,(offset,0))
        screen.blit(batmobilepic,((50 + offset),622))
        ###### Blitting batman
        pic = pics[move][int(frame)]
        batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)      
        draw.rect(screen,WHITE,Rect(BATMAN[X]+offset,BATMAN[Y],40,70),1)
        draw.rect(screen,LightBLue,batRect,2)
        screen.blit(pic, (540,BATMAN[Y]))
        ###### Blitting The ALiens
        pic2 = Epics[move2][int(frame2)]
        for i in range(5):
            aliensRect[i].move(offset,0)
            screen.blit(pic2,aliensRect[i])
            draw.rect(screen,RED,aliensRect[i],2)
        # print(offset,batRect.x,aliensRect[i],BATMAN[X])
        ######### BLitting FLash########
        print(frame3,move3)
        pic_3 = FlashPics[move3][int(frame3)]
        pic3 = transform.scale(pic_3,(40,70))
        Flashrect = Rect((FLASH[X] + offset),FLASH[Y],40,70)
        screen.blit(pic3,Flashrect)
        draw.rect(screen,WHITE,Flashrect,2)

        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        keys = key.get_pressed()
        newMove = -1   
        ############ MOVING BATMAN ###############   
        if keys[K_a]:
            Boss = True  
        if keys[K_LEFT] and BATMAN[X] > 540:
            newMove = LEFT
            Dir = -1
            BATMAN[X] -= 13
            for i in range(5):
                aliensRect[i][0] +=10

        if keys[K_RIGHT] and BATMAN[X] < 4050:
            newMove = RIGHT
            Dir = 1
            BATMAN[X] += 13
            for i in range(5):
                aliensRect[i][0] -=10

        if keys[K_UP] and BATMAN[ONGROUND]:
            newMove = Jump
            BATMAN[VY] = -10
            BATMAN[ONGROUND]=False

        if keys[K_SPACE]:
            if Dir == 1:
                if rapid < 10:
                    rapid+=1
                if keys[K_SPACE] and rapid==10:
                    rapid = 0
                    VX = 10
                    VY1 = 0
                    bullets.append([(BATMAN[X] + offset),BATMAN[Y]+20,VX,VY1])
            elif Dir == -1:
                if rapid < 10:
                    rapid+=1
                if keys[K_SPACE] and rapid==10:
                    rapid = 0
                    VX1 = -10
                    VY2 = 0
                    bullets2.append([(BATMAN[X] + offset),BATMAN[Y]+20,VX1,VY2])


        BATMAN[Y]+=BATMAN[VY]     # add current speed to Y
        if BATMAN[Y] >= 650:
           BATMAN[Y] = 650
           BATMAN[VY] = 0
           BATMAN[ONGROUND]=True
        BATMAN[VY]+=.7     # add current speed to Y
        ################################################################

        ######## BATMAN PUNCH #######
        if keys[K_b]:
            newMove = Punch

        elif newMove == -1:
            frame = 0
        ##############################

        ########## ANIMATION FOR BATMAN ############
        if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame = frame + 0.4 # adding 0.2 allows us to slow down the animation
            if frame >= len(pics[move]):
                frame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            frame = 1

        mx, my = mouse.get_pos() 

        ############ MOVING THE ENEMY ###################
        for i in range(5):

            newMove2 = -1
            if (BATMAN[X]+offset) < aliensRect[i][0] and aliensRect[i][0] > 10: ## Checking if Batman's x is greater than alien's x
                newMove2 = LEFT
                eV=randint(1,7)
                aliensRect[i][0] -= eV
                
            if (BATMAN[X] + offset) > aliensRect[i][0] and aliensRect[i][0] < 2090: ## Checking if Batman's x is less than the alien's x
                newMove2 = RIGHT
                eV=randint(1,7)
                aliensRect[i][0] += eV
            
            if aliensRect[i].colliderect(batRect): ## Checking for collide between the aliens and Batman
                newMove2 = -1
                frame2 = 0
                aliensRect[i][0] +=0
                if HEALTH > 0:
                    HEALTH -=5
                    heal = int(heal * (HEALTH/100))

        if move2 == newMove2:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame2 = frame2 + 0.2 # adding 0.2 allows us to slow down the animation
            if frame2 >= len(Epics[move2]):
                frame2 = 1
        elif newMove2 != -1:     # a move was selected
            move2 = newMove2      # make that our current move
            frame2 = 1     
        ##########################################################

        #################### MOVING FLASH #######################
        newMove3 = -1
        if Boss == True:
            if (BATMAN[X] + offset) > FLASH[X] and FLASH[X] < 4050:
                newMove3 = RIGHT
                FLASH[X] +=20

            if (BATMAN[X] + offset) < FLASH[X] and FLASH[X] > 10:
                newMove3 = LEFT
                FLASH[X] -=20

            if move3 == newMove3:     # 0 is a standing pose, so we want to skip over it when we are moving
                frame3 = frame3 + 0.4 # adding 0.2 allows us to slow down the animation
                if frame3 >= len(Epics[move2]):
                    frame3 = 1
            elif newMove3 != -1:     # a move was selected
                move3 = newMove3      # make that our current move
                frame3 = 0 
        ############# MOVING THE BULLETS #############
        for b in bullets[:]:
            b[0]+=b[2]
            b[1]+=b[3]

            if max(b) > 1080 or min(b) < -0:
                bullets.remove(b)

        for b in bullets:
            screen.blit(bullet,(int(b[0]),int(b[1])))

        for o in bullets2[:]:
            o[0]+=o[2]
            o[1]+=o[3]

        for i in bullets2:
            screen.blit(bullet1,(int(i[0]),int(i[1])))
        ##############################################
        ######## Checking for collide with bullets and alien ###########
        for m in range(5):
            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets[bullets.index(i)]
                    EhealthList[m] -=10
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -=10
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)

        # print(Ehealth, eheal)            
            if batRect.colliderect(aliensRect[m]):
                pass         

            if EhealthList[m] == 0:
                aliensRect[m].top = 1500

        ################################################################
        enemyHealth()
        health()
        display.update()
        myClock.tick(25)
        display.flip()
    
    return "menu"

def enemyHealth():
    global Ehealth, eheal, hit
    for i in range(5):
        draw.rect(screen,RED,(aliensRect[i][0],aliensRect[i][1]-20,35,5),0)
        draw.rect(screen,GREEN,(aliensRect[i][0],aliensRect[i][1]-20,ehealList[i],5),0)

RIGHT = 0 # These are just the indices of the moves
LEFT = 1
Jump = 2
Punch = 3

pics = [] #2d list
pics.append(makeMove("Run",0,16))# RIGHT
pics.append(makeMove("RunLeft",0,16))# LEFT
pics.append(makeMove("Jump",0,4))# Jumping
pics.append(makeMove("Punch",0,11))# Punching

Epics=[]
Epics.append(moveEnemy("alien",1,7))# RIGHT
Epics.append(moveEnemy("alien",8,14))# LEFT

FlashPics = []
# FlashPics.append(moveFlash("FlashRun",0,1))# Right 
# FlashPics.append(moveFlash("FlashRunLeft",0,1))# Left
FlashPics.append(moveFlash("FlashPunch",0,11)) # Punch Right
FlashPics.append(moveFlash("FlashPunchLeft",0,11))# Punch Left
FlashPics.append(moveFlash("FlashDead",0,5))

frame = 0     # current frame within the move
move = 0      # current move being performed (right, down, up, left)
frame2 = 0
move2 = 0
frame3 = 0
move3 = 0

def instructions():
    global music_List
    mixer.music.stop()
    mixer.music.play(-1)
    mixer.music.load(music_List[2])
    inst = image.load("images/instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    running = True
    
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect.collidepoint(mx,my):
            draw.rect(screen,BLUE,buttonRect,2)
        else:
            draw.rect(screen,WHITE,(940,10,150,50))

        if mb[0] == 1 and buttonRect.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,10)) # blitting the button

        display.flip()
    return "menu"
        
def credit():
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[0])
    mixer.music.play()
    running = True
    cred = image.load("images/credits.png")
    cred = transform.smoothscale(cred, screen.get_size())
    buttonRect1 = Rect(940,660,130,50)
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect1.collidepoint(mx,my):
            draw.rect(screen,BLUE,buttonRect1,2)
        else:
            draw.rect(screen,WHITE,buttonRect1)
        if mb[0] == 1 and buttonRect1.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,660)) # blitting the button
        display.flip()
    return "menu"

def story():
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[3])
    mixer.music.play(-1)
    buttonRect2 = Rect(940,0,130,50)
    running = True
    story = image.load("images/story.png")
    storyLine = image.load("images/Storyline.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    screen.blit(storyLine,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect2.collidepoint(mx,my):
            draw.rect(screen,WHITE,buttonRect2,2)
        else:
            draw.rect(screen,BLACK,buttonRect2)
        if mb[0] == 1 and buttonRect2.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,0)) # blitting the button
        display.flip()
    return "menu"

running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = Game()    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()    
    
quit()
