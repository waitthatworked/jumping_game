# This game was made following the Tech With Tim Pygame
# Tutorial series as a guide

# Many creative alterations were made in the process
import pygame

pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 500

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Colours
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Player sprites
walkRight = [pygame.image.load('sprites/R1.png'), 
pygame.image.load('sprites/R2.png'), pygame.image.load('sprites/R3.png'), 
pygame.image.load('sprites/R4.png'), pygame.image.load('sprites/R5.png'), 
pygame.image.load('sprites/R6.png'), pygame.image.load('sprites/R7.png'), 
pygame.image.load('sprites/R8.png'),pygame.image.load('sprites/R9.png')]

walkLeft = [pygame.image.load('sprites/L1.png'),
pygame.image.load('sprites/L2.png'), pygame.image.load('sprites/L3.png'),
pygame.image.load('sprites/L4.png'), pygame.image.load('sprites/L5.png'),
pygame.image.load('sprites/L6.png'), pygame.image.load('sprites/L7.png'),
pygame.image.load('sprites/L8.png'), pygame.image.load('sprites/L9.png')]

bg = pygame.image.load('sprites/bg.jpg')
char = pygame.image.load('sprites/standing.png')

pygame.display.set_caption("Jumping Game")

x = 50
y = 50
width = 40
height = 60
vel = 15
gravity = 10
isJump = False
jumpCount = 10

run = True
while run:
    pygame.time.delay(50)

    # if y < WIN_HEIGHT - height:
    #     y += gravity

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
    if keys[pygame.K_RIGHT] and x < WIN_WIDTH - width:
        x += vel
    if not(isJump):
        if keys[pygame.K_UP] and y > 0:
            y -= vel
        if keys[pygame.K_DOWN] and y < WIN_HEIGHT - height:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.7 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    win.fill(black)

    pygame.draw.rect(win, red, (x, y, width, height))
    pygame.display.update()

pygame.quit()
