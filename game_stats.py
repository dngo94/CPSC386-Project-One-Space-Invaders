class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.hs_active = False
        self.game_active = False
        self.reset_stats()
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
