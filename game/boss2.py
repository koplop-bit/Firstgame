import pygame
import random
from pygame.sprite import Sprite, Group
import math

class Boss2(Sprite):
    def __init__(self, screen):
        super(Boss2, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Завантаження зображення боса
        try:
            self.image = pygame.image.load('images/emp6.png').convert_alpha()
            self.rect = self.image.get_rect()
        except:
            # Якщо зображення не знайдено, створюємо червоний прямокутник
            self.image = pygame.Surface((80, 80))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
        
        # Початкова позиція боса 
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 50
        
        # Параметри боса
        self.health = 1000# життів
        self.speed = 3.0  # Збільшена швидкість руху
        self.direction = 1  # 1 для руху вправо, -1 для руху вліво
        self.bullets = Group()
        self.last_shot_time = pygame.time.get_ticks()
        self.x = float(self.rect.x)
        self.target_player = None
        
    def set_player(self, player):
        self.target_player = player
        
    def update(self):
        """Оновлення позиції боса"""
        # Горизонтальний рух
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.direction = 1
        elif self.x >= self.screen_rect.width - self.rect.width:
            self.direction = -1
        self.rect.x = self.x
        
    def take_damage(self, amount):
        self.health -= amount
        
    def draw(self):
        """Відображення боса на екрані"""
        self.screen.blit(self.image, self.rect)
        # Малюємо кулі
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
    def shoot(self):
        """Спец атаки боса 2"""
        from bossbullet import BossBullet
        
        attack_type = random.randint(1, 3)
        
        if attack_type == 1:
            # Атака 1: 3 великих трикутних снаряди повільно
            positions = [-200, 0, 200]
            for pos in positions:
                new_bullet = BossBullet(self.screen, self)
                new_bullet.resize(120)
                new_bullet.shape_type = 'triangle'
                new_bullet.rect.centerx = self.rect.centerx + pos
                new_bullet.rect.top = self.rect.bottom + 20
                new_bullet.x = float(new_bullet.rect.x)
                new_bullet.y = float(new_bullet.rect.y)
                new_bullet.speed_y = 1.5
                new_bullet.homing_factor = 0.015  # Трикутники наводяться
                self.bullets.add(new_bullet)
                
        elif attack_type == 2:
            # Атака 2: Розкид квадратів у боки
            for _ in range(6):
                new_bullet = BossBullet(self.screen, self)
                new_bullet.resize(40)
                new_bullet.shape_type = 'square'
                new_bullet.rect.centerx = self.rect.centerx
                new_bullet.rect.top = self.rect.bottom + 10
                new_bullet.x = float(new_bullet.rect.x)
                new_bullet.y = float(new_bullet.rect.y)
                new_bullet.speed_y = 3
                new_bullet.speed_x = random.uniform(-4, 4)
                self.bullets.add(new_bullet)
                
        elif attack_type == 3:
            # Атака 3: Швидкі кола
            positions = [-100, -50, 0, 50, 100]
            for pos in positions:
                new_bullet = BossBullet(self.screen, self)
                new_bullet.resize(30)
                new_bullet.shape_type = 'circle'
                new_bullet.rect.centerx = self.rect.centerx + pos
                new_bullet.rect.top = self.rect.bottom + 20
                new_bullet.x = float(new_bullet.rect.x)
                new_bullet.y = float(new_bullet.rect.y)
                new_bullet.speed_y = 6
                self.bullets.add(new_bullet)
            
    def update_bullets(self):
        """Оновлення позиції куль боса"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.top >= self.screen_rect.bottom:
                self.bullets.remove(bullet) 