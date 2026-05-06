import pygame
from pygame.sprite import Sprite
import random

class Drop(Sprite):
    def __init__(self, screen, x, y):
        super(Drop, self).__init__()
        self.screen = screen
        self.type = random.choices(
            ['armor', 'double_bullet', 'iron', 'crystal', 'core'],
            weights=[5, 5, 40, 20, 5]
        )[0]
        
        self.image = pygame.Surface((15, 15))
        if self.type == 'armor':
            self.image.fill((0, 255, 0)) # Green
        elif self.type == 'double_bullet':
            self.image.fill((255, 255, 0)) # Yellow
        elif self.type == 'iron':
            self.image.fill((150, 150, 150)) # Gray
        elif self.type == 'crystal':
            self.image.fill((0, 255, 255)) # Cyan
        elif self.type == 'core':
            self.image.fill((255, 0, 255)) # Magenta
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = 2.5
        
    def update(self):
        self.rect.y += self.speed_y
        
    def draw(self):
        self.screen.blit(self.image, self.rect)
