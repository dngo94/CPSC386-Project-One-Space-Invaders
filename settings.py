class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)

        self.ship_limit = 2
        self.bullet_width = 2
        self.bullet_height = 30
        self.bullet_color = 255, 0, 0
        self.bullets_every = 1

        self.fleet_drop_speed = 2
        self.debounce = 0.0001

        self.score_scale = 1.5
        self.alien_points = [10, 20, 30]
        self.ufo_points = 100
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 5
        self.alien_speed = 13
        self.ufo_speed = -0.5
        self.fleet_direction = 1
        self.ufo_fleet_direction = 1
        self.alien_points = 10
        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.bullet_speed_factor *= scale
        self.alien_speed *= scale
        self.alien_points = int(self.alien_points * self.score_scale)
