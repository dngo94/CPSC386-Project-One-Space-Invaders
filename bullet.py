import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.screen = game.screen

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class BulletFromAlien(Bullet):
    """A class to manage bullets fired from the alien"""
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y)
        settings = game.settings
        self.color = settings.alien_bullet_color
        self.speed_factor = -settings.bullet_speed_factor
        self.width = settings.alien_bullet_width
        self.height = settings.alien_bullet_height

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.top = y
        self.rect.centerx = x
        self.y = float(self.rect.y)

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class BulletFromShip(Bullet):
    """A class to manage bullets fired from the ship"""
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y)
        settings = game.settings
        self.color = settings.ship_bullet_color
        self.speed_factor = -settings.bullet_speed_factor
        self.width = settings.ship_bullet_width
        self.height = settings.ship_bullet_height

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.top = y
        self.rect.centerx = x
        self.y = float(self.rect.y)
        self.speed_factor = game.settings.bullet_speed_factor

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)