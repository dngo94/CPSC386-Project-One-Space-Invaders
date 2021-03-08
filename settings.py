class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        self.ship_limit = 2
        self.alien_bullet_width = 2
        self.alien_bullet_height = 30
        self.alien_bullet_color = 0, 255, 0
        self.alien_bullets_every = 1

        self.ship_bullet_height = 30
        self.ship_bullet_width = 2
        self.ship_bullet_color = 148,0,211
        self.ship_bullets_every = 1

        self.fleet_drop_speed = 10
        self.debounce = 0.0001

        self.score_scale = 1.5
        self.ufo_points = 1000
        self.alien_points = 50
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 1
        self.alien_speed = 1
        self.fleet_direction = 1
        self.alien_points = 50
        self.ufo_speed = -0.5
        self.ufo_fleet_direction = -1
        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.bullet_speed_factor *= scale
        self.alien_speed *= scale
        self.alien_points = int(self.alien_points * self.score_scale)
