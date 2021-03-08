import pygame as pg
from pygame.sprite import Sprite
from pygame.sprite import Group

class Barrier:
    def __init__(self, ship_height, game):
        self.settings = game.settings
        self.screen = game.screen
        self.game = game
        self.barrier_group = Group()
        self.ship_height = ship_height
        self.create_fleet()

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        barrier = Barriers(parent=self, game =self.game )
        barrier_width = barrier.rect.width
        barrier_height = barrier.rect.height + 530  # position of alien
        barrier_per_row = self.barrier_per_row(settings=settings, barrier_width=barrier_width)
        rows_per_screen = self.rows_per_screen(settings=settings, barrier_height=barrier_height)

        for y in range(rows_per_screen):
            for x in range(barrier_per_row):
                barrier = Barriers(parent=self, game=self.game, x=barrier_width + 2 * barrier_width * x,
                              y=barrier_height + 2 * barrier_height * y)
                self.barrier_group.add(barrier)

    def barrier_per_row(self, settings, barrier_width):
        space_x = settings.screen_width - 2 * barrier_width
        return 4 # column

    def rows_per_screen(self, settings, barrier_height):
        space_y = settings.screen_height - (2 * barrier_height) - self.ship_height
        return 1      # row ,  og code int(space_y / (2 * alien_height))

    def add(self, barrier): self.barrier_group.add(barrier)

    def update(self):
        self.barrier_group.update()


    def draw(self):
        for barrier in self.barrier_group.sprites():
            barrier.draw()


class Barriers(Sprite):   # INHERITS from SPRITE
    def __init__(self,game, parent, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.number = number
        self.game = game
        self.parent = parent
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
