import pygame
from pygame.sprite import Sprite

class BossBullet(Sprite):
    def __init__(self, screen, boss, x=None, y=None):
        super(BossBullet, self).__init__()
        self.screen = screen
        self.size = 20  # Початковий розмір
        self.width = self.size
        self.height = self.size
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.color = (255, 255, 255)  # Білий колір за замовчуванням
        self.speed = 1.5  # Зменшена швидкість
        self.speed_x = 0
        self.speed_y = self.speed
        self.shape_type = 'circle'  # За замовчуванням
        
        self.target = getattr(boss, 'target_player', None)
        self.homing_factor = 0.0
        
        # Створюємо поверхню для кулі
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Позиція кулі
        if x is not None and y is not None:
            # Для Boss1
            self.rect.centerx = x
            self.rect.top = y
        else:
            # Для Boss2/Boss3
            self.rect.centerx = boss.rect.centerx
            self.rect.top = boss.rect.bottom
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    def resize(self, width, height=None):
        """Змінює розмір кулі. Якщо height не вказано, використовує width як розмір квадрата"""
        self.width = width
        self.height = height if height is not None else width
        old_center = self.rect.center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = old_center
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
    def update(self):
        """Переміщення кулі"""
        if self.target and self.homing_factor > 0:
            if self.target.rect.centerx > self.rect.centerx:
                self.speed_x += self.homing_factor * 0.3 # Зменшуємо силу наведення
            elif self.target.rect.centerx < self.rect.centerx:
                self.speed_x -= self.homing_factor * 0.3
                
            # Обмежуємо максимальну швидкість повороту
            max_homing_speed = 1.0
            if self.speed_x > max_homing_speed:
                self.speed_x = max_homing_speed
            elif self.speed_x < -max_homing_speed:
                self.speed_x = -max_homing_speed
                
        self.y += self.speed_y
        self.x += self.speed_x
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
        
        # Видалення кулі, якщо вона вийшла за межі екрана
        if (self.rect.top > self.screen.get_rect().bottom or 
            self.rect.bottom < 0 or 
            self.rect.right < 0 or 
            self.rect.left > self.screen.get_rect().width):
            self.kill()
        
    def draw_bullet(self):
        """Малювання кулі"""
        # Очищаємо поверхню
        self.image.fill((0, 0, 0, 0))
        
        if self.shape_type == 'circle':
            radius = min(self.width, self.height) // 2
            pygame.draw.circle(self.image, self.color, 
                             (self.width//2, self.height//2), 
                             radius)
        elif self.shape_type == 'triangle':
            points = [
                (self.width//2, 0),
                (0, self.height),
                (self.width, self.height)
            ]
            pygame.draw.polygon(self.image, self.color, points)
        elif self.shape_type == 'square':
            pygame.draw.rect(self.image, self.color, 
                           (0, 0, self.width, self.height))
        elif self.shape_type == 'rectangle':
            pygame.draw.rect(self.image, self.color, 
                           (0, 0, self.width, self.height))
        elif self.shape_type == 'dick':
            radius = self.width // 2
            # Balls at the top
            pygame.draw.circle(self.image, self.color, (radius, radius), radius)
            pygame.draw.circle(self.image, self.color, (self.width - radius, radius), radius)
            # Shaft
            shaft_width = self.width // 2
            pygame.draw.rect(self.image, self.color, 
                           (self.width//2 - shaft_width//2, radius, shaft_width, self.height - radius))
            
            
        self.screen.blit(self.image, self.rect)
