import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, screen, gun, stats=None):
        super(Bullet, self).__init__()
        self.screen = screen

        # Базові параметри
        base_width = 10
        base_height = 1
        base_damage = 10
        
        # Застосування прокачки
        damage_multiplier = 1.0
        size_addition = 0
        
        if stats:
            import pygame
            damage_multiplier = 1.0 + (0.1 * stats.damage_level) + (0.25 * getattr(stats, 'damage_level_2', 0))
            if getattr(stats, 'super_mode_active', False) and pygame.time.get_ticks() < getattr(stats, 'super_mode_end_time', 0):
                damage_multiplier *= 2.0
            
            size_addition = 10 * stats.size_level + 20 * getattr(stats, 'size_level_2', 0)
            
        width = base_width + size_addition
        height = base_height + size_addition
        
        # Створення кулі як прямокутника
        self.rect = pygame.Rect(0, 0, width, height)  
        self.color = (255, 255, 0)  # Жовтий колір для кращої видимості
        
        base_speed = 7
        if stats:
            base_speed += getattr(stats, 'bullet_speed_level', 0) * 1.5
        self.speed = base_speed
        
        self.speed_x = 0  # Горизонтальна швидкість
        self.damage = base_damage * damage_multiplier  # Урон від кулі

        # Початкова позиція кулі — з дула гравця
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top

        self.y = float(self.rect.y)
        self.x = float(self.rect.centerx)

    def update(self):
        """Рух кулі вгору та в сторони"""
        self.y -= self.speed
        self.x += self.speed_x
        
        self.rect.y = int(self.y)
        self.rect.centerx = int(self.x)

        # Видалення кулі, якщо вона вийшла за межі екрана
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > self.screen.get_rect().width:
            self.kill()

    def draw_bullet(self):
        """Малювання кулі"""
        pygame.draw.rect(self.screen, self.color, self.rect)
