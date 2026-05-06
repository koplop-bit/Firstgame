import pygame
from pygame.sprite import Sprite

class FastEnemy(Sprite):
    def __init__(self, screen):
        super(FastEnemy, self).__init__()
        self.screen = screen
        try:
            self.image = pygame.image.load('images/emp9.png').convert_alpha() # Reusing small sprite
        except:
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.image.fill((255, 100, 0))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
        self.speed_y = 1.2 # Very fast down
        self.speed_x = 1.5
        self.direction = 1
        self.health = 15 # 1-2 hits
        
    def update(self, wave=1):
        self.y += self.speed_y
        self.x += self.speed_x * self.direction
        
        if self.rect.right >= self.screen_rect.right:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1
            
        self.rect.y = self.y
        self.rect.x = self.x
        
    def take_damage(self, amount):
        self.health -= amount
