import pygame
from pygame.sprite import Sprite

class Ino(Sprite):
    def __init__(self, screen, image_type=1):
        super(Ino, self).__init__()
        self.screen = screen
        self.image_type = image_type

        # Завантаження відповідного зображення інопланетянина
        if self.image_type == 1:
            self.original_image = pygame.image.load('images/emp.png').convert_alpha()
        elif self.image_type == 2:
            self.original_image = pygame.image.load('images/emp2.png').convert_alpha()
        elif self.image_type == 3:
            self.original_image = pygame.image.load('images/emp3.png').convert_alpha()
        elif self.image_type == 4:
            self.original_image = pygame.image.load('images/emp4.png').convert_alpha()
        else:
            self.original_image = pygame.image.load('images/emp.png').convert_alpha()  # запасне

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.health = self.image_type * 10  # Здоров'я залежить від типу

        import random
        self.is_shielded = False
        self.is_anomalous = False
        
        if random.random() < 0.15: # 15% шанс елітного
            if random.random() < 0.5:
                self.is_shielded = True
                self.image.fill((0, 100, 255), special_flags=pygame.BLEND_RGBA_ADD)
                self.health += 50
            else:
                self.is_anomalous = True
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                self.health *= 3

    def apply_skin(self, color):
        if color == (255, 255, 255):
            self.image = self.original_image.copy()
        else:
            self.image = self.original_image.copy()
            self.image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    def take_damage(self, amount):
        if getattr(self, 'is_shielded', False):
            self.is_shielded = False
            self.image = self.original_image.copy() # знімаємо щит, блокуємо 1 удар
            return
        self.health -= amount

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, wave=1):
        """Рух ворогів трохи вниз і ухиляння (dodging) на вищих хвилях"""
        # Швидкість зростає з кожною хвилею
        speed = 0.05 + (wave * 0.01)
        self.y += speed
        self.rect.y = self.y
        
        # Вороги стають ухилянтами після 5 хвилі або випадково
        import random
        if wave >= 5 and random.random() < 0.02:
            direction = random.choice([-1, 1])
            self.x += direction * speed * 20
            
            # Тримаємо їх в межах екрану
            if self.x < 0: self.x = 0
            if self.x > self.screen.get_rect().right - self.rect.width:
                self.x = self.screen.get_rect().right - self.rect.width
                
            self.rect.x = self.x
