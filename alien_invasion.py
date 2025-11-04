import sys
import pygame
from random import randint, choice
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.screen = self.get_screen()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Vertical Alien Invasion')
        self.star_pattern = self._generate_star_pattern()
        self.stats = GameStats(self)        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(60)
            self._update_screen()

    def get_screen(self):
        if self.settings.fullscreen:
            wh = (0, 0)
            f = pygame.FULLSCREEN
        else:
            wh = (self.settings.screen_width, self.settings.screen_height)
            f = 0
        return pygame.display.set_mode(wh, f)


    #Helper Methods
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_events(event.key, True)
            elif event.type == pygame.KEYUP:
                self._check_key_events(event.key, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

                 
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_stars()
        self._draw_bullets()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _draw_bullets(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

    def _generate_star_pattern(self):
        pattern = []
        MARGIN = 100
        star_image = pygame.image.load('images/starBig.bmp')
        # star_image.get_rect() = (0, 0, 23, 21)
        x_count, y_count, width, height = star_image.get_rect()
        while y_count < self.settings.screen_height:
            while x_count < self.settings.screen_width:
                star = {
                    'img': choice(['images/starBig.bmp', 'images/starSmall.bmp']), 
                    'x': randint(x_count, x_count + MARGIN - width),
                    'y': randint(y_count, y_count + MARGIN - height)
                }
                pattern.append(star)
                x_count += MARGIN
            y_count += MARGIN
            x_count = 0
        return pattern

    def _draw_stars(self):
        for star in self.star_pattern:
            img = pygame.image.load(star['img'])
            self.screen.blit(img, (star['x'], star['y']))

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(
            self.ship, self.aliens
        ) or self._check_aliens_bottom():
            self._ship_hit()
    
    def _check_aliens_bottom(self):
        is_game_over = False
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                is_game_over = True
        return is_game_over

    def _ship_hit(self):
        if self.stats.lives > 0:
            sleep(0.5)
            self.stats.lives -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_dir()
                break

    def _check_play_button(self, pos):
        if self.play_button.rect.collidepoint(pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_images()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            pygame.mouse.set_visible(False)


    def _check_key_events(self, key, is_key_down):
        if key == pygame.K_UP:
            self.ship.moving_up = is_key_down
        elif key == pygame.K_DOWN:
            self.ship.moving_down = is_key_down
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE and is_key_down: 
            self._fire_bullet()
        elif key == pygame.K_p:
            self._check_play_button(self.play_button.rect.center)


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _change_fleet_dir(self):
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_dir *= -1
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                points = self.settings.alien_points
                for alien in aliens:
                    points += (self.settings.screen_height - alien.rect.y) 
                self.stats.score += points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()


    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        fleet_width = alien_width * 2
        fleet_height = alien_height
        while fleet_height < (self.settings.screen_height - 2 * alien_height):
            while fleet_width < (self.settings.screen_width - alien_width):
                self._create_alien(fleet_width, fleet_height)
                fleet_width += 2 * alien_width
            fleet_width = alien_width * 2
            fleet_height +=2 * alien_height

    def _create_alien(self, x, y):
        new_alien = Alien(self)
        new_alien.y = y
        new_alien.rect.x = x
        new_alien.rect.y = y
        self.aliens.add(new_alien)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()