import time

import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
import threading
class Ufos:
    def __init__(self, ship_height, game):

        self.settings = game.settings
        self.screen = game.screen
        self.game = game
        self.ufo_group = Group()
        self.ship_height = ship_height
        self.create_fleet()
        self.ufo_type = None
        self.count = 0
        self.apperance = 0
        self.tic = None

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        ufo = Ufo(parent=self, game=self.game)
        ufo_width = 285
        ufo_height = ufo.rect.height-20
        ufo_per_row = self.ufo_per_row(settings=settings, ufo_width=ufo_width)
        rows_per_screen = self.rows_per_screen(settings=settings, ufo_height=ufo_height)

        for y in range(rows_per_screen):
            ufo_type = y
            for x in range(ufo_per_row):
                ufo = Ufo(parent=self, game=self.game, number=y // 2, x=ufo_width * (4 + 1.5 * x), y=ufo_height * (3 + y))
                # alien = Alien(settings=settings, screen=screen, x=alien_width * (1 + 2 * x), y=alien_height * (1 + 2 * y))
                self.ufo_group.add(ufo)

    def ufo_per_row(self, settings, ufo_width):
        space_x = settings.screen_width - 2 * ufo_width
        return 1

    def rows_per_screen(self, settings, ufo_height): return 1
        # space_y = settings.screen_height - (alien_height) - self.ship_height
        # # space_y = settings.screen_height - (3 * alien_height) - self.ship_height
        # return int(space_y / (alien_height))
        # # return int(space_y / (2 * alien_height))

    def add(self, ufo): self.ufo_group.add(ufo)

    def empty(self):
        self.ufo_group.empty()

    def group(self):
        return self.ufo_group

    def remove(self, ufo): self.ufo_group.remove(ufo)

    def change_direction(self):
        self.settings.ufo_fleet_direction *= -1
        self.ufo_group.remove()

    def check_edges(self):
        for ufo in self.ufo_group.sprites():
            if ufo.check_edges():
             return True
        return False

    def check_ufos_bottom(self):
        r = self.screen.get_rect()
        for ufo in self.ufo_group.sprites():
            if ufo.rect.bottom > r.bottom:
                return True
        return False


    def update(self):
        self.ufo_group.update()
        if self.check_edges():
            self.change_direction()

        if self.check_ufos_bottom() or pg.sprite.spritecollideany(self.game.ship, self.ufo_group):
            # print("Resetting game")
            self.game.reset()
            return

        # for y in range(rows_per_screen):
        #     for x in range(aliens_per_row):
        # row = 5
        for ufo in self.ufo_group.copy():
            ufo.update()
            if ufo.rect.bottom <= 0 or ufo.reallydead: self.ufo_group.remove(ufo)

        if self.apperance > 1:
            elapsed_time = time.perf_counter() - self.tic
            if elapsed_time > 4:
                self.draw()

    def draw(self):
        for ufo in self.ufo_group.sprites():
            ufo.draw()
            self.tic = time.perf_counter()
            self.apperance += 1

class Ufo(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/ufo' + str(number) + str(i) + '.png') for i in range(2)] for number in range(1)]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(4)]

    timers = []
    for i in range(1):
        timers.append(Timer(frames=images[i], wait=700))
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, game, parent, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game=game
        self.parent=parent
        self.number = number
        self.update_requests = 0
        self.dead = False
        self.reallydead = False
        self.timer_switched = False

        # self.image = pg.image.load('images/alien.bmp')
        # self.rect = self.image.get_rect()
        # self.images = ['images/invader' + str(number) + str(i) + '.png' for i in range(2)]
        # print(self.images)
        # self.frames = [pg.image.load(self.images[i]) for i in range(len(self.images))]
        self.timer = Ufo.timers[number]
        # self.timer = Timer(frames=self.frames, wait=700)
        self.rect = self.timer.imagerect().get_rect()

        self.rect.x = self.x = x
        self.rect.y = self.y = y
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = speed

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def update(self):
        if self.dead and not self.timer_switched:
            self.timer = Ufo.timer_boom
            self.timer_switched = True
            self.game.stats.score += self.settings.ufo_points  # del. * len(self.parent.alien_group)
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()
        elif self.dead and self.timer_switched:
            # print("switched to boom timer", self.timer_boom.frame_index(), len(Alien.images_boom))
            if self.timer_boom.frame_index() == len(Ufo.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.parent.remove(self)
                self.timer.reset()
        delta = self.settings.ufo_speed * self.settings.ufo_fleet_direction

        self.rect.x += delta
        self.x = self.rect.x

    def draw(self):
        # image = Alien.images[self.number]
        # self.screen.blit(image, self.rect)
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

    @staticmethod
    def run_tests():
        print(Ufo.images)
