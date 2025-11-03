import pygame.font

class Button:
    def __init__(self, game, msg, pos=1):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = 200
        self.height = 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        w, h = self.screen_rect.center
        margin = 50
        self.positions = [w - self.width - margin, w, w + self.width + margin]
        self._prep_msg(msg, (self.positions[pos],h))
        self.rect.center = (self.positions[pos],h)

    def _prep_msg(self, msg, pos):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = pos
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)