# This game was made following the Tech With Tim Pygame
# Tutorial series as a guide

# Many creative alterations were made in the process
import pygame

pygame.init()

WIN_HEIGHT = 480
WIN_WIDTH = 500

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Colours
black = (0, 0, 0)
red = (255, 0, 0)
pink = (255, 100, 100)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Jumping variables
ground = WIN_HEIGHT - 80
gravity = 10
timeDelay = 50 #milliseconds
timer = 0

# Player sprites
walkRight = [pygame.image.load('sprites/R1.png'), 
pygame.image.load('sprites/R2.png'), pygame.image.load('sprites/R3.png'), 
pygame.image.load('sprites/R4.png'), pygame.image.load('sprites/R5.png'), 
pygame.image.load('sprites/R6.png'), pygame.image.load('sprites/R7.png'), 
pygame.image.load('sprites/R8.png'), pygame.image.load('sprites/R9.png')]

walkLeft = [pygame.image.load('sprites/L1.png'),
pygame.image.load('sprites/L2.png'), pygame.image.load('sprites/L3.png'),
pygame.image.load('sprites/L4.png'), pygame.image.load('sprites/L5.png'),
pygame.image.load('sprites/L6.png'), pygame.image.load('sprites/L7.png'),
pygame.image.load('sprites/L8.png'), pygame.image.load('sprites/L9.png')]

bg = pygame.image.load('sprites/bg.jpg')
char = pygame.image.load('sprites/standing.png')

pygame.display.set_caption("Worm's Revenge")

# Variables
clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        
        # Movement and position variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.left = False
        self.right = True
        self.standing = True

        # Jumping Variables
        self.isJump = False
        self.touchingSurface = True
        self.jumpTimer = 0

    # draws the player
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        # Controls walking animations
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else: 
                win.blit(walkLeft[0], (self.x, self.y))

# class for bullets
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    # draws the projectile
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Redraws the game window when called
def redrawGameWindow():
    win.blit(bg, (0, 0))
    worm.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# Main Loop:
worm = player(WIN_WIDTH/3, ground, 64, 64)
bullets = []
run = True
while run:
    clock.tick(27)
    pygame.time.delay(timeDelay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # If a bullet goes offscreen, player can shoot more bullets
    for bullet in bullets:
        if bullet.x < WIN_WIDTH and bullet.x > 0:
            bullet.x += bullet.vel
        else: 
            bullets.pop(bullets.index(bullet))

    # Use keyboard inputs to control movement
    keys = pygame.key.get_pressed()

    # Code for shooting bullets
    if keys[pygame.K_SPACE]:
        # Which way the worm is facing
        if worm.left:
            facing = -1
        else:
            facing = 1

        # Caps the number of bullets
        if len(bullets) < 20:
            bullets.append(projectile(round(worm.x + worm.width //2), round(worm.y + worm.height//2), 6, pink, facing))

    # Leftward Movement
    if keys[pygame.K_LEFT] and worm.x > 0:
        worm.x -= worm.vel
        worm.left = True
        worm.right = False
        worm.standing = False
    # Rightward Movement
    elif keys[pygame.K_RIGHT] and worm.x < WIN_WIDTH - worm.width:
        worm.x += worm.vel
        worm.left = False
        worm.right = True
        worm.standing = False
    # Standing
    else:
        worm.standing = True
        worm.walkCount = 0

    # My jumping code:
    if not(worm.isJump):
        if keys[pygame.K_UP] and worm.touchingSurface:
            worm.isJump = True
            worm.walkCount = 0
            
            # Important variables for jumping
            worm.touchingSurface = False
            worm.jumpTimer = 0
    else:
        # v = u + at
        vel_y = 40 - (gravity * (worm.jumpTimer))
        worm.y -= vel_y
        worm.jumpTimer += 0.5
        
        # If the worm is on/past the ground
        if worm.y >= ground:
            worm.y = ground
            worm.isJump = False
            worm.touchingSurface = True
    
    redrawGameWindow()

pygame.quit()

    # Tim's Strange Jumping Code:    
    # if not(isJump):
    #     if keys[pygame.K_UP] and y > 0:
    #         y -= vel
    #     if keys[pygame.K_DOWN] and y < WIN_HEIGHT - height:
    #         y += vel
    #     if keys[pygame.K_SPACE]:
    #         isJump = True
    # else:
    #     if jumpCount >= -10:
    #         neg = 1
    #         if jumpCount < 0:
    #             neg = -1
    #         y -= (jumpCount ** 2) * 0.7 * neg
    #         jumpCount -= 1
    #     else:
    #         isJump = False
    #         jumpCount = 10