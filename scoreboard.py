from pathlib import Path
import json
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.path = Path('high_score.json')
        self.prep_images()
    
    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.lives):
            ship = Ship(self.game)
            w, h = (ship.rect.width / 2, ship.rect.height / 2)
            ship.image = pygame.transform.scale(ship.image, (w, h))
            ship.rect.x = 10 + ship_number * (w + 5)
            ship.rect.y = 10
            self.ships.add(ship)
    
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.render_text(level_str)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.render_text(score_str)
        self.score_rect = self.score_image.get_rect()
        #self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.x = self.settings.screen_width - self.score_rect.width - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.render_text(high_score_str)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def render_text(self, text):
        x = self.font.render(text, True, self.text_color, None)
        return x

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.prep_ships()
        self.ships.draw(self.screen)
        
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            json_obj = json.loads((Path('high_score.json').read_text()))
            json_obj['high_score'] = self.stats.score
            self.path.write_text(json.dumps(json_obj))
            self.prep_high_score()
        