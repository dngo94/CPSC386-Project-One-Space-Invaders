import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
from bullet import BulletFromShip


class Ship(Sprite):
    images = [pg.image.load('images/ship.bmp')]
    images_boom = [pg.image.load('images/ship_boom' + str(i) + '.png') for i in range(9)]
    timer = Timer(frames=images, wait=1000)
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, sound, game, aliens=None):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.sound = sound
        self.game = game
        self.aliens = aliens

        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()

        self.center = 0
        self.center_ship()

        self.moving_right = False
        self.moving_left = False

        self.shooting_bullets = False
        self.bullets_attempted = 0
        self.dead, self.reallydead, self.timer_switched = False, False, False
        self.ship_group = Group()
        self.ship_group.add(self)        # only one Ship (myself) in the Ship group to simplify collision tracking
        self.bullet_group_that_kill_aliens = Group()
        self.timer = Ship.timer
        # self.bullets = Bullets(settings=game.settings, is_alien_bullet=False)

    def add_bullet(self, game, x, y):
        self.bullet_group_that_kill_aliens.add(BulletFromShip(game=self.game,
                                                              x=self.rect.centerx, y=self.rect.top))

    def group(self): return self.ship_group

    def killed(self):
        if not self.reallydead: self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = Ship.timer_boom
            self.timer_switched = True

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def update(self):
        self.bullet_group_that_kill_aliens.update()
        bullet_alien_collisions = pg.sprite.groupcollide(self.aliens.group(), self.bullet_group_that_kill_aliens,
                                                         False, True)
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Ship.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
                self.game.reset()

        if bullet_alien_collisions:
            for alien in bullet_alien_collisions:
                alien.dead = True
                alien.killed()
        if len(self.aliens.group()) == 0:
            self.bullet_group_that_kill_aliens.empty()
            self.settings.increase_speed()
            self.aliens.create_fleet()
            self.game.stats.level += 1
            self.game.sb.prep_level()

        delta = self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right: self.center += delta
        if self.moving_left  and self.rect.left > 0: self.center -= delta
        if self.shooting_bullets and not self.dead:
            self.sound.shoot_bullet()
            self.add_bullet(game=self.game, x=self.rect.centerx, y=self.rect.top)
            self.shooting_bullets = False
        self.rect.centerx = self.center

    def draw(self):
        for bullet in self.bullet_group_that_kill_aliens:
            bullet.draw()
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
