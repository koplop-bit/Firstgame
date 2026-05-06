import pygame
from pygame.sprite import Sprite

class Mmp8(Sprite):
    def __init__(self, screen):
        super(Mmp8, self).__init__()
        self.screen = screen
        try:
            self.image = pygame.image.load('images/emp8.png').convert_alpha()
        except:
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.x = self.screen_rect.width // 2
        self.rect.y = 150
        self.direction = 1
        self.speed = 3
        self.health = 250
        
        self.is_mmp8 = True
        self.last_spawn_time = pygame.time.get_ticks()

    def update(self, wave=1):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.screen_rect.right:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1
            
    def take_damage(self, amount):
        self.health -= amount
