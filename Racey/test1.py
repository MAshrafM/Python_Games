import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
dark_green = (0,200,0)
blue = (0,0,255)
dark_blue = (0,0,200)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

pause = False
#crash = True

carImg = pygame.image.load('car.png')
pygame.display.set_icon(carImg)
car_width = 75
car_height = 150
carImg = pygame.transform.scale(carImg, (car_width, car_height))

def blocks(block_x, block_y, block_width, block_height, block_color):
    pygame.draw.rect(gameDisplay, block_color, [block_x, block_y, block_width, block_height])
    
def Score(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Score : "+str(count), True, blue)
    gameDisplay.blit(text, (0,0))
    
def car(x,y):
    #draw image to window
    gameDisplay.blit(carImg, (x,y))

def textObjects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
    
##def messageDisplay(text):
##    message = pygame.font.SysFont("comicsansms", 115)
##    messageSurf, messageRect = textObjects(text, message)
##    messageRect.center = ((display_width/2), (display_height/2))
##    gameDisplay.blit(messageSurf, messageRect)
##
##    pygame.display.update()
##    time.sleep(2)
##
##    game_loop()
    
def crash():
    
    message = pygame.font.SysFont("comicsansms", 115)
    messageSurf, messageRect = textObjects("You Crashed", message)
    messageRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(messageSurf, messageRect)    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)


        button("Play Again", 150,400,100,50, green, dark_green, game_loop)
        button("Quit!", 550,400,100,50, blue, dark_blue, quitgame)
        
        pygame.display.update()
        clock.tick(60)


def button(msg, x, y, width, hieght, inactive_c, active_c, function = None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if (x < mouse[0] < x + width) and (y < mouse[1] < y + hieght ):
        pygame.draw.rect(gameDisplay, inactive_c, (x,y,width,hieght))
        if click[0] == 1 and function != None:
            function()            
    else:
        pygame.draw.rect(gameDisplay, active_c, (x,y,width,hieght))

    smallText = pygame.font.SysFont("comicsansms", 20)
    messageSurf, messageRect = textObjects(msg, smallText)
    messageRect.center = ((x+ width/2), (y + hieght/2))
    gameDisplay.blit(messageSurf, messageRect)
def unpause():
	global pause
	pause = False
def paused():


    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message = pygame.font.SysFont("comicsansms", 115)
        messageSurf, messageRect = textObjects("Paused", message)
        messageRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(messageSurf, messageRect)

        button("Continue", 150,400,100,50, green, dark_green, unpause)
        button("Quit!", 550,400,100,50, blue, dark_blue, quitgame)
        
        pygame.display.update()
        clock.tick(60)

	
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message = pygame.font.SysFont("comicsansms", 115)
        messageSurf, messageRect = textObjects("A Bit Racey", message)
        messageRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(messageSurf, messageRect)

        button("GO!", 150,400,100,50, green, dark_green, game_loop)
        button("Quit!", 550,400,100,50, blue, dark_blue, quitgame)
        
        pygame.display.update()
        clock.tick(60)

def quitgame():
    pygame.quit()
    quit()    

    
def game_loop():
    global pause
    pos_x = (display_width * 0.45)
    pos_y = (display_height * 0.75)

    x_new = 0

    block_startx = random.randrange(0, display_width)
    block_starty = -600
    block_speed = 7
    block_w = 100
    block_h = 100
    score = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                gameExit = True

            #pressed key 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_new = -5
                if event.key == pygame.K_RIGHT:
                    x_new = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            #key up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_new = 0

                    

            
        #updating position
        pos_x += x_new            
                
        #background
        gameDisplay.fill(white)

        #blocks(block_x, block_y, block_width, block_height, block_color)
        blocks(block_startx, block_starty, block_w, block_h, black)
        block_starty += block_speed
        #draw car
        car(pos_x,pos_y)
        #draw score
        Score(score);

        #boundaries
        if pos_x > display_width - car_width or pos_x < 0:
            crash()

        #new blocks
        if block_starty > display_height:
            block_starty = 0 - display_height
            block_startx = random.randrange(0, display_width)
            score += 1
            if score%5 == 0:
                block_speed += 2
            
            
        if pos_y < block_starty+block_h:
            if pos_x > block_startx and pos_x < block_startx + block_w or pos_x + car_width > block_startx and pos_x + car_width < block_startx + block_w:
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
