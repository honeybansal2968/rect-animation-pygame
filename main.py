import pygame as pg
from settings import *
import math
import sys

vec = pg.math.Vector2
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
""" Add player name top of the game who is playing now"""
clock = pg.time.Clock()

dt = clock.tick(FPS) / 1000
hand_img = pg.image.load('laserRed.png')


# direction = "right"


class Player1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.pos = vec(400, 380)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 250
        self.jumping = True
        print("player1:", self.pos)

    def update(self):
        self.acc = vec(0, GRAVITY)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.acc.x = -0.5
        if keystate[pg.K_RIGHT]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos


class Hand(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.orig_image = pg.Surface((60, 3))
        self.orig_image.fill(RED)
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec(player1.pos[0], player1.pos[1])
        self.rect.center = player1.rect.center
        self.angle = 0
        self.rot_speed = 8

    def update(self):
        self.pos.x = player1.pos[0] + 30
        self.pos.y = player1.pos[1] - 20
        self.angle += self.rot_speed
        new_image = pg.transform.rotate(self.orig_image, self.angle)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.groups = all_sprites, grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y


def jump():
    hits = pg.sprite.spritecollide(player1, grounds, False)
    if hits:
        player1.vel.y = -20


all_sprites = pg.sprite.Group()
grounds = pg.sprite.Group()
for ground in GROUND_LIST:
    Ground(*ground)
bullets = pg.sprite.Group()
player1 = Player1()
all_sprites.add(player1)
Hand()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # global direction
    # Process input (events)
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                pg.quit()
            if event.key == pg.K_SPACE:
                jump()

    # Update
    all_sprites.update()

    if player1.vel.y > 0:
        hits = pg.sprite.spritecollide(player1, grounds, False)
        if hits:
            for hit in hits:
                player1.pos.y = hit.rect.top
                player1.vel.y = 0

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
