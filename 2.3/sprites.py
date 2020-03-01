import pygame as pg
from settings import *
import sys
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((50, 50))
        self.image.fill(YELLOW)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = (WIDTH / 2, HEIGHT / 2)

    def update(self):

        # keys = pg.key.get_pressed()
        # if keys[pg.K_UP]:
        #     self.rect.centery += -10
        # if keys[pg.K_DOWN]:
        #     self.rect.centery += 10

        with open("Pipe", 'r') as f:
            try:
                action = f.read()
            except:
                action = "SAME"

        if action == "UP":
            self.rect.centery += -5
        elif action == "DOWN":
            self.rect.centery += 5

        if self.rect.top > HEIGHT:
            self.rect.centery -= HEIGHT
        if self.rect.bottom < 0:
            self.rect.centery += HEIGHT


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.centerx += -3


class Gap():
    def __init__(self, y, all_sprites, platform):
        self.p1 = Platform(WIDTH, 0, 70, y - GAP_SIZE/2)
        self.p2 = Platform(WIDTH, y + GAP_SIZE/2, 70, HEIGHT - y - GAP_SIZE/2)
        all_sprites.add(self.p1)
        platform.add(self.p1)
        all_sprites.add(self.p2)
        platform.add(self.p2)
