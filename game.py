#imports
import pygame
from pygame.locals import *
import sys

#init 2d game
pygame.init()
vec = pygame.math.Vector2

#game vars
HEIGHT    = 450
WIDTH     = 800
ACC       = 1
FRIC      = -0.25
GRAV      = 0.5
MAX_JUMPS = 1
EX_JUMPS  = 1
FALL_CAP  = 15
FPS       = 60

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
    if rect1.top > rect2.top:
        return "top"
    elif rect1.left > rect2.left:
        return "left"
    elif rect1.right < rect2.right:
        return "right"
    else:
        return "bottom"

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #position
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        #sprite
        #self.image = pygame.image.load("sprites/idle.png")
        self.surf = pygame.Surface((15, 15), pygame.SRCALPHA)
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
        #self.surf.blit(self.image, self.rect)

        #states
        self.walljump = False

    #movement
    def move(self):
        self.acc = vec(0, GRAV)

        pressed_keys = pygame.key.get_pressed()

        #left and right arrows for movement
        if pressed_keys[left]:
            self.acc.x = -ACC
        if pressed_keys[right]:
            self.acc.x = ACC

        #update and slide movement
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #screen boundary
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - 7.5
            self.vel.x = 0
        if self.rect.left < 0:
            self.pos.x = 7.5
            self.vel.x = 0
             
        #update sprite
        self.rect.midbottom = self.pos

    #jump
    def jump(self):
        global EX_JUMPS, MAX_JUMPS
        #checks if on ground before jumping
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits or EX_JUMPS > 0:
            self.vel.y = -10
            if self.walljump == 'left':
                self.vel.y = -15
                self.vel.x = -10
            elif self.walljump == 'right':
                self.vel.y = -15
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
        for obj in hits:
            #if len(hits) > 0:
                #print(determineSide(obj.rect, self.rect))
            if P1.vel.y > 0 and hits and determineSide(obj.rect, self.rect) == 'top':
                self.vel.y = 0
                self.pos.y = obj.rect.top
                EX_JUMPS = MAX_JUMPS
            elif hits and determineSide(obj.rect, self.rect) == 'bottom':
                self.vel.y = 0
                self.pos.y = obj.rect.bottom + 16
                self.walljump = False
            if hits and determineSide(obj.rect, self.rect) == 'left':
                if self.walljump == False:
                    self.vel.x = 0
                self.vel.y /= 2
                self.pos.x = obj.rect.left - 7.5
                self.walljump = 'left'
            elif hits and determineSide(obj.rect, self.rect) == 'right':
                if self.walljump == False:
                    self.vel.x = 0
                self.vel.y /= 2
                self.pos.x = obj.rect.right + 7.5
                self.walljump = 'right'
        if len(hits) < 1:
            self.walljump = False
        
        #print(self.pos)

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
PT2 = platform(50, 200, (200, 200))
PT3 = platform(50, 200, (600, 200))
PT4 = platform(50, 200, (400, 400))
P1 = Player()

#assign player and platform to group of all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(PT3)
all_sprites.add(PT4)
all_sprites.add(P1)

#assign platform to group for platforms
platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)
platforms.add(PT3)
platforms.add(PT4)

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