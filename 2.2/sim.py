import pygame as pg
from sprite import *
from settings import *
from Read import *
import math


def distance(x1, y1, x2, y2):

    return math.sqrt(math.pow(x2 - x1, 2) +
                     math.pow(y2 - y1, 2) * 1.0)


class Game:
    def __init__(self):
        self.image = input("Image: ")
        pg.init()
        pg.mixer.init()
        _, _, self.circs, self.WIDTH, self.HEIGHT, _, _, _, _ = LandC(self.image)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.speed = 5

    def new(self):
        self.score = 0
        # Initiate sprites
        self.all_sprites = pg.sprite.Group()
        self.balls = []
        for i in range(len(self.circs)):
            c = Circle(self, self.circs[i][0], self.circs[i][1], self.circs[i][2], self.speed)
            self.balls.append(c)
            self.all_sprites.add(c)

        dx, dy, _, _, _, X1, Y1, X2, Y2 = LandC(self.image)
        print(dx, " ", dy)
        _min = math.inf
        for i in range(len(self.balls)):
            dist1 = distance(self.balls[i].x, self.balls[i].y, X1, Y1)
            dist2 = distance(self.balls[i].x, self.balls[i].y, X2, Y2)
            min_ = min(dist1, dist2)
            if _min > min_:
                _min = min_
                minIndex = i

        self.balls[minIndex].dx = dx
        self.balls[minIndex].dy = dy
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        index = 0
        for i in range(len(self.balls)):
            if self.balls[i].dx != 0 and self.balls[i].dy != 0:
                index = i

        for i in range(len(self.balls)):
            if index != i:

                x = self.balls[index].rect.centerx - self.balls[i].rect.centerx
                y = self.balls[index].rect.centery - self.balls[i].rect.centery

                distance = math.hypot(abs(x), abs(y))

                if distance <= self.balls[i].r + self.balls[index].r:
                    self.balls[i].dx = self.balls[index].dx
                    self.balls[index].dx = 0

                    self.balls[i].dy = self.balls[index].dy
                    self.balls[index].dy = 0
                    self.score += 1

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 30, BLACK, self.WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use arrows to move, and collect points", 30, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 30, RED, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 30, BLUE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, BLUE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 30, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 30, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 30, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore),
                           30, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
# g.show_start_screen()
while g.running:
    g.new()
#     g.show_go_screen()

pg.quit()
