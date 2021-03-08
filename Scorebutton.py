import pygame as pg
import pygame.font


class scorebutton:
    def __init__(self, settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (171, 130, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pg.Rect(0, 0, self.width+30, self.height)
        self.rect.center = (600, 700)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)