import pygame
from pygame.sprite import Sprite

class Gun(Sprite):
    def __init__(self, screen):
        super(Gun, self).__init__()
        self.screen = screen
        self.original_image = pygame.image.load('images/pixil-frame-0.png').convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Початкове положення гравця
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Рухи гравця
        self.mright = False
        self.mleft = False
        self.mup = False
        self.mdown = False

        # Контроль стрільби
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 150  # Зменшуємо затримку між пострілами до 150мс (було 250мс)

    def apply_skin(self, color):
        if color == (255, 255, 255):
            self.image = self.original_image.copy()
        else:
            self.image = self.original_image.copy()
            self.image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    def output(self):
        """Малює гравця на екрані"""
        self.screen.blit(self.image, self.rect)

    def update(self, stats=None):
        """Оновлення положення гравця"""
        speed = 1.0
        if stats:
            speed += getattr(stats, 'player_speed_level', 0) * 0.5
            
        if self.mright and self.rect.right < self.screen_rect.right:
            self.x += speed
        if self.mleft and self.rect.left > 0:
            self.x -= speed
        if self.mup and self.rect.top > 0:
            self.y -= speed
        if self.mdown and self.rect.bottom < self.screen_rect.bottom:
            self.y += speed
            
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def create_gun(self):
        """Встановлює гравця на стартову позицію"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
