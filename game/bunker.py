import pygame
from pygame.sprite import Sprite

class Bunker(Sprite):
    def __init__(self, screen, x, y):
        super(Bunker, self).__init__()
        self.screen = screen
        # Створюємо преграду як прямокутник
        self.rect = pygame.Rect(x, y, 80, 20)
        self.color = (0, 255, 0)  # Зелений колір
        self.health = 200

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
