import pygame as pg
from settings import Settings
import game_functions as gf
from Scorebutton import scorebutton
from ship import Ship
from alien import Aliens
from game_stats import GameStats
from button import Button
from scariestalien import Ufos
from scoreboard import Scoreboard
from pygame.sprite import Group
from sound import Sound
from threading import Timer
import random
from barrier import Barrier

import time


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        ship_image = pg.image.load('images/ship.bmp')
        self.ship_height = ship_image.get_rect().height
        self.hs = 0

        self.sound = Sound(bg_music="sounds/crazy-space.wav")
        title = pg.image.load('images/title.bmp')
        # alein1 = pg.image.load('images/'alien00.bmp'')
        x = 200
        y = 150
        self.screen.blit(title, (x, y))
        ali0 = pg.image.load('images/ali00.png')

        x = 500
        y = 330
        self.screen.blit(ali0, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=10 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 340))

        ali1 = pg.image.load('images/ali10.png')

        x = 500
        y = 380
        self.screen.blit(ali1, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=20 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 390))

        ali2 = pg.image.load('images/ali20.png')

        x = 500
        y = 430
        self.screen.blit(ali2, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=40 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 440))
        ufo = pg.image.load('images/ufo00.png')

        x = 500
        y = 480
        self.screen.blit(ufo, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=???", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 490))
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.aliens = self.stats = self.sb = self.ship = None

        self.restart()
    def play2(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")

        title = pg.image.load('images/title.bmp')
        # alein1 = pg.image.load('images/'alien00.bmp'')
        x = 200
        y = 150
        self.screen.blit(title, (x, y))
        ali0 = pg.image.load('images/ali00.png')

        x = 500
        y = 330
        self.screen.blit(ali0, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=10 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 340))

        ali1 = pg.image.load('images/ali10.png')

        x = 500
        y = 380
        self.screen.blit(ali1, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=20 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 390))

        ali2 = pg.image.load('images/ali20.png')

        x = 500
        y = 430
        self.screen.blit(ali2, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=40 PTS", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 440))
        ufo = pg.image.load('images/ufo00.png')

        x = 500
        y = 480
        self.screen.blit(ufo, (x, y))
        myfont = pg.font.SysFont("monospace", 25)
        label1 = myfont.render("=???", 1, (230, 230, 230))
        self.screen.blit(label1, (560, 490))
        self.hs = self.stats.high_score
        self.sound = Sound(bg_music="sounds/crazy-space.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.restart()


    def restart(self):

        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play")
        self.hs_button = scorebutton(settings=self.settings, screen=self.screen, msg="HIGH SCORES")
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(game=self, sound=self.sound)
        self.settings.init_dynamic_settings()
        self.barrier = Barrier(ship_height=self.ship_height, game=self)
        self.ufo = Ufos(ship_height=self.ship_height, game=self)
        self.aliens = Aliens(ship_height=self.ship_height, game=self)
        self.ship = Ship(aliens=self.aliens, sound=self.sound, game=self , ufo=self.ufo )

        self.aliens.add_ship(ship=self.ship)

        self.stats.high_score = self.hs
        self.sb.prep_high_score()

    def scores(self):
        myfont = pg.font.SysFont("monospace", 60)
        label = myfont.render("HIGH SCORES", 1, (171, 130, 255))
        self.screen.blit(label, (420, 50))
        score_display = myfont.render(str(self.hs), 1, (171, 130, 255))
        self.screen.blit(score_display, (570, 150))

    def play(self):


        while True:


            gf.check_events(stats=self.stats, play_button=self.play_button, ship=self.ship, sound=self.sound, hs_button=self.hs_button)
            if self.stats.game_active:
                self.ship.update()
                self.aliens.update()
                self.ufo.update()
                self.barrier.update()


            if not self.stats.hs_active:
                self.hs_button.draw_button()
            else:
                self.screen.fill(self.settings.bg_color)
                self.scores()


            if not self.stats.game_active:
                self.play_button.draw()
                self.hs_button.draw_button()
                self.sound.pause_bg()
            else:
                if not self.sound.playing_bg: self.sound.unpause_bg()
                self.screen.fill(self.settings.bg_color)
                self.ship.draw()
                self.aliens.draw()
                self.sb.show_score()
                self.ufo.draw()
                self.barrier.draw()


            pg.display.flip()

    def reset(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ufo.empty()
            self.ufo.create_fleet()
            self.ship.center_ship()
            time.sleep(0.5)
            self.ship.timer = Ship.timer
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            self.hs = self.stats.high_score
            self.play2()
        with open("score.txt", 'a') as f:
            f.write(f'The high score was {self.hs}\n')


def main():
    g = Game()
    g.play()
    # Vector.run_tests()
    # Quaternion.run_tests()
    # Matrix.run_tests()
    # Alien.run_tests()


if __name__ == '__main__':
    main()
