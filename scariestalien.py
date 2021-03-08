import pygame as pg
from pygame.sprite import Sprite
from timer import Timer


class Ufo:
    def __init__(self, settings, screen, ufo_group, ship_height, game):
        self.settings = settings
        self.screen = screen
        self.ufo = ufo_group
        self.game = game
        self.ship_height = ship_height
        self.create_fleet()
        self.is_moving = False

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        scaryalien = ScaryUfo(settings=settings, screen=self.screen)
        ufo_width = scaryalien.rect.width + 220
        ufo_height = scaryalien.rect.height - 25
        ufo_per_row = self.ufo_per_row(settings=settings, ufo_width=ufo_width)
        rows_per_screen = self.rows_per_screen(settings=settings, ufo_height=ufo_height)

        for y in range(rows_per_screen):
            for x in range(ufo_per_row):
                scaryalien = ScaryUfo(settings=settings, screen=screen, number=y // 2, x=ufo_width * (4 + 1.5 * x),
                                      y=ufo_height * (3 + y))
                # alien = Alien(settings=settings, screen=screen, x=alien_width * (1 + 2 * x), y=alien_height * (1 + 2 * y))
                self.ufo.add(scaryalien)

    def ufo_per_row(self, settings, ufo_width):
        return 1

    def rows_per_screen(self, settings, ufo_height):
        return 1

    # space_y = settings.screen_height - (alien_height) - self.ship_height
    # # space_y = settings.screen_height - (3 * alien_height) - self.ship_height
    # return int(space_y / (alien_height))
    # # return int(space_y / (2 * alien_height))

    def add(self, scaryalien):
        self.ufo.add(scaryalien)

    def remove(self, scaryalien):
        self.ufo.ufo.remove(scaryalien)



    def check_edges(self):
        for scaryalien in self.ufo:
            if scaryalien.check_edges(): return True

        return False

    def check_ufo_bottom(self):
        r = self.screen.get_rect()
        for scaryalien in self.ufo.sprites():
            if scaryalien.rect.bottom > r.bottom:
                return True
        return False

    def update(self):
        self.ufo.update()
        if self.check_edges():
            self.is_moving = True
        if self.check_ufo_bottom() or pg.sprite.spritecollideany(self.game.ship, self.ufo):
            # print("Resetting game")
            self.game.reset()
            return

        # for y in range(rows_per_screen):
        #     for x in range(aliens_per_row):
        # row = 5
        for scaryalien in self.ufo.copy():
            scaryalien.update()
            if scaryalien.rect.bottom <= 0 or scaryalien.reallydead: self.ufo.remove(scaryalien)

    def draw(self):
        if not self.is_moving:
            for scaryalien in self.ufo.sprites(): scaryalien.draw()
        else:

            print("hello")            #part where alien hit the edge


class ScaryUfo(Sprite):  # INHERITS from SPRITE
    images = [[pg.image.load('images/ufo' + str(number) + str(i) + '.png') for i in range(2)] for number in range(1)]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(4)]

    timers = []
    for i in range(1):
        timers.append(Timer(frames=images[i], wait=700))
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, settings, screen, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = screen
        self.settings = settings
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
        self.timer = ScaryUfo.timers[number]
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
            self.timer = ScaryUfo.timer_boom
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            # print("switched to boom timer", self.timer_boom.frame_index(), len(Alien.images_boom))
            if self.timer_boom.frame_index() == len(ScaryUfo.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
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
        print(ScaryUfo.images)
