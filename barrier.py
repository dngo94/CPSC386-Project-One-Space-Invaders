import pygame as pg
from pygame.sprite import Sprite


class Barrier:
    def __init__(self, settings, screen, barrier_group, ship_height, game):
        self.settings = settings
        self.barriers = barrier_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.create_fleet()

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        barrier = Barriers(settings=settings, screen=self.screen)
        barrier_width = barrier.rect.width
        barrier_height = barrier.rect.height + 530  # position of alien
        barrier_per_row = self.barrier_per_row(settings=settings, barrier_width=barrier_width)
        rows_per_screen = self.rows_per_screen(settings=settings, barrier_height=barrier_height)

        for y in range(rows_per_screen):
            for x in range(barrier_per_row):
                barrier = Barriers(settings=settings, screen=screen, x=barrier_width + 2 * barrier_width * x,
                              y=barrier_height + 2 * barrier_height * y)
                self.barriers.add(barrier)

    def barrier_per_row(self, settings, barrier_width):
        space_x = settings.screen_width - 2 * barrier_width
        return int(space_x / (2 * barrier_width))  # column

    def rows_per_screen(self, settings, barrier_height):
        space_y = settings.screen_height - (2 * barrier_height) - self.ship_height
        return 2        # row ,  og code int(space_y / (2 * alien_height))

    def add(self, barrier): self.barriers.add(barrier)

    def update(self):
        self.barriers.update()


    def draw(self):
        for barrier in self.barriers.sprites(): barrier.draw()


class Barriers(Sprite):   # INHERITS from SPRITE
    def __init__(self, settings, screen, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.number = number

        self.image = pg.image.load('images/bar.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.x = x
        self.rect.y = self.y = y
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = speed

    def draw(self):

        self.screen.blit(self.image, self.rect)
