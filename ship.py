import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, settings, screen, sound, bullets=None):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.sound = sound

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.center = 0
        self.center_ship()

        self.moving_right = False
        self.moving_left = False
        self.bullets = bullets
        self.shooting_bullets = False
        self.bullets_attempted = 0

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def update(self):
        delta = self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right: self.center += delta
        if self.moving_left  and self.rect.left > 0: self.center -= delta
        if self.shooting_bullets:
            self.sound.shoot_bullet()
            self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
            #self.shooting_bullets = False
            self.bullets_attempted += 1
            if self.bullets_attempted % self.settings.bullets_every == 0:
                self.sound.shoot_bullet()
                self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
        self.rect.centerx = self.center

    def draw(self): self.screen.blit(self.image, self.rect)
