#imports
import pygame
from pygame.locals import *
import sys

#init 2d game
pygame.init()
vec = pygame.math.Vector2

#game vars
HEIGHT   = 900
WIDTH    = 1600
ACC      = 0.75
FRIC     = -0.12
GRAV     = 0.5
EX_JUMPS = 1
FALL_CAP = 15
FPS      = 60

#set up fps
FramePerSec = pygame.time.Clock()

#set up window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#key bindings
left  = pygame.K_LEFT
right = pygame.K_RIGHT
jump  = pygame.K_SPACE

#collision direction
def determineSide(rect1, rect2):
    if rect1.midtop[1] > rect2.midtop[1]:
        return "top"
    elif rect1.midleft[0] > rect2.midleft[0]:
        return "left"
    elif rect1.midright[0] < rect2.midright[0]:
        return "right"
    else:
        return "bottom"

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()

        #position
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #states
        self.walljump = False

    #movement
    def move(self):
        self.acc = vec(0, GRAV)

        pressed_keys = pygame.key.get_pressed()

        #left and right arrows for movement
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #update and slide movement
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #screen wrapping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        #update sprite
        self.rect.midbottom = self.pos

    #jump
    def jump(self):
        global EX_JUMPS
        #checks if on ground before jumping
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits or EX_JUMPS > 0:
            self.vel.y = -15
            if self.walljump == 'left':
                self.vel.y *= 2
                self.vel.x = -10
            elif self.walljump == 'right':
                self.vel.y *= 2
                self.vel.x = 10
            if not hits:
               EX_JUMPS = EX_JUMPS - 1

    def update(self):
        global EX_JUMPS
        #fall speed cap
        if self.vel.y > FALL_CAP:
            self.vel.y = FALL_CAP
        #wall and platform collision
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            print(determineSide(hits[0].rect, self.rect))
        if P1.vel.y > 0 and hits and determineSide(hits[0].rect, self.rect) == 'top':
            self.vel.y = 0
            self.pos.y = hits[0].rect.top + 1
            EX_JUMPS = 1
        elif P1.vel.y < 0 and hits and determineSide(self.rect, hits[0].rect) == 'bottom':
            self.vel.y = 0
            self.pos.y = hits[0].rect.bottom - 1
        if hits and determineSide(hits[0].rect, self.rect) == 'left':
            if self.walljump == False:
                self.vel.x = 0
            self.vel.y /= 2
            self.rect.right = hits[0].rect.left
            self.walljump = 'left'
        elif hits and determineSide(hits[0].rect, self.rect) == 'right':
            if self.walljump == False:
                self.vel.x = 0
            self.vel.y /= 2
            self.rect.left = hits[0].rect.right
            self.walljump = 'right'
        else:
            self.walljump = False

#platform
class platform(pygame.sprite.Sprite):
    def __init__(self, width, height, pos):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = pos)

    def move(self):
        pass

#define test player and platform
PT1 = platform(WIDTH, 20, (WIDTH/2, HEIGHT - 10))
PT2 = platform(100, 400, (400, 400))
PT3 = platform(100, 400, (1200, 400))
P1 = Player()

#assign player and platform to group of all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(PT3)
all_sprites.add(P1)

#assign platform to group for platforms
platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)
platforms.add(PT3)

#game loop
while True:
    for event in pygame.event.get():
        #escape
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #jump
        if event.type == pygame.KEYDOWN:    
            if event.key == jump:
                P1.jump()

    #update screen
    displaysurface.fill((0,0,0))
    P1.update()

    #update movement
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)