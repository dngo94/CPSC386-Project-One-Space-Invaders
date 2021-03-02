import pygame as pg

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.5)
        bullet_sound = pg.mixer.Sound('sounds/bullet2.wav')
        pg.mixer.Sound.set_volume(bullet_sound, 0.22)
        self.sounds = {'bullet': bullet_sound}
        self.playing_bg = None
        self.play()
        self.pause_bg()

    def pause_bg(self):
        self.playing_bg = False
        pg.mixer.music.pause()

    def unpause_bg(self):
        self.playing_bg = True
        pg.mixer.music.unpause()

    def play(self):
        self.playing_bg = True
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        self.playing_bg = False
        pg.mixer.music.stop()

    def shoot_bullet(self): pg.mixer.Sound.play(self.sounds['bullet'])
