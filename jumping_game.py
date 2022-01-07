# This game was made following the Tech With Tim Pygame
# Tutorial series as a guide

# Many creative alterations were made in the process
import pygame

pygame.init()

WIN_HEIGHT = 420
WIN_WIDTH = 740

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bg = pygame.image.load('sprites/moon_small.png')

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
walkRight = [pygame.image.load('worm_sprites/R1.png'), 
pygame.image.load('worm_sprites/R2.png'), pygame.image.load('worm_sprites/R3.png')]

walkLeft = [pygame.image.load('worm_sprites/L1.png'), 
pygame.image.load('worm_sprites/L2.png'), pygame.image.load('worm_sprites/L3.png')]

standRight = [pygame.image.load('worm_sprites/R1.png'), pygame.image.load('worm_sprites/HR1.png'), 
pygame.image.load('worm_sprites/HR2.png'), pygame.image.load('worm_sprites/HR1.png'), 
pygame.image.load('worm_sprites/R1.png')]

standLeft = [pygame.image.load('worm_sprites/L1.png'), pygame.image.load('worm_sprites/HL1.png'), 
pygame.image.load('worm_sprites/HL2.png'), pygame.image.load('worm_sprites/HL1.png'), 
pygame.image.load('worm_sprites/L1.png')]

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
        self.standCount = 0
        self.left = False
        self.right = True
        self.standing = True
        self.hitbox = (self.x-7, self.y + 40, 80, 25)
    
        # Jumping Variables
        self.isJump = False
        self.touchingSurface = True
        self.jumpTimer = 0

    # draws the player
    def draw(self, win):
        # resets walk/stand count
        if self.walkCount >= 9:
            self.walkCount = 0

        if self.standCount >= 9:
            self.standCount = 0

        # Controls walking animations
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(standLeft[self.standCount//3], (self.x, self.y))
                self.standCount += 1
            else: 
                win.blit(standRight[self.standCount//3], (self.x, self.y))
                self.standCount += 1
        self.hitbox = (self.x-7, self.y + 40, 80, 25)
        pygame.draw.rect(win, red, self.hitbox, 2)

class enemy(object):
    walkRight = [pygame.image.load('sprites/R1E.png'),
    pygame.image.load('sprites/R2E.png'), pygame.image.load('sprites/R3E.png'),
    pygame.image.load('sprites/R4E.png'), pygame.image.load('sprites/R5E.png'),
    pygame.image.load('sprites/R6E.png'), pygame.image.load('sprites/R7E.png'), 
    pygame.image.load('sprites/R8E.png'), pygame.image.load('sprites/R9E.png'), 
    pygame.image.load('sprites/R10E.png'), pygame.image.load('sprites/R11E.png')]
    walkLeft = [pygame.image.load('sprites/L1E.png'), 
    pygame.image.load('sprites/L2E.png'), pygame.image.load('sprites/L3E.png'), 
    pygame.image.load('sprites/L4E.png'), pygame.image.load('sprites/L5E.png'), 
    pygame.image.load('sprites/L6E.png'), pygame.image.load('sprites/L7E.png'), 
    pygame.image.load('sprites/L8E.png'), pygame.image.load('sprites/L9E.png'), 
    pygame.image.load('sprites/L10E.png'), pygame.image.load('sprites/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 20, self.y, 28, 60)
        pygame.draw.rect(win, red, self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    def hit(self):
        print('hit')

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
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# Main Loop:
worm = player(WIN_WIDTH/3, ground, 64, 64)
goblin = enemy(100, WIN_HEIGHT-64, 64,64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    pygame.time.delay(timeDelay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # If a bullet goes offscreen, player can shoot more bullets
    for bullet in bullets:

        # Checks if bullet falls within enemy hitbox
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < WIN_WIDTH and bullet.x > 0:
            bullet.x += bullet.vel
        else: 
            bullets.pop(bullets.index(bullet))

    # Use keyboard inputs to control movement
    keys = pygame.key.get_pressed()

    # Code for shooting bullets
    if keys[pygame.K_SPACE] and shootLoop == 0:
        # Which way the worm is facing
        if worm.left:
            facing = -1
        else:
            facing = 1

        shootLoop = 1

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