import pygame as pg
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self, game, sound):
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.sound = sound

        self.text_color = (230, 230, 230)
        self.font = pg.font.SysFont(None, 48)
        self.score_image, self.score_rect = None, None
        self.high_score_image, self.high_score_rect = None, None
        self.level_image, self.level_rect = None, None
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def check_high_score(self, score):
        if score > self.stats.high_score:
            self.stats.high_score = score
            self.prep_high_score()

    def prep_high_score(self):
        rounded_score = int(round(self.stats.high_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.high_score_image = self.font.render(score_str, True, self.text_color,
                                                 self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                            self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            ship = Ship(game=self.game, sound=self.sound)
            ship.rect.x = 10 + i * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

