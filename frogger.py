import pygame
import time
import random
#initialize pygame (always do this)
pygame.init()

#create a window (the (500,500) is a tuple.  This is width and height)
win = pygame.display.set_mode((700, 650))

#set display name
pygame.display.set_caption("Bootleg Frogger")

#set background color
sea = (135,206,250)
win.fill(sea)
#fill screen with image: win.blit(img, (0,0))
#after making a change, you need to refresh the screen.
pygame.display.flip()

#coding a character
#setting up variables (coordinates, w/h, velocity, color)
#EDIT: setting up shark variables as well
frog = pygame.image.load('extras/frog.png')
sharks = [pygame.image.load('extras/shark.png'), pygame.image.load('extras/shark.png'), pygame.image.load('extras/shark.png'),\
    pygame.image.load('extras/shark2.png'), pygame.image.load('extras/shark2.png'),]
width = 60
height = 55
sharkw = 90
sharkh = 45
default = (280, 600)
shark_default = (0, (700 - sharkw))
x,y = default
a,b = shark_default
vel = 30
upvel = 100
shark_vel = 2
green = (0,128,0)
random_spawn = [100, 200, 300, 400, 500]

def draw_shark():
    for i in range (0, 3):
        win.blit(sharks[i], (a, random_spawn[i]))
    for i in range (3, 5):
        win.blit(sharks[i], (b, random_spawn[i]))

#determine new shark spawn locations       
def randomize():
    global random_spawn
    for i in range(0, 5):
        random_spawn[i] = random.randint(100, 501)

#game variables
passed = False
failed = False
level = 1
clock = pygame.time.Clock
#for text
font = pygame.font.SysFont('comicsans', 30, True, True)
level_font = pygame.font.SysFont('impact', 150, True)
#sound effects can only be .wav, music can be either .wav or .mp3
win_sound = pygame.mixer.Sound('extras/win.wav')
lose_sound = pygame.mixer.Sound('extras/lose.wav')
hop_sound = pygame.mixer.Sound('extras/hop.wav')

music = pygame.mixer.music.load('extras/music.mp3')
#play music continuously
pygame.mixer.music.play(-1)

#drawing frog and sharks
def redraw_window():
    win.fill(sea)

    #creating level text, permanent
    newlevel_text = level_font.render("Level:" + str(level), 1, (255,0,0))
    win.blit(newlevel_text, (100, 230))

    #drawing frog
    win.blit(frog, (x,y))

    #drawing sharks
    draw_shark()

    #for things to actually show up, you need to refresh the display
    #unlike flip, update only refreshes a portion of the screen
    pygame.display.update()

def display_level():
    t_end = time.time() + 1.5
    while time.time() < t_end:
        #level text, temporary
        newlevel_text = level_font.render("Level:" + str(level), 1, (255,0,0))
        win.blit(newlevel_text, (100, 230))
    redraw_window();

#All games have a loop that ends when something happens.  Main loop
run = True
while run:

    #the time.delay is in miliseconds
    pygame.time.delay(50)

    if passed:
        pygame.time.delay(1000)
        passed = False
        x,y = default
        a,b = shark_default
        shark_vel += 5
        randomize()
        level += 1

    if failed:
        pygame.time.delay(1000)
        failed = False
        x,y = default
        a,b = shark_default
        shark_vel = 2
        level = 1

    #checking to see if user touched shark
    for i in range (0, 3):
        if (x < a + sharkw) and (x + width > a)\
        and (y < random_spawn[i] + sharkh) and\
        (y + height > random_spawn[i]):
            failed = True
            lose_sound.play()
    for i in range (3, 5):
        if (x < b + sharkw) and (x + width > b)\
        and (y < random_spawn[i] + sharkh) and\
        (y + height > random_spawn[i]):
            failed = True
            lose_sound.play()

    #an event in pygame is anything that happens from user
    for event in pygame.event.get():

        #pygame.QUIT is the big red 'X' in the top right corner
        if event.type == pygame.QUIT:
            run = False
        
        #also a way to quit using the 'Esc' key
        if event.type == pygame.K_ESCAPE:
            run = False

        #Now for the keys.  Creating a list
        keys = pygame.key.get_pressed()
        #conditionals for key pressed
        #the rest for movement
        if keys[pygame.K_LEFT]:
            if x > 0:
                x -= vel
            #hop_sound.play()
        if keys[pygame.K_RIGHT]:
            if x < (700 - width):
                x += vel
            #hop_sound.play()
        if keys[pygame.K_UP]:
            y -= upvel
            if y == 0:
                passed = True
                win_sound.play()
            else:
                hop_sound.play()
    #movement for sharks
    if a >= shark_default[1]:
        a = shark_default[0]
    else:
        a += shark_vel
    if b <= shark_default[0]:
        b = shark_default[1]
    else:
        b -= shark_vel
    #redraw screen after movement
    redraw_window()

pygame.quit()



