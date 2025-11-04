from pathlib import Path
import json

class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.high_score = json.loads(
            (Path('high_score.json').read_text())
        )['high_score']
        self.reset_stats()

    def reset_stats(self, level=1):
        self.lives = self.settings.lives
        self.score = 0
        self.level = level
