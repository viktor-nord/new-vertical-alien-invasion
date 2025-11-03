class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (171, 70, 203)
        self.fullscreen = False
        # Ship
        self.ship_speed = 7.5
        # Bullet
        self.bullet_speed = 2.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_dir = 1 #1=right -1=left
        # Player
        self.not_super_bullet = True