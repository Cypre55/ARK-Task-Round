import pygame as pg
from settings import *
import pygame.gfxdraw
import time


class Circle(pg.sprite.Sprite):
    def __init__(self, game, x, y, r, speed):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.r = r
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.image = pg.Surface((2 * self.r + 2, 2 * self.r + 2), pg.SRCALPHA)
        pygame.gfxdraw.circle(self.image, self.r + 1, self.r + 1, self.r, BLACK)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.oldtime = time.time()

    def update(self):
        self.speedx = self.dx * self.speed
        self.speedy = self.dy * self.speed
        if (self.rect.centerx + self.r - 2) >= self.game.WIDTH and self.dx > 0:
            self.dx = -self.dx
        elif (self.rect.centery + self.r - 2) >= self.game.HEIGHT and self.dy > 0:
            self.dy = -self.dy
        elif (self.rect.centerx - self.r + 2) <= 0 and self.dx < 0:
            self.dx = -self.dx
        elif (self.rect.centery - self.r + 2) <= 0 and self.dy < 0:
            self.dy = -self.dy

        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
